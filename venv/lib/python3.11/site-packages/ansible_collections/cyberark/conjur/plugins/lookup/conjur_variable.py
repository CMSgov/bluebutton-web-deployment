# (c) 2020 CyberArk Software Ltd. All rights reserved.
# (c) 2018 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type  # pylint: disable=invalid-name

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = """
    name: conjur_variable
    version_added: "1.0.2"
    short_description: Fetch credentials from CyberArk Conjur.
    author:
      - CyberArk BizDev (@cyberark-bizdev)
    description:
      Retrieves credentials from Conjur using the controlling host's Conjur identity,
      environment variables, or extra-vars.
      Environment variables could be CONJUR_ACCOUNT, CONJUR_APPLIANCE_URL, CONJUR_CERT_FILE, CONJUR_CERT_CONTENT,
      CONJUR_AUTHN_LOGIN, CONJUR_AUTHN_API_KEY, CONJUR_AUTHN_TOKEN_FILE
      Extra-vars could be conjur_account, conjur_appliance_url, conjur_cert_file, conjur_cert_content,
      conjur_authn_login, conjur_authn_api_key, conjur_authn_token_file
      Conjur info - U(https://www.conjur.org/).
    requirements:
      - 'The controlling host running Ansible has a Conjur identity.
        (More: U(https://docs.conjur.org/latest/en/Content/Get%20Started/key_concepts/machine_identity.html))'
    options:
      _terms:
        description: Variable path
        required: True
      validate_certs:
        description: Flag to control SSL certificate validation
        type: boolean
        default: True
      as_file:
        description: >
          Store lookup result in a temporary file and returns the file path. Thus allowing it to be consumed as an ansible file parameter
          (eg ansible_ssh_private_key_file).
        type: boolean
        default: False
      identity_file:
        description: Path to the Conjur identity file. The identity file follows the netrc file format convention.
        type: path
        default: /etc/conjur.identity
        required: False
        ini:
          - section: conjur,
            key: identity_file_path
        env:
          - name: CONJUR_IDENTITY_FILE
      config_file:
        description: Path to the Conjur configuration file. The configuration file is a YAML file.
        type: path
        default: /etc/conjur.conf
        required: False
        ini:
          - section: conjur,
            key: config_file_path
        env:
          - name: CONJUR_CONFIG_FILE
      conjur_appliance_url:
        description: Conjur appliance url
        type: string
        required: False
        ini:
          - section: conjur,
            key: appliance_url
        vars:
          - name: conjur_appliance_url
        env:
          - name: CONJUR_APPLIANCE_URL
      conjur_authn_login:
        description: Conjur authn login
        type: string
        required: False
        ini:
          - section: conjur,
            key: authn_login
        vars:
          - name: conjur_authn_login
        env:
          - name: CONJUR_AUTHN_LOGIN
      conjur_account:
        description: Conjur account
        type: string
        required: False
        ini:
          - section: conjur,
            key: account
        vars:
          - name: conjur_account
        env:
          - name: CONJUR_ACCOUNT
      conjur_authn_api_key:
        description: Conjur authn api key
        type: string
        required: False
        ini:
          - section: conjur,
            key: authn_api_key
        vars:
          - name: conjur_authn_api_key
        env:
          - name: CONJUR_AUTHN_API_KEY
      conjur_cert_file:
        description: Path to the Conjur cert file
        type: path
        required: False
        ini:
          - section: conjur,
            key: cert_file
        vars:
          - name: conjur_cert_file
        env:
          - name: CONJUR_CERT_FILE
      conjur_cert_content:
        description: Content of the Conjur cert
        type: string
        required: False
        ini:
          - section: conjur,
            key: cert_content
        vars:
          - name: conjur_cert_content
        env:
          - name: CONJUR_CERT_CONTENT
      conjur_authn_token_file:
        description: Path to the access token file
        type: path
        required: False
        ini:
          - section: conjur,
            key: authn_token_file
        vars:
          - name: conjur_authn_token_file
        env:
          - name: CONJUR_AUTHN_TOKEN_FILE
"""

EXAMPLES = """
---
- hosts: localhost
  collections:
    - cyberark.conjur
  tasks:
    - name: Lookup variable in Conjur
      debug:
        msg: "{{ lookup('cyberark.conjur.conjur_variable', '/path/to/secret') }}"
"""

RETURN = """
  _raw:
    description:
      - Value stored in Conjur.
"""

