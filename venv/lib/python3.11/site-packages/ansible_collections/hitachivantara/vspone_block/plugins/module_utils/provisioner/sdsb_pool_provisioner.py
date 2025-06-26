try:
    from ..gateway.gateway_factory import GatewayFactory
    from ..common.hv_constants import GatewayClassTypes
    from ..common.ansible_common import log_entry_exit

except ImportError:

    from gateway.gateway_factory import GatewayFactory
    from common.hv_constants import GatewayClassTypes
    from common.ansible_common import log_entry_exit


class SDSBPoolProvisioner:

    def __init__(self, connection_info):
        self.gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.SDSB_POOL
        )

    @log_entry_exit
    def get_pool_by_name(self, name):
        return self.gateway.get_pool_by_name(name)
