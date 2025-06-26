from dataclasses import dataclass, field, asdict
from typing import Optional, List

try:
    from .common_base_models import BaseDataClass, SingleBaseClass
    from ..common.hv_log import Log

except ImportError:
    from .common_base_models import BaseDataClass, SingleBaseClass
    from common.hv_log import Log

logger = Log()


@dataclass
class VolumeFactSpec:
    ldev_id: Optional[str] = None
    name: Optional[str] = None
    count: Optional[int] = None
    end_ldev_id: Optional[int] = None
    start_ldev_id: Optional[int] = None
    is_detailed: Optional[bool] = None
    query: Optional[List[str]] = None


@dataclass
class TieringPolicySpec:
    tier_level: Optional[int] = None
    tier1_allocation_rate_min: Optional[int] = None
    tier1_allocation_rate_max: Optional[int] = None
    tier3_allocation_rate_min: Optional[int] = None
    tier3_allocation_rate_max: Optional[int] = None


@dataclass
class VolumeQosParamsOutput:
    upperIops: Optional[int] = field(default=-1)
    upperTransferRate: Optional[int] = field(default=-1)
    upperAlertAllowableTime: Optional[int] = field(default=-1)
    upperAlertTime: Optional[int] = field(default=-1)
    lowerIops: Optional[int] = field(default=-1)
    lowerTransferRate: Optional[int] = field(default=-1)
    lowerAlertAllowableTime: Optional[str] = field(default=-1)
    lowerAlertTime: Optional[int] = field(default=-1)
    responsePriority: Optional[int] = field(default=-1)
    targetResponseTime: Optional[int] = field(default=-1)
    responseAlertAllowableTime: Optional[int] = field(default=-1)
    responseAlertTime: Optional[int] = field(default=-1)


@dataclass
class VolumeQosParamsSpec:
    upper_iops: int = None
    upper_transfer_rate: int = None
    upper_alert_allowable_time: int = None
    lower_iops: int = None
    lower_transfer_rate: int = None
    lower_alert_allowable_time: int = None
    response_priority: int = None
    response_alert_allowable_time: int = None


@dataclass
class CreateVolumeSpec:
    data_reduction_share: Optional[bool] = None
    name: Optional[str] = None
    size: Optional[str] = None
    block_size: Optional[int] = None
    ldev_id: Optional[str] = None
    # sng20241205 vldev_id
    vldev_id: Optional[str] = None
    pool_id: Optional[int] = None
    capacity_saving: Optional[str] = None
    parity_group: Optional[str] = None
    force: Optional[bool] = None
    is_relocation_enabled: Optional[bool] = None
    is_compression_acceleration_enabled: Optional[bool] = None
    compression_acceleration_status: Optional[str] = None
    tier_level_for_new_page_allocation: Optional[str] = None
    tiering_policy: Optional[TieringPolicySpec] = None
    nvm_subsystem_name: Optional[str] = None
    host_nqns: Optional[List[str]] = None
    state: Optional[str] = None
    should_shred_volume_enable: Optional[bool] = None
    qos_settings: Optional[VolumeQosParamsSpec] = None
    mp_blade_id: Optional[int] = None
    should_reclaim_zero_pages: Optional[bool] = None
    # Added for UCA-3302
    is_parallel_execution_enabled: Optional[bool] = None
    start_ldev_id: Optional[int] = None
    end_ldev_id: Optional[int] = None
    external_parity_group: Optional[str] = None
    is_compression_acceleration_enabled: Optional[bool] = None
    should_format_volume: Optional[bool] = None
    data_reduction_process_mode: Optional[str] = None
    is_relocation_enabled: Optional[bool] = None
    is_full_allocation_enabled: Optional[bool] = None
    is_alua_enabled: Optional[bool] = None
    format_type: Optional[str] = None
    is_task_timeout: Optional[bool] = None
    # added comment for ldev module
    comment: Optional[str] = None

    def __post_init__(self):
        if self.qos_settings:
            self.qos_settings = VolumeQosParamsSpec(**self.qos_settings)


@dataclass
class VSPPortInfo(SingleBaseClass):
    portId: Optional[str] = None
    hostGroupNumber: Optional[int] = None
    hostGroupName: Optional[str] = None
    lun: Optional[int] = None


