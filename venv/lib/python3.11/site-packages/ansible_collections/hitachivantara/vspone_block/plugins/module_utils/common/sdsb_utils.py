try:
    from ..common.hv_constants import ConnectionTypes
    from ..model.common_base_models import ConnectionInfo
    from ..model.sdsb_volume_models import VolumeFactSpec, VolumeSpec
    from ..model.sdsb_compute_node_models import ComputeNodeFactSpec, ComputeNodeSpec
    from ..model.sdsb_chap_user_models import ChapUserFactSpec, ChapUserSpec
    from ..model.sdsb_port_auth_models import PortAuthSpec
    from ..model.sdsb_port_models import PortFactSpec
    from ..model.sdsb_vps_models import VpsFactSpec, VpsSpec
    from ..message.sdsb_connection_msgs import SDSBConnectionValidationMsg
    from ..message.sdsb_volume_msgs import SDSBVolValidationMsg
    from ..common.sdsb_constants import AutomationConstants
except ImportError:
    from common.hv_constants import ConnectionTypes
    from model.common_base_models import ConnectionInfo
    from model.sdsb_volume_models import VolumeFactSpec, VolumeSpec
    from model.sdsb_compute_node_models import ComputeNodeFactSpec, ComputeNodeSpec
    from model.sdsb_chap_user_models import ChapUserFactSpec, ChapUserSpec
    from model.sdsb_port_auth_models import PortAuthSpec
    from model.sdsb_port_models import PortFactSpec
    from model.sdsb_vps_models import VpsFactSpec, VpsSpec
    from message.sdsb_connection_msgs import SDSBConnectionValidationMsg
    from message.sdsb_volume_msgs import SDSBVolValidationMsg
    from common.sdsb_constants import AutomationConstants


# SDSB Parameter manager
class SDSBParametersManager:

    def __init__(self, params):
        self.params = params
        self.connection_info = ConnectionInfo(**self.params.get("connection_info", {}))
        self.state = self.params.get("state", None)

        SDSBSpecValidators.validate_connection_info(self.connection_info)

    def get_state(self):
        return self.state

    def get_connection_info(self):
        return self.connection_info

    def get_volume_fact_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = VolumeFactSpec(**self.params["spec"])
        else:
            input_spec = VolumeFactSpec()
        return input_spec

    def get_volume_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = VolumeSpec(**self.params["spec"])
            SDSBSpecValidators().validate_volume_spec(self.get_state(), input_spec)
        else:
            input_spec = VolumeSpec()
        return input_spec

    def get_compute_node_fact_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = ComputeNodeFactSpec(**self.params["spec"])
        else:
            input_spec = ComputeNodeFactSpec()
        return input_spec

    def get_compute_node_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = ComputeNodeSpec(**self.params["spec"])
        else:
            input_spec = ComputeNodeSpec()
        return input_spec

    def get_compute_port_fact_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = PortFactSpec(**self.params["spec"])
        else:
            input_spec = PortFactSpec()
        return input_spec

    def get_chap_user_fact_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = ChapUserFactSpec(**self.params["spec"])
        else:
            input_spec = ChapUserFactSpec()
        return input_spec

    def get_chap_user_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = ChapUserSpec(**self.params["spec"])
        else:
            input_spec = ChapUserSpec()
        return input_spec

    def get_port_auth_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = PortAuthSpec(**self.params["spec"])
        else:
            input_spec = PortAuthSpec()
        return input_spec

    def get_vps_fact_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = VpsFactSpec(**self.params["spec"])
        else:
            input_spec = VpsFactSpec()
        return input_spec

    def get_vps_spec(self):
        if "spec" in self.params and self.params["spec"] is not None:
            input_spec = VpsSpec(**self.params["spec"])
        else:
            input_spec = VpsSpec()
        return input_spec


class SDSBCommonParameters:

    @staticmethod
    def get_connection_info():
        return {
            "required": True,
            "type": "dict",
            "options": {
                "address": {
                    "required": True,
                    "type": "str",
                },
                "username": {
                    "required": True,
                    "type": "str",
                },
                "password": {
                    "required": True,
                    "type": "str",
                    "no_log": True,
                },
                "connection_type": {
                    "required": False,
                    "type": "str",
                    "choices": [
                        "direct"
                    ],  # Removed gateway connection type as it is not supported
                    "default": "direct",
                },
            },
        }

    @staticmethod
    def state():
        return {
            "required": False,
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        }


class UAIGTokenArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
    }
    common_arguments["connection_info"]["options"].pop("connection_type")

    @classmethod
    def get_arguments(cls):
        return cls.common_arguments


class SDSBComputeNodeArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
        "state": {
            "required": False,
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
    }

    @classmethod
    def compute_node(cls):
        spec_options = {
            "id": {
                "required": False,
                "type": "str",
            },
            "name": {
                "required": False,
                "type": "str",
            },
            "os_type": {
                "required": False,
                "type": "str",
            },
            "state": {
                "required": False,
                "type": "str",
                "choices": [
                    "add_iscsi_initiator",
                    "remove_iscsi_initiator",
                    "attach_volume",
                    "detach_volume",
                    "add_host_nqn",
                    "remove_host_nqn",
                ],
            },
            "iscsi_initiators": {"required": False, "type": "list", "elements": "str"},
            "host_nqns": {"required": False, "type": "list", "elements": "str"},
            "volumes": {"required": False, "type": "list", "elements": "str"},
            "should_delete_all_volumes": {
                "required": False,
                "type": "bool",
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments["spec"]["required"] = True
        return cls.common_arguments

    @classmethod
    def compute_node_facts(cls):
        spec_options = {
            "names": {
                "required": False,
                "type": "list",
                "elements": "str",
            },
            "hba_name": {
                "required": False,
                "type": "str",
            },
            # "vps_name": {
            #     "required": False,
            #     "type": "str",
            #     "description": "Compute nodes that belongs to this vps",
            # },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments.pop("state")
        cls.common_arguments["spec"]["required"] = False
        return cls.common_arguments


class SDSBVolumeArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
        "state": {
            "required": False,
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
    }

    @classmethod
    def volume(cls):
        spec_options = {
            "id": {
                "required": False,
                "type": "str",
            },
            "name": {
                "required": False,
                "type": "str",
            },
            "nickname": {
                "required": False,
                "type": "str",
            },
            "capacity": {
                "required": False,
                "type": "str",
            },
            "capacity_saving": {
                "required": False,
                "type": "str",
            },
            "pool_name": {
                "required": False,
                "type": "str",
            },
            # "vps_name": {
            #     "required": False,
            #     "type": "str",
            # },
            "state": {
                "required": False,
                "type": "str",
                "choices": [
                    "add_compute_node",
                    "remove_compute_node",
                ],
            },
            "compute_nodes": {
                "required": False,
                "type": "list",
                "elements": "str",
            },
            "qos_param": {
                "required": False,
                "type": "dict",
                "options": {
                    "upper_limit_for_iops": {
                        "required": False,
                        "type": "int",
                    },
                    "upper_limit_for_transfer_rate_mb_per_sec": {
                        "required": False,
                        "type": "int",
                    },
                    "upper_alert_allowable_time_in_sec": {
                        "required": False,
                        "type": "int",
                    },
                },
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments["spec"]["required"] = True
        return cls.common_arguments

    @classmethod
    def volume_facts(cls):
        spec_options = {
            "count": {
                "required": False,
                "type": "int",
                "default": 500,
            },
            "names": {
                "required": False,
                "type": "list",
                "elements": "str",
            },
            "nicknames": {
                "required": False,
                "type": "list",
                "elements": "str",
            },
            "capacity_saving": {
                "required": False,
                "type": "str",
                "choices": ["Disabled", "Compression"],
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments.pop("state")
        cls.common_arguments["spec"]["required"] = False
        return cls.common_arguments


class SDSBPortArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
    }

    @classmethod
    def port_facts(cls):
        spec_options = {
            "nicknames": {
                "required": False,
                "type": "list",
                "elements": "str",
            },
            "names": {
                "required": False,
                "type": "list",
                "elements": "str",
            },
            # 'protocol': {'required': False, 'type': 'str', 'description': 'Compute nodes that belongs to this vps'},
        }
        cls.common_arguments["spec"]["options"] = spec_options
        return cls.common_arguments


class SDSBPortAuthArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
        "state": {
            "required": False,
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
    }

    @classmethod
    def port_auth(cls):
        spec_options = {
            "port_name": {
                "required": False,
                "type": "str",
            },
            "state": {
                "required": False,
                "type": "str",
                "choices": [
                    "add_chap_user",
                    "remove_chap_user",
                ],
            },
            "authentication_mode": {
                "required": False,
                "type": "str",
                "choices": [
                    "CHAP",
                    "CHAP_complying_with_initiator_setting",
                    "None",
                ],
            },
            "is_discovery_chap_authentication": {
                "required": False,
                "type": "bool",
            },
            "target_chap_users": {
                "required": False,
                "type": "list",
                "elements": "str",
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments["spec"]["required"] = True
        return cls.common_arguments


class SDSBChapUserArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
        "state": {
            "required": False,
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
    }

    @classmethod
    def chap_user(cls):
        spec_options = {
            "id": {
                "required": False,
                "type": "str",
            },
            "target_chap_user_name": {
                "required": False,
                "type": "str",
            },
            "target_chap_secret": {
                "required": False,
                "type": "str",
                "no_log": True,
            },
            "initiator_chap_user_name": {
                "required": False,
                "type": "str",
            },
            "initiator_chap_secret": {
                "required": False,
                "type": "str",
                "no_log": True,
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments["spec"]["required"] = True
        return cls.common_arguments

    @classmethod
    def chap_user_facts(cls):
        spec_options = {
            "id": {
                "required": False,
                "type": "str",
            },
            "target_chap_user_name": {
                "required": False,
                "type": "str",
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments["spec"]["required"] = False
        cls.common_arguments.pop("state")

        return cls.common_arguments


class SDSBStorageSystemArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
        # "spec": {
        #     "required": False,
        #     "type": "dict",
        #     "options": {},
        # },# commented out as it is not used
    }

    @classmethod
    def storage_system_fact(cls):
        return cls.common_arguments


class SDSBVpsArguments:

    common_arguments = {
        "connection_info": SDSBCommonParameters.get_connection_info(),
        "state": {
            "required": False,
            "type": "str",
            "choices": ["present", "absent"],
            "default": "present",
        },
        "spec": {
            "required": False,
            "type": "dict",
            "options": {},
        },
    }

    @classmethod
    def vps(cls):
        spec_options = {
            "vps_name": {
                "required": False,
                "type": "str",
            },
            "vps_id": {
                "required": False,
                "type": "str",
            },
            # "id": {
            #     "required": False,
            #     "type": "str",
            # },
            # "name": {
            #     "required": False,
            #     "type": "str",
            # },
            # "upper_limit_for_number_of_user_groups": {
            #     "required": False,
            #     "type": "int",
            # },
            # "upper_limit_for_number_of_users": {
            #     "required": False,
            #     "type": "int",
            # },
            # "upper_limit_for_number_of_sessions": {
            #     "required": False,
            #     "type": "int",
            # },
            # "upper_limit_for_number_of_servers": {
            #     "required": False,
            #     "type": "int",
            # },
            # "volume_settings": {
            #     "required": False,
            #     "type": "list",
            # },
            "capacity_saving": {
                "required": False,
                "type": "str",
                "choices": ["Disabled", "Compression"],
                "default": "Disabled",
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments["spec"]["required"] = True
        return cls.common_arguments

    @classmethod
    def vps_facts(cls):
        spec_options = {
            "id": {
                "required": False,
                "type": "str",
            },
            "name": {
                "required": False,
                "type": "str",
            },
        }
        cls.common_arguments["spec"]["options"] = spec_options
        cls.common_arguments.pop("state")
        cls.common_arguments["spec"]["required"] = False
        return cls.common_arguments


# Validator functions
class SDSBSpecValidators:

    @staticmethod
    def validate_connection_info(conn_info: ConnectionInfo):

        if conn_info.connection_type == ConnectionTypes.DIRECT and conn_info.api_token:
            raise ValueError(SDSBConnectionValidationMsg.DIRECT_API_TOKEN_ERROR.value)
        elif conn_info.username and conn_info.password and conn_info.api_token:
            raise ValueError(
                SDSBConnectionValidationMsg.BOTH_API_TOKEN_USER_DETAILS.value
            )
        elif (
            not conn_info.username
            and not conn_info.password
            and not conn_info.api_token
        ):
            raise ValueError(
                SDSBConnectionValidationMsg.NOT_API_TOKEN_USER_DETAILS.value
            )

    @staticmethod
    def validate_volume_spec(state, input_spec: VolumeSpec):

        if input_spec.qos_param:
            if input_spec.qos_param.upper_limit_for_iops:
                if input_spec.qos_param.upper_limit_for_iops != -1:
                    if (
                        input_spec.qos_param.upper_limit_for_iops
                        < AutomationConstants.QOS_UPPER_LIMIT_IOPS_MIN
                        or input_spec.qos_param.upper_limit_for_iops
                        > AutomationConstants.QOS_UPPER_LIMIT_IOPS_MAX
                    ):
                        raise ValueError(
                            SDSBVolValidationMsg.QOS_UPPER_LIMIT_IOPS_OUT_OF_RANGE.value
                        )
            if input_spec.qos_param.upper_limit_for_transfer_rate_mb_per_sec:
                if input_spec.qos_param.upper_limit_for_transfer_rate_mb_per_sec != -1:
                    if (
                        input_spec.qos_param.upper_limit_for_transfer_rate_mb_per_sec
                        < AutomationConstants.QOS_UPPER_LIMIT_XFER_RATE_MIN
                        or input_spec.qos_param.upper_limit_for_transfer_rate_mb_per_sec
                        > AutomationConstants.QOS_UPPER_LIMIT_XFER_RATE_MAX
                    ):
                        raise ValueError(
                            SDSBVolValidationMsg.QOS_UPPER_LIMIT_XFER_RATE_OUT_OF_RANGE.value
                        )
            if input_spec.qos_param.upper_alert_allowable_time_in_sec:
                if input_spec.qos_param.upper_alert_allowable_time_in_sec != -1:
                    if (
                        input_spec.qos_param.upper_alert_allowable_time_in_sec
                        < AutomationConstants.QOS_UPPER_ALERT_ALLOWABLE_TIME_OUT_MIN
                        or input_spec.qos_param.upper_alert_allowable_time_in_sec
                        > AutomationConstants.QOS_UPPER_ALERT_ALLOWABLE_TIME_OUT_MAX
                    ):
                        raise ValueError(
                            SDSBVolValidationMsg.QOS_UPPER_ALERT_ALLOWABLE_TIME_OUT_OF_RANGE.value
                        )
