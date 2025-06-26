#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: hv_nvm_subsystems
short_description: Manages NVM subsystems on Hitachi VSP storage systems.
description:
  - This module allows creation, deletion, and other operations on NVM subsystems on Hitachi VSP storage systems.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/nvm_subsystems.yml)
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
  state:
    description: The desired state of the NVM subsystem.
    type: str
    required: false
    choices: ['present', 'absent']
    default: 'present'
  spec:
    description: Specification for the NVM subsystems to be used.
    type: dict
    required: true
    suboptions:
      name:
        description: The name of the NVM subsystem.If not given, it assigns the name of the NVM subsystem to "smrha-<10 digit random number>".
        type: str
        required: false
      id:
        description: The ID of the NVM subsystem.
        type: int
        required: false
      host_mode:
        description: The host mode of the NVM subsystem.
        type: str
        required: false
      enable_namespace_security:
        description: Namespace security settings.
        type: bool
        required: false
        default: true
      ports:
        description: The ports of the NVM subsystem.
        type: list
        elements: str
        required: false
      host_nqns:
        description: The host NQNs of the NVM subsystem.
        type: list
        elements: dict
        required: false
      namespaces:
        description: The namespaces of the NVM subsystem.
        type: list
        elements: dict
        required: false
        suboptions:
          ldev_id:
            description: The LDEV ID of the namespace.
            type: int
            required: true
          nickname:
            description: The nickname of the namespace.
            type: str
            required: false
          paths:
            description: The paths of the namespace.
            type: list
            elements: str
            required: false
      force:
        description: This flag is used to force the operation.
        type: bool
        required: false
        default: false
      state:
        description:
          - The specific operation to perform on the NVM subsystem.
          - C(add_port) - Add ports to the NVM subsystem.
          - C(remove_port) - Remove ports from the NVM subsystem.
          - C(add_host_nqn) - Add host NQNs to the NVM subsystem.
          - C(remove_host_nqn) - Remove host NQNs from the NVM subsystem.
          - C(add_namespace) - Add namespaces to the NVM subsystem.
          - C(remove_namespace) - Remove namespaces from the NVM subsystem.
          - C(add_namespace_path) - Add paths to the namespace.
          - C(remove_namespace_path) - Remove paths from the namespace.
        type: str
        required: false
        choices: ['add_port', 'remove_port', 'add_host_nqn', 'remove_host_nqn', 'add_namespace',
                  'remove_namespace', 'add_namespace_path', 'remove_namespace_path']
"""

EXAMPLES = """
- name: Create an NVM Subsystem
  hitachivantara.vspone_block.vsp.hv_nvm_subsystems:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    state: "present"
    spec:
      name: "nvm_tcp_01"
      id: 1000
      host_mode: "VMWARE_EX"
      enable_namespace_security: true
      ports: ["CL1-D"]
      host_nqns:
        - nqn: "nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa40"
          nickname: "my_host_nqn_40"
      namespaces:
        - ldev_id: 11101
          nickname: "nickname"
          paths: ["nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa40"]

- name: Add host NQNs to an NVM Subsystem with a specific ID
  hitachivantara.vspone_block.vsp.hv_nvm_subsystems:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    spec:
      id: 1000
      state: "add_host_nqn"
      host_nqns:
        - nqn: "nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa41"
          nickname: "my_host_nqn_41"

- name: Remove host NQNs from an NVM Subsystem with a specific ID
  hitachivantara.vspone_block.vsp.hv_nvm_subsystems:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    spec:
      id: 1000
      state: "remove_host_nqn"
      host_nqns:
        - nqn: "nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa41"
          nickname: "my_host_nqn_41"

- name: Delete an NVM Subsystem with a specific Id forcefully
  hitachivantara.vspone_block.vsp.hv_nvm_subsystems:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    state: "absent"
    spec:
      id: "nvm_subsystems_id_18"
      force: true
