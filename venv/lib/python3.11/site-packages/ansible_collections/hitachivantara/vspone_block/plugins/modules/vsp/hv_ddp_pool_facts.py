#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_ddp_pool_facts
short_description: Get facts of DDP Pools on Hitachi VSP storage systems.
description: >
  - This module retrieves details of DDP Pools on Hitachi VSP storage systems.
  - This module is only available for VSP One storage systems.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/ddp_pool_facts.yml)
version_added: '3.4.0'
author:
  - Hitachi Vantara, LTD. (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: full
extends_documentation_fragment:
- hitachivantara.vspone_block.common.gateway_note
options:
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
        description: Username for authentication. This is a required field.
        type: str
        required: true
      password:
        description: Password for authentication. This is a required field.
        type: str
        required: true
  spec:
    description: Specification for retrieving DDP pool information.
    type: dict
    required: false
    suboptions:
      pool_id:
        description: ID of the DDP Pool.
        type: int
        required: false
      pool_name:
        description: Name of the DDP Pool.
        type: str
        required: false
"""

EXAMPLES = """
- name: Get all DDP Pools
  hitachivantara.vspone_block.vsp.hv_ddp_pool_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"

- name: Get DDP Pool by ID
  hitachivantara.vspone_block.vsp.hv_ddp_pool_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"
    spec:
      pool_id: 15

- name: Get DDP Pool by Name
  hitachivantara.vspone_block.vsp.hv_ddp_pool_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"
    spec:
      pool_name: "DDP-1"
"""

RETURN = """
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the DDP pools.
  returned: always
  type: dict
  contains:
    DDP_Pools:
      description: A list of DDP pools information.
      returned: success
      type: dict
      contains:
        capacity_manage:
          description: Capacity management details.
          type: list
          elements: dict
          contains:
            threshold_depletion:
              description: Threshold for capacity depletion.
              type: int
              sample: 80
            threshold_warning:
              description: Threshold for capacity warning.
              type: int
              sample: 70
            used_capacity_rate:
              description: Used capacity rate.
              type: int
              sample: 0
        config_status:
          description: Configuration status of the pool.
          type: list
          elements: str
        contains_capacity_saving_volume:
          description: Indicates if the pool contains capacity-saving volumes.
          type: bool
          sample: false
        drives:
          description: Details of the drives in the pool.
          type: list
          elements: dict
          contains:
            display_drive_capacity:
              description: Display capacity of the drive.
              type: str
              sample: "1.9 TB"
            drive_capacity_gb:
              description: Capacity of the drive in GB.
              type: int
              sample: 1900
            drive_interface:
              description: Interface type of the drive.
              type: str
              sample: "NVMe"
            drive_rpm:
              description: Drive RPM.
              type: str
              sample: "NUMBER_0"
            drive_type:
              description: Type of the drive.
              type: str
              sample: "SSD"
            locations:
              description: Locations of the drives.
              type: list
              elements: str
              sample: ["0-0", "0-1", "0-2", "0-3"]
            number_of_drives:
              description: Number of drives.
              type: int
              sample: 4
            parity_group_type:
              description: Parity group type.
              type: str
              sample: "DEFAULT"
            raid_level:
              description: RAID level.
              type: str
              sample: "RAID5"
            total_capacity:
              description: Total capacity of the drives in GB.
              type: int
              sample: 7600
        effective_capacity:
          description: Effective capacity of the pool in GB.
          type: int
          sample: 3990
        encryption:
          description: Encryption status of the pool.
          type: str
          sample: "DISABLED"
        free_capacity_mb:
          description: Free capacity of the pool in MB.
          type: int
          sample: 3990
        id:
          description: ID of the DDP Pool.
          type: int
          sample: 15
        name:
          description: Name of the DDP Pool.
          type: str
          sample: "GK-21268"
        number_of_drive_types:
          description: Number of drive types in the pool.
          type: int
          sample: 1
        number_of_tiers:
          description: Number of tiers in the pool.
          type: int
          sample: 0
        number_of_volumes:
          description: Number of volumes in the pool.
          type: int
          sample: 13
        saving_effects:
          description: Details of saving effects in the pool.
          type: dict
          contains:
            calculation_end_time:
              description: End time of the calculation.
              type: str
              sample: "2025-04-03T22:23:00Z"
            calculation_start_time:
              description: Start time of the calculation.
              type: str
              sample: "2025-04-03T22:21:19Z"
            data_reduction_without_system_data:
              description: Data reduction without system data.
              type: int
              sample: -1
            data_reduction_without_system_data_status:
              description: Status of data reduction without system data.
              type: str
              sample: "NoTargetData"
            efficiency_data_reduction:
              description: Efficiency of data reduction.
              type: int
              sample: -1
            efficiency_fmd_saving:
              description: Efficiency of FMD saving.
              type: int
              sample: -1
            is_total_efficiency_support:
              description: Indicates if total efficiency is supported.
              type: bool
              sample: true
            post_capacity_fmd_saving:
              description: Post-capacity FMD saving.
              type: int
              sample: 0
            pre_capacity_fmd_saving:
              description: Pre-capacity FMD saving.
              type: int
              sample: 0
            software_saving_without_system_data:
              description: Software saving without system data.
              type: int
              sample: -1
            software_saving_without_system_data_status:
              description: Status of software saving without system data.
              type: str
              sample: "NoTargetData"
            total_efficiency:
              description: Total efficiency of the pool.
              type: int
              sample: 9223372036854775807
            total_efficiency_status:
              description: Status of total efficiency.
              type: str
              sample: "Valid"
        status:
          description: Status of the pool.
          type: str
          sample: "Normal"
        subscription_limit:
          description: Subscription limit details.
          type: dict
          contains:
            current_rate:
              description: Current subscription rate.
              type: int
              sample: 396
            is_enabled:
              description: Indicates if subscription limit is enabled.
              type: bool
              sample: false
        tiers:
          description: Details of the tiers in the pool.
          type: list
          elements: dict
        total_capacity_mb:
          description: Total capacity of the pool in MiB.
          type: int
          sample: 3990
        used_capacity_mb:
          description: Used capacity of the pool in MB.
          type: int
          sample: 0
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler import (
    vsp_dynamic_pool_reconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPParametersManager,
    VSPDynamicPoolArgs,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPDynamicPoolFacts:
    def __init__(self):
        self.logger = Log()

        self.argument_spec = VSPDynamicPoolArgs().vsp_dynamic_pool_facts_spec()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.params_manager = VSPParametersManager(self.module.params)
            self.spec = self.params_manager.get_dynamic_pool_facts_spec()
            self.connection_info = self.params_manager.get_connection_info()
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of DDP Pool facts operation. ===")
        try:
            registration_message = validate_ansible_product_registration()
            result = vsp_dynamic_pool_reconciler.VspDynamicPoolReconciler(
                self.params_manager.connection_info,
            ).dynamic_pool_facts(self.spec)

            data = {
                "DDP_Pools": result,
            }
            if registration_message:
                data["user_consent_required"] = registration_message
            self.logger.writeInfo("=== End of DDP Pool facts operation. ===")
            self.module.exit_json(changed=False, ansible_facts=data)
        except Exception as ex:
            self.logger.writeException(ex)
            self.logger.writeInfo("=== End of DDP Pool facts operation. ===")
            self.module.fail_json(msg=str(ex))


def main():
    obj_store = VSPDynamicPoolFacts()
    obj_store.apply()


if __name__ == "__main__":
    main()
