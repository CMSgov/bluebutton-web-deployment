try:
    from ..provisioner.sdsb_port_provisioner import SDSBPortProvisioner
    from ..provisioner.sdsb_port_auth_provisioner import SDSBPortAuthProvisioner
    from ..common.hv_log import Log
    from ..common.ansible_common import log_entry_exit
    from ..model.sdsb_port_models import SDSBPortDetailInfoList, SDSBPortDetailInfo
except ImportError:
    from provisioner.sdsb_port_provisioner import SDSBPortProvisioner
    from provisioner.sdsb_port_auth_provisioner import SDSBPortAuthProvisioner
    from common.hv_log import Log
    from common.ansible_common import log_entry_exit
    from model.sdsb_port_models import SDSBPortDetailInfoList, SDSBPortDetailInfo

logger = Log()


class SDSBPortReconciler:
    def __init__(self, connection_info):
        self.connection_info = connection_info
        self.provisioner = SDSBPortProvisioner(self.connection_info)
        self.port_auth_prov = SDSBPortAuthProvisioner(self.connection_info)

    @log_entry_exit
    def get_compute_ports(self, spec=None):
        ports = self.provisioner.get_compute_ports(spec)
        logger.writeDebug("RC:get_compute_ports:ports={}", ports)
        detail_ports = self.get_detail_ports(ports.data)

        logger.writeDebug("RC:get_compute_ports:detail_ports={}", detail_ports)
        return SDSBPortDetailInfoList(data=detail_ports)

    @log_entry_exit
    def get_detail_ports(self, ports):
        port_detail_list = []

        for port in ports:
            port_id = port.id
            pd = self.get_detail_port(port_id)
            port_detail_list.append(pd)
        logger.writeDebug("RC:get_compute_ports:port_detail_list={}", port_detail_list)
        return port_detail_list

    @log_entry_exit
    def get_detail_port(self, port_id):
        port = self.provisioner.get_port_by_id(port_id)
        port_auth_info = self.port_auth_prov.get_port_auth_settings(port_id)
        chap_user_info = self.port_auth_prov.get_port_chap_users(port_id)
        pd = SDSBPortDetailInfo(
            portInfo=port,
            portAuthInfo=port_auth_info,
            chapUsersInfo=chap_user_info.data,
        )
        return pd
