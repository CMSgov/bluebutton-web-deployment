#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_shadow_image_pair
short_description: Manages shadow image pairs on Hitachi VSP storage systems.
description:
  - This module allows for the creation, deletion, splitting, syncing, restoring and migrating of shadow image pairs on Hitachi VSP storage systems.
  - It supports various shadow image pairs operations based on the specified task level.
  - For examples, go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/shadow_image_pair.yml)
version_added: '3.0.0'
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
notes:
  - The output parameters C(entitlement_status), C(subscriber_id) and C(partner_id) were removed in version 3.4.0.
    They were also deprecated due to internal API simplification and are no longer supported.
options:
  state:
    description: The level of the shadow image pairs task. Choices are C(present), C(absent), C(split), C(restore), C(sync), C(migrate).
    type: str
    required: false
    choices: ['present', 'absent', 'split', 'restore', 'sync', 'migrate']
    default: 'present'
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
    description: Specification for the shadow image pairs task.
    type: dict
    required: true
    suboptions:
      primary_volume_id:
        description: Primary volume id.
        type: int
        required: false
      secondary_volume_id:
        description: Secondary volume id.
        type: int
        required: false
      secondary_pool_id:
        description: Secondary storage pool id.
        type: int
        required: false
      auto_split:
        description: Auto split.
        type: bool
        required: false
      allocate_new_consistency_group:
        description: New consistency group.
        type: bool
        required: false
      consistency_group_id:
        description: Consistency group id.
        type: int
        required: false
      copy_pace_track_size:
        description: Copy pace track size.
        type: str
        required: false
        choices: ['SLOW', 'MEDIUM', 'FAST']
      enable_quick_mode:
        description: Enable quick mode.
        type: bool
        required: false
      enable_read_write:
        description: Enable read write.
        type: bool
        required: false
      pair_id:
        description: Pair Id.
        type: str
        required: false
      is_data_reduction_force_copy:
        description: Enable data reduction force copy.
        type: bool
        required: false
      copy_group_name:
        description: Copy group name.
        type: str
        required: false
      copy_pair_name:
        description: Copy pair name.
        type: str
        required: false
      primary_volume_device_group_name:
        description: Primary volume device name.
        type: str
        required: false
      secondary_volume_device_group_name:
        description: Secondary volume device name.
        type: str
        required: false
      should_delete_svol:
        description: Specify to delete SVOL from hostgroup, iSCSI Target, and NVM Subsystem.
        type: bool
        required: false
      should_force_split:
        description: Specify to force split.
        type: bool
        required: false
      create_for_migration:
        description: Specify to create shadow image pair for migration.
        type: bool
        required: false
"""

EXAMPLES = """
- name: Create shadow image pair for non-existing secondary volume
  hitachivantara.vspone_block.vsp.hv_shadow_image_pair:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    state: "present"
    spec:
      primary_volume_id: 274
      secondary_pool_id: 1
      allocate_new_consistency_group: true
      copy_pace_track_size: "MEDIUM"
      enable_quick_mode: false
      auto_split: true
      copy_group_name: "CGTest"
      copy_pair_name: "CPTest"
      primary_volume_device_group_name: "CPTestP"
      secondary_volume_device_group_name: "CPTestS"
"""

RETURN = """
data:
  description: Newly created shadow image pair object.
  returned: success
  type: dict
  contains:
    consistency_group_id:
      description: Consistency group id.
      type: int
      sample: -1
    copy_pace_track_size:
      description: Copy pace track size.
      type: str
      sample: "MEDIUM"
    copy_rate:
      description: Copy rate.
      type: int
      sample: 100
    mirror_unit_id:
      description: Mirror unit id.
      type: int
      sample: -1
    primary_hex_volume_id:
      description: Primary hex volume id.
      type: str
      sample: "00:01:12"
    primary_volume_id:
      description: Primary volume id.
      type: int
      sample: 274
    resource_id:
      description: Resource id.
      type: str
      sample: "localpair-2749fed78e8d23a61ed17a8af71c85f8"
    secondary_hex_volume_id:
      description: Secondary hex volume id.
      type: str
      sample: "00:01:17"
    secondary_volume_id:
      description: Secondary volume id.
      type: int
      sample: 279
    status:
      description: Status.
      type: str
      sample: "PAIR"
    storage_serial_number:
      description: Storage serial number.
      type: str
      sample: "811150"
    svol_access_mode:
      description: Svol access mode.
      type: str
      sample: "READONLY"
    pvol_nvm_subsystem_name:
      description: Primary volume's nvm subsystem name.
      type: str
      sample: "smrha-3950276934"
    svol_nvm_subsystem_name:
      description: Secondary volume's nvm subsystem name.
      type: str
      sample: "smrha-3950276934"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPShadowImagePairArguments,
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_constants import (
    StateValue,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler import (
    vsp_shadow_image_pair_reconciler,
)

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    operation_constants,
)


class VSPShadowImagePairManager:
    def __init__(self):

        self.logger = Log()
        self.argument_spec = VSPShadowImagePairArguments().shadow_image_pair()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
        )

        try:
            self.params_manager = VSPParametersManager(self.module.params)
            self.connection_info = self.params_manager.get_connection_info()
            self.serial = self.params_manager.get_serial()
            self.state = self.params_manager.get_state()
            if self.state is None:
                self.state = StateValue.PRESENT
            self.logger.writeDebug(f"State: {self.state}")

            self.spec = self.params_manager.set_shadow_image_pair_spec()

        except Exception as e:
            self.logger.writeError(f"An error occurred during initialization: {str(e)}")
            self.module.fail_json(msg=str(e))

    def shadow_image_pair(self):
        reconciler = vsp_shadow_image_pair_reconciler.VSPShadowImagePairReconciler(
            self.params_manager.connection_info,
            self.params_manager.storage_system_info.serial,
            self.spec,
        )
        return reconciler.shadow_image_pair_module(self.state)

    def apply(self):
        self.logger.writeInfo("=== Start of Shadow Image operation. ===")
        registration_message = validate_ansible_product_registration()
        self.logger.writeInfo(
            f"{self.params_manager.connection_info.connection_type} connection type"
        )
        shadow_image_resposne = None
        try:
            shadow_image_resposne = self.shadow_image_pair()

        except Exception as e:
            self.logger.writeError(f"An error occurred: {str(e)}")
            self.logger.writeInfo("=== End of Shadow Image operation. ===")
            self.module.fail_json(msg=str(e))
        operation = operation_constants(self.module.params["state"])
        if operation == "split" and self.spec.should_split_force is not None:
            operation = "migration cancelled"
        msg = (
            f"Shadow image pair {operation} successfully."
            if not isinstance(shadow_image_resposne, str)
            else shadow_image_resposne
        )
        response = {
            "changed": self.connection_info.changed,
            "data": (
                shadow_image_resposne
                if not isinstance(shadow_image_resposne, str)
                else None
            ),
            "msg": msg,
        }
        if registration_message:
            response["registration_message"] = registration_message
        self.logger.writeInfo(f"{response}")
        self.logger.writeInfo("=== End of Shadow Image operation. ===")
        self.module.exit_json(**response)


def main(module=None):

    obj_store = VSPShadowImagePairManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
