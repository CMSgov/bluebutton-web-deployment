try:
    from ..common.hv_log import Log
    from ..common.ansible_common import (
        log_entry_exit,
        camel_to_snake_case,
        get_default_value,
    )
    from ..provisioner.vsp_external_volume_provisioner import (
        VSPExternalVolumeProvisioner,
    )
    from ..model.vsp_external_parity_group_models import (
        ExternalParityGroupFactSpec,
    )
    from ..gateway.vsp_storage_system_gateway import VSPStorageSystemDirectGateway

except ImportError:
    from common.hv_log import Log
    from common.ansible_common import (
        log_entry_exit,
        camel_to_snake_case,
        get_default_value,
    )
    from provisioner.vsp_external_volume_provisioner import (
        VSPExternalVolumeProvisioner,
    )
    from model.vsp_external_parity_group_models import ExternalParityGroupFactSpec
    from gateway.vsp_storage_system_gateway import VSPStorageSystemDirectGateway

logger = Log()


class VSPExternalParityGroupReconciler:

    def __init__(self, connection_info, serial=None):
        self.connection_info = connection_info
        if serial is None:
            self.serial = self.get_storage_serial_number()
        self.ext_vol_provisioner = VSPExternalVolumeProvisioner(
            self.connection_info, self.serial
        )

    def get_storage_serial_number(self):
        storage_gw = VSPStorageSystemDirectGateway(self.connection_info)
        storage_system = storage_gw.get_current_storage_system_info()
        return storage_system.serialNumber

    @log_entry_exit
    def external_parity_group_facts(self, spec: ExternalParityGroupFactSpec = None):
        if spec is None:
            rsp = self.ext_vol_provisioner.get_all_external_parity_groups()
            if rsp is None:
                rsp = []
            logger.writeInfo(f"external_parity_group_facts={rsp}")
            extracted_data = ExternalParityGroupInfoExtractor(self.serial).extract(
                rsp.data_to_list()
            )
            return extracted_data
        else:
            return self.get_one_external_parity_group(spec.external_parity_group)

    @log_entry_exit
    def get_one_external_parity_group(self, ext_parity_grp):
        rsp = self.ext_vol_provisioner.get_one_external_parity_group(ext_parity_grp)
        if rsp is None:
            rsp = []
        logger.writeDebug(f"external_path_group_facts={rsp}")
        extracted_data = ExternalParityGroupInfoExtractor(self.serial).extract(
            [rsp.to_dict()]
        )
        logger.writeDebug(f"external_path_group_facts:extracted_data={extracted_data}")
        return extracted_data

    # @log_entry_exit
    # def validate_create_spec(self, spec: ExternalVolumeSpec):
    #     if (
    #         spec is None
    #         # or spec.ldev_id is None
    #         or spec.external_storage_serial is None
    #         or spec.external_ldev_id is None
    #     ):
    #         raise ValueError(VSPSExternalVolumeValidateMsg.REQUIRED_FOR_CREATE.value)

    # @log_entry_exit
    # def validate_delete_spec(self, spec: ExternalVolumeSpec):
    #     if spec is None or spec.ldev_id is None:
    #         raise ValueError(
    #             VSPSExternalVolumeValidateMsg.LDEV_REQUIRED_FOR_DELETE.value
    #         )

    # @log_entry_exit
    # def validate_external_path_spec(self, spec: ExternalPathGroupSpec):
    #     if spec is None or spec.external_path_group_id is None:
    #         raise ValueError(
    #             VSPSExternalPathGroupValidateMsg.EXT_PATH_GROUP_ID_REQD.value
    #         )
    #     if not spec.external_fc_paths and not spec.external_iscsi_target_paths:
    #         raise ValueError(VSPSExternalPathGroupValidateMsg.PATHS_REQD.value)


class ExternalParityGroupInfoExtractor:
    def __init__(self, storage_serial_number):
        self.storage_serial_number = storage_serial_number
        self.common_properties = {
            "externalParityGroupId": str,
            "usedCapacityRate": int,
            "availableVolumeCapacity": int,
            "spaces": list,
            # Not used fields
            # numOfLdevs: int = None
            # emulationType: str = None
            # clprId: int = None
            # externalProductId: str = None
            # availableVolumeCapacityInKB: int = None
        }

    def process_list(self, response_key):
        new_items = []

        if response_key is None:
            return []

        for item in response_key:
            new_dict = {}
            for key, value in item.items():
                key = camel_to_snake_case(key)
                value_type = type(value)
                # if value_type == list:
                #     value = self.process_list(value)
                if value is None:
                    default_value = get_default_value(value_type)
                    value = default_value
                new_dict[key] = value
            new_items.append(new_dict)
        return new_items

    @log_entry_exit
    def extract(self, responses):
        logger.writeDebug(
            f"external_path_group_facts={responses} len = {len(responses)}"
        )
        new_items = []
        for response in responses:
            new_dict = {"storage_serial_number": self.storage_serial_number}
            for key, value_type in self.common_properties.items():
                # Get the corresponding key from the response or its mapped key
                response_key = response.get(key)
                if value_type == list:
                    response_key = self.process_list(response_key)
                # Assign the value based on the response key and its data type
                cased_key = camel_to_snake_case(key)
                # if cased_key in self.parameter_mapping.keys():
                #     cased_key = self.parameter_mapping[cased_key]
                if response_key is not None:
                    new_dict[cased_key] = response_key
                else:
                    # Handle missing keys by assigning default values
                    default_value = get_default_value(value_type)
                    new_dict[cased_key] = default_value
            new_items.append(new_dict)
        return new_items
