#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_shadow_image_group_facts
short_description: Retrieves Local Copy Groups information from Hitachi VSP storage systems.
description:
  - This module retrieves information about Local Copy Groups from Hitachi VSP storage systems.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/local_copy_group_facts.yml)
version_added: '3.2.0'
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
  spec:
    description: Specification for the Local Copy Group facts to be gathered.
    type: dict
    required: false
    suboptions:
      name:
        description: The local copy group name. If not provided, list of all copy groups will be returned.
        type: str
        required: false
      primary_volume_device_group_name:
        description: Specify the device group name for the P-VOL. Value should not exceed 31 characters. The name is case sensitive.
        type: str
        required: false
      secondary_volume_device_group_name:
        description: Specify the device group name for the S-VOL. Value should not exceed 31 characters. The name is case sensitive.
        type: str
        required: false
      should_include_copy_pairs:
        description: Whether we want to get all local copy pairs from a specific copy group. Should be specified along with the 'name' parameter in spec.
        type: bool
        required: false
"""

EXAMPLES = """
- name: Get all shadow image groups
  hitachivantara.vspone_block.vsp.hv_shadow_image_group_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"

- name: Get one shadow image group by name
  hitachivantara.vspone_block.vsp.hv_shadow_image_group_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"
    spec:
      name: "copygroup1"

- name: Get one shadow image group by name with copy pairs information
  hitachivantara.vspone_block.vsp.hv_shadow_image_group_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"
    spec:
      name: "copygroup1"
      should_include_remote_replication_pairs: true
"""

RETURN = r"""
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the local copy groups.
  returned: always
  type: dict
  contains:
    shadow_image_groups:
      description: A list of local copy groups gathered from the storage system.
      type: list
      elements: dict
      contains:
        copy_group_name:
          description: The name of the local copy group.
          type: str
          sample: "CG_366_444"
        pvol_device_group_name:
          description: The name of the primary volume device group.
          type: str
          sample: "CG_366_444P_"
        svol_device_group_name:
          description: The name of the secondary volume device group.
          type: str
          sample: "CG_366_444S_"
        local_clone_copygroup_id:
          description: The ID of the local clone copy group.
          type: str
          sample: "CG_366_444,CG_366_444P_,CG_366_444S_,CP_366_444"
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.vsp_local_copy_group import (
    VSPLocalCopyGroupReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPLocalCopyGroupArguments,
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPLocalCopyGroupFactsManager:
    def __init__(self):
        self.logger = Log()
        self.argument_spec = VSPLocalCopyGroupArguments().local_copy_group_facts()

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.parameter_manager = VSPParametersManager(self.module.params)
            self.connection_info = self.parameter_manager.get_connection_info()
            self.storage_serial_number = self.parameter_manager.get_serial()
            self.spec = self.parameter_manager.get_local_copy_groups_fact_spec()
            # self.spec.copy_group_name = self.spec.name
            self.state = self.parameter_manager.get_state()
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of Local Copy Group Facts ===")

        registration_message = validate_ansible_product_registration()
        try:
            reconciler = VSPLocalCopyGroupReconciler(
                self.connection_info, self.storage_serial_number, self.state
            )

            copy_groups = reconciler.get_local_copy_group_facts(self.spec)
            msg = ""

            if (
                self.spec.name is not None
                and self.spec.should_include_copy_pairs is True
            ):
                if "copy_pairs" not in copy_groups:
                    msg = "Copy pair information not available for copy group {} as operations cannot be performed for this copy group".format(
                        self.spec.name
                    )
                elif copy_groups is not None:
                    msg = "Shadow Image Group  information along with copy pairs retrieved successfully"
            elif self.spec.name is not None and copy_groups is not None:
                msg = "Shadow Image Group information retrieved successfully"
            elif copy_groups is not None:
                msg = "Shadow Image Groups retrieved successfully"
            self.logger.writeDebug(
                f"MOD:hv_shadow_image_group_facts:copy_groups= {copy_groups}"
            )

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of Local Copy Group Facts ===")
            self.module.fail_json(msg=str(e))
        data = {"shadow_image_groups": copy_groups, "msg": msg}
        if registration_message:
            data["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of Local Copy Group Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main(module=None):
    obj_store = VSPLocalCopyGroupFactsManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
