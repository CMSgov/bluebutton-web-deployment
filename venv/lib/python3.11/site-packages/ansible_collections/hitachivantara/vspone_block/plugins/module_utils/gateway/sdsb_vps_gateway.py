try:
    from ..common.sdsb_constants import SDSBlockEndpoints
    from ..common.ansible_common import dicts_to_dataclass_list
    from ..common.hv_log import Log
    from ..common.ansible_common import log_entry_exit
    from .gateway_manager import SDSBConnectionManager
    from ..model.sdsb_vps_models import SDSBVpsListInfo, SDSBVpsInfo, SummaryInformation


except ImportError:
    from common.sdsb_constants import SDSBlockEndpoints
    from common.ansible_common import dicts_to_dataclass_list
    from common.hv_log import Log
    from common.ansible_common import log_entry_exit
    from .gateway_manager import SDSBConnectionManager
    from model.sdsb_vps_models import SDSBVpsListInfo, SDSBVpsInfo, SummaryInformation


logger = Log()


class SDSBVpsDirectGateway:

    def __init__(self, connection_info):
        self.connection_manager = SDSBConnectionManager(
            connection_info.address, connection_info.username, connection_info.password
        )

    @log_entry_exit
    def get_vps(self):
        end_point = SDSBlockEndpoints.GET_VPS
        vps_data = self.connection_manager.get(end_point)
        return SDSBVpsListInfo(
            dicts_to_dataclass_list(vps_data["data"], SDSBVpsInfo),
            SummaryInformation(**vps_data["summaryInformation"]),
        )

    @log_entry_exit
    def get_vps_by_id(self, id):
        try:
            end_point = SDSBlockEndpoints.GET_VPS_BY_ID.format(id)
            data = self.connection_manager.get(end_point)
            logger.writeDebug("GW:get_vps_by_id:data={}", data)
            return SDSBVpsInfo(**data)
        except Exception as ex:
            logger.writeDebug("GW:get_vps_by_id:=Exception{}", ex)
            return None

    @log_entry_exit
    def delete_vps_by_id(self, id):
        try:
            end_point = SDSBlockEndpoints.DELETE_VPS.format(id)
            data = self.connection_manager.delete(end_point)
            return data
        except Exception as ex:
            logger.writeDebug("GW:delete_vps_by_id:=Exception{}", ex)
            return None

    @log_entry_exit
    def create_vps(self, spec):
        end_point = SDSBlockEndpoints.POST_VPS
        payload = {
            "name": spec.name,
            "upperLimitForNumberOfServers": spec.upper_limit_for_number_of_servers,
            "volumeSettings": spec.volume_settings,
        }

        return self.connection_manager.post(end_point, payload)

    @log_entry_exit
    def update_vps_volume_adr_setting(self, vps_id, adr_setting):
        end_point = SDSBlockEndpoints.UPDATE_VPS.format(vps_id)
        payload = {"savingSettingOfVolume": adr_setting}
        data = self.connection_manager.patch(end_point, payload)
        logger.writeDebug("GW:update_vps_volume_adr_setting:data={}", data)
        return data
