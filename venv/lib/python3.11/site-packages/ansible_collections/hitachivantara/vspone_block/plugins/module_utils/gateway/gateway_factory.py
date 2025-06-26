try:
    from ..common.hv_constants import ConnectionTypes, GatewayClassTypes
except ImportError:
    from common.hv_constants import ConnectionTypes, GatewayClassTypes

from .sdsb_compute_node_gateway import (
    SDSBComputeNodeDirectGateway,
)
from .sdsb_volume_gateway import SDSBVolumeDirectGateway
from .sdsb_chap_user_gateway import SDSBChapUserDirectGateway
from .sdsb_pool_gateway import SDSBPoolDirectGateway
from .sdsb_port_auth_gateway import SDSBPortAuthDirectGateway
from .sdsb_port_gateway import SDSBPortDirectGateway
from .sdsb_vps_gateway import SDSBVpsDirectGateway

from .vsp_snapshot_gateway import VSPHtiSnapshotDirectGateway

from .vsp_volume import VSPVolumeDirectGateway
from .vsp_host_group_gateway import VSPHostGroupDirectGateway
from .vsp_shadow_image_pair_gateway import (
    VSPShadowImagePairDirectGateway,
)
from .vsp_storage_system_gateway import (
    VSPStorageSystemDirectGateway,
)
from .sdsb_storage_system_gateway import SDSBStorageSystemDirectGateway
from .vsp_iscsi_target_gateway import (
    VSPIscsiTargetDirectGateway,
)
from .vsp_storage_pool_gateway import (
    VSPStoragePoolDirectGateway,
)
from .vsp_journal_volume_gateway import (
    VSPSJournalVolumeDirectGateway,
)
from .vsp_parity_group_gateway import (
    VSPParityGroupDirectGateway,
)
from .vsp_storage_port_gateway import (
    VSPStoragePortDirectGateway,
)
from .vsp_copy_groups_gateway import VSPCopyGroupsDirectGateway
from .vsp_true_copy_gateway import VSPTrueCopyDirectGateway
from .vsp_hur_gateway import VSPHurDirectGateway
from .vsp_nvme_gateway import VSPOneNvmeSubsystemDirectGateway
from .vsp_resource_group_gateway import (
    VSPResourceGroupDirectGateway,
)
from .vsp_user_group_gateway import VSPUserGroupDirectGateway
from .vsp_user_gateway import VSPUserDirectGateway
from .vsp_gad_pair_gateway import VSPGadPairDirectGateway
from .vsp_cmd_dev_gateway import VSPCmdDevDirectGateway
from .vsp_rg_lock_gateway import (
    VSPResourceGroupLockDirectGateway,
)
from .vsp_remote_storage_registration_gw import (
    VSPRemoteStorageRegistrationDirectGateway,
)
from .vsp_quorum_disk_gateway import VSPQuorumDiskDirectGateway
from .vsp_remote_connection_gateway import VSPRemoteConnectionDirectGateway
from .vsp_external_volume_gateway import VSPExternalVolumeDirectGateway
from .vsp_iscsi_remote_connection_gateway import VSPIscsiRemoteConnectionDirectGateway
from .vsp_local_copy_group_gateway import (
    VSPLocalCopyGroupDirectGateway,
)
from .vsp_dynamic_pool_gateway import VspDynamicPoolGateway
from .vsp_uvm_gateway import VSPUvmGateway

