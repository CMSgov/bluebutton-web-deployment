from __future__ import absolute_import, division, print_function

__metaclass__ = type

from abc import ABC, abstractmethod
import json
import time
import urllib.error as urllib_error
from ansible.module_utils.urls import socket

try:
    from ..common.hv_api_constants import API
    from ..common.hv_log import Log
    from ..common.vsp_constants import Endpoints
    from .ansible_url import open_url
    from .vsp_session_manager import SessionManager
    from ..model.common_base_models import ConnectionInfo
except ImportError:
    from common.hv_api_constants import API
    from common.hv_log import Log
    from common.vsp_constants import Endpoints
    from .ansible_url import open_url
    from .vsp_session_manager import SessionManager
    from model.common_base_models import ConnectionInfo

logger = Log()
moduleName = "Gateway Manager"
OPEN_URL_TIMEOUT = 600


class SessionObject:
    def __init__(self, session_id, token):
        self.session_id = session_id
        self.token = token
        self.create_time = time.time()
        self.expiry_time = self.create_time + 99999999


class ConnectionManager(ABC):
    retryCount = 0
    server_busy_msg = "The server might be temporarily busy"

    def __init__(self, address, username=None, password=None, token=None):
        self.address = address
        self.username = username
        self.password = password
        self.token = token
        self.base_url = None

        if not self.base_url:
            self.base_url = self.form_base_url()

    @abstractmethod
    def form_base_url(self) -> str:
        return ""

    def getAuthToken(self) -> dict[str, str]:
        return {}

    def get_job(self, job_id) -> dict:
        """get job method"""
        return {}

    def _load_response(self, response):
        """returns dict if json, native string otherwise"""
        try:
            text = response.read().decode("utf-8")
            if "token" not in text:
                logger.writeDebug(f"{text[:5000]} ...")
            msg = {}
            raw_message = json.loads(text)
            if not len(raw_message):
                if raw_message.get("errorSource"):
                    msg[API.CAUSE] = raw_message[API.CAUSE]
                    msg[API.SOLUTION] = raw_message[API.SOLUTION]
                    return msg
            return raw_message
        except ValueError:
            return text

    def _make_request(self, method, end_point, data=None):

        url = self.base_url + "/" + end_point
        logger.writeDebug("url = {}", url)

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if data is not None:
            data = json.dumps(data)
            x = url.endswith("chap-users")
            if not x:
                logger.writeDebug("data = {}", data)

        logger.writeDebug("method = {}", method)
        logger.writeDebug("headers = {}", headers)

        MAX_TIME_OUT = 300

        try:
            response = open_url(
                url=url,
                method=method,
                headers=headers,
                data=data,
                use_proxy=False,
                timeout=MAX_TIME_OUT,
                url_username=self.username,
                url_password=self.password,
                force_basic_auth=True,
                validate_certs=False,
            )
        except socket.timeout as t_err:
            logger.writeError(f"ConnectionManager._make_request - TimeoutError {t_err}")
            raise Exception(t_err)
        except urllib_error.HTTPError as err:
            logger.writeError(f"ConnectionManager._make_request - HTTPError {err}")

            if err.code == 503:
                # 503 Service Unavailable
                # wait for 5 mins and try to re-authenticate, we will retry 5 times
                if self.retryCount < 5:
                    logger.writeDebug(
                        f"{self.server_busy_msg}, wait for 5 mins and try to generate session token again."
                    )
                    time.sleep(300)
                    self.retryCount += 1
                    return self._make_request(method, end_point, data)
                else:
                    if hasattr(err, "read"):
                        error_resp = json.loads(err.read().decode())
                        logger.writeDebug(
                            f"ConnectionManager.error_resp - error_resp {error_resp}"
                        )
                        error_dtls = (
                            error_resp.get("message")
                            if error_resp.get("message")
                            else error_resp.get("errorMessage")
                        )
                        if error_resp.get("cause"):
                            error_dtls = error_dtls + " " + error_resp.get("cause")

                        if error_resp.get("solution"):
                            error_dtls = error_dtls + " " + error_resp.get("solution")

                        raise Exception(error_dtls)
            raise Exception(err)
        except Exception as err:
            logger.writeException(err)
            raise err

        if response.status not in (200, 201, 202):
            error_msg = json.loads(response.read())
            logger.writeError("error_msg = {}", error_msg)
            raise Exception(error_msg, response.status)

        return self._load_response(response)

    def create(self, endpoint, data):
        return self._make_request(method="POST", end_point=endpoint, data=data)

    def _process_job(self, job_id):
        response = None
        retryCount = 0
        while response is None and retryCount < 60:
            job_response = self.get_job(job_id)
            logger.writeDebug("_process_job: job_response = {}", job_response)
            job_status = job_response[API.STATUS]
            job_state = job_response[API.STATE]
            response = None
            if job_status == API.COMPLETED:
                if job_state == API.SUCCEEDED:
                    # For POST call to add chap user to port, affected resource is empty
                    # For PATCH port-auth-settings, affected resource is empty
                    if len(job_response[API.AFFECTED_RESOURCES]) > 0:
                        response = job_response[API.AFFECTED_RESOURCES][0]
                    else:
                        response = job_response["self"]
                else:
                    raise Exception(self.job_exception_text(job_response))
            else:
                retryCount = retryCount + 1
                time.sleep(10)

        if response is None:
            raise Exception("Timeout Error! The tasks was not completed in 10 minutes")

        resourceId = response.split("/")[-1]
        logger.writeDebug("response = {}", response)
        logger.writeDebug("resourceId = {}", resourceId)
        return resourceId

    def post(self, endpoint, data):

        post_response = self._make_request(method="POST", end_point=endpoint, data=data)
        logger.writeDebug("post_response = {}", post_response)
        job_id = post_response[API.JOB_ID]
        return self._process_job(job_id)

    def patch(self, endpoint, data):
        patch_response = self._make_request(
            method="PATCH", end_point=endpoint, data=data
        )
        job_id = patch_response[API.JOB_ID]
        return self._process_job(job_id)

    def job_exception_text(self, job_response):

        keys = job_response[API.ERROR].keys()
        logger.writeDebug("job_response_error_keys= {}", keys)
        result_text = ""
        if API.MESSAGE_ID in keys:
            result_text += job_response[API.ERROR][API.MESSAGE_ID] + " "
        if API.MESSAGE in keys:
            result_text += job_response[API.ERROR][API.MESSAGE] + " "
        if API.CAUSE in keys:
            result_text += job_response[API.ERROR][API.CAUSE] + " "
        if API.SOLUTION in keys:
            result_text += job_response[API.ERROR][API.SOLUTION] + " "
        if API.SOLUTION_TYPE in keys:
            result_text += job_response[API.ERROR][API.SOLUTION_TYPE] + " "
        if API.ERROR_CODE in keys:
            error_value = job_response[API.ERROR][API.ERROR_CODE]
            result_text += " " + "errorCode : " + str(error_value) + " "
        if API.DETAIL_CODE in keys:
            result_text += (
                "detailCode : " + job_response[API.ERROR][API.DETAIL_CODE] + " "
            )

        return result_text

    def read(self, endpoint):
        return self._make_request("GET", endpoint)

    def get(self, endpoint):
        return self._make_request("GET", endpoint)

    def update(self, endpoint, data):
        put_response = self._make_request(method="PUT", end_point=endpoint, data=data)
        job_id = put_response[API.JOB_ID]
        return self._process_job(job_id)

    def delete(self, endpoint, data=None):
        delete_response = self._make_request(
            method="DELETE", end_point=endpoint, data=data
        )
        job_id = delete_response[API.JOB_ID]
        return self._process_job(job_id)


