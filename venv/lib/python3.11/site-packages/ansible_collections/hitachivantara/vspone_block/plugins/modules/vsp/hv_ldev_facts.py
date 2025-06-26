#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_ldev_facts
short_description: Retrieves information about logical devices (LDEVs) from Hitachi VSP storage systems.
description:
  - This module retrieves information about logical devices (LDEVs) from Hitachi VSP storage systems.
  - It provides details such as LDEV IDs, names, and other relevant information.
  - For examples, go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/ldev_facts.yml)
version_added: '3.0.0'
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
    description: Specification for retrieving LDEV information.
    type: dict
    required: false
    suboptions:
      ldev_id:
        description: ID of the specific LDEV to retrieve information for.
        type: int
        required: false
      start_ldev_id:
        description: Starting LDEV ID for filtering LDEVs.
        type: int
        required: false
      name:
        description: Name of the LDEV.
        type: str
        required: false
      count:
        description: Number of LDEVs to retrieve.
        type: int
        required: false
      end_ldev_id:
        description: Ending LDEV ID for filtering LDEVs.
        type: int
        required: false
      is_detailed:
        description: Flag to retrieve all the additional properties that are not returned with regular LDEV facts output.
        type: bool
        required: false
        default: false
      query:
        description: >
          Getting all the additional properties of the LDEV facts output is time-consuming.
          To optimize the performance, you can specify a list of additional properties to be retrieved.
          This field allows you to specify a list of strings, where each string indicates which additional properties are retrieved.
          If is_detailed is set to true, this field will be ignored and all additional properties will be retrieved.
          The supported additional properties are: "cmd_device_settings", "encryption_settings", "nvm_subsystem_info", "qos_settings", and "snapshots_info".
        type: list
        required: false
        elements: str
"""

EXAMPLES = """
- name: Get all ldevs
  hitachivantara.vspone_block.vsp.hv_ldev_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"

- name: Retrieve information about a specific LDEV
  hitachivantara.vspone_block.vsp.hv_ldev_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"
    spec:
      ldev_id: 123
"""

RETURN = r"""
ansible_facts:
    description: >
        Dictionary containing the discovered properties of the storage volumes.
    returned: always
    type: dict
    contains:
        volumes:
            description: List of storage volumes with their attributes.
            type: list
            elements: dict
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
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler import (
    vsp_volume,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.message.module_msgs import (
    ModuleMessage,
)


class VSPVolumeFactManager:
    def __init__(self):
        self.logger = Log()
        self.argument_spec = VSPVolumeArguments().volume_fact()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
            # can be added mandatory , optional mandatory arguments
        )
        try:
            params_manager = VSPParametersManager(self.module.params)
            self.spec = params_manager.set_volume_fact_spec()
            self.connection_info = params_manager.get_connection_info()
            self.serial = params_manager.get_serial()
        except Exception as e:
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of LDEV Facts ===")
        registration_message = validate_ansible_product_registration()

        volume_data = None

        try:
            volume_data = self.direct_volume_read()
            volume_data_extracted = vsp_volume.VolumeCommonPropertiesExtractor(
                self.serial
            ).extract(volume_data)
        except Exception as e:
            self.logger.writeException(e)
            self.logger.writeInfo("=== End of LDEV Facts ===")
            self.module.fail_json(msg=str(e))

        data = {"volumes": volume_data_extracted}

        if registration_message:
            data["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of LDEV Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)

    def direct_volume_read(self):

        result = vsp_volume.VSPVolumeReconciler(
            self.connection_info,
            self.serial,
        ).get_volumes(self.spec)

        if not result:
            raise ValueError(ModuleMessage.VOLUME_NOT_FOUND.value)
        return result.data_to_list()


def main(module=None):
    obj_store = VSPVolumeFactManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