import os
import socket
import traceback
import ssl
import re
from base64 import b64encode
from netrc import netrc
from time import sleep
from stat import S_IRUSR, S_IWUSR
from tempfile import gettempdir, NamedTemporaryFile
import yaml
import ansible.module_utils.six.moves.urllib.error as urllib_error
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils.six.moves.urllib.parse import quote
from ansible.module_utils.urls import open_url
from ansible.utils.display import Display
try:
    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.backends import default_backend
except ImportError:
    CRYPTOGRAPHY_IMPORT_ERROR = traceback.format_exc()
else:
    CRYPTOGRAPHY_IMPORT_ERROR = None

display = Display()
TEMP_CERT_FILE = None


def _validate_pem_certificate(cert_content):
    # Normalize line endings
    if '\r\n' in cert_content:
        cert_content = cert_content.replace('\r\n', '\n').strip()
    elif '\r' in cert_content:
        cert_content = cert_content.replace('\r', '\n').strip()
    cert_content = re.sub(r'^[ \t]+', '', cert_content, flags=re.M)
    cert_content = re.sub(r'[ \t]+$', '', cert_content, flags=re.M)
    cert_content = re.sub(r'\n+', '\n', cert_content)

    if not re.match(r"^-----BEGIN CERTIFICATE-----.+-----END CERTIFICATE-----$", cert_content, re.DOTALL):
        raise AnsibleError("Invalid Certificate format.")

    try:
        load_pem_x509_certificate(cert_content.encode(), default_backend())
        return cert_content
    except ValueError as err:
        raise AnsibleError(
            f"Invalid certificate content provided: {str(err)}. "
            "Please check the certificate format."
        ) from err
    except ssl.SSLError as err:
        raise AnsibleError(
            f"SSL error while validating the certificate: {str(err)}. "
            "The certificate may be corrupted or invalid."
        ) from err
    except Exception as err:
        raise AnsibleError(
            f"An error occurred while validating the certificate: {str(err)}. "
            "Please verify the certificate format and try again."
        ) from err


def _get_valid_certificate(cert_content, cert_file):
    if cert_content:
        try:
            display.vvv("Validating provided certificate content")
            cert_content = _validate_pem_certificate(cert_content)
            return cert_content
        except AnsibleError as err:
            display.warning(f"Invalid certificate content: {str(err)}. Attempting to use certificate file.")

    # If cert_content is invalid or missing, fall back to cert_file
    if cert_file:
        if not os.path.exists(cert_file):
            raise AnsibleError(f"Certificate file `{cert_file}` does not exist or cannot be found.")
        try:
            with open(cert_file, 'rb') as file:
                cert_file_content = file.read().decode('utf-8')
                cert_file_content = _validate_pem_certificate(cert_file_content)
                return cert_file_content
        except Exception as err:
            raise AnsibleError(f"Failed to load or validate certificate file `{cert_file}`: {str(err)}") from err

    # If both cert_content and cert_file are missing or invalid, raise an error
    raise AnsibleError("Both certificate content and certificate file are invalid or missing. Please provide a valid certificate.")


def _get_certificate_file(cert_content, cert_file):
    global TEMP_CERT_FILE
    cert_content = _get_valid_certificate(cert_content, cert_file)

    if cert_content:
        try:
            TEMP_CERT_FILE = NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')  # pylint: disable=consider-using-with
            TEMP_CERT_FILE.write(cert_content)
            TEMP_CERT_FILE.close()
            cert_file = TEMP_CERT_FILE.name
        except Exception as err:
            raise AnsibleError(f"Failed to create temporary certificate file: {str(err)}") from err

    return cert_file


# Load configuration and return as dictionary if file is present on file system
def _load_conf_from_file(conf_path):
    display.vvv(f'conf file: {conf_path}')

    if not os.path.exists(conf_path):
        return {}
        # raise AnsibleError('Conjur configuration file `{conf_path}` was not found on the controlling host')

    display.vvvv(f'Loading configuration from: {conf_path}')
    with open(conf_path, encoding="utf-8") as file:
        config = yaml.safe_load(file.read())
        return config


# Load identity and return as dictionary if file is present on file system
def _load_identity_from_file(identity_path, appliance_url):
    display.vvvv(f'identity file: {identity_path}')

    if not os.path.exists(identity_path):
        return {}
        # raise AnsibleError(f'Conjur identity file `{identity_path}` was not found on the controlling host')

    display.vvvv(f'Loading identity from: {identity_path} for {appliance_url}')

    conjur_authn_url = f'{appliance_url}/authn'
    identity = netrc(identity_path)

    if identity.authenticators(conjur_authn_url) is None:
        raise AnsibleError(f'The netrc file on the controlling host does not contain an entry for: {conjur_authn_url}')

    host_id, unused, api_key = identity.authenticators(conjur_authn_url)  # pylint: disable=unused-variable

    if not host_id or not api_key:
        return {}

    return {'id': host_id, 'api_key': api_key}