class SDSBConnectionManager(ConnectionManager):

    def form_base_url(self):
        return f"https://{self.address}/ConfigurationManager/simple"

    def get_job(self, job_id):
        end_point = "v1/objects/jobs/" + job_id
        return self._make_request("GET", end_point)


class VSPConnectionManager(ConnectionManager):
    session = None
    retryCount = 0
    session_expired_msg = "The specified token is invalid"

    session_manager = SessionManager()

    def getAuthToken(self, retry=False):
        logger.writeDebug("Entering VSPConnectionManager.getAuthToken")
        connection_info = ConnectionInfo(
            address=self.address, username=self.username, password=self.password
        )
        if not retry:
            self.token = self.session_manager.get_current_session(connection_info)
        else:
            self.token = self.session_manager.renew_session(connection_info)
        headers = {"Authorization": "Session {0}".format(self.token)}
        return headers

    # def getAuthToken(self):
    #     logger.writeDebug("Entering VSPConnectionManager.getAuthToken")

    #     if self.token is not None:
    #         logger.writeDebug(
    #             "VSPConnectionManager.getAuthToken:self.token is not None"
    #         )
    #         return {"Authorization": "Session {0}".format(self.token)}

    #     headers = {}
    #     if self.session:
    #         logger.writeDebug(
    #             "VSPConnectionManager.getAuthToken:self.session is not None"
    #         )
    #         if self.session.expiry_time > time.time():
    #             headers = {"Authorization": "Session {0}".format(self.session.token)}
    #             return headers

    #     end_point = Endpoints.SESSIONS
    #     try:
    #         logger.writeDebug(
    #             "VSPConnectionManager.getAuthToken:generate a new session"
    #         )
    #         response = self._make_request(method="POST", end_point=end_point, data=None)
    #     except Exception as e:
    #         # can be due to wrong address or kong is not ready
    #         logger.writeException(e)
    #         err_msg = (
    #             "Failed to establish a connection, please check the Management System address or the credentials."
    #             + str(e)
    #         )
    #         raise Exception(err_msg)

    #     session_id = response.get(API.SESSION_ID)
    #     token = response.get(API.TOKEN)
    #     logger.writeDebug(
    #         f"VSPConnectionManager.getAuthToken session id = {session_id} token = {token}"
    #     )
    #     if self.session and self.session.expiry_time > 0:
    #         previous_session_id = self.session.session_id
    #         try:
    #             self.delete_session(previous_session_id)
    #         except Exception:
    #             logger.writeDebug(
    #                 "could not delete previous session id = {}", previous_session_id
    #             )
    #             # do not throw exception as this session is not active

    #     self.session = SessionObject(session_id, token)
    #     self.token = token
    #     headers = {"Authorization": "Session {0}".format(token)}
    #     return headers

    def get_lock_session_token(self):
        end_point = Endpoints.SESSIONS
        try:
            response = self._make_request(method="POST", end_point=end_point, data=None)

        except Exception as e:
            # can be due to wrong address or kong is not ready
            logger.writeException(e)
            err_msg = (
                "Failed to establish a connection, please check the Management System address or the credentials."
                + str(e)
            )
            raise Exception(err_msg)

        session_id = response.get(API.SESSION_ID)
        token = response.get(API.TOKEN)
        logger.writeDebug(
            "get_lock_session_token session id = {} token = {}", session_id, token
        )
        return session_id, token

    def form_base_url(self):
        return f"https://{self.address}/ConfigurationManager"

    def get_job(self, job_id):
        end_point = "v1/objects/jobs/{}".format(job_id)
        return self._make_vsp_request("GET", end_point)

    def create(self, endpoint, data, token=None):
        return self._make_vsp_request(
            method="POST", end_point=endpoint, data=data, token=token
        )

    def read(self, endpoint, headers_input=None, token=None):
        return self._make_vsp_request(
            "GET", endpoint, headers_input=headers_input, token=token
        )

    def update(self, endpoint, data, headers_input=None, token=None):
        put_response = self._make_vsp_request(
            method="PUT",
            end_point=endpoint,
            data=data,
            headers_input=headers_input,
            token=token,
        )
        job_id = put_response[API.JOB_ID]
        return self._process_job(job_id)

    def get(self, endpoint, headers_input=None, token=None):
        return self._make_vsp_request(
            "GET", endpoint, data=None, headers_input=headers_input, token=token
        )

    def get_with_headers(self, end_point, headers_input=None):
        return self._make_vsp_request("GET", end_point, None, headers_input)

    def delete_with_headers(self, end_point, headers=None):
        response = self._make_vsp_request("DELETE", end_point, None, headers)
        job_id = response[API.JOB_ID]
        return self._process_job(job_id)

    def pegasus_get(self, endpoint):
        return self._make_vsp_request("GET", endpoint)

    def pegasus_post(self, endpoint, data):
        post_response = self._make_vsp_request("POST", endpoint, data)

        job_id = post_response.get("statusResource").split("/")[-1]
        return self._process_pegasus_job(job_id)

    def pegasus_patch(self, endpoint, data):
        patch_response = self._make_vsp_request("PATCH", endpoint, data)

        if patch_response.get("statusResource") is None:
            return patch_response
        job_id = patch_response.get("statusResource").split("/")[-1]
        return self._process_pegasus_job(job_id)

    def pegasus_delete(self, endpoint, data):
        delete_response = self._make_vsp_request("DELETE", endpoint, data)

        job_id = delete_response.get("statusResource").split("/")[-1]
        return self._process_pegasus_job(job_id)

    def pegasus_post_header(self, endpoint, data, headers_input):
        post_response = self._make_vsp_request("POST", endpoint, data, headers_input)

        job_id = post_response.get("statusResource").split("/")[-1]
        return self._process_pegasus_job(job_id)

    def _process_pegasus_job(self, job_id):
        response = None
        retryCount = 0
        while response is None and retryCount < 60:
            job_response = self.get_pegasus_job(job_id)
            job_status = job_response.get(API.STATUS)
            job_progress = job_response.get(API.PEGASUS_PROGRESS)
            logger.writeDebug("patch: job_response = {}", job_response)
            response = None
            if job_progress == API.PEGASUS_COMPLETED:
                if job_status == API.PEGASUS_NORMAL:
                    # For PATCH port-auth-settings, affected resource is empty
                    response = job_response.get(API.AFFECTED_RESOURCES)[0]

                else:
                    raise Exception(job_response.get(API.ERROR_MESSAGE))
            else:
                retryCount = retryCount + 1
                time.sleep(10)

        if response is None:
            raise Exception("Timeout Error! The tasks was not completed in 10 minutes")

        resourceId = response.split("/")[-1]
        logger.writeDebug("response = {}", response)
        logger.writeDebug("resourceId = {}", resourceId)
        return resourceId

    def get_pegasus_job(self, job_id):
        url = Endpoints.PEGASUS_JOB
        return self._make_vsp_request("GET", url.format(job_id))

    def delete(self, endpoint, data=None, headers_input=None, token=None):
        delete_response = self._make_vsp_request(
            method="DELETE",
            end_point=endpoint,
            data=data,
            headers_input=headers_input,
            token=token,
        )
        job_id = delete_response[API.JOB_ID]
        return self._process_job(job_id)

    def post(self, endpoint, data, headers_input=None, token=None):

        post_response = self._make_vsp_request(
            method="POST",
            end_point=endpoint,
            data=data,
            headers_input=headers_input,
            token=token,
        )
        logger.writeDebug("post_response = {}", post_response)
        job_id = post_response[API.JOB_ID]
        return self._process_job(job_id)

    def post_without_job(self, endpoint, data, headers_input=None, token=None):

        post_response = self._make_vsp_request(
            method="POST",
            end_point=endpoint,
            data=data,
            headers_input=headers_input,
            token=token,
        )
        logger.writeDebug("post_response = {}", post_response)
        return post_response

    def post_wo_job(self, endpoint, data=None, headers_input=None):
        post_response = self._make_vsp_request(
            method="POST", end_point=endpoint, data=data, headers_input=headers_input
        )
        logger.writeDebug("post_response = {}", post_response)
        return post_response

    def patch(self, endpoint, data):
        patch_response = self._make_vsp_request(
            method="PATCH", end_point=endpoint, data=data
        )
        job_id = patch_response[API.JOB_ID]
        return self._process_job(job_id)

    def _make_vsp_request(
        self, method, end_point, data=None, headers_input=None, token=None, retry=False
    ):

        logger.writeDebug(
            f"VSPConnectionManager._make_vsp_request token= {token} self.token = {self.token}"
        )

        url = self.base_url + "/" + end_point
        headers = {}
        if token is None and self.token is None:
            headers = self.getAuthToken(retry)
        else:
            if token:
                headers = {"Authorization": "Session {0}".format(token)}
            elif self.token:
                headers = {"Authorization": "Session {0}".format(self.token)}

        headers["Content-Type"] = "application/json"
        if headers_input is not None:
            headers.update(headers_input)

        logger.writeDebug("url = {}", url)
        logger.writeDebug("headers = {}", headers)
        TIME_OUT = 300
        if data is not None and retry is False:
            data = json.dumps(data)
            logger.writeDebug("data = {}", data)
        try:

            response = open_url(
                url=url,
                method=method,
                headers=headers,
                data=data,
                use_proxy=False,
                url_username=None,
                url_password=None,
                force_basic_auth=False,
                validate_certs=False,
                timeout=TIME_OUT,
            )
        except socket.timeout as t_err:
            logger.writeError(str(t_err))
            raise Exception(t_err)
        except urllib_error.HTTPError as err:
            logger.writeError(
                f"VSPConnectionManager._make_vsp_request - HTTPError {err}"
            )
            if err.code == 503:
                # 503 Service Unavailable
                # wait for 5 mins and try to re-authenticate, we will retry 5 times
                if self.retryCount < 5:
                    logger.writeDebug(
                        f"{self.server_busy_msg}, wait for 5 mins and try to generate session token again."
                    )
                    time.sleep(300)
                    self.retryCount += 1
                    return self._make_vsp_request(
                        method, end_point, data, headers_input, token=None, retry=True
                    )
            else:
                if hasattr(err, "read"):
                    error_resp = json.loads(err.read().decode())
                    logger.writeDebug(
                        f"VSPConnectionManager.error_resp - error_resp {error_resp}"
                    )
                    error_dtls = (
                        error_resp.get("message")
                        if error_resp.get("message")
                        else error_resp.get("errorMessage")
                    )
                    if error_resp.get("cause"):
                        error_dtls = error_dtls + " " + error_resp.get("cause")

                    if error_resp.get("solution"):
                        error_dtls = error_dtls + " " + error_resp.get("solution")

                    if self.session_expired_msg in error_dtls and self.retryCount < 5:
                        logger.writeDebug(
                            "The specified token is invalid, trying to re-authenticate."
                        )
                        self.token = None
                        if self.session:
                            self.session.expiry_time = 0
                        self.retryCount += 1
                        return self._make_vsp_request(
                            method,
                            end_point,
                            data,
                            headers_input,
                            token=None,
                            retry=True,
                        )

                    else:
                        raise Exception(error_dtls)
            raise Exception(err)
        except Exception as err:
            logger.writeException(err)
            raise err

        if response.status not in (200, 201, 202):
            raise Exception(
                f"Failed to make {method} request to {url}: {response.read()}"
            )
        return self._load_response(response)

    def delete_current_session(self):
        session_id = self.session.session_id
        self.delete_session(session_id)

    def delete_session(self, session_id):
        try:
            endpoint = Endpoints.DELETE_SESSION.format(session_id)
            self.delete(endpoint)
        except Exception:
            logger.writeDebug(
                "VSPConnectionManager.delete_session - Could not discard the session."
            )
            # raise Exception("Could not discard the session.")

    # def __del__(self):
    #     logger.writeDebug("VSPConnectionManager - Destructor called.")
    #     if self.session:
    #         try:
    #            self.delete_current_session()
    #         except Exception:
    #             logger.writeDebug("VSPConnectionManager.__del__ - Could not discard the current session.")
    # raise Exception("Could not discard the current session.")

    def set_base_url_for_vsp_one_server(self):
        self.base_url = "https://{self.address}/ConfigurationManager/simple"

    def get_base_url(self):
        return self.base_url

    def set_base_url(self, url):
        self.base_url = url


# This class is added to use Administrator API for Storage Management
class AdministratorConnectionManager(VSPConnectionManager):
    def form_base_url(self):
        self.base_url = "https://{self.address}/ConfigurationManager/simple"
