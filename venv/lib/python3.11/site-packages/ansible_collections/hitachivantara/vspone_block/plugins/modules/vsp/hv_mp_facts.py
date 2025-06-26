#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_mp_facts
short_description: Retrieves MP blades information from Hitachi VSP storage systems.
description:
    - This module retrieves information about MP Blade from Hitachi VSP storage systems.
    - For examples, go to URL
      U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_direct/mp_blade_facts.yml)
version_added: '3.5.0'
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
        description: Username for authentication. TThis is a required field if api_token is not provided.
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
    description: Specification for the resource group facts to be gathered.
    type: dict
    required: false
    suboptions:
      mp_id:
        description: The ID of the MP blade. This is an optional field.
        type: int
        required: false
"""

EXAMPLES = """
- name: Get all MP Blades
  hitachivantara.vspone_block.vsp.hv_mp_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"

- name: Get MP Blade by id
  hitachivantara.vspone_block.vsp.hv_mp_facts:
    connection_info:
      address: storage1.company.com
      username: "admin"
      password: "secret"
    spec:
      mp_id: 1
"""


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.reconciler.vsp_mp_blade_reconciler import (
    MpBladeReconciler,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    VSPMPBladeArguments,
    VSPParametersManager,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)


class VSPMPBladeFactsManager(object):
    def __init__(self):

        self.logger = Log()
        self.argument_spec = VSPMPBladeArguments().mp_facts()

        self.module = AnsibleModule(
            argument_spec=self.argument_spec,
            supports_check_mode=True,
        )
        try:
            self.parameter_manager = VSPParametersManager(self.module.params)

            self.spec = self.parameter_manager.mp_blade_facts_spec()

        except Exception as e:
            self.logger.writeError(f"An error occurred during initialization: {str(e)}")
            self.module.fail_json(msg=str(e))

    def apply(self):

        self.logger.writeInfo("=== Start of MP Blade Facts ===")
        registration_message = validate_ansible_product_registration()

        try:
            response = MpBladeReconciler(
                self.parameter_manager.connection_info
            ).mp_blade_facts(self.spec)

        except Exception as e:
            self.logger.writeError(str(e))
            self.logger.writeInfo("=== End of MP Blade Facts ===")
            self.module.fail_json(msg=str(e))

        data = {
            "mp_blades": response,
        }
        if registration_message:
            data["user_consent_required"] = registration_message

        self.logger.writeInfo(f"{data}")
        self.logger.writeInfo("=== End of MP Blade Facts ===")
        self.module.exit_json(changed=False, ansible_facts=data)


def main():
    obj_store = VSPMPBladeFactsManager()
    obj_store.apply()


if __name__ == "__main__":
    main()
