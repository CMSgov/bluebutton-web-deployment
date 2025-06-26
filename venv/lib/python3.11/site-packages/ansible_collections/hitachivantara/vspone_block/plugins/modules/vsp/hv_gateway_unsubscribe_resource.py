#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_gateway_unsubscribe_resource
short_description: Manages un-subscription of resources for a subscriber on Hitachi VSP storage systems.
description:
  - This module unsubscribes different resources for a subscriber.
  - This module is supported only for C(gateway) connection type.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_uai_gateway/unsubscribe_resource.yml)
version_added: '3.1.0'
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
  spec:
    description: Specification for the un-subscription task.
    type: dict
    required: true
    suboptions:
      resources:
        description: Resources information that to be unsubscribed.
        type: list
        required: true
        elements: dict
        suboptions:
          type:
            description: Type of the resource.
            type: str
            required: true
          values:
            description: List of values for the resource.
            type: list
            required: true
            elements: str
"""

EXAMPLES = """
- name: Try to unsubscribe listed resources
  hitachivantara.vspone_block.vsp.hv_gateway_unsubscribe_resource:
    connection_info:
      address: gateway.company.com
      api_token: "eyJhbGciOiJS......"
      connection_type: "gateway"
      subscriber_id: "1234"
    spec:
      resources:
        - type: "hostgroup"
          values: ["test-001", "test-005"]
        - type: "volume"
          values: ["5015", "5016"]
        - type: "port"
          values: ["CL5-A", "CL1-A"]
"""


RETURN = """
data:
  description: List of failure and success tasks for the un-subscription try.
  returned: success
  type: list
  elements: dict
  contains:
    error:
      description: List of error messages encountered during the un-subscription process.
      type: list
      elements: str
      sample: [
        "Did not find Host Group test-001.",
        "Unable to untag Host Group test-005 from subscriber 811150 since it is already attached to volumes.",
        "Failed to untag storage volume 5015 from subscriber 811150 as it is tagged to a host group or iSCSI target",
        "Failed to untag storage volume 5016 from subscriber 811150 as it is tagged to a host group or iSCSI target",
        "Host group is present in Port CL5-A that tagged to the subscriber 811150",
        "Did not find Port with ID CL1-A.",
        "Storage is not registered",
        "Resource not found",
        "Unable to find the resource. localpair-6764f2c78f8f53a1766ad716a65206f8."
      ]
    info:
      description: List of informational messages encountered during the un-subscription process.
      type: list
      elements: str
      sample: [
        "Found 1 Host Group(s) called test-005.",
        "Found Volume with LDEV ID 5015.",
        "Found Volume with LDEV ID 5016.",
        "Found Port with ID CL5-A.",
        "Found shadowimage with ID localpair-6764f2c78f8f53a1766ad716a65206f7."
      ]
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.gw_module_args import (
    GatewayArgs,
    DEPCRECATED_MSG,
)

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_constants import (
    ConnectionTypes,
)

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log_decorator import (
    LogDecorator,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.message.module_msgs import (
    ModuleMessage,
)


@LogDecorator.debug_methods
class UnsubscriberManager:

    def __init__(self):
        self.logger = Log()
        self.argument_spec = GatewayArgs().get_unsubscribe_resource_args()

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
        )
        try:

            self.params_manager = None  # VSPParametersManager(self.module.params)
            self.connection_info = self.params_manager.connection_info
            self.storage_serial_number = self.params_manager.storage_system_info.serial
            self.spec = self.params_manager.unsubscribe_spec()
            self.state = self.params_manager.get_state()

        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(DEPCRECATED_MSG))

    def apply(self):
        self.logger.writeInfo("=== Start of Gateway Unsubscribe operation ===")
        registration_message = validate_ansible_product_registration()
        data = None
        self.logger.writeDebug(f"Spec = {self.spec}")
        self.logger.writeDebug("state = {}", self.state)
        try:

            err, data = self.unsubscribe_module()

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of Gateway Unsubscribe operation ===")
            self.module.fail_json(msg=str(DEPCRECATED_MSG))

        resp = {
            "changed": self.connection_info.changed,
            "info": data,
            "error": err,
            "msg": "Un-subscription tasks completed.",
        }
        if registration_message:
            resp["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{resp}")
        self.logger.writeInfo("=== End of Gateway Unsubscribe operation ===")
        self.module.exit_json(**resp)

    def unsubscribe_module(self):

        reconciler = self.argument_spec.VSPUnsubscriberReconciler(
            self.connection_info, self.storage_serial_number, self.state
        )
        if self.connection_info.connection_type == ConnectionTypes.GATEWAY:
            found = reconciler.check_storage_in_ucpsystem()
            if not found:
                raise ValueError(ModuleMessage.STORAGE_SYSTEM_ONBOARDING.value)

        result = reconciler.unsubscribe(self.spec)
        return result


def main(module=None):
    obj_store = UnsubscriberManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
