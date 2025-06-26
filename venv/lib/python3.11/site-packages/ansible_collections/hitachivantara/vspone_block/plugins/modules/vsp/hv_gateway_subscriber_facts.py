#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_gateway_subscriber_facts
short_description: Retrieves information about subscriber on Hitachi VSP storage systems.
description:
  - This module retrieves information about subscriber.
  - It provides details about a subscriber such as name, ID and other relevant information.
  - This module is supported only for C(gateway) connection type.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_uai_gateway/subscriber_facts.yml)
version_added: '3.0.0'
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
        description: IP address or hostname of the UAI gateway.
        type: str
        required: true
      username:
        description: Username for authentication. Not needed for this module.
        type: str
        required: false
      password:
        description: Password for authentication. Not needed for this module.
        type: str
        required: false
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: false
        choices: ['gateway']
        default: 'gateway'
      api_token:
        description: Token value to access UAI gateway.
        type: str
        required: false
  spec:
    description: Specification for retrieving subscriber information.
    type: dict
    required: false
    suboptions:
      subscriber_id:
        description: ID of the specific subscriber to retrieve information for. Works for C(gateway) connection type only.
        type: str
        required: false
"""

EXAMPLES = """
- name: Retrieve information about all subscribers
  hitachivantara.vspone_block.vsp.hv_gateway_subscriber_facts:
    connection_info:
      address: gateway.company.com
      api_token: "eyJhbGciOiJS......"
      connection_type: "gateway"
    spec:
      subscriber_id: "811150"

- name: Retrieve information about a specific subscriber
  hitachivantara.vspone_block.vsp.hv_gateway_subscriber_facts:
    connection_info:
      address: gateway.company.com
      api_token: "eyJhbGciOiJS......"
      connection_type: "gateway"
    spec:
      subscriber_id: "1234"
"""

RETURN = r"""
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the subscribers.
  returned: always
  type: dict
  contains:
    subscriber_data:
      description: List of subscribers with their attributes.
      type: list
      elements: dict
      contains:
        hard_limit_in_percent:
          description: Hard limit percentage for the subscriber.
          type: str
          sample: "90"
        message:
          description: Message related to the subscriber.
          type: str
          sample: ""
        name:
          description: Name of the subscriber.
          type: str
          sample: "TestSubscriber"
        partner_id:
          description: Partner ID associated with the subscriber.
          type: str
          sample: "apiadmin"
        quota_limit_in_gb:
          description: Quota limit in GB for the subscriber.
          type: str
          sample: "90"
        soft_limit_in_percent:
          description: Soft limit percentage for the subscriber.
          type: str
          sample: "80"
        state:
          description: State of the subscriber.
          type: str
          sample: "NORMAL"
        subscriber_id:
          description: Unique identifier for the subscriber.
          type: str
          sample: "811150"
        time:
          description: Timestamp of the subscriber data.
          type: int
          sample: 1716260209
        type:
          description: Type of the subscriber.
          type: str
          sample: "subscriber"
        used_quota_in_gb:
          description: Used quota in GB for the subscriber.
          type: str
          sample: "0.1953125"
        used_quota_in_percent:
          description: Used quota percentage for the subscriber.
          type: float
          sample: 0.2170139
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


class SubscriberFactsManager:
    def __init__(self):

        self.logger = Log()
        self.argument_spec = GatewayArgs().get_subscriber_facts_args()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.params_manager = None
            self.spec = None
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of Gateway Subscriber Facts ===")
        registration_message = validate_ansible_product_registration()
        subscriber_data = None

        try:

            subscriber_data = self.SubscriberReconciler(
                self.params_manager.connection_info
            ).get_subscriber_facts(self.params_manager.spec)

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
    obj_store = SubscriberFactsManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
