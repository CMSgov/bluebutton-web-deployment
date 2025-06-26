#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_sds_block_vps
short_description: Manages Hitachi SDS block storage system Virtual Private Storages (VPS) volume ADR setting.
description:
  - This module allows to update Virtual Private Storages volume ADR setting.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/sds_block_direct/update_vps_volume_adr_setting.yml)
version_added: '3.1.0'
author:
  - Hitachi Vantara LTD (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: none
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
  state:
    description: State of the VPS volume ADR setting.
    required: false
    type: str
    choices: ['present', 'absent']
    default: 'present'
  spec:
    description: Specification for VPS information.
    required: true
    type: dict
    suboptions:
      vps_id:
        description: ID of the VPS to retrieve information for.
        type: str
        required: false
      vps_name:
        description: VPS name to retrieve information for.
        type: str
        required: false
      capacity_saving:
        description: Capacity saving for the VPS volumes.
        type: str
        required: false
        choices: ['Disabled', 'Compression']
        default: 'Disabled'
"""

EXAMPLES = """
- name: Update VPS Volume ADR setting by VPS Id
  hitachivantara.vspone_block.sds_block.hv_sds_block_vps:
    connection_info:
      address: sdsb.company.com
      username: "admin"
      password: "password"

    spec:
      vps_id: "464e1fd1-9892-4134-866c-6964ce786676"
      capacity_saving: "Disabled"

- name: Update VPS Volume ADR setting by VPS name
  hitachivantara.vspone_block.sds_block.hv_sds_block_vps:
    connection_info:
      address: sdsb.company.com
      username: "admin"
      password: "password"

    spec:
      vps_name: "VPS_01"
      capacity_saving: "Compression"
"""

RETURN = """
vps:
  description: Attributes of the VPS.
  returned: always
  type: dict
  contains:
    id:
      description: ID of the VPS.
      type: str
      sample: "d2c1fa60-5c41-486a-9551-ec41c74d9f01"
    name:
      description: Name of the VPS.
      type: str
      sample: "VPS_01"
    number_of_hbas_created:
      description: Number of HBAs created.
      type: int
      sample: 0
    number_of_servers_created:
      description: Number of servers created.
      type: int
      sample: 0
    number_of_sessions_created:
      description: Number of sessions created.
      type: int
      sample: 0
    number_of_user_groups_created:
      description: Number of user groups created.
      type: int
      sample: 0
    number_of_users_created:
      description: Number of users created.
      type: int
      sample: 0
    number_of_volume_server_connections_created:
      description: Number of volume server connections created.
      type: int
      sample: 0
    upper_limit_for_number_of_hbas:
      description: Upper limit for the number of HBAs.
      type: int
      sample: 400
    upper_limit_for_number_of_servers:
      description: Upper limit for the number of servers.
      type: int
      sample: 100
    upper_limit_for_number_of_sessions:
      description: Upper limit for the number of sessions.
      type: int
      sample: 436
    upper_limit_for_number_of_user_groups:
      description: Upper limit for the number of user groups.
      type: int
      sample: 256
    upper_limit_for_number_of_users:
      description: Upper limit for the number of users.
      type: int
      sample: 256
    upper_limit_for_number_of_volume_server_connections:
      description: Upper limit for the number of volume server connections.
      type: int
      sample: 100
    volume_settings:
      description: Settings for the volumes.
      type: dict
      contains:
        capacity_of_volumes_created:
          description: Capacity of volumes created.
          type: int
          sample: 0
        capacity_saving_of_volume:
          description: Capacity saving mode of the volume.
          type: str
          sample: "Compression"
        number_of_volumes_created:
          description: Number of volumes created.
          type: int
          sample: 0
        pool_id:
          description: Pool ID associated with the volume.
          type: str
          sample: "f5ef8935-ed38-4894-a90b-f821ab6d3d89"
        qos_param:
          description: Quality of Service parameters for the volume.
          type: dict
          contains:
            upper_alert_allowable_time_of_volume:
              description: Upper alert allowable time of the volume.
              type: int
              sample: -1
            upper_limit_for_iops_of_volume:
              description: Upper limit for IOPS of the volume.
              type: int
              sample: -1
            upper_limit_for_transfer_rate_of_volume:
              description: Upper limit for transfer rate of the volume.
              type: int
              sample: -1
        saving_mode_of_volume:
          description: Saving mode of the volume.
          type: str
          sample: "Inline"
        upper_limit_for_capacity_of_single_volume:
          description: Upper limit for the capacity of a single volume.
          type: int
          sample: -1
        upper_limit_for_capacity_of_volumes:
          description: Upper limit for the capacity of volumes.
          type: int
          sample: 100
        upper_limit_for_number_of_volumes:
          description: Upper limit for the number of volumes.
          type: int
          sample: 50
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.sdsb_vps import (
    SDSBVpsReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.sdsb_utils import (
    SDSBVpsArguments,
    SDSBParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)

logger = Log()


class SDSBVpsManager:
    def __init__(self):

        self.argument_spec = SDSBVpsArguments().vps()
        logger.writeDebug(f"MOD:hv_sds_block_vps:argument_spec= {self.argument_spec}")
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
        )

        parameter_manager = SDSBParametersManager(self.module.params)
        self.state = parameter_manager.get_state()
        self.connection_info = parameter_manager.get_connection_info()
        self.spec = parameter_manager.get_vps_spec()
        logger.writeDebug(f"MOD:hv_sds_block_vsp:spec= {self.spec}")

    def apply(self):

        registration_message = validate_ansible_product_registration()
        logger.writeInfo(f"{self.connection_info.connection_type} connection type")
        try:
            sdsb_reconciler = SDSBVpsReconciler(self.connection_info)
            vps = sdsb_reconciler.reconcile_vps(self.state, self.spec)

            logger.writeDebug(f"MOD:hv_sds_block_vps:vps= {vps}")

        except Exception as e:
            self.module.fail_json(msg=str(e))

        response = {
            "changed": self.connection_info.changed,
            "data": vps,
        }

        if registration_message:
            response["user_consent_required"] = registration_message
        self.module.exit_json(**response)
        # self.module.exit_json(vsp=vps)


def main(module=None):
    obj_store = SDSBVpsManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
