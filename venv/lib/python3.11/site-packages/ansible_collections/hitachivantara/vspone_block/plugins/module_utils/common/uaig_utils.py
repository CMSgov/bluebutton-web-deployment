import copy

try:
    from ..common.hv_constants import CommonConstants
    from ..model.uaig_subscriber_models import SubscriberFactSpec, SubscriberSpec
    from ..model.uaig_password_model import PasswordSpec
    from ..model.common_base_models import (
        ConnectionInfo,
        StorageSystemInfo,
        TenantInfo,
    )
    from ..common.ansible_common import camel_to_snake_case
    from ..message.gateway_msgs import GatewayValidationMsg
    from ..common.hv_log import Log
except ImportError:
    from model.common_base_models import (
        ConnectionInfo,
        StorageSystemInfo,
        TenantInfo,
    )
    from model.uaig_subscriber_models import SubscriberFactSpec, SubscriberSpec
    from model.uaig_password_model import PasswordSpec
    from common.ansible_common import camel_to_snake_case
    from message.gateway_msgs import GatewayValidationMsg
    from common.hv_log import Log


import hashlib

logger = Log()


class UAIGCommonParameters:

    @staticmethod
    def storage_system_info():
        return {
            "required": True,
            "type": "dict",
            "options": {
                "serial": {
                    "required": True,
                    "type": "str",
                }
            },
        }

    @staticmethod
    def task_level():
        return {
            "required": True,
            "type": "dict",
            "options": {
                "state": {
                    "required": False,
                    "type": "str",
                    "choices": ["present", "absent"],
                    "default": "present",
                }
            },
        }

    @staticmethod
    def connection_info():
        return {
            "required": True,
            "type": "dict",
            "options": {
                "address": {
                    "required": True,
                    "type": "str",
                },
                "username": {
                    "required": False,
                    "type": "str",
                },
                "password": {
                    "required": False,
                    "type": "str",
                    "no_log": True,
                },
                "api_token": {
                    "required": False,
                    "type": "str",
                    "no_log": True,
                },
                "subscriber_id": {
                    "required": False,
                    "type": "str",
                },
                "connection_type": {
                    "required": False,
                    "type": "str",
                    "choices": ["gateway"],
                    "default": "gateway",
                },
            },
        }

    @staticmethod
    def tenant_info():
        return {
            "required": False,
            "type": "dict",
            "options": {
                "partnerId": {
                    "required": False,
                    "type": "str",
                },
                "subscriberId": {
                    "required": False,
                    "type": "str",
                },
            },
        }


class UAIGParametersManager:

    def __init__(self, params):
        self.params = params
        self.storage_system_info = StorageSystemInfo(
            **self.params.get("storage_system_info", {})
        )
        self.connection_info = ConnectionInfo(**self.params.get("connection_info", {}))
        self.spec = None


