#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_hg
short_description: Manages host group on Hitachi VSP storage system.
description:
  - This module provides the following host group management operations
  - 1. create host group.
  - 2. delete host group.
  - 3. add logical unit to host group.
  - 4. remove logical unit from host group.
  - 5. add host WWN to host group.
  - 6. remove host WWN from host group.
  - 7. set host mode.
  - 8. add host mode option to host group.
  - 9. remove host mode option from host group.
  - For examples, go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/hostgroup.yml)
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
    description:
      - Set state to C(present) for create and update host group
      - Set state to C(absent) for delete host group
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
        description: Password for authentication. This is a required field if api_token is not provided..
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
    description: Specification for hostgroup operation.
    type: dict
    required: false
    suboptions:
      state:
        description: Subtask operation.
        type: str
        required: false
        choices: ['present_ldev', 'unpresent_ldev', 'add_wwn', 'remove_wwn', 'set_host_mode_and_hmo', 'present']
        default: 'present'
      name:
        description: Name of the host group. If not given,
          it will create the name with prefix "smrha-" and add 10 digit random number at the end, for example "smrha-0806262996".
        type: str
        required: false
      port:
        description: FC Port.
        type: str
        required: true
      wwns:
        description: List of host WWN to add or remove.
        type: list
        elements: dict
        suboptions:
          wwn:
            description: WWN of the host.
            type: str
            required: true
          nick_name:
            description: Nickname of the host.
            type: str
            required: false
        required: false
      ldevs:
        description: LDEVs to be mapped/unmapped with the host group. Supported format can be decimal or HEX.
        type: list
        elements: str
        required: false
      host_mode:
        description: Host mode of host group.
        type: str
        required: false
        choices: ['LINUX', 'VMWARE', 'HP', 'OPEN_VMS', 'TRU64', 'SOLARIS',
          'NETWARE', 'WINDOWS', 'HI_UX', 'AIX', 'VMWARE_EXTENSION',
          'WINDOWS_EXTENSION', 'UVM', 'HP_XP', 'DYNIX']
      host_mode_options:
        description:
          - List of host group host mode option numbers.
          - '0 # RESERVED'
          - '2 # VERITAS_DB_EDITION_ADV_CLUSTER'
          - '6 # TPRLO'
          - '7 # AUTO_LUN_RECOGNITION'
          - '12 # NO_DISPLAY_FOR_GHOST_LUN'
          - '13 # SIM_REPORT_AT_LINK_FAILURE'
          - '14 # HP_TRUECLUSTER_WITH_TRUECOPY'
          - '15 # RAID_HACMP'
          - '22 # VERITAS_CLUSTER_SERVER'
          - '23 # REC_COMMAND_SUPPORT'
          - '25 # SUPPORT_SPC_3_PERSISTENT_RESERVATION'
          - '33 # SET_REPORT_DEVICE_ID_ENABLE'
          - '39 # CHANGE_NEXUS_SPECIFIED_IN_SCSI_TARGET_RESET'
          - '40 # VVOL_EXPANSION'
          - '41 # PRIORITIZED_DEVICE_RECOGNITION'
          - '42 # PREVENT_OHUB_PCI_RETRY'
          - '43 # QUEUE_FULL_RESPONSE'
          - '48 # HAM_SVOL_READ'
          - '49 # BB_CREDIT_SETUP_1'
          - '50 # BB_CREDIT_SETUP_2'
          - '51 # ROUND_TRIP_SETUP'
          - '52 # HAM_AND_CLUSTER_SW_FOR_SCSI_2'
          - '54 # EXTENDED_COPY'
          - '57 # HAM_RESPONSE_CHANGE'
          - '60 # LUN0_CHANGE_GUARD'
          - '61 # EXPANDED_PERSISTENT_RESERVE_KEY'
          - '63 # VSTORAGE_APIS_ON_T10_STANDARDS'
          - '65 # ROUND_TRIP_EXTENDED_SETUP'
          - '67 # CHANGE_OF_ED_TOV_VALUE'
          - '68 # PAGE_RECLAMATION_LINUX'
          - '69 # ONLINE_LUSE_EXPANSION'
          - '71 # CHANGE_UNIT_ATTENTION_FOR_BLOCKED_POOL_VOLS'
          - '72 # AIX_GPFS'
          - '73 # WS2012'
          - '78 # NON_PREFERRED_PATH'
          - '91 # DISABLE_IO_WAIT_FOR_OPEN_STACK'
          - '95 # CHANGE_SCSI_LU_RESET_NEXUS_VSP_HUS_VM'
          - '96 # CHANGE_SCSI_LU_RESET_NEXUS'
          - '97 # PROPRIETARY_ANCHOR_COMMAND_SUPPORT'
          - '100 # HITACHI_HBA_EMULATION_CONNECTION_OPTION'
          - '102 # GAD_STANDARD_INQURY_EXPANSION_HCS'
          - '105 # TASK_SET_FULL_RESPONSE_FOR_IO_OVERLOAD'
          - '110 # ODX Support for WS2012'
          - '113 # iSCSI CHAP Authentication Log'
          - '114 # Auto Asynchronous Reclamation on ESXi 6.5+ '
          - '122 # TASK_SET_FULL_RESPONSE_AFTER_QOS_UPPER_LIMIT'
          - '124 # GUARANTEED_RESPONSE_DURING_CONTROLLER_FAILURE'
          - '131 # WCE_BIT_OFF_MODE'
        type: list
        elements: int
        required: false
      should_delete_all_ldevs:
        description: If the value is true, destroy the logical devices that are no longer attached to any host group or iSCSI target.
        required: false
        type: bool
      host_group_number:
        description: The host group number.
        type: int
        required: false
      should_release_host_reserve:
        description: If the value is true, release the host reserve.
        type: bool
        required: false
      lun:
        description: LUN ID to be releases the host reservation status of the LU mapped to a specified LU path.
        type: int
        required: false
      asymmetric_access_priority:
        description: Asymmetric access priority level for ALUA host group.
        type: str
        required: false
        choices: ['low', 'high']