# Merge multiple dictionaries by using dict.update mechanism
def _merge_dictionaries(*arg):
    ret = {}
    for item in arg:
        ret.update(item)
    return ret


# The `quote` method's default value for `safe` is '/' so it doesn't encode slashes
# into "%2F" which is what the Conjur server expects. Thus, we need to use this
# method with no safe characters. We can't use the method `quote_plus` (which encodes
# slashes correctly) because it encodes spaces into the character '+' instead of "%20"
# as expected by the Conjur server
def _encode_str(input_str):
    return quote(input_str, safe='')


# Use credentials to retrieve temporary authorization token
def _fetch_conjur_token(conjur_url, account, username, api_key, validate_certs, cert_file):  # pylint: disable=too-many-arguments
    conjur_url = f'{conjur_url}/authn/{account}/{_encode_str(username)}/authenticate'
    display.vvvv(f'Authentication request to Conjur at: {conjur_url}, with user: {_encode_str(username)}')

    response = open_url(conjur_url,
                        data=api_key,
                        method='POST',
                        validate_certs=validate_certs,
                        ca_path=cert_file)
    code = response.getcode()
    if code != 200:
        raise AnsibleError(f'Failed to authenticate as \'{username}\' (got {code} response)')

    return response.read()


def retry(retries, retry_interval):
    """
    Custom retry decorator

    Args:
        retries (int, optional): Number of retries. Defaults to 5.
        retry_interval (int, optional): Time to wait between intervals. Defaults to 10.
    """
    def parameters_wrapper(target):
        def decorator(*args, **kwargs):
            retry_count = 0
            while True:
                retry_count += 1
                try:
                    return_value = target(*args, **kwargs)
                    return return_value
                except urllib_error.HTTPError as err:
                    if retry_count >= retries:
                        raise err
                    display.v('Error encountered. Retrying..')
                except socket.timeout as err:
                    if retry_count >= retries:
                        raise err
                    display.v('Socket timeout encountered. Retrying..')
                sleep(retry_interval)
        return decorator
    return parameters_wrapper


@retry(retries=5, retry_interval=10)
def _repeat_open_url(url, headers=None, method=None, validate_certs=True, ca_path=None):
    return open_url(url,
                    headers=headers,
                    method=method,
                    validate_certs=validate_certs,
                    ca_path=ca_path)


# Retrieve Conjur variable using the temporary token
def _fetch_conjur_variable(conjur_variable, token, conjur_url, account, validate_certs, cert_file):  # pylint: disable=too-many-arguments
    token = b64encode(token)
    headers = {'Authorization': f'Token token="{token.decode("utf-8")}"'}

    url = f'{conjur_url}/secrets/{account}/variable/{_encode_str(conjur_variable)}'
    display.vvvv(f'Conjur Variable URL: {url}')

    response = _repeat_open_url(url,
                                headers=headers,
                                method='GET',
                                validate_certs=validate_certs,
                                ca_path=cert_file)

    if response.getcode() == 200:
        display.vvvv(f'Conjur variable {conjur_variable} was successfully retrieved')
        value = response.read().decode("utf-8")
        return [value]
    if response.getcode() == 401:
        raise AnsibleError('Conjur request has invalid authorization credentials')
    if response.getcode() == 403:
        raise AnsibleError(f'The controlling host\'s Conjur identity does not have authorization to retrieve {conjur_variable}')
    if response.getcode() == 404:
        raise AnsibleError(f'The variable {conjur_variable} does not exist')

    return {}


def _default_tmp_path():
    if os.access("/dev/shm", os.W_OK):
        return "/dev/shm"

    return gettempdir()


