#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_resource_group_lock
short_description: Allows the locking and unlocking of resource groups on Hitachi VSP storage systems.
description:
    - This module allows the locking and unlocking of resource groups on Hitachi VSP storage systems.
    - For examples, go to URL
      U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/resource_management_with_lock/vsp_direct)
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
notes:
  - The input parameters C(id) and C(name) were removed in version 3.4.0.
    They were deprecated due to internal API simplification and are no longer supported.
  - The output parameters C(entitlement_status), C(subscriber_id), and C(partner_id) were removed in version 3.4.0.
    They were also deprecated due to internal API simplification and are no longer supported.
options:
  state:
    description:
      - Set state to C(present) for locking resource group.
      - Set state to C(absent) for unlocking resource group.
    type: str
    required: false
    choices: ['present', 'absent']
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
        description: This token is required while working on locked resources. Provide the lock_token value returned
          by lock resource group task for primary storage system.
        type: str
        required: false
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: false
        choices: ['direct']
        default: 'direct'
  secondary_connection_info:
    description: Information required to establish a connection to the remote storage system.
    type: dict
    required: false
    suboptions:
      address:
        description: IP address or hostname of the storage system.
        type: str
        required: true
      username:
        description: Username for authentication for secondary storage. This is a required field if api_token is not provided.
        type: str
        required: false
      password:
        description: Password for authentication for secondary storage. This is a required field if api_token is not provided.
        type: str
        required: false
      api_token:
        description: This token is required while working on locked resources. Provide the lock_token value returned
          by lock resource group task for secondary storage system.
        type: str
        required: false
  spec:
    description: Specification for the resource group lock.
    type: dict
    required: false
    suboptions:
      lock_timeout_sec:
        description: The time that elapses before a lock timeout (in seconds). Specify a value from 0 to 7200.
          Default is 0.
        type: int
        required: false
"""

EXAMPLES = """
- name: Resource management with Resource Group Lock where single storage system is involved
  tasks:
    - name: Lock resource groups
      hitachivantara.vspone_block.vsp.hv_resource_group_lock:
        connection_info:
          address: storage1.company.com
          username: "admin"
          password: "secret"
        spec:
          lock_timeout_sec: 300
      register: response

    - name: Debug lock resource group result
      ansible.builtin.debug:
        var: response

    - name: Create ldev
      hitachivantara.vspone_block.vsp.hv_ldevs:
        connection_info:
          address: storage1.company.com
          api_token: lock_token_value
        spec:
          pool_id: 0
          size: 2GB
          name: RD_LOCK_TEST_120424
      register: create_ldev_result

    - name: Debug lock resource group result
      ansible.builtin.debug:
        var: create_ldev_result

    - name: Unlock the Resource Groups that were locked
      hitachivantara.vspone_block.vsp.hv_resource_group_lock:
        connection_info:
          address: storage1.company.com
          api_token: lock_token_value
        state: absent
      register: result

    - name: Debug lock resource group result
      ansible.builtin.debug:
        var: result
"""

RETURN = """
response:
    description: >
        First lock resource groups output, then ldev creation output and finally unlock resource group output.
        Ansible sorts the output, so the outputs were jumbled with three tasks. Ignore the underscores (_) in the beginning of the variables,
        they are added to keep the output in order with the tasks.
        For first task three (___), for the second task two (__), and for the third task one (_) underscores are added in the beginning.
    returned: always
    type: list
    elements: dict
    sample:

        # Result of the first task (lock resource groups)

        ___lock_session_id: 26945
        ___lock_token: "62316257-5362-458a-8a9a-8922beaf7460"
        ___locked_resource_groups:
              -   id: 0
                  name: "meta_resource"
              -   id: 1
                  name: "test-rg-1"
              -   id: 2
                  name: "test-rg-2"
              -   id: 3
                  name: "test-rg-3"

        # Result of the second task (create ldev)

        __canonical_name: "naa.60060e80089c4e0000509c4e00000024"
        __dedup_compression_progress: -1
        __dedup_compression_status: "DISABLED"
        __deduplication_compression_mode: "disabled"
        __emulation_type: "OPEN-V-CVS"
        __hostgroups: []
        __is_alua: false
        __is_command_device: false
        __is_data_reduction_share_enabled: false
        __is_device_group_definition_enabled: false
        __is_encryption_enabled: false
        __is_security_enabled: false
        __is_user_authentication_enabled: false
        __is_write_protected: false
        __is_write_protected_by_key: false
        __iscsi_targets: []
        __ldev_id: 36
        __logical_unit_id_hex_format: "00:00:24"
        __name: "RD_LOCK_TEST_120424"
        __num_of_ports: -1
        __nvm_subsystems: []
        __parity_group_id: ""
        __path_count: -1
        __pool_id: 0
        __provision_type: "CVSHDP"
        __qos_settings: {}
        __resource_group_id: 0
        __snapshots: []
        __status: "NML"
        __storage_serial_number: "40014"
        __tiering_policy: {}
        __total_capacity: "2.00GB"
        __used_capacity: "0.00B"
        __virtual_ldev_id: -1

        # Result of the third task (unlock resource groups)

        _comment: "Resource Groups unlocked successfully."
        _changed: true
        _failed: false
"""
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.vsp_rg_lock_reconciler import (
    VSPResourceGroupLockReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPResourceGroupLockArguments,
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPResourceGroupLockManager:
    def __init__(self):

        self.logger = Log()
        self.argument_spec = VSPResourceGroupLockArguments().rg_lock()

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
            # can be added mandotary , optional mandatory arguments
        )
        try:
            self.parameter_manager = VSPParametersManager(self.module.params)
            self.connection_info = self.parameter_manager.get_connection_info()
            self.storage_serial_number = (
                self.parameter_manager.storage_system_info.serial
            )
            self.spec = self.parameter_manager.get_rg_lock_spec()
            self.state = self.parameter_manager.get_state()
            self.secondary_connection_info = (
                self.parameter_manager.get_secondary_connection_info()
            )
            if self.secondary_connection_info:
                self.spec.secondary_connection_info = self.secondary_connection_info

        except Exception as e:
            self.logger.writeError(f"An error occurred during initialization: {str(e)}")
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of Resource Group Lock operation ===")
        registration_message = validate_ansible_product_registration()

        response = None
        comment = None
        try:
            reconciler = VSPResourceGroupLockReconciler(
                self.connection_info, self.storage_serial_number, self.state
            )
            response = reconciler.reconcile_rg_lock(self.spec)

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of Resource Group Lock operation ===")
            self.module.fail_json(msg=str(e))

        resp = {
            "changed": self.connection_info.changed,
        }
        comment = None
        if self.state == "absent":
            if response is None:
                comment = "Resource Groups unlocked successfully."
            else:
                comment = response
        else:
            if response:
                comment = "Resource Groups locked successfully."
                resp["locked_resource_groups"] = response
        if comment:
            resp["comment"] = comment
        if registration_message:
            resp["user_consent_required"] = registration_message
        self.logger.writeInfo(f"{resp}")
        self.logger.writeInfo("=== End of Resource Group Lock operation ===")
        self.module.exit_json(**resp)


def main(module=None):
    obj_store = VSPResourceGroupLockManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
