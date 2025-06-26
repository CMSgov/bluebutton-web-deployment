#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_ldev
short_description: Manages logical devices (LDEVs) on Hitachi VSP storage systems.
description:
  - This module allows for the creation, modification, or deletion of logical devices (LDEVs) on Hitachi VSP storage systems.
  - It supports operations such as creating a new LDEV, updating an existing LDEV, or deleting a LDEV.
  - For examples, go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/ldev.yml)
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
    description: The desired state of the LDEV.
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
    description: Specification for the LDEV.
    type: dict
    required: true
    suboptions:
      pool_id:
        description: ID of the pool where the LDEV will be created. Options pool_id and parity_group_id are mutually exclusive.
        type: int
        required: false
      parity_group:
        description: ID of the parity_group where the LDEV will be created. Options pool_id and parity_group_id are mutually exclusive.
        type: str
        required: false
      size:
        description: Size of the LDEV. Can be specified in units such as GB, TB, or MB (e.g., '10GB', '5TB', '100MB', 200).
        type: str
        required: false
      ldev_id:
        description: ID of the LDEV (required for delete and update operations), for new it will assigned to this ldev if it's free.
        type: int
        required: false
      name:
        description: Name of the LDEV (optional). If not given, it assigns the name of the LDEV to "smrha-<ldev_id>".
        type: str
        required: false
      capacity_saving:
        description: >
          Whether to enable the capacity saving functions. Valid value is one of the following three options:
          - 1. compression -  Enable the capacity saving function (compression).
          - 2. compression_deduplication - Enable the capacity saving function (compression and deduplication).
          - 3 disabled - Disable the capacity saving function (compression and deduplication)
          Default value is disabled.
        type: str
        required: false
      data_reduction_share:
        description: Specify whether to create a data reduction shared volume.
          This value is set to true for Thin Image Advance.
        type: bool
        required: false
      nvm_subsystem_name:
        description: Specify whether the LDEV created will be part of an NVM subsystem.
        type: str
        required: false
      state:
        description:
          - State of the NVM subsystems task. This is valid only when nvm_subsystem_name is specified.
          - C(add_host_nqn) - Add the host NQNs to the LDEV.
          - C(remove_host_nqn) - Remove the host NQNs from the LDEV.
        type: str
        required: false
        choices: ['add_host_nqn', 'remove_host_nqn']
        default: 'add_host_nqn'
      host_nqns:
        description: List of host nqns to add to or remove from the LDEV depending on the state value.
        type: list
        required: false
        elements: str
      is_relocation_enabled:
        description: Specify whether to enable the tier relocation setting for the HDT volume.
        type: bool
        required: false
      tier_level_for_new_page_allocation:
        description: Specify which tier of the HDT pool will be prioritized when a new page is allocated.
        type: str
        required: false
      tiering_policy:
        description: Tiering policy for the LDEV.
        type: dict
        required: false
        suboptions:
          tier_level:
            description: Tier level, a value from 0 to 31.
            type: int
            required: false
          tier1_allocation_rate_min:
            description: Tier1 min, a value from 1 to 100.
            type: int
            required: false
          tier1_allocation_rate_max:
            description: Tier1 max, a value from 1 to 100.
            type: int
            required: false
          tier3_allocation_rate_min:
            description: Tier3 min, a value from 1 to 100.
            type: int
            required: false
          tier3_allocation_rate_max:
            description: Tier3 max, a value from 1 to 100.
            type: int
            required: false
      vldev_id:
        description: Specify the virtual LDEV id.
        type: int
        required: false
      force:
        description: Force delete. Delete the LDEV and removes the LDEV from hostgroups, iscsi targets or NVM subsystem namespace.
        type: bool
        required: false
      should_shred_volume_enable:
        description: It shreds an LDEV (basic volume) or DP volume. Overwrites the volume three times with dummy data.
        type: bool
        required: false
      qos_settings:
        description: QoS settings for the LDEV.
        type: dict
        required: false
        suboptions:
          upper_iops:
            description: Upper IOPS limit.
            type: int
            required: false
          lower_iops:
            description: Lower IOPS limit.
            type: int
            required: false
          upper_transfer_rate:
            description: Upper transfer rate limit.
            type: int
            required: false
          lower_transfer_rate:
            description: Lower transfer rate limit.
            type: int
            required: false
          upper_alert_allowable_time:
            description: Upper alert allowable time.
            type: int
            required: false
          lower_alert_allowable_time:
            description: Lower alert allowable time.
            type: int
            required: false
          response_priority:
            description: Response priority.
            type: int
            required: false
          response_alert_allowable_time:
            description: Response alert allowable time.
            type: int
            required: false
      is_compression_acceleration_enabled:
        description: Whether the compression accelerator of the capacity saving function is enabled.
        type: bool
        required: false
      data_reduction_process_mode:
        description: >
          The data reduction process mode of the capacity saving function.
          Valid values are:
          - "post_process" -  Post-process mode.
          - "inline" - Inline mode.
        choices: ["post_process", "inline"]
        type: str
      is_alua_enabled:
        description: Whether the ALUA (Asymmetric Logical Unit Access) is enabled for the LDEV.
        type: bool
        required: false
      is_full_allocation_enabled:
        description: Whether the LDEV is a full allocation volume.
        type: bool
        required: false
      should_format_volume:
        description: Whether to format the volume after creation or existing volume.
        type: bool
        required: false
      format_type:
        description: >
          The format type of the volume. Valid values are:
          - "quick" - Quick formatting.
          - "normal" - Normal formatting, It may take time to finish the formatting process.
        type: str
        required: false
        choices: ["quick", "normal"]
        default: "quick"
      start_ldev_id:
        description: >
          The starting LDEV ID for the range of LDEVs to be created. This is used when creating multiple LDEVs.
          If not specified, a free LDEV ID will be assigned.
        type: int
        required: false
      end_ldev_id:
        description: >
          The ending LDEV ID for the range of LDEVs to be created. This is used when creating multiple LDEVs.
          If not specified, only one LDEV will be created.
        type: int
        required: false
      mp_blade_id:
        description: >
          The MP blade ID to which the LDEV will be assigned. This is used for specifying the MP blade for the LDEV.
          If not specified, the LDEV will be assigned to the default MP blade.
        type: int
        required: false
      should_reclaim_zero_pages:
        description: >
          Whether to reclaim zero pages of a DP volume. This is used to reclaim space in a DP volume.
          If set to true, it will reclaim the zero pages of the DP volume.
        type: bool
        required: false
      external_parity_group:
        description: >
          The external parity group ID to which the LDEV will be assigned. This is used for specifying the external parity group for the LDEV.
          If not specified, the LDEV will be assigned to the default parity group.
        type: str
        required: false
      is_parallel_execution_enabled:
        description: >
          Whether to enable parallel execution for the LDEV operations. This is used to speed up the LDEV operations.
          If set to true, it will enable parallel execution for the LDEV operations.
        type: bool