"""

EXAMPLES = """
- name: Create host group with LUN in decimal
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      name: 'testhg26dec'
      port: 'CL1-A'
      host_mode: 'VMWARE_EXTENSION'
      host_mode_options: [40]
      wwns:
        - wwn: '100000109B583B2D'
          nick_name: 'test1'
        - wwn: '100000109B583B2C'
          nick_name: 'test2'
      ldevs: [393, 851]

- name: Create host group with LUN in HEX
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    host_group_info:
      name: 'testhg26dec'
      port: 'CL1-A'
      host_mode: 'VMWARE_EXTENSION'
      host_mode_options: [54, 63]
      wwns:
        - wwn: '200000109B3C0FD3'
          nick_name: 'test1'
        - wwn: '200000109B3C0FD4'
          nick_name: 'test2'
      ldevs: ['00:23:A4']

- name: Delete host group
  hitachivantara.vspone_block.vsp.hv_hg:
    state: absent
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      name: 'testhg26dec'
      port: 'CL1-A'

- name: Present LUN
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      state: present_ldev
      name: 'testhg26dec'
      port: 'CL1-A'
      ldevs: ['00:05:77', '00:05:7D']

- name: Unpresent LUN
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      state: unpresent_ldev
      name: 'testhg26dec'
      port: 'CL1-A'
      ldevs: [800, 801]

- name: Add WWN
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      state: add_wwn
      name: 'testhg26dec'
      port: 'CL1-A'
      wwns:
        - wwn: '200000109B3C0FD3'
          nick_name: 'test1'
        - wwn: '200000109B3C0FD4'
        - wwn: '200000109B3C0FD5'

- name: Remove WWN
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      state: remove_wwn
      name: 'testhg26dec'
      port: 'CL1-A'
      wwns:
        - wwn: '200000109B3C0FD3'

