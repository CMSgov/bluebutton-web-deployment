#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, [ Hitachi Vantara ]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
---
module: hv_storagesystem
short_description: Manages Hitachi VSP storage systems.
description:
  - This module manages Hitachi VSP storage systems.
  - This module is supported only for C(gateway) connection type.
  - For examples go to URL
    U(https://github.com/hitachi-vantara/vspone-block-ansible/blob/main/playbooks/vsp_uai_gateway/storagesystem.yml)
version_added: '3.0.0'
author:
  - Hitachi Vantara LTD (@hitachi-vantara)
requirements:
  - python >= 3.9
attributes:
  check_mode:
    description: Determines if the module should run in check mode.
    support: none
deprecated:
  removed_in: '4.0.0'
  why: The connection type C(gateway) is deprecated.
  alternative: Not available.
extends_documentation_fragment:
- hitachivantara.vspone_block.common.deprecated_note
options:
  state:
    description: The desired state of the storage system.
    type: str
    required: false
    choices: ['present', 'absent']
    default: 'present'
  storage_system_info:
    description:
      - Information about the Hitachi storage system. This field is required for gateway connection type only.
    type: dict
    required: true
    suboptions:
      serial:
        description: Serial number of the Hitachi storage system.
        type: str
        required: false
      address:
        description: IP address or hostname of the storage system.
        type: str
        required: true
      username:
        description: Username for authentication. This field is valid for C(direct) connection type only, and it is a required field.
        type: str
        required: true
      password:
        description: Password for authentication. This field is valid for C(direct) connection type only, and it is a required field.
        type: str
        required: true
      remote_gateway_address:
        description: Remote gateway address for the storage system.
        type: str
        required: false
  connection_info:
    description: Information required to establish a connection to the storage system.
    type: dict
    required: true
    suboptions:
      address:
        description: IP address or hostname of either the UAI gateway.
        type: str
        required: true
      username:
        description:
          Username for authentication. This field is valid for C(direct) connection type only, and it is a required field.
          Not needed for this module.
        type: str
        required: false
      password:
        description:
          Password for authentication. This field is valid for C(direct) connection type only, and it is a required field.
          Not needed for this module.
        type: str
        required: false
      connection_type:
        description: Type of connection to the storage system.
        type: str
        required: True
        choices: ['gateway']
      subscriber_id:
        description: This field is valid for C(gateway) connection type only. This is an optional field and only needed to support multi-tenancy environment.
        type: str
        required: false
      api_token:
        description: Token value to access UAI gateway. This is a required field for C(gateway) connection type.
        type: str
        required: false
"""

EXAMPLES = """
- name: Add Storage System for gateway connection type
  hitachivantara.vspone_block.vsp.hv_storagesystem:
    storage_system_info:
      serial: "811150"
      address: storage1.company.com
      username: "username"
      password: "password"
    connection_info:
      address: gateway.company.com
      api_token: "api token value"
      connection_type: "gateway"
      subscriber_id: 12345
    state: present

- name: Delete Storage System for gateway connection type
  hitachivantara.vspone_block.vsp.hv_storagesystem:
    storage_system_info:
      serial: "811150"
    connection_info:
      address: gateway.company.com
      api_token: "api token value"
      connection_type: "gateway"
      subscriber_id: 12345
    state: absent
"""

RETURN = """
storage_systems:
  description: >
    Dictionary containing the discovered properties of the storage systems.
  returned: always
  type: dict
  contains:
    controller_address:
      description: IP address of the storage system controller.
      type: str
      sample: "192.168.0.126"
    device_limits:
      description: Limits for various device parameters.
      type: dict
      contains:
        external_group_number_range:
          description: Range for external group numbers.
          type: dict
          contains:
            is_valid:
              description: Indicates if the range is valid.
              type: bool
              sample: true
            max_value:
              description: Maximum value of the range.
              type: int
              sample: 16384
            min_value:
              description: Minimum value of the range.
              type: int
              sample: 1
        external_group_sub_number_range:
          description: Range for external group sub-numbers.
          type: dict
          contains:
            is_valid:
              description: Indicates if the range is valid.
              type: bool
              sample: true
            max_value:
              description: Maximum value of the range.
              type: int
              sample: 4096
            min_value:
              description: Minimum value of the range.
              type: int
              sample: 1
        parity_group_number_range:
          description: Range for parity group numbers.
          type: dict
          contains:
            is_valid:
              description: Indicates if the range is valid.
              type: bool
              sample: true
            max_value:
              description: Maximum value of the range.
              type: int
              sample: 1
            min_value:
              description: Minimum value of the range.
              type: int
              sample: 1
        parity_group_sub_number_range:
          description: Range for parity group sub-numbers.
          type: dict
          contains:
            is_valid:
              description: Indicates if the range is valid.
              type: bool
              sample: true
            max_value:
              description: Maximum value of the range.
              type: int
              sample: 32
            min_value:
              description: Minimum value of the range.
              type: int
              sample: 1
    free_capacity:
      description: Free capacity of the storage system.
      type: str
      sample: "15.88 TB"
    free_capacity_in_mb:
      description: Free capacity of the storage system in megabytes.
      type: int
      sample: 16655844
    free_local_clone_consistency_group_id:
      description: Free local clone consistency group ID.
      type: int
      sample: -1
    free_remote_clone_consistency_group_id:
      description: Free remote clone consistency group ID.
      type: int
      sample: -1
    management_address:
      description: Management IP address of the storage system.
      type: str
      sample: "192.168.0.126"
    microcode_version:
      description: Microcode version of the storage system.
      type: str
      sample: "93-07-23-80/01"
    model:
      description: Model of the storage system.
      type: str
      sample: "VSP E1090H"
    operational_status:
      description: Operational status of the storage system.
      type: str
      sample: "Normal"
    serial_number:
      description: Serial number of the storage system.
      type: str
      sample: "715036"
    syslog_config:
      description: Syslog configuration of the storage system.
      type: dict
      contains:
        detailed:
          description: Indicates if detailed logging is enabled.
          type: bool
          sample: true
        syslog_servers:
          description: List of syslog servers.
          type: list
          elements: dict
          contains:
            id:
              description: ID of the syslog server.
              type: int
              sample: 0
            syslog_server_address:
              description: Address of the syslog server.
              type: str
              sample: "192.168.0.143"
            syslog_server_port:
              description: Port of the syslog server.
              type: str
              sample: "514"
    total_capacity:
      description: Total capacity of the storage system.
      type: str
      sample: "27.62 TB"
    total_capacity_in_mb:
      description: Total capacity of the storage system in megabytes.
      type: int
      sample: 28958726
"""

import json
import os

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.gw_module_args import (
    DEPCRECATED_MSG,
)

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_log import (
    Log,
)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.hv_constants import (
    CommonConstants,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.vsp_utils import (
    camel_to_snake_case_dict,
)
from ansible_collections.hitachivantara.vspone_block.plugins.module_utils.common.ansible_common import (
    validate_ansible_product_registration,
)

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "supported_by": "certified",
    "status": ["stableinterface"],
}

logger = Log()
moduleName = "Storage System"


def getStorageJson(storageProfile):
    logger.writeDebug("storageProfile={}", storageProfile)

    if storageProfile is None:
        storageProfile = "./storage.json"
    else:

        # expect the input from playbook a list

        storageProfile = storageProfile[0]

    logger.writeParam("storageProfile={}", storageProfile)

    if not os.path.exists(storageProfile):
        raise Exception(
            "The storage profile {0} does not exist.".format(storageProfile)
        )

    # setenv for password decrypt

    storageProfile = os.path.abspath(storageProfile)
    os.environ["HV_STORAGE_ANSIBLE_PROFILE"] = storageProfile
    logger.writeDebug("abs storageProfile={}", storageProfile)
    logger.writeDebug("env storageProfile={}", os.getenv("HV_STORAGE_ANSIBLE_PROFILE"))

    with open(storageProfile) as connectionFile:
        connections = json.load(connectionFile)

    return connections


def main(module=None):
    fields = {
        "state": {"default": "present", "choices": ["present", "absent"]},
        "storage_system_info": {"required": True, "type": "dict"},
        "connection_info": {"required": True, "type": "dict"},
    }

    if module is None:
        module = AnsibleModule(argument_spec=fields, supports_check_mode=False)

    try:

        logger.writeEnterModule(moduleName)
        logger.writeInfo("=== Start of Storage System operation. ===")
        registration_message = validate_ansible_product_registration()
        storage_system_info = module.params.get("storage_system_info", None)
        if storage_system_info is None:
            logger.writeError(
                "Invalid storage_system_info, please correct it and try again."
            )
            raise Exception(
                "Invalid storage_system_info, please correct it and try again."
            )

        # storage_system_info = json.loads(storage_system_info)
        # if storage_system_info is None:
        #     raise Exception(
        #         "Invalid storage_system_info, please correct it and try again."
        #     )

        # valid UCP

        ucp_serial = CommonConstants.UCP_NAME
        logger.writeDebug("ucp_name={}", ucp_serial)

        if ucp_serial is None:
            logger.writeError("The parameter ucp_name is required.")
            raise Exception("The parameter ucp_name is required.")

        # x = re.search("^(UCP-CI|UCP-HC|UCP-RS|Logical-UCP)-\d{5,10}$", ucp_serial)
        # if not x:
        #     raise Exception('The UCP serial number is invalid.')

        connection_info = module.params.get("connection_info", None)
        if connection_info is None:
            logger.writeError(
                "Invalid connection_info, please correct it and try again."
            )
            raise Exception("Invalid connection_info, please correct it and try again.")

        # connection_info = json.loads(connection_info)
        # if connection_info is None:
        #     raise Exception("Invalid connection_info, please correct it and try again.")

        management_address = connection_info.get("address", None)
        management_username = connection_info.get("username", None)
        management_password = connection_info.get("password", None)
        auth_token = connection_info.get("api_token", None)
        logger.writeDebug("management_address={}", management_address)
        logger.writeDebug("management_username={}", management_username)

        if management_address is None:
            logger.writeError(
                "Missing management_address, please correct it and try again."
            )
            raise Exception(
                "Missing management_address, please correct it and try again."
            )

        ucpManager = None

        storage_serial = storage_system_info.get("serial", None)
        storage_address = storage_system_info.get("address", None)
        storage_user = storage_system_info.get("username", None)
        storage_password = storage_system_info.get("password", None)
        remote_gateway_address = storage_system_info.get("remote_gateway_address", None)
        logger.writeDebug("management_address={}", management_address)
        logger.writeDebug("storage_serial={}", storage_serial)
        logger.writeDebug("20230620 storage_user={}", storage_user)
        logger.writeDebug("20230620 remote_gateway_address={}", remote_gateway_address)

        if storage_serial is None:
            logger.writeError(
                "Missing storage_serial, please correct it and try again."
            )
            raise Exception("Missing storage_serial, please correct it and try again.")

        if int(storage_serial) < 10000 or int(storage_serial) > 999999:
            logger.writeError(
                "Invalid storage serial number, please correct it and try again."
            )
            raise Exception(
                "Invalid storage serial number, please correct it and try again."
            )

        if remote_gateway_address == management_address:
            logger.writeError(
                "The remote_gateway_address cannot be the same as the management_address."
            )
            raise Exception(
                "The remote_gateway_address cannot be the same as the management_address."
            )

        #  get the ucp_serial by remote gateway, if given
        conv_system_name, conv_system_serial, conv_mgmt_address = None, None, None
        logger.writeDebug("name={}", conv_system_name)
        logger.writeDebug("serial={}", conv_system_serial)
        logger.writeDebug("gateway={}", conv_mgmt_address)

        # ucp is mandatory input
        # get the puma getway info out of it
        theUCP = ucpManager.getUcpSystem(conv_system_name)
        if theUCP is None:
            theUCP = ucpManager.createUcpSystem(
                conv_system_serial,
                conv_mgmt_address,
                "UCP CI",
                conv_system_name,
                "AMERICA",
                "United States",
                "95054",
                "",
            )
            theUCP = ucpManager.getUcpSystem(conv_system_name)
            # raise Exception("UCP {} is not found.".format(conv_system_name))
        if theUCP is None:
            #  sng,a2.4 system is not ready
            logger.writeError("Unable to perform basic setup, the system is not ready.")
            raise Exception("Unable to perform basic setup, the system is not ready.")

        logger.writeDebug("the system={}", theUCP)

        #  to work with StorageSystem, it needs the serial, not name
        ucp_serial = theUCP["serialNumber"]
        logger.writeDebug("system_serial={}", ucp_serial)

        state = module.params["state"]
        if state != "absent":

            #  2.4 - handle ss already onboarded
            # logger.writeDebug("380 theUCP={}", theUCP['storageDevices'])
            storageDevices = theUCP.get("storageDevices", None)
            if storageDevices:
                for storageDevice in storageDevices:
                    tmp = storageDevice.get("serialNumber", None)
                    if tmp is None:
                        continue
                    # logger.writeDebug("380 storage_serial={}", storage_serial)
                    # logger.writeDebug("380 storageDevice['serialNumber']={}", storageDevice['serialNumber'])
                    if str(storageDevice["serialNumber"]) == str(storage_serial):
                        # it is already onboarded
                        storageDevice.pop("ucpSystems", None)
                        logger.writeExitModule(moduleName)
                        data = {
                            "storage_systems": storageDevice,
                        }
                        if registration_message:
                            data["user_consent_required"] = registration_message

                        logger.writeInfo(f"{data}")
                        logger.writeInfo("=== End of Storage System operation. ===")
                        module.exit_json(**data)

            if storage_address is None:
                logger.writeError(
                    "Missing storage_address, please correct it and try again."
                )
                raise Exception(
                    "Missing storage_address, please correct it and try again."
                )
            if storage_user is None:
                logger.writeError(
                    "Missing storage_user, please correct it and try again."
                )
                raise Exception(
                    "Missing storage_user, please correct it and try again."
                )
            if storage_password is None:
                logger.writeError(
                    "Missing storage_password, please correct it and try again."
                )
                raise Exception(
                    "Missing storage_password, please correct it and try again."
                )

            gatewayIP = theUCP["gatewayAddress"]
            logger.writeDebug("20230616 gatewayIP={}", gatewayIP)

            results = ucpManager.addStorageSystem(
                storage_serial,
                storage_address,
                gatewayIP,
                8444,
                storage_user,
                storage_password,
                False,
                ucp_serial,
            )

            #  sng,a2.4 - expect only one ss here
            results.pop("ucpSystems", None)
            results = formatSS(results)

            logger.writeExitModule(moduleName)
            data = {
                "storage_system": results,
                "changed": True,
            }
            if registration_message:
                data["user_consent_required"] = registration_message
            logger.writeInfo(f"{data}")
            logger.writeInfo("=== End of Storage System operation. ===")
            module.exit_json(**data)
            # details=results['details'])
        else:
            results = ucpManager.removeStorageSystem(
                storage_serial,
                ucp_serial,
            )
            if results is not None and results:
                logger.writeError("Storage is no longer in the system.")
                logger.writeInfo("=== End of Storage System operation. ===")
                module.exit_json(msg="Storage is no longer in the system.")

            logger.writeError(
                f"Storage with serial {storage_serial} successfully deleted."
            )
            logger.writeInfo("=== End of Storage System operation. ===")
            module.exit_json(
                changed=True,
                msg=f"Storage with serial {storage_serial} successfully deleted.",
            )

    except EnvironmentError as ex:
        logger.writeDebug("EnvironmentError={}", ex)
        if ex is None or ex.strerror is None:
            msg = "Failed to add storage, please check input parameters."
        else:
            msg = ex.strerror
        logger.writeError(msg)
        logger.writeInfo("=== End of Storage System operation. ===")
        module.fail_json(msg=DEPCRECATED_MSG)
    except Exception as ex:
        logger.writeDebug("326 Exception={}", ex)
        # sng,a2.4 - there is no str(ex)?
        # if ex is None or str(ex) is None:
        if ex is None:
            msg = "Failed during add storage, please check input parameters."
        else:
            msg = str(ex)
        logger.writeError(msg)
        logger.writeInfo("=== End of Storage System operation. ===")
        module.fail_json(msg=DEPCRECATED_MSG)


def formatSS(storageSystem):
    logger.writeDebug("storageSystem={}", storageSystem)
    if storageSystem.get("freeCapacity"):
        del storageSystem["freeCapacity"]

    if storageSystem.get("totalCapacity"):
        del storageSystem["totalCapacity"]
    if storageSystem.get("freeCapacityInMb"):
        del storageSystem["freeCapacityInMb"]
    if storageSystem.get("freePoolCapacity"):
        del storageSystem["freePoolCapacity"]

    if storageSystem.get("freePoolCapacityInMb"):
        del storageSystem["freePoolCapacityInMb"]

    if storageSystem["totalCapacityInMb"]:
        del storageSystem["totalCapacityInMb"]

    if storageSystem.get("totalPoolCapacity"):
        del storageSystem["totalPoolCapacity"]

    if storageSystem.get("totalPoolCapacityInMb"):
        del storageSystem["totalPoolCapacityInMb"]

    return camel_to_snake_case_dict(storageSystem)


if __name__ == "__main__":
    main()
