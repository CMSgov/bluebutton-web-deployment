#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_nvm_subsystems_facts
short_description: Retrieves information about NVM subsystems from Hitachi VSP storage systems.
description:
  - This module gathers facts about NVM subsystems from Hitachi VSP storage systems.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/nvm_subsystem_facts.yml)
version_added: '3.1.0'
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
  spec:
    description: Specification for the NVM subsystems facts to be gathered.
    type: dict
    required: false
    suboptions:
      name:
        description: The name of the NVM subsystem to retrieve.
        type: str
        required: false
      id:
        description: The ID of the NVM subsystem to retrieve.
        type: int
        required: false
"""

EXAMPLES = """
- name: Get all NVM subsystems
  hitachivantara.vspone_block.vsp.hv_nvm_subsystems_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"

- name: Get a specific NVM subsystem
  hitachivantara.vspone_block.vsp.hv_nvm_subsystems_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    spec:
      name: "Nvm_subsystem_01"
"""

RETURN = r"""
ansible_facts:
  description: >
    Dictionary containing the discovered properties of the NVM subsystems.
  returned: always
  type: dict
  contains:
    nvm_subsystems:
      description: The NVM subsystem information.
      type: list
      elements: dict
      contains:
        storage_serial_number:
          description: The serial number of the storage system.
          type: str
          sample: "810005"
        host_nqn_info:
          description: List of host NQN information.
          type: list
          elements: dict
          contains:
            host_nqn:
              description: Host NQN.
              type: str
              sample: "nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa40"
            host_nqn_nickname:
              description: Nickname for the host NQN.
              type: str
              sample: "my_host_nqn_40"
        namespace_paths_info:
          description: List of namespace paths information.
          type: list
          elements: dict
          contains:
            host_nqn:
              description: Host NQN.
              type: str
              sample: "nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa40"
            ldev_id:
              description: Logical device ID.
              type: int
              sample: 11101
            ldev_hex_id:
              description: Logical device hex ID.
              type: str
              sample: "00:2b:5c"
            namespace_id:
              description: Namespace ID.
              type: int
              sample: 3
        namespaces_info:
          description: List of namespaces information.
          type: list
          elements: dict
          contains:
            block_capacity:
              description: Block capacity of the namespace.
              type: int
              sample: 23068672
            capacity_in_unit:
              description: Capacity in human-readable unit.
              type: str
              sample: "11.00 G"
            ldev_id:
              description: Logical device ID.
              type: int
              sample: 11101
            ldev_hex_id:
              description: Logical device hex ID.
              type: str
              sample: "00:2b:5c"
            namespace_id:
              description: Namespace ID.
              type: int
              sample: 3
            namespace_nickname:
              description: Nickname for the namespace.
              type: str
              sample: "nickname"
        nvm_subsystem_info:
          description: Information about the NVM subsystem.
          type: dict
          contains:
            host_mode:
              description: Host mode.
              type: str
              sample: "VMWARE_EX"
            namespace_security_setting:
              description: Namespace security setting.
              type: str
              sample: "Enable"
            nvm_subsystem_id:
              description: NVM subsystem ID.
              type: int
              sample: 1000
            nvm_subsystem_name:
              description: NVM subsystem name.
              type: str
              sample: "nvm_tcp_01"
            resource_group_id:
              description: Resource group ID.
              type: int
              sample: 0
            t10pi_mode:
              description: T10PI mode.
              type: str
              sample: "Disable"
        port:
          description: List of port information.
          type: list
          elements: dict
          contains:
            port_id:
              description: Port ID.
              type: str
              sample: "CL1-D"
            port_type:
              description: Port type.
              type: str
              sample: "NVME_TCP"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.vsp_nvme import (
    VSPNvmeReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPNvmeSubsystemArguments,
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPNvmSubsystemFactsManager:
    def __init__(self):

        self.logger = Log()
        self.argument_spec = VSPNvmeSubsystemArguments().nvme_subsystem_facts()

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )

        try:
            self.parameter_manager = VSPParametersManager(self.module.params)
            self.connection_info = self.parameter_manager.get_connection_info()
            self.storage_serial_number = None
            self.spec = self.parameter_manager.get_nvme_subsystem_fact_spec()
            self.state = self.parameter_manager.get_state()
            self.logger.writeDebug(f"MOD:hv_nvm_subsystem_facts:spec= {self.spec}")
        except Exception as e:
            self.logger.writeError(f"An error occurred during initialization: {str(e)}")
            self.module.fail_json(msg=str(e))

    def apply(self):

        self.logger.writeInfo("=== Start of NVM Subsystem Facts ===")
        registration_message = validate_ansible_product_registration()
        try:
            reconciler = VSPNvmeReconciler(
                self.connection_info, self.storage_serial_number, self.state
            )
            nvme_subsystems = reconciler.get_nvme_subsystem_facts(self.spec)

            self.logger.writeDebug(
                f"MOD:hv_nvm_subsystem_facts:nvme_subsystems= {nvme_subsystems}"
            )

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of NVM Subsystem Facts ===")
            self.module.fail_json(msg=str(e))
        data = {
            "nvm_subsystems": nvme_subsystems,
        }
        if registration_message:
            data["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of NVM Subsystem Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main(module=None):
    obj_store = VSPNvmSubsystemFactsManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