"""

EXAMPLES = """
- name: Create ldev with free id and present to NVM System
  hitachivantara.vspone_block.vsp.hv_ldev:
    state: present
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    spec:
      pool_id: 1
      size: "10GB"
      name: "New_LDEV"
      capacity_saving: "compression_deduplication"
      data_reduction_share: true
      state: "add_host_nqn"
      nvm_subsystem_name: "nvm_subsystem_01"
      host_nqns: ["nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa39"]

- name: Present existing volume to NVM System
  hitachivantara.vspone_block.vsp.hv_ldev:
    state: present
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    spec:
      ldev_id: 1
      state: "add_host_nqn"
      nvm_subsystem_name: "nvm_subsystem_01"
      host_nqns: ["nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa39"]

- name: Force delete ldev removes the ldev from hostgroups, iscsi targets or NVMe subsystem namespace
  hitachivantara.vspone_block.vsp.hv_ldev:
    state: absent
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    spec:
      ldev_id: 123
      force: true

- name: Update the qos settings for an existing LDEV
  hitachivantara.vspone_block.vsp.hv_ldev:
    state: absent
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    spec:
      ldev_id: 123
      qos_settings:
        upper_iops: 1000
        lower_iops: 500
        upper_transfer_rate: 1000
        lower_transfer_rate: 500
        upper_alert_allowable_time: 1000
        lower_alert_allowable_time: 500
        response_priority: 1000
        response_alert_allowable_time: 1000