class GatewayArguments:

    common_arguments = {
        "connection_info": UAIGCommonParameters.connection_info(),
        "storage_system_info": {
            "required": False,
            "type": "dict",
            "options": {
                "serial": {
                    "required": True,
                    "type": "str",
                }
            },
        },
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
        "state": {
            "required": False,
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
    }

    @classmethod
    def get_subscriber_fact(cls):
        spec_options = {
            "subscriber_id": {
                "required": False,
                "type": "str",
            },
        }
        args = copy.deepcopy(cls.common_arguments)
        args["connection_info"]["options"].pop("subscriber_id")
        args["spec"]["options"] = spec_options
        args["spec"]["required"] = False
        args.pop("state")
        args.pop("storage_system_info")
        return args

    @classmethod
    def get_subscription_fact(cls):
        args = copy.deepcopy(cls.common_arguments)
        args.pop("spec")
        args.pop("state")
        return args

    @classmethod
    def gateway_subscriber(cls):
        spec_options = {
            "subscriber_id": {
                "required": True,
                "type": "str",
            },
            "name": {
                "required": False,
                "type": "str",
            },
            "soft_limit": {
                "required": False,
                "type": "str",
            },
            "hard_limit": {
                "required": False,
                "type": "str",
            },
            "quota_limit": {
                "required": False,
                "type": "str",
            },
            "description": {
                "required": False,
                "type": "str",
            },
        }
        args = copy.deepcopy(cls.common_arguments)
        args["spec"]["options"] = spec_options
        args["spec"]["required"] = True
        args.pop("storage_system_info")
        args["connection_info"]["options"].pop("subscriber_id")
        return args

    @classmethod
    def gateway_password(cls):
        gw_arguments = {
            "connection_info": {
                "required": True,
                "type": "dict",
                "options": {},
            },
            "spec": {
                "required": False,
                "type": "dict",
                "options": {},
            },
        }
        connection_option = {
            "uai_gateway_address": {
                "required": True,
                "type": "str",
            },
            "api_token": {
                "required": True,
                "type": "str",
                "no_log": True,
            },
        }
        spec_options = {
            "password": {
                "required": True,
                "type": "str",
                "no_log": True,
            },
        }
        gw_arguments["connection_info"]["options"] = connection_option
        gw_arguments["spec"]["options"] = spec_options
        return gw_arguments


class GatewayParametersManager:

    def __init__(self, params):
        self.params = params
        if (
            "storage_system_info" in self.params
            and self.params.get("storage_system_info") is not None
        ):
            self.storage_system_info = StorageSystemInfo(
                **self.params.get("storage_system_info", {"serial": None})
            )
        else:
            self.storage_system_info = StorageSystemInfo(**{"serial": None})
        self.connection_info = ConnectionInfo(**self.params.get("connection_info", {}))
        self.spec = None
        self.connection_info_map = self.params["connection_info"]
        self.spec_map = self.params.get("spec")
        if "tenant_info" in self.params:
            self.tenant_info = TenantInfo(**self.params.get("tenant_info", {}))
        else:
            self.tenant_info = TenantInfo()
        self.state = self.params.get("state", None)

    def get_state(self):
        return self.state

    def get_tenant_info(self):
        return self.tenant_info

    def set_subscriber_fact_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            self.spec = SubscriberFactSpec(
                self.params.get("spec", {}).get("subscriber_id")
            )
        else:
            self.spec = SubscriberFactSpec()

    def set_subscriber_spec(self, state):
        input_spec = SubscriberSpec(**self.params.get("spec", {}))
        GatewaySpecValidators().validate_subscriber(state, input_spec)
        return input_spec

    def set_admin_password_spec(self):
        input_spec = PasswordSpec(**self.params.get("spec", {}))
        return input_spec

    def get_connection_info(self):
        address = self.connection_info_map.get("management_address")
        username = self.connection_info_map.get("username")
        password = self.connection_info_map.get("password")
        api_token = self.connection_info_map.get("api_token")
        connection_type = self.connection_info_map.get("connection_type")
        return ConnectionInfo(address, username, password, api_token, connection_type)


class UAIGSnapshotArguments:

    common_arguments = {
        "storage_system_info": UAIGCommonParameters.storage_system_info(),
        "connection_info": UAIGCommonParameters.connection_info(),
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
        "task_level": {
            "required": False,
            "type": "dict",
            "options": {},
        },
    }

    @classmethod
    def get_snapshot_fact_args(cls):
        spec_options = {
            "pvol": {
                "required": False,
                "type": "int",
            },
            "mirror_unit_id": {
                "required": False,
                "type": "int",
            },
        }

        cls.common_arguments["spec"]["options"] = spec_options
        return cls.common_arguments

    @classmethod
    def get_snapshot_reconcile_args(cls):
        spec_options = {
            "pvol": {
                "required": True,
                "type": "int",
            },
            "pool_id": {
                "required": False,
                "type": "int",
            },
            "allocate_consistency_group": {
                "required": False,
                "type": "bool",
            },
            "consistency_group_id": {
                "required": False,
                "type": "int",
            },
            "enable_quick_mode": {
                "required": False,
                "type": "bool",
            },
            "auto_split": {
                "required": False,
                "type": "bool",
            },
            "mirror_unit_id": {
                "required": False,
                "type": "int",
            },
            "snapshot_group_name": {
                "required": False,
                "type": "str",
            },
            "is_data_reduction_force_copy": {
                "required": False,
                "type": "bool",
            },
            "can_cascade": {
                "required": False,
                "type": "bool",
            },
            "is_clone": {
                "required": False,
                "type": "bool",
            },
        }

        task_level_options = {
            "state": {
                "required": False,
                "type": "str",
                "choices": ["present", "absent", "split", "resync", "restore", "clone"],
                "default": "present",
            }
        }

        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments["task_level"]["options"] = task_level_options
        return cls.common_arguments


def camel_to_snake_case_dict_array(items):
    new_items = []
    if items:
        for item in items:
            new_dict = camel_to_snake_case_dict(item)
            new_items.append(new_dict)
    return new_items


def camel_to_snake_case_dict(response):
    new_dict = {}
    if response is None:
        return
    try:
        for key in response.keys():
            cased_key = camel_to_snake_case(key)
            new_dict[cased_key] = response[key]
    except Exception as ex:
        logger.writeDebug(f"exception in icamel_to_snake_case_dict {ex}")

    return new_dict


class UAIGResourceID:
    """
    This class is used to generate resource id for different resources
    md5 hash is used to generate resource id not to expose the actual value
    This is used to generate resource id for storage, ldev, snapshot, localpair, replpair, journalpool and so on
    nosec: No security issue here as it is does not exploit any security vulnerability
    """

    def get_md5_hash(self, data):
        # hash is used to generate the same resource ID in the UAIG gateway, non-security purposes
        md5_hash = hashlib.md5()
        md5_hash.update(data.encode("utf-8"))
        return md5_hash.hexdigest()

    def storage_resourceId(self, storage_serial_number):
        str_for_hash = f"{storage_serial_number}"
        return f"storage-{self.get_md5_hash(str_for_hash)}"

    def ldev_resourceId(self, storage_serial_number, ldev):
        str_for_hash = f"{storage_serial_number}:{ldev}"
        return f"storagevolume-{self.get_md5_hash(str_for_hash)}"

    def snapshot_resourceId(self, storage_serial_number, pvol, mirror_unit_id):
        storage_resourceId = self.storage_resourceId(storage_serial_number)
        return f"ssp-{storage_resourceId}-{pvol}-{mirror_unit_id}"

    def localpair_resourceId(self, p_vol, s_vol, primary_storage_serial_number):
        str_for_hash = f"{p_vol}:{s_vol}:{primary_storage_serial_number}"
        return f"localpair-{self.get_md5_hash(str_for_hash)}"

    def replpair_resourceId(self, p_vol, s_vol, primary_storage_serial_number):
        str_for_hash = f"{p_vol}:{s_vol}:{primary_storage_serial_number}"
        return f"replpair-{self.get_md5_hash(str_for_hash)}"

    def journal_pool_id(self, storage_serial_number, pool_id):
        str_for_hash = f"{storage_serial_number}:{pool_id}"
        return f"journalpool-{self.get_md5_hash(str_for_hash)}"

    def resource_group_resourceId(self, storage_serial_number, resource_group_name):
        resource_group_name_lower = resource_group_name.lower()
        str_for_hash = f"{storage_serial_number}:{resource_group_name_lower}"
        return f"resourcegroup-{self.get_md5_hash(str_for_hash)}"

    @classmethod
    def getSystemSerial(cls, management_address, remote_gateway_address):
        system_name = CommonConstants.UCP_NAME
        system_serial = CommonConstants.UCP_SERIAL
        system_gateway = management_address
        if remote_gateway_address and remote_gateway_address != "":
            #  expect ip address or fqdn
            hash_obj = hashlib.sha256(remote_gateway_address.encode("utf-8"))
            ss = str(int.from_bytes(hash_obj.digest(), "big"))
            last6 = ss[-6:]
            system_serial = CommonConstants.UCP_SERIAL_PREFIX + last6
            system_name = CommonConstants.UCP_NAME_PREFIX + last6
            system_gateway = remote_gateway_address
        return system_name, system_serial, system_gateway


class GatewaySpecValidators:

    @staticmethod
    def validate_subscriber(state, input_spec: SubscriberSpec):

        if state == "present":
            if not input_spec.subscriber_id:
                raise ValueError(GatewayValidationMsg.SUBSCRIBER_ID_MISSING.value)
            if not input_spec.name:
                raise ValueError(GatewayValidationMsg.SUBSCRIBER_NAME_MISSING.value)
            if not input_spec.quota_limit:
                raise ValueError(GatewayValidationMsg.QUOTA_LIMIT_MISSING.value)
        if state == "present" or state == "update":
            if input_spec.name:
                if len(input_spec.name) < 3 or len(input_spec.name) > 255:
                    raise ValueError(GatewayValidationMsg.NAME_LENGTH.value)
            if input_spec.quota_limit:
                try:
                    if int(input_spec.quota_limit) < 1:
                        raise ValueError(GatewayValidationMsg.QUOTA_LIMIT.value)
                except (ValueError, TypeError):
                    raise ValueError(GatewayValidationMsg.QUOTA_LIMIT.value)
            if input_spec.subscriber_id:
                try:
                    if not int(input_spec.subscriber_id):
                        raise ValueError(GatewayValidationMsg.ID_NUMERIC.value)
                except (ValueError, TypeError):
                    raise ValueError(GatewayValidationMsg.ID_NUMERIC.value)
                if (
                    len(input_spec.subscriber_id) < 1
                    or len(input_spec.subscriber_id) > 15
                ):
                    raise ValueError(GatewayValidationMsg.ID_LENGTH.value)
            if input_spec.soft_limit:
                try:
                    if (
                        int(input_spec.soft_limit) < 0
                        or int(input_spec.soft_limit) > 99
                    ):
                        raise ValueError(GatewayValidationMsg.SOFT_LIMIT.value)
                except (ValueError, TypeError):
                    raise ValueError(GatewayValidationMsg.SOFT_LIMIT.value)
            if input_spec.hard_limit:
                try:
                    if (
                        int(input_spec.hard_limit) < 1
                        or int(input_spec.hard_limit) > 100
                    ):
                        raise ValueError(GatewayValidationMsg.HARD_LIMIT.value)
                except (ValueError, TypeError):
                    raise ValueError(GatewayValidationMsg.HARD_LIMIT.value)
            if input_spec.soft_limit and input_spec.hard_limit:
                try:
                    if int(input_spec.hard_limit) <= int(input_spec.soft_limit):
                        raise ValueError(GatewayValidationMsg.HARD_LIMIT_GREATER.value)
                except (ValueError, TypeError):
                    raise ValueError(GatewayValidationMsg.HARD_LIMIT_GREATER.value)
