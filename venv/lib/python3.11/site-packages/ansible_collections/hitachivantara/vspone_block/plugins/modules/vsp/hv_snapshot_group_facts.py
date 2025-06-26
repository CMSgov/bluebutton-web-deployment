#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_snapshot_group_facts
short_description: Retrieves snapshot information in units of snapshot groups from Hitachi VSP storage systems.
description:
  - This module retrieves information about snapshots in units of snapshot groups from Hitachi VSP storage systems.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/snapshot_group_facts.yml)
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
    description: Specification for the snapshot group facts to be gathered.
    type: dict
    required: false
    suboptions:
      snapshot_group_name:
        description: The name of the snapshot group.
        type: str
        required: true
"""

EXAMPLES = """
- name: Gather snapshot facts with primary volume and mirror unit ID
  hitachivantara.vspone_block.vsp.hv_snapshot_group_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    spec:
      snapshot_group_name: 'NewNameSPG'
"""


RETURN = r"""
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the snapshot groups.
  returned: always
  type: dict
  contains:
    snapshots:
      description: A list of snapshots gathered from the storage system.
      type: list
      elements: dict
      contains:
        snapshot_group_id:
          description: Unique identifier for the snapshot group.
          type: str
          sample: "SampleNameSPG"
        snapshot_group_name:
          description: Name of the snapshot group.
          type: str
          sample: "SampleNameSPG"
        snapshots:
          description: List of snapshots within the group.
          type: list
          elements: dict
          contains:
            storage_serial_number:
              description: Serial number of the storage system.
              type: int
              sample: 810050
            primary_volume_id:
              description: ID of the primary volume.
              type: int
              sample: 1030
            primary_hex_volume_id:
              description: Hexadecimal ID of the primary volume.
              type: str
              sample: "00:04:06"
            secondary_volume_id:
              description: ID of the secondary volume.
              type: int
              sample: 1031
            secondary_hex_volume_id:
              description: Hexadecimal ID of the secondary volume.
              type: str
              sample: "00:04:07"
            svol_access_mode:
              description: Access mode of the secondary volume.
              type: str
              sample: ""
            pool_id:
              description: ID of the pool.
              type: int
              sample: 12
            consistency_group_id:
              description: ID of the consistency group.
              type: int
              sample: -1
            mirror_unit_id:
              description: ID of the mirror unit.
              type: int
              sample: 3
            copy_rate:
              description: Copy rate of the snapshot.
              type: int
              sample: -1
            copy_pace_track_size:
              description: Track size for copy pace.
              type: str
              sample: ""
            status:
              description: Status of the snapshot.
              type: str
              sample: "PAIR"
            type:
              description: Type of the snapshot.
              type: str
              sample: ""
            snapshot_id:
              description: ID of the snapshot.
              type: str
              sample: "1030,3"
            is_consistency_group:
              description: Indicates if it is a consistency group.
              type: bool
              sample: true
            primary_or_secondary:
              description: Indicates if it is a primary or secondary volume.
              type: str
              sample: "P-VOL"
            can_cascade:
              description: Indicates if the snapshot can cascade.
              type: bool
              sample: true
            retention_period:
              description: Retention period for the snapshot.
              type: int
              sample: 60
"""

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPSnapshotArguments,
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.vsp_snapshot_reconciler import (
    VSPHtiSnapshotReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log_decorator import (
    LogDecorator,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


@LogDecorator.debug_methods
class VSPHtiSnapshotGrpFactManager:

    def __init__(self):
        self.logger = Log()
        self.argument_spec = VSPSnapshotArguments().snapshot_grp_fact_args()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:

            self.params_manager = VSPParametersManager(self.module.params)
            self.connection_info = self.params_manager.connection_info
            self.storage_serial_number = None
            self.spec = self.params_manager.snapshot_grp_fact_spec()
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of Snapshot Group Facts ===")
        snapshot_data = None
        registration_message = validate_ansible_product_registration()

        try:
            snapshot_data = VSPHtiSnapshotReconciler(
                self.connection_info, self.storage_serial_number
            ).get_snapshot_facts(self.spec)

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of Snapshot Group Facts ===")
            self.module.fail_json(msg=str(e))
        data = {
            "snapshot_groups": snapshot_data,
        }
        if registration_message:
            data["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of Snapshot Group Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main(module=None):
    """Main function to execute the module."""
    obj_store = VSPHtiSnapshotGrpFactManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
