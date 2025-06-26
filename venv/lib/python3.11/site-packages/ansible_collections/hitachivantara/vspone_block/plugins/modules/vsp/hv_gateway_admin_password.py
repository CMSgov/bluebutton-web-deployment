#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_gateway_admin_password
short_description: Updates password of gateway admin on Hitachi VSP storage systems.
description:
  - This module updates the password of gateway admin.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_uai_gateway/admin_password.yml)
version_added: '3.0.0'
author:
  - Hitachi Vantara LTD (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: none
deprecated:
  removed_in: '4.0.0'
  why: The connection type C(gateway) is deprecated.
  alternative: Not available.
extends_documentation_fragment:
- hitachivantara.vspone_block.common.deprecated_note
options:
  connection_info:
    description: Information required to establish a connection to the storage system.
    required: true
    type: dict
    suboptions:
      uai_gateway_address:
        description: IP address or hostname of UAI gateway.
        type: str
        required: true
      api_token:
        description: Token value to access UAI gateway. This is a required field for C(gateway) connection type.
        type: str
        required: true
  spec:
    description: Specification for updating admin password.
    type: dict
    required: false
    suboptions:
      password:
        type: str
        description: The new password value to be updated.
        required: true
"""

EXAMPLES = """
- name: Update password of UAI gateway admin
  hitachivantara.vspone_block.vsp.hv_gateway_admin_password:
    connection_info:
      uai_gateway_address: gateway.company.com
      api_token: "eyJhbGciOiJS......"
    spec:
      password: "changeMe!"
"""

RETURN = """
data:
  description: Indicates whether gateway admin password task completed successfully or not.
  returned: success
  type: str
  sample:
    - "Successfully updated apiadmin password"
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.gw_module_args import (
    GatewayArgs,
    DEPCRECATED_MSG,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_constants import (
    StateValue,
)

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class GatewayPasswordManager:
    def __init__(self):
        self.logger = Log()
        self.argument_spec = GatewayArgs().gateway_password()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
        )
        try:
            c_info = self.module.params.get("connection_info")
            self.logger.writeInfo(f"{c_info} module_params_connection_info")
            field = c_info.pop("uai_gateway_address")
            c_info["address"] = field
            c_info["connection_type"] = "gateway"
            self.params_manager = self.GatewayParametersManager(self.module.params)
            self.connection_info = self.params_manager.get_connection_info()
            self.state = self.params_manager.get_state()
            self.logger.writeInfo(f"State: {self.state}")
            self.spec = self.params_manager.set_admin_password_spec()
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(DEPCRECATED_MSG))

    def apply(self):
        self.logger.writeInfo("=== Start of Admin Password operation ===")
        registration_message = validate_ansible_product_registration()

        try:

            if not self.state:
                data = self.GatewayPasswordReconciler(
                    self.params_manager.connection_info
                ).gateway_password(self.spec)
            elif self.state == StateValue.PRESENT:
                data = self.GatewayPasswordReconciler(
                    self.params_manager.connection_info
                ).gateway_password(self.spec)
            else:
                data = "Absent operation is not supported"
            if "Successfully updated apiadmin password" in data:
                self.connection_info.changed = True

        except Exception as e:
            self.logger.writeError(f"{e}")
            self.logger.writeInfo("=== End of Admin Password operation ===")
            self.module.fail_json(msg=str(DEPCRECATED_MSG))

        response = {"changed": self.connection_info.changed, "data": data}
        if registration_message:
            response["user_consent_required"] = registration_message
        self.logger.writeInfo(f"{response}")
        self.logger.writeInfo("=== End of Admin Password operation ===")
        self.module.exit_json(**response)


def main(module=None):
    obj_store = GatewayPasswordManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
