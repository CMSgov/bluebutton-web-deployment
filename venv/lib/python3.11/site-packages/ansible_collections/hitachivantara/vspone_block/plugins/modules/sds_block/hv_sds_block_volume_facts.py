#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_sds_block_volume_facts
short_description: Retrieves information about Hitachi SDS block storage system volumes.
description:
  - This module retrieves information about storage volumes.
  - It provides details about a storage volume such as name, type and other details.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/sds_block_direct/volume_facts.yml)
version_added: '3.0.0'
author:
  - Hitachi Vantara LTD (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: full
options:
  connection_info:
    description: Information required to establish a connection to the storage system.
    required: true
    type: dict
    suboptions:
      address:
        description: IP address or hostname of the storage system.
        type: str
        required: true
      username:
        description: Username for authentication.
        type: str
        required: true
      password:
        description: Password for authentication.
        type: str
        required: true
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: false
        choices: ['direct']
        default: 'direct'
  spec:
    description: Specification for retrieving volume information.
    type: dict
    required: false
    suboptions:
      count:
        type: int
        description: The maximum number of obtained volume information items. Default is 500.
        required: false
        default: 500
      names:
        type: list
        description: The names of the volumes.
        required: false
        elements: str
      nicknames:
        type: list
        description: The nickname of the volume.
        required: false
        elements: str
      capacity_saving:
        type: str
        description: Settings of the data reduction function for volumes.
        required: false
        choices: ['Disabled', 'Compression']
"""

EXAMPLES = """
- name: Get volumes by default count
  hitachivantara.vspone_block.sds_block.hv_sds_block_volume_facts:
    connection_info:
      address: sdsb.company.com
      username: "admin"
      password: "password"

- name: Get volumes by count
  hitachivantara.vspone_block.sds_block.hv_sds_block_volume_facts:
    connection_info:
      address: sdsb.company.com
      username: "admin"
      password: "password"

    spec:
      count: 200

- name: Get volumes by names
  hitachivantara.vspone_block.sds_block.hv_sds_block_volume_facts:
    connection_info:
      address: sdsb.company.com
      username: "admin"
      password: "password"

    spec:
      names: ['test-volume1', 'test-volume2']

- name: Get volumes by other filters
  hitachivantara.vspone_block.sds_block.hv_sds_block_volume_facts:
    connection_info:
      address: sdsb.company.com
      username: "admin"
      password: "password"

    spec:
      count: 200
      capacity_saving: 'Disabled'
"""

RETURN = """
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
        compute_node_info:
          description: Information about the compute nodes connected to the volume.
          type: list
          elements: dict
          contains:
            id:
              description: Unique identifier for the compute node.
              type: str
              sample: "4f9041aa-ab2f-4789-af2e-df4a0178a4d3"
            name:
              description: Name of the compute node.
              type: str
              sample: "hitachitest"
        volume_info:
          description: Detailed information about the volume.
          type: dict
          contains:
            data_reduction_effects:
              description: Effects of data reduction on the volume.
              type: dict
              contains:
                post_capacity_data_reduction:
                  description: Capacity after data reduction.
                  type: int
                  sample: 0
                pre_capacity_data_reduction_without_system_data:
                  description: Capacity before data reduction without system data.
                  type: int
                  sample: 0
                system_data_capacity:
                  description: Capacity of system data.
                  type: int
                  sample: 0
            data_reduction_progress_rate:
              description: Progress rate of data reduction.
              type: bool
              sample: false
            data_reduction_status:
              description: Status of data reduction.
              type: str
              sample: "Disabled"
            full_allocated:
              description: Whether the volume is fully allocated.
              type: bool
              sample: false
            id:
              description: Unique identifier for the volume.
              type: str
              sample: "ef69d5c6-ed7c-4302-959f-b8b8a7382f3b"
            naa_id:
              description: NAA identifier for the volume.
              type: str
              sample: "60060e810a85a000600a85a000000017"
            name:
              description: Name of the volume.
              type: str
              sample: "vol010"
            nickname:
              description: Nickname of the volume.
              type: str
              sample: "vol010"
            number_of_connecting_servers:
              description: Number of servers connected to the volume.
              type: int
              sample: 1
            number_of_snapshots:
              description: Number of snapshots of the volume.
              type: int
              sample: 0
            pool_id:
              description: Identifier of the pool to which the volume belongs.
              type: str
              sample: "cb9f7ecf-ceba-4d8e-808b-9c7bc3e59c03"
            pool_name:
              description: Name of the pool to which the volume belongs.
              type: str
              sample: "SP01"
            protection_domain_id:
              description: Identifier of the protection domain.
              type: str
              sample: "645c36b6-da9e-44bb-b711-430e06c7ad2b"
            qos_param:
              description: Quality of Service parameters for the volume.
              type: dict
              contains:
                upper_alert_allowable_time:
                  description: Upper alert allowable time.
                  type: int
                  sample: -1
                upper_alert_time:
                  description: Upper alert time.
                  type: bool
                  sample: false
                upper_limit_for_iops:
                  description: Upper limit for IOPS.
                  type: int
                  sample: -1
                upper_limit_for_transfer_rate:
                  description: Upper limit for transfer rate.
                  type: int
                  sample: -1
            saving_mode:
              description: Whether saving mode is enabled.
              type: bool
              sample: false
            capacity_saving:
              description: Capacity saving status.
              type: str
              sample: "Disabled"
            snapshot_attribute:
              description: Snapshot attribute.
              type: str
              sample: "-"
            snapshot_status:
              description: Snapshot status.
              type: bool
              sample: false
            status:
              description: Status of the volume.
              type: str
              sample: "Normal"
            status_summary:
              description: Summary of the volume status.
              type: str
              sample: "Normal"
            storage_controller_id:
              description: Identifier of the storage controller.
              type: str
              sample: "fc22f6d3-2bd3-4df5-b5db-8a728e301af9"
            total_capacity_mb:
              description: Total capacity of the volume in MB.
              type: int
              sample: 120
            used_capacity_mb:
              description: Used capacity of the volume in MB.
              type: int
              sample: 0
            volume_number:
              description: Volume number.
              type: int
              sample: 23
            volume_type:
              description: Type of the volume.
              type: str
              sample: "Normal"
            vps_id:
              description: Identifier of the VPS.
              type: str
              sample: "(system)"
            vps_name:
              description: Name of the VPS.
              type: str
              sample: "(system)"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.sdsb_volume import (
    SDSBVolumeReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.sdsb_properties_extractor import (
    VolumePropertiesExtractor,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.sdsb_utils import (
    SDSBVolumeArguments,
    SDSBParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)

logger = Log()


class SDSBVolumeFactsManager:
    def __init__(self):

        self.argument_spec = SDSBVolumeArguments().volume_facts()
        logger.writeDebug(
            f"MOD:hv_sds_volume_facts:argument_spec= {self.argument_spec}"
        )
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )

        parameter_manager = SDSBParametersManager(self.module.params)
        self.connection_info = parameter_manager.get_connection_info()
        # logger.writeDebug(f"MOD:hv_sds_block_compute_node_facts:argument_spec= {self.connection_info}")
        self.spec = parameter_manager.get_volume_fact_spec()
        logger.writeDebug(f"MOD:hv_sds_volume_facts:spec= {self.spec}")

    def apply(self):
        volumes = None
        volumes_data_extracted = None
        registration_message = validate_ansible_product_registration()

        logger.writeInfo(f"{self.connection_info.connection_type} connection type")
        try:
            sdsb_reconciler = SDSBVolumeReconciler(self.connection_info)
            volumes = sdsb_reconciler.get_volumes(self.spec)

            logger.writeDebug(f"MOD:hv_sds_volume_facts:volumes= {volumes}")
            output_dict = volumes.data_to_list()
            volumes_data_extracted = VolumePropertiesExtractor().extract(output_dict)
            # volumes_data_extracted = VolumePropertiesExtractor().extract(output_dict)

        except Exception as e:
            self.module.fail_json(msg=str(e))

        data = {"volumes": volumes_data_extracted}
        if registration_message:
            data["user_consent_required"] = registration_message
        self.module.exit_json(changed=False, ansible_facts=data)


def main():
    obj_store = SDSBVolumeFactsManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
