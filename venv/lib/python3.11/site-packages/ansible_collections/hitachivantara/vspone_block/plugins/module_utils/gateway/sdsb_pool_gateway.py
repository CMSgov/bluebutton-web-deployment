try:
    from ..common.sdsb_constants import SDSBlockEndpoints
    from ..common.ansible_common import dicts_to_dataclass_list
    from ..common.hv_log import Log
    from ..common.ansible_common import log_entry_exit
    from .gateway_manager import SDSBConnectionManager
    from ..model.sdsb_pool_models import SDSBPoolsInfo, SDSBPoolInfo


except ImportError:
    from common.sdsb_constants import SDSBlockEndpoints
    from common.ansible_common import dicts_to_dataclass_list
    from common.hv_log import Log
    from common.ansible_common import log_entry_exit
    from .gateway_manager import SDSBConnectionManager
    from model.sdsb_pool_models import SDSBPoolsInfo, SDSBPoolInfo


logger = Log()


class SDSBPoolDirectGateway:

    def __init__(self, connection_info):
        self.connection_manager = SDSBConnectionManager(
            connection_info.address, connection_info.username, connection_info.password
        )

    @log_entry_exit
    def get_pools(self):
        end_point = SDSBlockEndpoints.GET_POOLS
        pool_data = self.connection_manager.get(end_point)
        return SDSBPoolsInfo(dicts_to_dataclass_list(pool_data["data"], SDSBPoolInfo))

    @log_entry_exit
    def get_pool_by_name(self, name):
        end_point = SDSBlockEndpoints.GET_POOLS_AND_QUERY.format(name)
        data = self.connection_manager.get(end_point)
        logger.writeDebug(
            "GW:get_pool_by_name:data={} len={}", data, len(data.get("data"))
        )
        if data is not None and len(data.get("data")) > 0:
            return SDSBPoolInfo(**data.get("data")[0])
        else:
            return None
