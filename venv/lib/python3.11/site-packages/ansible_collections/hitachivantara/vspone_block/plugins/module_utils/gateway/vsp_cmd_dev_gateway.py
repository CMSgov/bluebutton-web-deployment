import time

try:
    from .gateway_manager import VSPConnectionManager
    from ..common.hv_log import Log
    from ..common.ansible_common import log_entry_exit
    from ..model.common_base_models import VSPStorageDevice
    from ..common.vsp_constants import PEGASUS_MODELS
except ImportError:
    from .gateway_manager import VSPConnectionManager
    from common.hv_log import Log
    from common.ansible_common import log_entry_exit
    from model.common_base_models import VSPStorageDevice
    from common.vsp_constants import PEGASUS_MODELS

SET_CMD_DEVICE_DIRECT = "v1/objects/ldevs/{}/actions/set-as-command-device/invoke"
POST_UPDATE_CACHE = "v1/services/storage-cache-service/actions/refresh/invoke"
GET_STORAGE_INFO_DIRECT = "v1/objects/storages/instance"


logger = Log()
gCopyGroupList = None


class VSPCmdDevDirectGateway:

    def __init__(self, connection_info):
        self.connection_manager = VSPConnectionManager(
            connection_info.address,
            connection_info.username,
            connection_info.password,
            connection_info.api_token,
        )
        self.connection_info = connection_info
        self.remote_connection_manager = None
        self.serial = None
        self.pegasus_model = None

    @log_entry_exit
    def set_serial(self, serial):
        self.serial = serial

    @log_entry_exit
    def is_pegasus(self):
        if self.pegasus_model is None:
            end_point = GET_STORAGE_INFO_DIRECT
            storage_info = self.connection_manager.get(end_point)
            logger.writeDebug(f"CMD_DEV:storage details{storage_info}")
            storage_info = VSPStorageDevice(**storage_info)

            pegasus_model = any(sub in storage_info.model for sub in PEGASUS_MODELS)
            logger.writeDebug(f"CMD_DEV: Storage Model: {storage_info.model}")
            self.pegasus_model = pegasus_model
        return self.pegasus_model

    @log_entry_exit
    def update_cache_of_storage_system(self):
        if self.is_pegasus():
            return
        end_point = POST_UPDATE_CACHE
        self.connection_manager.post_wo_job(end_point, data=None)
        time.sleep(5)
        return

    @log_entry_exit
    def create_command_device(self, spec):
        """Create Command Device"""
        ldev_id = spec.ldev_id
        parameters = {
            "isCommandDevice": True,
        }
        if spec.is_security_enabled is not None:
            parameters["isSecurityEnabled"] = spec.is_security_enabled
        if spec.is_user_authentication_enabled is not None:
            parameters["isUserAuthenticationEnabled"] = (
                spec.is_user_authentication_enabled
            )
        if spec.is_device_group_definition_enabled is not None:
            parameters["isDeviceGroupDefinitionEnabled"] = (
                spec.is_device_group_definition_enabled
            )
        payload = {"parameters": parameters}
        end_point = SET_CMD_DEVICE_DIRECT.format(ldev_id)
        response = self.connection_manager.post(end_point, payload)
        logger.writeDebug(f"CMD_DEV:response={response}")
        self.connection_info.changed = True

        self.update_cache_of_storage_system()
        return response

    @log_entry_exit
    def delete_command_device(self, ldev_id):
        """Delete Command Device"""
        parameters = {
            "isCommandDevice": False,
        }
        payload = {"parameters": parameters}
        end_point = SET_CMD_DEVICE_DIRECT.format(ldev_id)
        response = self.connection_manager.post(end_point, payload)
        logger.writeDebug(f"CMD_DEV:response={response}")
        self.connection_info.changed = True
        return response
