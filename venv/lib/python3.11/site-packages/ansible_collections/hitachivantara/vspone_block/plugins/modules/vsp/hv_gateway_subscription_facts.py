#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_gateway_subscription_facts
short_description: Retrieves information about resources of a subscriber on Hitachi VSP storage systems.
description:
  - This module retrieves information about resources of a subscriber.
  - It provides details about resources of a subscriber such as type, value and other relevant information.
  - This module is supported only for C(gateway) connection type.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_uai_gateway/subscription_facts.yml)
version_added: '3.1.0'
author:
  - Hitachi Vantara LTD (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: full
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
      address:
        description: IP address or hostname of UAI gateway.
        type: str
        required: true
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: false
        choices: ['gateway']
        default: 'gateway'
      subscriber_id:
        description: This field is valid for C(gateway) connection type only. This is an optional field and only needed to support multi-tenancy environment.
        type: str
        required: false
      api_token:
        description: Token value to access UAI gateway.
        type: str
        required: false
      username:
        description: Username for authentication. This field is valid for C(direct) connection type only, and it is a required field.
          Not needed for this module.
        type: str
        required: false
      password:
        description: Password for authentication. This field is valid for C(direct) connection type only, and it is a required field.
          Not needed for this module.
        type: str
        required: false
  storage_system_info:
    description:
      - Information about the Hitachi storage system. This field is required for gateway connection type only.
    type: dict
    required: false
    suboptions:
      serial:
        description: Serial number of the Hitachi storage system.
        type: str
        required: true
"""

EXAMPLES = """
- name: Retrieve resource information about a specific subscriber
  hitachivantara.vspone_block.vsp.hv_gateway_subscription_facts:
    connection_info:
      address: gateway.company.com
      api_token: "eyJhbGciOiJS......"
      connection_type: "gateway"
      subscriber_id: "1234"
    storage_system_info:
      serial: "50015"
"""

RETURN = """
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the subscriber resources.
  returned: always
  type: dict
  contains:
    subscriber_data:
      description: List of subscribers belonging to partner apiadmin.
      type: list
      elements: dict
      contains:
        resource_value:
          description: Value of the resource.
          type: str
          sample: "CL1-A"
        storage_serial:
          description: Serial number of the Hitachi storage system.
          type: str
          sample: "50015"
        subscriber_id:
          description: ID of the subscriber.
          type: str
          sample: "811150"
        type:
          description: Type of the resource.
          type: str
          sample: "Port"
        total_capacity:
          description: Total capacity of the resource (if applicable).
          type: int
          sample: 1073741824
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.gw_module_args import (
    GatewayArgs,
    DEPCRECATED_MSG,
)

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class SubscriberResourceFactsManager:
    def __init__(self):
        self.logger = Log()
        self.argument_spec = GatewayArgs().get_subscription_facts_args()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.params_manager = None  # GatewayParametersManager(self.module.params)
            self.connection_info = self.params_manager.connection_info
            self.storage_serial_number = self.params_manager.storage_system_info.serial
        except Exception as e:
            self.module.fail_json(msg=str(DEPCRECATED_MSG))

    def apply(self):
        self.logger.writeInfo("=== Start of Gateway Subscriber Facts ===")
        registration_message = validate_ansible_product_registration()
        subscriber_data = None
        self.logger.writeInfo(
            f"{self.params_manager.connection_info.connection_type} connection type"
        )
        try:
            subscriber_data = self.SubscriberResourceReconciler(
                self.connection_info, self.storage_serial_number
            ).get_subscriber_resource_facts()

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of Gateway Subscriber Facts ===")
            self.module.fail_json(msg=str(DEPCRECATED_MSG))

        data = {
            "subscriber_data": subscriber_data,
        }
        if registration_message:
            data["user_consent_required"] = registration_message
        self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of Gateway Subscriber Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main():
    obj_store = SubscriberResourceFactsManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
