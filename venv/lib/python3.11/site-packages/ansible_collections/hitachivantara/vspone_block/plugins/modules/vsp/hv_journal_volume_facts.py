#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_journal_volume_facts
short_description: Retrieves information about Journal Volumes from Hitachi VSP storage systems.
description:
  - This module retrieves information about Journal Volumes from Hitachi VSP storage systems.
  - It provides details such as journalId, journalStatus, and other relevant information..
  - Forexamples, go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/journal_volume_facts.yml)
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
    description: Specification for retrieving Journal Volume information.
    type: dict
    required: false
    suboptions:
      journal_id:
        description: Journal ID of the Journal Volume.
        type: int
        required: false
      is_free_journal_pool_id:
        description: Whether to get free journal id.
        type: bool
        required: false
        default: false
      free_journal_pool_id_count:
        description: Number of free journal id to get.
        type: int
        required: false
        default: 1
      is_mirror_not_used:
        description: Whether to get mirror not used.
        type: bool
        required: false
        default: false

"""

EXAMPLES = """
- name: Retrieve information about all Journal Volumes
  hitachivantara.vspone_block.vsp.hv_journal_volume_facts:
    storage_system_info:
      serial: "811150"
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"

- name: Retrieve information about a specific Journal Volume
  hitachivantara.vspone_block.vsp.hv_journal_volume_facts:
    storage_system_info:
      serial: "811150"
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "password"
    spec:
      journal_id: 10
"""

RETURN = r"""
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the Journal Volumes.
  returned: always
  type: dict
  contains:
    journal_volumes:
      description: List of Journal Volumes managed by the module.
      returned: success
      type: list
      elements: dict
      contains:
        data_overflow_watch_seconds:
          description: Data overflow watch in seconds.
          type: int
          sample: 60
        first_ldev_id:
          description: First LDEV ID of the Journal Volume.
          type: int
          sample: 1992
        is_cache_mode_enabled:
          description: Indicates if cache mode is enabled.
          type: bool
          sample: true
        is_inflow_control_enabled:
          description: Indicates if inflow control is enabled.
          type: bool
          sample: false
        journal_id:
          description: Journal ID of the Journal Volume.
          type: int
          sample: 37
        journal_status:
          description: Status of the Journal Volume.
          type: str
          sample: "PJNN"
        mirror_unit_ids:
          description: List of mirror unit IDs.
          type: list
          elements: dict
          contains:
            consistency_group_id:
              description: Consistency group ID.
              type: int
              sample: 0
            copy_pace:
              description: Copy pace.
              type: str
              sample: "L"
            copy_speed:
              description: Copy speed.
              type: int
              sample: 256
            is_data_copying:
              description: Indicates if data copying is in progress.
              type: bool
              sample: true
            journal_status:
              description: Status of the journal.
              type: str
              sample: "SMPL"
            mu_number:
              description: Mirror unit number.
              type: int
              sample: 0
            path_blockade_watch_in_minutes:
              description: Path blockade watch in minutes.
              type: int
              sample: 5
        mp_blade_id:
          description: MP Blade ID of the Journal Volume.
          type: int
          sample: 1
        num_of_active_paths:
          description: Number of active paths.
          type: int
          sample: 2
        num_of_ldevs:
          description: Number of LDEVs.
          type: int
          sample: 1
        q_count:
          description: Queue count.
          type: int
          sample: 0
        q_marker:
          description: Queue marker.
          type: str
          sample: "00000002"
        total_capacity_mb:
          description: Total capacity in MB.
          type: int
          sample: 19
        usage_rate:
          description: Usage rate.
          type: int
          sample: 0
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler import (
    vsp_journal_volume,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPParametersManager,
    VSPJournalVolumeArguments,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPJournalVolumeFactManager:
    def __init__(self):
        self.logger = Log()

        self.argument_spec = VSPJournalVolumeArguments().journal_volume_fact()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.params_manager = VSPParametersManager(self.module.params)
            self.spec = self.params_manager.get_journal_volume_fact_spec()
            self.serial = self.params_manager.get_serial()
        except Exception as e:
            self.logger.writeException(e)
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of Journal Volume Facts ===")
        registration_message = validate_ansible_product_registration()
        try:
            result = []
            result = vsp_journal_volume.VSPJournalVolumeReconciler(
                self.params_manager.connection_info, self.serial
            ).journal_volume_facts(self.spec)

        except Exception as ex:

            self.logger.writeException(ex)
            self.logger.writeInfo("=== End of Journal Volume Facts ===")
            self.module.fail_json(msg=str(ex))
        data = {
            "journal_volume": result,
        }
        if registration_message:
            data["user_consent_required"] = registration_message
        self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of Journal Volume Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main(module=None):
    obj_store = VSPJournalVolumeFactManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