"""

RETURN = """
nvm_subsystems:
  description: The NVM subsystem information.
  returned: always
  type: list
  elements: dict
  contains:
    storage_serial_number:
      description: The serial number of the storage system.
      type: str
      sample: "810005"
    host_nqn_info:
      description: List of host NQNs and their nicknames.
      type: list
      elements: dict
      contains:
        host_nqn:
          description: The host NQN.
          type: str
          sample: "nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa40"
        host_nqn_nickname:
          description: The nickname of the host NQN.
          type: str
          sample: "my_host_nqn_40"
    namespace_paths_info:
      description: List of namespace paths information.
      type: list
      elements: dict
      contains:
        host_nqn:
          description: The host NQN.
          type: str
          sample: "nqn.2014-08.org.example:uuid:4b73e622-ddc1-449a-99f7-412c0d3baa40"
        ldev_id:
          description: The LDEV ID of the namespace.
          type: int
          sample: 11101
        ldev_hex_id:
          description: The hexadecimal ID of the LDEV.
          type: str
          sample: "00:2b:5c"
        namespace_id:
          description: The ID of the namespace.
          type: int
          sample: 3
    namespaces_info:
      description: List of namespaces information.
      type: list
      elements: dict
      contains:
        block_capacity:
          description: The block capacity of the namespace.
          type: int
          sample: 23068672
        capacity_in_unit:
          description: The capacity of the namespace in human-readable format.
          type: str
          sample: "11.00 G"
        ldev_id:
          description: The LDEV ID of the namespace.
          type: int
          sample: 11101
        ldev_hex_id:
          description: The hexadecimal ID of the LDEV.
          type: str
          sample: "00:2b:5c"
        namespace_id:
          description: The ID of the namespace.
          type: int
          sample: 3
        namespace_nickname:
          description: The nickname of the namespace.
          type: str
          sample: "nickname"
    nvm_subsystem_info:
      description: Information about the NVM subsystem.
      type: dict
      contains:
        host_mode:
          description: The host mode of the NVM subsystem.
          type: str
          sample: "VMWARE_EX"
        namespace_security_setting:
          description: The namespace security setting.
          type: str
          sample: "Enable"
        nvm_subsystem_id:
          description: The ID of the NVM subsystem.
          type: int
          sample: 1000
        nvm_subsystem_name:
          description: The name of the NVM subsystem.
          type: str
          sample: "nvm_tcp_01"
        resource_group_id:
          description: The resource group ID of the NVM subsystem.
          type: int
          sample: 0
        t10pi_mode:
          description: The T10PI mode of the NVM subsystem.
          type: str
          sample: "Disable"
    port:
      description: List of ports of the NVM subsystem.
      type: list
      elements: dict
      contains:
        port_id:
          description: The ID of the port.
          type: str
          sample: "CL1-D"
        port_type:
          description: The type of the port.
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


class VSPNvmSubsystemManager:
    def __init__(self):
        self.logger = Log()
        self.argument_spec = VSPNvmeSubsystemArguments().nvme_subsystem()

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=False,
        )
        try:
            self.parameter_manager = VSPParametersManager(self.module.params)
            self.connection_info = self.parameter_manager.get_connection_info()
            self.storage_serial_number = None
            self.spec = self.parameter_manager.get_nvme_subsystem_spec()
            self.state = self.parameter_manager.get_state()

        except Exception as e:
            self.logger.writeError(f"An error occurred during initialization: {str(e)}")
            self.module.fail_json(msg=str(e))

    def apply(self):
        self.logger.writeInfo("=== Start of NVM Subsystem operation ===")
        registration_message = validate_ansible_product_registration()

        nvm_subsystems = None
        try:
            reconciler = VSPNvmeReconciler(
                self.connection_info, self.storage_serial_number, self.state
            )
            nvm_subsystems = reconciler.reconcile_nvm_subsystem(self.spec)

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of NVM Subsystem operation ===")
            self.module.fail_json(msg=str(e))

        resp = {
            "changed": self.connection_info.changed,
            "nvm_subsystems": nvm_subsystems,
        }
        if registration_message:
            resp["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{resp}")
        self.logger.writeInfo("=== End of NVM Subsystem operation ===")
        self.module.exit_json(**resp)


def main(module=None):
    obj_store = VSPNvmSubsystemManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