@dataclass
class VSPVolumeSnapshotInfo(SingleBaseClass):
    pvolLdevId: Optional[int] = None
    muNumber: Optional[int] = None
    svolLdevId: Optional[int] = None


@dataclass
class VSPVolumePortInfo(SingleBaseClass):
    portId: Optional[int] = None
    id: Optional[int] = None
    name: Optional[str] = None


@dataclass
class VSPVolumeNvmSubsystenInfo(SingleBaseClass):
    id: Optional[int] = None
    name: Optional[str] = None
    ports: Optional[List[str]] = None
    host_nqns: Optional[List[str]] = None


@dataclass
class VSPVolumeInfo(SingleBaseClass):

    ldevId: int
    clprId: int
    emulationType: str
    externalVolumeId: Optional[str] = None
    externalVolumeIdString: Optional[str] = None
    byteFormatCapacity: Optional[str] = None
    blockCapacity: Optional[int] = None
    numOfPorts: Optional[int] = None
    externalPorts: Optional[List[VSPPortInfo]] = None
    ports: Optional[List[VSPPortInfo]] = None
    composingPoolId: Optional[int] = None
    attributes: Optional[List[str]] = None
    raidLevel: Optional[str] = None
    raidType: Optional[str] = None
    numOfParityGroups: Optional[int] = None
    parityGroupIds: Optional[List[str]] = None
    driveType: Optional[str] = None
    driveByteFormatCapacity: Optional[str] = None
    driveBlockCapacity: Optional[int] = None
    label: Optional[str] = None
    status: Optional[str] = None
    mpBladeId: Optional[int] = None
    ssid: Optional[str] = None
    resourceGroupId: Optional[int] = None
    isAluaEnabled: Optional[bool] = None
    virtualLdevId: Optional[int] = None
    poolId: Optional[int] = None
    numOfUsedBlock: Optional[int] = None
    dataReductionMode: Optional[str] = None
    dataReductionStatus: Optional[str] = None
    dataReductionProcessMode: Optional[str] = None
    isEncryptionEnabled: Optional[bool] = None
    isDRS: Optional[bool] = None
    namespaceId: Optional[str] = None
    nvmSubsystemId: Optional[str] = None
    snapshots: Optional[List[VSPVolumeSnapshotInfo]] = None
    hostgroups: Optional[List[VSPVolumePortInfo]] = None
    iscsiTargets: Optional[List[VSPVolumePortInfo]] = None
    nvmSubsystems: List[VSPVolumeNvmSubsystenInfo] = None
    canonicalName: Optional[str] = None
    storageSerialNumber: Optional[str] = None
    isDataReductionShareEnabled: Optional[bool] = None
    qosSettings: Optional[VolumeQosParamsOutput] = None
    virtualLdevId: Optional[int] = None
    isCommandDevice: Optional[bool] = None
    isSecurityEnabled: Optional[bool] = None
    isUserAuthenticationEnabled: Optional[bool] = None
    isDeviceGroupDefinitionEnabled: Optional[bool] = None
    naaId: Optional[str] = None
    tierLevel: Optional[int] = None
    tierLevelForNewPageAllocation: Optional[str] = None
    tier1AllocationRateMin: Optional[int] = None
    tier1AllocationRateMax: Optional[int] = None
    tier3AllocationRateMin: Optional[int] = None
    tier3AllocationRateMax: Optional[int] = None
    isCompressionAccelerationEnabled: Optional[bool] = None
    compressionAccelerationStatus: Optional[str] = None
    dataReductionProcessMode: Optional[str] = None
    isRelocationEnabled: Optional[bool] = None
    isFullAllocationEnabled: Optional[bool] = None

    def __init__(self, **kwargs):
        try:
            from ..common.vsp_utils import NAIDCalculator
            from ..common.vsp_constants import get_basic_storage_details
        except ImportError:
            from common.vsp_utils import NAIDCalculator
            from common.vsp_constants import get_basic_storage_details

        super().__init__(**kwargs)
        try:
            storage_info = get_basic_storage_details()
            if storage_info is None:
                return
            self.storageSerialNumber = storage_info.serialNumber
            if self.naaId is None:
                if storage_info.firstWWN and self.canonicalName is None:
                    self.canonicalName = NAIDCalculator(
                        storage_info.firstWWN,
                        int(storage_info.serialNumber),
                        storage_info.model,
                    ).calculate_naid(kwargs.get("ldevId", None))
            else:
                self.canonicalName = self.naaId

            self.isDataReductionShareEnabled = (
                True if "DRS" in self.attributes else None
            )

            if self.qosSettings is not None:
                self.qosSettings = VolumeQosParamsOutput(**self.qosSettings)

        except Exception as ex:
            logger.writeDebug(f"MODEL: exception in initializing VSPVolumeInfo {ex}")
        return


