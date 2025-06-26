try:
    from ..common.sdsb_constants import SDSBlockEndpoints
    from ..common.ansible_common import dicts_to_dataclass_list
    from ..model.sdsb_port_models import SDSBComputePortInfo, SDSBComputePortsInfo
    from ..common.ansible_common import log_entry_exit
    from .gateway_manager import SDSBConnectionManager
    from ..common.hv_log import Log

except ImportError:
    from common.sdsb_constants import SDSBlockEndpoints
    from common.ansible_common import dicts_to_dataclass_list
    from model.sdsb_port_models import SDSBComputePortInfo, SDSBComputePortsInfo
    from common.ansible_common import log_entry_exit
    from .gateway_manager import SDSBConnectionManager
    from common.hv_log import Log

logger = Log()


class SDSBPortDirectGateway:

    def __init__(self, connection_info):
        self.connection_manager = SDSBConnectionManager(
            connection_info.address, connection_info.username, connection_info.password
        )

    @log_entry_exit
    def get_port_by_id(self, id):
        end_point = SDSBlockEndpoints.GET_PORT_BY_ID.format(id)
        data = self.connection_manager.get(end_point)
        logger.writeDebug("GW:get_port_by_id:data={}", data)
        return SDSBComputePortInfo(**data)

    @log_entry_exit
    def get_compute_ports(self):
        end_point = SDSBlockEndpoints.GET_PORTS
        compute_ports_data = self.connection_manager.get(end_point)
        logger.writeDebug(
            "GW:get_compute_ports:compute_ports_data={}", compute_ports_data
        )
        return SDSBComputePortsInfo(
            dicts_to_dataclass_list(compute_ports_data["data"], SDSBComputePortInfo)
        )
