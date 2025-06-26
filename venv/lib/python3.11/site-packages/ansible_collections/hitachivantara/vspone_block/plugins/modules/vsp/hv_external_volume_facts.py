#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_external_volume_facts
short_description: Retrieves information about External Volume from Hitachi VSP storage systems.
description:
  - This module retrieves information about External Volume from Hitachi VSP storage systems.
  - For examples, go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/external_volume_facts.yml)
version_added: '3.3.0'
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
      api_token:
        description: This field is used to pass the value of the lock token to operate on locked resources.
        type: str
        required: false
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: false
        choices: ['direct']
        default: 'direct'
  spec:
    description: Specification for retrieving External Volume information.
    type: dict
    required: false
    suboptions:
      external_storage_serial:
        description: The external storage serial number.
        type: str
        required: false
      external_ldev_id:
        description: The external LDEV ID.
        type: int
        required: false

"""

EXAMPLES = """
- name: Retrieve information about all External Volume
  hitachivantara.vspone_block.vsp.hv_external_volume_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "changeme"
    spec:
      external_storage_serial: '410109'
      external_ldev_id: 1354
"""

RETURN = """
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the external path groups.
  returned: always
  type: list
  elements: dict
  contains:
    external_path_groups:
      description: The list of external path groups.
      type: list
      elements: dict
      contains:
        external_path_group_id:
          description: External path group number.
          type: int
          sample: 1
        external_serial_number:
          description: Serial number of the external storage system.
          type: str
          sample: "410109"
        storage_serial_number:
          description: Serial number of the storage system.
          type: str
          sample: "410109"
        external_parity_groups:
          description: The list of external parity groups.
          type: list
          elements: dict
          contains:
            cache_mode:
              description: Cache mode.
              type: str
              sample: "E"
            external_parity_group_id:
              description: External parity group ID.
              type: str
              sample: "1-3"
            external_parity_group_status:
              description: Status of the external parity group.
              type: str
              sample: "NML"
            is_data_direct_mapping:
              description: Whether the data direct mapping attribute is enabled.
              type: bool
              sample: false
            is_inflow_control_enabled:
              description: Inflow cache control.
              type: bool
              sample: false
            load_balance_mode:
              description: The load balancing method for I/O operations for the external storage system.
              type: str
              sample: "N"
            mp_blade_id:
              description: Inflow cache control.
              type: int
              sample: 0
            path_mode:
              description: Path mode of the external storage system.
              type: str
              sample: "M"
            external_luns:
              description: List of LUNs of the external storage system.
              type: list
              elements: dict
              contains:
                external_lun:
                  description: LUN within the ports of the external storage system.
                  type: int
                  sample: 2
                external_wwn:
                  description: WWN of the external storage system.
                  type: str
                  sample: "50060e8012277d71"
                path_status:
                  description: Status of the external path.
                  type: str
                  sample: "NML"
                port_id:
                  description: Port number.
                  type: str
                  sample: "CL6-B"
                priority:
                  description: Priority within the external path group.
                  type: int
                  sample: 1
 """

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.vsp_external_volume_reconciler import (
    VSPExternalVolumeReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPParametersManager,
    VSPExternalVolumeArguments,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPExternalVolumeFactManager:
    def __init__(self):
        self.logger = Log()

        self.argument_spec = VSPExternalVolumeArguments().external_volume_fact()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.params_manager = VSPParametersManager(self.module.params)
            self.spec = self.params_manager.get_external_volume_fact_spec()
            self.serial = self.params_manager.get_serial()
            self.logger.writeDebug("20250228 serial={}", self.serial)
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of External Volume Facts ===")
        registration_message = validate_ansible_product_registration()
        try:
            result = []
            result = VSPExternalVolumeReconciler(
                self.params_manager.connection_info, self.serial
            ).external_volume_facts(self.spec)

        except Exception as ex:

            self.logger.writeException(ex)
            self.logger.writeInfo("=== End of External Volume Facts ===")
            self.module.fail_json(msg=str(ex))
        data = {
            "external_volume": result,
        }
        if registration_message:
            data["user_consent_required"] = registration_message
        # self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of External Volume Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main(module=None):
    obj_store = VSPExternalVolumeFactManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