@dataclass
class VSPVolumesInfo(BaseDataClass):
    data: List[VSPVolumeInfo] = None


@dataclass
class VSPVolumeDetailInfo(SingleBaseClass):
    volumeInfo: VSPVolumeInfo
    snapshotInfo: List[VSPVolumeSnapshotInfo]
    hostgroupInfo: List[VSPVolumePortInfo]
    iscsiTargetInfo: List[VSPVolumePortInfo]
    nvmSubsystemInfo: List[VSPVolumeNvmSubsystenInfo]

    def to_dict(self):
        return asdict(self)


@dataclass
class VSPVolumeDetailInfoList(BaseDataClass):
    data: List[VSPVolumeDetailInfo]


@dataclass
class VSPStorageVolumeUAIGInfo(SingleBaseClass):
    ldevId: int = -1
    poolId: int = -1
    totalCapacity: int = 0
    usedCapacity: int = 0
    poolName: str = None


@dataclass
class VSPStorageVolumeUAIG(SingleBaseClass):
    resourceId: str = None
    type: str = None
    storageId: str = None
    entitlementStatus: str = None
    partnerId: str = None
    subscriberId: str = None
    storageVolumeInfo: VSPStorageVolumeUAIGInfo = None


@dataclass
class VSPStorageVolumesUAIG(BaseDataClass):
    data: List[VSPStorageVolumeUAIG] = None


@dataclass
class PortGroups:
    group: int = -1
    lun: int = -1
    port: str = None


@dataclass
class Policy:
    level: int = -1
    tier1AllocRateMin: int = -1
    tier1AllocRateMax: int = -1
    tier3AllocRateMin: int = -1
    tier3AllocRateMax: int = -1


@dataclass
class TieringPropertiesDto:
    policy: Policy = None
    tier1UsedCapacityMB: int = -1
    tier2UsedCapacityMB: int = -1
    tier3UsedCapacityMB: int = -1
    tierLevelForNewPageAlloc: str = None


@dataclass
class VSPVolume_V2:
    resourceId: str = None
    deduplicationCompressionMode: str = None
    emulationType: str = None
    formatOrShredRate: int = 0
    ldevId: int = 0
    name: str = None
    parityGroupId: str = None
    poolId: int = 0
    resourceGroupId: int = 0
    status: str = None
    totalCapacity: int = 0
    usedCapacity: int = 0
    virtualStorageDeviceId: str = None
    stripeSize: int = 0
    type: str = None
    pathCount: int = 0
    provisionType: str = None
    isCommandDevice: bool = False
    logicalUnitIdHexFormat: str = None
    virtualLogicalUnitId: int = 0
    naaId: str = None
    dedupCompressionProgress: int = -1
    dedupCompressionStatus: str = None
    isALUA: bool = False
    isDynamicPoolVolume: bool = False
    isJournalPoolVolume: bool = False
    isPoolVolume: bool = False
    poolName: str = None
    quorumDiskId: int = -1
    isDRS: bool = False
    isInGadPair: bool = False
    isInTrueCopy: bool = False
    isVVol: bool = False
    portGroups: List[PortGroups] = None
    nvmNamespaceId: int = -1
    nvmSubsystemId: int = -1
    tieringPropertiesDto: TieringPropertiesDto = None
    isTieringRelocation: Optional[bool] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class VSPUndefinedVolumeInfo:
    ldevId: int = 0
    emulationType: str = None
    ssid: str = None
    resourceGroupId: int = 0
    virtualLdevId: int = 0


@dataclass
class VSPUndefinedVolumeInfoList(BaseDataClass):
    data: List[VSPUndefinedVolumeInfo] = None