- name: Set MP blade id of a volume.
  hitachivantara.vspone_block.vsp.hv_ldev:
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    state: "present"
    spec:
      ldev_id: 11
      mp_blade_id: 1

- name: Reclaiming zero pages of a DP volume.
  hitachivantara.vspone_block.vsp.hv_ldev:
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    state: "present"
    spec:
      ldev_id: 12
      should_reclaim_zero_pages: true

- name: Format a volume.
  hitachivantara.vspone_block.vsp.hv_ldev:
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    state: "present"
    spec:
      ldev_id: 12
      should_format_volume: true

- name: Change volume settings.
  hitachivantara.vspone_block.vsp.hv_ldev:
    connection_info:
      address: storage.company.com
      username: "admin"
      password: "passw0rd"
    state: "present"
    spec:
      ldev_id: 12
      is_alua_enabled: true
      is_full_allocation_enabled: true
      is_compression_acceleration_enabled: true
      is_relocation_enabled: true
      data_reduction_process_mode: "inline"
"""

RETURN = r"""
volume:
  description: Storage volumes with their attributes.
  returned: success
  type: dict
  contains:
    canonical_name:
      description: Unique identifier for the volume.
      type: str
      sample: "naa.60060e8028274200508027420000000a"
    dedup_compression_progress:
      description: Progress percentage of deduplication and compression.
      type: int
      sample: -1
    dedup_compression_status:
      description: Status of deduplication and compression.
      type: str
      sample: "DISABLED"
    deduplication_compression_mode:
      description: Mode of deduplication and compression.
      type: str
      sample: "disabled"
    emulation_type:
      description: Emulation type of the volume.
      type: str
      sample: "OPEN-V-CVS-CM"
    hostgroups:
      description: List of host groups associated with the volume.
      type: list
      elements: str
      sample: []
    is_alua:
      description: Indicates if ALUA is enabled.
      type: bool
      sample: false
    is_command_device:
      description: Indicates if the volume is a command device.
      type: bool
      sample: false
    is_data_reduction_share_enabled:
      description: Indicates if data reduction share is enabled.
      type: bool
      sample: false
    is_device_group_definition_enabled:
      description: Indicates if device group definition is enabled.
      type: bool
      sample: false
    is_encryption_enabled:
      description: Indicates if encryption is enabled.
      type: bool
      sample: false
    is_security_enabled:
      description: Indicates if security is enabled.
      type: bool
      sample: false
    is_user_authentication_enabled:
      description: Indicates if user authentication is enabled.
      type: bool
      sample: false
    is_write_protected:
      description: Indicates if the volume is write-protected.
      type: bool
      sample: false
    is_write_protected_by_key:
      description: Indicates if the volume is write-protected by key.
      type: bool
      sample: false
    iscsi_targets:
      description: List of associated iSCSI targets.
      type: list
      elements: str
      sample: []
    ldev_id:
      description: Logical Device ID.
      type: int
      sample: 10
    logical_unit_id_hex_format:
      description: Logical Unit ID in hexadecimal format.
      type: str
      sample: "00:00:0A"
    name:
      description: Name of the volume.
      type: str
      sample: "snewar-cmd"
    num_of_ports:
      description: Number of ports associated with the volume.
      type: int
      sample: 1
    nvm_subsystems:
      description: List of associated NVM subsystems.
      type: list
      elements: str
      sample: []
    parity_group_id:
      description: Parity group ID of the volume.
      type: str
      sample: ""
    path_count:
      description: Number of paths to the volume.
      type: int
      sample: 1
    pool_id:
      description: Pool ID where the volume resides.
      type: int
      sample: 0
    provision_type:
      description: Provisioning type of the volume.
      type: str
      sample: "CMD,CVS,HDP"
    qos_settings:
      description: Quality of Service settings for the volume.
      type: dict
      sample: {}
    resource_group_id:
      description: Resource group ID of the volume.
      type: int
      sample: 0
    snapshots:
      description: List of snapshots associated with the volume.
      type: list
      elements: str
      sample: []
    status:
      description: Current status of the volume.
      type: str
      sample: "NML"
    storage_serial_number:
      description: Serial number of the storage system.
      type: str
      sample: "810050"
    tiering_policy:
      description: Tiering policy applied to the volume.
      type: dict
      sample: {}
    total_capacity:
      description: Total capacity of the volume.
      type: str
      sample: "50.00MB"
    total_capacity_in_mb:
      description: Total capacity of the volume in megabytes.
      type: str
      sample: "50.0 MB"
    used_capacity:
      description: Used capacity of the volume.
      type: str
      sample: "0.00B"
    used_capacity_in_mb:
      description: Used capacity of the volume in megabytes.
      type: str
      sample: "0.0 MB"
    virtual_ldev_id:
      description: Virtual Logical Device ID.
      type: int
      sample: -1
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPVolumeArguments,
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_constants import (
    StateValue,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler import (
    vsp_volume,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPVolume:
    def __init__(self):

        self.logger = Log()
        self.argument_spec = VSPVolumeArguments().volume()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
        )

        try:
            params_manager = VSPParametersManager(self.module.params)
            self.spec = params_manager.set_volume_spec()
            self.connection_info = params_manager.get_connection_info()
            self.serial = params_manager.get_serial()
            self.state = params_manager.get_state()
        except Exception as e:
            self.logger.writeError(f"An error occurred during initialization: {str(e)}")
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of LDEV operation ===")
        registration_message = validate_ansible_product_registration()

        try:
            comment = ""

            volume_data = self.direct_volume()

            if self.state == StateValue.ABSENT and not volume_data:
                volume_response = "Volume deleted"
            else:
                if isinstance(volume_data, str):
                    volume_response = volume_data
                else:
                    if isinstance(volume_data, dict):
                        comment = volume_data.get("comment", None)
                    volume_response = self.extract_volume_properties(volume_data)
                if self.spec.should_shred_volume_enable:
                    comment = "Volume shredded successfully," + comment
                if self.spec.should_format_volume:
                    if self.spec.is_task_timeout:
                        comment = (
                            "Volume format task is still in progress. It will finish after sometime "
                            + comment
                        )
                    else:
                        comment = "Volume formatted successfully," + comment
                if self.spec.should_reclaim_zero_pages:
                    comment = "Volume reclaimed to zero pages successfully," + comment

                if self.spec.vldev_id:
                    vldev_id = self.spec.vldev_id
                    if comment is None:
                        comment = ""
                    else:
                        comment = comment + " "
                    if vldev_id == -1:
                        comment = "Unassigned vldev_id successfully." + comment
                    else:
                        comment = (
                            "Assigned vldev_id "
                            + str(self.spec.vldev_id)
                            + " successfully."
                            + comment
                        )
                if self.spec.comment:
                    comment = f"{self.spec.comment} " + comment

        except Exception as e:
            self.logger.writeError(f"An error occurred: {str(e)}")
            self.logger.writeInfo("=== End of LDEV operation ===")
            self.module.fail_json(msg=str(e))

        response = {"changed": self.connection_info.changed, "volume": volume_response}
        if comment:
            response["comment"] = comment

        if registration_message:
            response["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{response}")
        self.logger.writeInfo("=== End of LDEV operation ===")
        self.module.exit_json(**response)

    def direct_volume(self):

        result = vsp_volume.VSPVolumeReconciler(
            self.connection_info,
            self.serial,
        ).volume_reconcile(self.state, self.spec)
        return result

    def extract_volume_properties(self, volume_data):
        if not volume_data:
            return None

        # self.logger.writeDebug('20240726 volume_data={}',volume_data)
        self.logger.writeDebug("115 type={}", type(volume_data))
        if isinstance(volume_data, dict):
            volume_dict = volume_data.get("lun")
        else:
            volume_dict = volume_data.to_dict() if volume_data else {}
        return vsp_volume.VolumeCommonPropertiesExtractor(self.serial).extract(
            [volume_dict]
        )[0]


def main(module=None):
    """
    :return: None
    """
    obj_store = VSPVolume()
    obj_store.apply()


if __name__ == "__main__":
    main()