def _store_secret_in_file(value):
    secrets_file = NamedTemporaryFile(mode='w', dir=_default_tmp_path(), delete=False)  # pylint: disable=consider-using-with
    os.chmod(secrets_file.name, S_IRUSR | S_IWUSR)
    secrets_file.write(value[0])

    return [secrets_file.name]


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):  # pylint: disable=too-many-locals,missing-function-docstring,too-many-branches,too-many-statements
        if terms == []:
            raise AnsibleError("Invalid secret path: no secret path provided.")
        if not terms[0] or terms[0].isspace():
            raise AnsibleError("Invalid secret path: empty secret path not accepted.")

        # We should register the variables as LookupModule options.
        #
        # Doing this has some nice advantages if we're considering supporting
        # a set of Ansible variables that could sometimes replace environment
        # variables.
        #
        # Registering the variables as options forces them to adhere to the
        # behavior described in the DOCUMENTATION variable. An option can have
        # both a Ansible variable and environment variable source, which means
        # Ansible will do some juggling on our behalf.
        self.set_options(var_options=variables, direct=kwargs)

        appliance_url = self.get_var_value("conjur_appliance_url")
        account = self.get_var_value("conjur_account")
        authn_login = self.get_var_value("conjur_authn_login")
        authn_api_key = self.get_var_value("conjur_authn_api_key")
        cert_file = self.get_var_value("conjur_cert_file")
        cert_content = self.get_var_value("conjur_cert_content")
        authn_token_file = self.get_var_value("conjur_authn_token_file")

        validate_certs = self.get_option('validate_certs')
        conf_file = self.get_option('config_file')
        as_file = self.get_option('as_file')

        if validate_certs is False:
            display.warning('Certificate validation has been disabled. Please enable with validate_certs option.')

        if 'http://' in str(appliance_url):
            raise AnsibleError(('[WARNING]: Conjur URL uses insecure connection. Please consider using HTTPS.'))

        if validate_certs is True:
            cert_file = _get_certificate_file(cert_content, cert_file)

        conf = _merge_dictionaries(
            _load_conf_from_file(conf_file),
            {
                "account": account,
                "appliance_url": appliance_url
            } if (
                account is not None
                and appliance_url is not None
            )
            else {},
            {
                "cert_file": cert_file
            } if (cert_file is not None)
            else {},
            {
                "authn_token_file": authn_token_file
            } if authn_token_file is not None
            else {}
        )

        if 'account' not in conf or 'appliance_url' not in conf:
            raise AnsibleError(
                """Configuration must define options `conjur_account` and `conjur_appliance_url`.
                This config can be set by any of the following methods, listed in order of priority:
                - Ansible variables of the same name, set either in the parent playbook or passed to
                  the ansible-playbook command with the --extra-vars flag
                - Environment variables `CONJUR_ACCOUNT` and `CONJUR_APPLIANCE_URL`
                - A configuration file on the controlling host with fields `account` and `appliance_url`"""
            )

        if 'authn_token_file' not in conf:
            identity_file = self.get_option('identity_file')
            identity = _merge_dictionaries(
                _load_identity_from_file(identity_file, conf['appliance_url']),
                {
                    "id": authn_login,
                    "api_key": authn_api_key
                } if authn_login is not None
                and authn_api_key is not None
                else {}
            )

            if 'id' not in identity or 'api_key' not in identity:
                raise AnsibleError(
                    """Configuration must define options `conjur_authn_login` and `conjur_authn_api_key`.
                    This config can be set by any of the following methods, listed in order of priority:
                    - Ansible variables of the same name, set either in the parent playbook or passed to
                      the ansible-playbook command with the --extra-vars flag
                    - Environment variables `CONJUR_AUTHN_LOGIN` and `CONJUR_AUTHN_API_KEY`
                    - An identity file on the controlling host with the fields `login` and `password`"""
                )

        cert_file = None
        if 'cert_file' in conf:
            display.vvv(f"Using cert file path {conf['cert_file']}")
            cert_file = conf['cert_file']

        try:
            token = None
            if 'authn_token_file' not in conf:
                token = _fetch_conjur_token(
                    conf['appliance_url'],
                    conf['account'],
                    identity['id'],
                    identity['api_key'],
                    validate_certs,
                    cert_file
                )
            else:
                if not os.path.exists(conf['authn_token_file']):
                    raise AnsibleError(f"Conjur authn token file `{conf['authn_token_file']}` was not found on the host")
                with open(conf['authn_token_file'], 'rb') as file:
                    token = file.read()

            conjur_variable = _fetch_conjur_variable(
                terms[0],
                token,
                conf['appliance_url'],
                conf['account'],
                validate_certs,
                cert_file
            )
        finally:
            if TEMP_CERT_FILE:
                try:
                    if os.path.exists(TEMP_CERT_FILE.name):
                        os.unlink(TEMP_CERT_FILE.name)
                except (OSError, PermissionError) as err:
                    raise AnsibleError(f"Failed to delete temporary certificate file `{TEMP_CERT_FILE.name}`: {str(err)}") from err

        if as_file:
            return _store_secret_in_file(conjur_variable)

        return conjur_variable

    def get_var_value(self, key):
        try:
            variable_value = self.get_option(key)
        except KeyError as err:
            raise AnsibleError(f"{key} was not defined in configuration") from err

        return variable_value