- name: Update host group
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      state: set_host_mode_and_hmo
      name: 'testhg26dec'
      port: 'CL1-A'
      host_mode: 'VMWARE_EXTENSION'
      host_mode_options: [54, 63]

- name: Asymmetric access priority level for ALUA host group.
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      host_group_number: 208
      port: 'CL1-A'
      asymmetric_access_priority: 'high'

- name: Release host reserve status of the LU mapped to a specified LU path.
  hitachivantara.vspone_block.vsp.hv_hg:
    state: present
    connection_info:
      address: storage1.company.com
      username: "dummy_user"
      password: "dummy_password"
    spec:
      host_group_number: 150
      port: 'CL1-A'
      should_release_host_reserve: true
      lun: 0
"""

RETURN = """
hostGroups:
  description: Information of host group.
  returned: always
  type: dict
  contains:
    host_group_id:
      description: ID of the host group.
      type: int
      sample: 93
    host_group_name:
      description: Name of the host group.
      type: str
      sample: "ansible-test-hg"
    host_mode:
      description: Host mode of the host group.
      type: str
      sample: "STANDARD"
    host_mode_options:
      description: List of host mode options for the host group.
      type: list
      elements: dict
      contains:
        host_mode_option:
          description: Name of the host mode option.
          type: str
          sample: "EXTENDED_COPY"
        host_mode_option_number:
          description: Number of the host mode option.
          type: int
          sample: 54
    lun_paths:
      description: List of LUN paths for the host group.
      type: list
      elements: dict
      contains:
        ldevId:
          description: ID of the logical device.
          type: int
          sample: 166
        lunId:
          description: ID of the LUN.
          type: int
          sample: 0
    port:
      description: Port associated with the host group.
      type: str
      sample: "CL1-A"
    resource_group_id:
      description: Resource group ID associated with the host group.
      type: int
      sample: 0
    storage_id:
      description: Storage ID associated with the host group.
      type: str
      sample: "storage-39f4eef0175c754bb90417358b0133c3"
    wwns:
      description: List of WWNs associated with the host group.
      type: list
      elements: dict
      contains:
        id:
          description: ID of the WWN.
          type: str
          sample: "1212121212121212"
        name:
          description: Name of the WWN.
          type: str
          sample: ""
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPHostGroupArguments,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler import (
    vsp_host_group,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.message.module_msgs import (
    ModuleMessage,
)


class VSPHostGroupManager:
    def __init__(self):
        self.logger = Log()
        self.argument_spec = VSPHostGroupArguments().host_group()
        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
        )

        try:
            params_manager = VSPParametersManager(self.module.params)
            self.connection_info = params_manager.get_connection_info()
            self.serial_number = params_manager.get_serial()
            self.state = params_manager.get_state()
            self.spec = params_manager.host_group_spec()
        except Exception as e:
            self.logger.writeError(str(e))
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of Host Group operation ===")
        registration_message = validate_ansible_product_registration()
        host_group_data = None
        host_group_data_extracted = None
        try:
            host_group_data = self.direct_host_group_modification()
            self.logger.writeInfo("host_group_data {}", host_group_data)
            host_group_data_extracted = host_group_data

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of Host Group operation ===")
            self.module.fail_json(msg=str(e))
        if registration_message:
            host_group_data_extracted["user_consent_required"] = registration_message
        self.logger.writeInfo(f"{host_group_data_extracted}")
        self.logger.writeInfo("=== End of Host Group operation ===")
        self.module.exit_json(**host_group_data_extracted)

    def direct_host_group_modification(self):
        result = vsp_host_group.VSPHostGroupReconciler(
            self.connection_info, self.serial_number
        ).host_group_reconcile(self.state, self.spec)
        if result is None:
            raise ValueError(ModuleMessage.HOST_GROUP_NOT_FOUND.value)
        return result


def main(module=None):
    obj_store = VSPHostGroupManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
