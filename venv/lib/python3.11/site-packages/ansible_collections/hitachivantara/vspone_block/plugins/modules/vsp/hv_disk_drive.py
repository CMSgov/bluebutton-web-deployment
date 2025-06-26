#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_disk_drive
short_description: Changes disk drive settings from Hitachi VSP storage systems.
description:
    - This module changes disk drive settings from Hitachi VSP storage systems.
    - For examples go to URL
      U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/disk_drive.yml)
version_added: '3.2.0'
author:
  - Hitachi Vantara LTD (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: none
extends_documentation_fragment:
- hitachivantara.vspone_block.common.gateway_note
options:
  state:
    description: The level of the Disk Drives task.
    type: str
    required: false
    choices: ['present']
    default: 'present'
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
    description: Specification for the hard drive tasks.
    type: dict
    required: false
    suboptions:
      drive_location_id:
        description: The drive location Id of the hard drive to retrieve.
        type: str
        required: false
      is_spared_drive:
        description: Specify whether the disk drive is a spared drive.
        type: bool
        required: false
"""

EXAMPLES = """
- name: Change disk drive settings
  hitachivantara.vspone_block.vsp.hv_disk_drive:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    state: "present"
    spec:
      drive_location_id: "0-16"
      is_spared_drive: true
"""

RETURN = r"""
disk_drive:
  description: Disk drive managed by the module.
  returned: success
  type: list
  elements: dict
  contains:
    copyback_mode:
      description: Indicates if copy back mode is enabled.
      type: bool
      sample: true
    drive_type:
      description: Type of the drive.
      type: str
      sample: "SSD"
    free_capacity:
      description: Free capacity of the drive.
      type: str
      sample: "5.16TB"
    is_accelerated_compression:
      description: Indicates if accelerated compression is enabled.
      type: bool
      sample: false
    is_encryption_enabled:
      description: Indicates if encryption is enabled.
      type: bool
      sample: true
    is_pool_array_group:
      description: Indicates if the drive is part of a pool array group.
      type: bool
      sample: false
    ldev_ids:
      description: List of LDEV IDs associated with the drive.
      type: list
      elements: int
      sample: []
    parity_group_id:
      description: ID of the parity group.
      type: str
      sample: "1-10"
    raid_level:
      description: RAID level of the drive.
      type: str
      sample: "RAID5"
    resource_group_id:
      description: ID of the resource group.
      type: int
      sample: -1
    status:
      description: Status of the drive.
      type: str
      sample: ""
    total_capacity:
      description: Total capacity of the drive.
      type: str
      sample: "5.16TB"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler import (
    vsp_disk_drive,
)

try:

    HAS_MESSAGE_ID = True
except ImportError:
    HAS_MESSAGE_ID = False

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPParametersManager,
    VSPParityGroupArguments,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    camel_dict_to_snake_case,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPDiskDriveManager:
    def __init__(self):
        self.logger = Log()

        self.argument_spec = VSPParityGroupArguments().drives()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
            # can be added mandotary , optional mandatory arguments
        )
        try:
            self.params_manager = VSPParametersManager(self.module.params)
            self.spec = self.params_manager.get_drives_fact_spec()
            self.serial = None
            self.state = self.params_manager.get_state()
            self.connection_info = self.params_manager.get_connection_info()
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of Disk Drive operation. ===")
        registration_message = validate_ansible_product_registration()
        try:
            result = vsp_disk_drive.VSPDiskDriveReconciler(
                self.params_manager.connection_info, self.state
            ).disk_drive_reconcile(self.state, self.spec)

            # if result is not None and result is not str:
            #   snake_case_parity_group_data = camel_dict_to_snake_case(result.to_dict())

            msg = (
                result
                if isinstance(result, str)
                else "Disk drive settings changed successfully."
            )
            result = (
                camel_dict_to_snake_case(result)
                if not isinstance(result, str)
                else None
            )
            response_dict = {
                "changed": self.connection_info.changed,
                "data": result,
                "msg": msg,
            }
            if registration_message:
                response_dict["user_consent_required"] = registration_message

            self.logger.writeInfo(f"{response_dict}")
            self.logger.writeInfo("=== End of Disk Drive operation. ===")
            self.module.exit_json(**response_dict)
        except Exception as ex:
            self.logger.writeException(ex)
            self.logger.writeInfo("=== End of Disk Drive operation. ===")
            self.module.fail_json(msg=str(ex))


def main():
    obj_store = VSPDiskDriveManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