GATEWAY_MAP = {
    ConnectionTypes.DIRECT: {
        GatewayClassTypes.VSP_EXT_VOLUME: VSPExternalVolumeDirectGateway,
        GatewayClassTypes.VSP_VOLUME: VSPVolumeDirectGateway,
        GatewayClassTypes.VSP_HOST_GROUP: VSPHostGroupDirectGateway,
        GatewayClassTypes.VSP_SHADOW_IMAGE_PAIR: VSPShadowImagePairDirectGateway,
        GatewayClassTypes.VSP_STORAGE_SYSTEM: VSPStorageSystemDirectGateway,
        GatewayClassTypes.VSP_ISCSI_TARGET: VSPIscsiTargetDirectGateway,
        GatewayClassTypes.VSP_STORAGE_POOL: VSPStoragePoolDirectGateway,
        GatewayClassTypes.VSP_SNAPSHOT: VSPHtiSnapshotDirectGateway,
        GatewayClassTypes.VSP_PARITY_GROUP: VSPParityGroupDirectGateway,
        GatewayClassTypes.VSP_NVME_SUBSYSTEM: VSPOneNvmeSubsystemDirectGateway,
        GatewayClassTypes.VSP_TRUE_COPY: VSPTrueCopyDirectGateway,
        #  sng1104
        GatewayClassTypes.VSP_QUORUM_DISK: VSPQuorumDiskDirectGateway,
        GatewayClassTypes.VSP_GAD_PAIR: VSPGadPairDirectGateway,
        GatewayClassTypes.VSP_HUR: VSPHurDirectGateway,
        GatewayClassTypes.VSP_RESOURCE_GROUP: VSPResourceGroupDirectGateway,
        GatewayClassTypes.VSP_COPY_GROUPS: VSPCopyGroupsDirectGateway,
        GatewayClassTypes.VSP_LOCAL_COPY_GROUP: VSPLocalCopyGroupDirectGateway,
        GatewayClassTypes.VSP_CMD_DEV: VSPCmdDevDirectGateway,
        GatewayClassTypes.VSP_RG_LOCK: VSPResourceGroupLockDirectGateway,
        GatewayClassTypes.VSP_JOURNAL_VOLUME: VSPSJournalVolumeDirectGateway,
        GatewayClassTypes.VSP_REMOTE_STORAGE_REGISTRATION: VSPRemoteStorageRegistrationDirectGateway,
        GatewayClassTypes.VSP_USER_GROUP: VSPUserGroupDirectGateway,
        GatewayClassTypes.VSP_USER: VSPUserDirectGateway,
        # Add more mappings for direct connection types here
        GatewayClassTypes.SDSB_CHAP_USER: SDSBChapUserDirectGateway,
        GatewayClassTypes.SDSB_COMPUTE_NODE: SDSBComputeNodeDirectGateway,
        GatewayClassTypes.SDSB_STORAGE_SYSTEM: SDSBStorageSystemDirectGateway,
        GatewayClassTypes.SDSB_VOLUME: SDSBVolumeDirectGateway,
        GatewayClassTypes.SDSB_POOL: SDSBPoolDirectGateway,
        GatewayClassTypes.SDSB_PORT_AUTH: SDSBPortAuthDirectGateway,
        GatewayClassTypes.SDSB_PORT: SDSBPortDirectGateway,
        GatewayClassTypes.SDSB_VPS: SDSBVpsDirectGateway,
        GatewayClassTypes.STORAGE_PORT: VSPStoragePortDirectGateway,
        GatewayClassTypes.VSP_REMOTE_CONNECTION: VSPRemoteConnectionDirectGateway,
        GatewayClassTypes.VSP_ISCSI_REMOTE_CONNECTION: VSPIscsiRemoteConnectionDirectGateway,
        GatewayClassTypes.VSP_DYNAMIC_POOL: VspDynamicPoolGateway,
        GatewayClassTypes.VSP_UVM: VSPUvmGateway,
    },
}


class GatewayFactory:
    """Factory class to get the gateway object"""

    @staticmethod
    def get_gateway(connection_info, gateway_type):
        """
        it takes the connection_info and the gateway_type argument and returns the gateway object
        """
        connection_map = GATEWAY_MAP.get(connection_info.connection_type.lower())
        if not connection_map:
            raise ValueError(
                f"Unsupported connection type: {connection_info.connection_type}"
            )

        gateway_class = connection_map.get(gateway_type)
        if not gateway_class:
            raise ValueError(f"Unsupported gateway type: {gateway_type}")

        return gateway_class(connection_info)
