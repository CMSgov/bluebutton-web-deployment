#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_external_parity_group_facts
short_description: Retrieves information about External Parity Group from Hitachi VSP storage systems.
description:
  - This module retrieves information about External Volume from Hitachi VSP storage systems.
  - For examples, go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/external_parity_group_facts.yml)
version_added: '3.5.0'
author:
  - Hitachi Vantara LTD (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: full
extends_documentation_fragment:
- hitachivantara.vspone_block.common.gateway_note
options:
  storage_system_info:
    description: Information about the storage system. This field is an optional field.
    type: dict
    required: false
    suboptions:
      serial:
        description: The serial number of the storage system.
        type: str
        required: false
  connection_info:
    description: Information required to establish a connection to the storage system.
    type: dict
    required: true
    suboptions:
      address:
        description: IP address or hostname of the storage system.
        type: str
        required: true
      username:
        description: Username for authentication. This is a required field if api_token is not provided.
        type: str
        required: false
      password:
        description: Password for authentication. This is a required field if api_token is not provided.
        type: str
        required: false
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: false
        choices: ['direct']
        default: 'direct'
      api_token:
        description: This field is used to pass the value of the lock token to operate on locked resources.
        type: str
        required: false
  spec:
    description: Specification for retrieving External Parity Group information.
    type: dict
    required: false
    suboptions:
      external_parity_group:
        description: The external parity group ID.
        type: str
        required: false
"""

EXAMPLES = """
- name: Retrieve information about all External Parity Groups
  hitachivantara.vspone_block.vsp.hv_external_path_group_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "changeme"

- name: Retrieve information about a specific External Parity Groups
  hitachivantara.vspone_block.vsp.hv_external_path_group_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "changeme"
    spec:
      external_parity_group: "1-1"
"""

RETURN = """
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the external parity groups.
  returned: always
  type: list
  elements: dict
  contains:
    external_parity_group_id:
      description: External parity group ID.
      type: str
      sample: "1-1"
    available_volume_capacity:
      description: Available capacity (GB).
      type: int
      sample: 12
    used_capacity_rate:
      description: Usage rate of the external parity group.
      type: int
      sample: 12
    storage_serial_number:
      description: Storage serial number.
      type: str
      sample: "810050"
    spaces:
      description: For the free space and the LDEV defined in the specified external parity group.
      type: list
      elements: dict
      contains:
        lba_size:
          description: ize of the partition in the external parity group (in a multiple of 512 bytes).
          type: str
          sample: "0x000000200000"
        ldev_id:
          description: LDEV number.
          type: int
          sample: 1351
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.vsp_external_parity_group import (
    VSPExternalParityGroupReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPParametersManager,
    VSPExternalParityGroupArguments,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class FactManager:
    def __init__(self):
        self.logger = Log()

        self.argument_spec = (
            VSPExternalParityGroupArguments().external_parity_group_fact()
        )
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.params_manager = VSPParametersManager(self.module.params)
            self.spec = self.params_manager.get_external_parity_group_fact_spec()
            self.serial = self.params_manager.get_serial()
            self.logger.writeDebug("20250228 serial={}", self.serial)
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of External Parity Group Facts ===")
        registration_message = validate_ansible_product_registration()
        try:
            result = []
            result = VSPExternalParityGroupReconciler(
                self.params_manager.connection_info, self.serial
            ).external_parity_group_facts(self.spec)

        except Exception as ex:

            self.logger.writeException(ex)
            self.logger.writeInfo("=== End of External Parity Group Facts ===")
            self.module.fail_json(msg=str(ex))
        data = {
            "external_parity_groups": result,
        }
        if registration_message:
            data["user_consent_required"] = registration_message
        # self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of External  Parity Group Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main(module=None):
    obj_store = FactManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
