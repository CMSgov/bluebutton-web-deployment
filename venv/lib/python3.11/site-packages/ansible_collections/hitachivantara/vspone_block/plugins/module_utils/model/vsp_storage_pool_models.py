from dataclasses import dataclass, fields
from typing import Optional, List

try:
    from .common_base_models import BaseDataClass, SingleBaseClass, camel_to_snake
except ImportError:
    from common_base_models import BaseDataClass, SingleBaseClass, camel_to_snake


@dataclass
class PoolFactSpec:
    pool_id: Optional[int] = None
    pool_name: Optional[str] = None


@dataclass
class PoolVolumesSpec:
    parity_group_id: str = None
    capacity: str = None


@dataclass
class StoragePoolSpec:
    id: int = None
    name: str = None
    type: str = None
    pool_volumes: List[PoolVolumesSpec] = None
    resource_group_id: int = None
    warning_threshold_rate: int = None
    depletion_threshold_rate: int = None
    should_enable_deduplication: bool = None
    ldev_ids: List[int] = None
    duplication_ldev_ids: List[int] = None

    def __post_init__(self):
        if self.pool_volumes:
            self.pool_volumes = [
                (
                    PoolVolumesSpec(**volume)
                    if not isinstance(volume, PoolVolumesSpec)
                    else volume
                )
                for volume in self.pool_volumes
            ]


@dataclass
class VSPPfrestStoragePool(SingleBaseClass):
    poolId: int = None
    poolName: str = None
    poolType: str = None
    poolStatus: str = None
    usedCapacityRate: int = None
    availableVolumeCapacity: int = None
    totalPoolCapacity: int = None
    totalLocatedCapacity: int = None
    warningThreshold: int = None
    depletionThreshold: int = None
    virtualVolumeCapacityRate: int = None
    locatedVolumeCount: int = None
    snapshotCount: int = None
    isShrinking: bool = None
    name: str = None
    # Not used info
    # usedPhysicalCapacityRate: int = None
    # availablePhysicalVolumeCapacity: int = None
    # totalPhysicalCapacity: int = None
    # numOfLdevs: int = None
    # firstLdevId: int = None
    # suspendSnapshot: bool = None
    # snapshotUsedCapacity: int = None
    # blockingMode: str = None
    # totalReservedCapacity: int = None
    # reservedVolumeCount: int = None
    # poolActionMode: str = None
    # monitoringMode: str = None
    # tierOperationStatus: str = None
    # dat: str = None
    # tiers: List[tier_object] = None
    # duplicationLdevIds: List[int] = None
    # duplicationNumber: int = None
    # dataReductionAccelerateCompCapacity: int = None
    # dataReductionCapacity: int = None
    # dataReductionBeforeCapacity: int = None
    # dataReductionAccelerateCompRate: int = None
    # dataReductionRate: int = None
    # dataReductionAccelerateCompIncludingSystemData: dataReductionAccelerateCompIncludingSystemData_object = None
    # dataReductionIncludingSystemData: dataReductionIncludingSystemData_object = None
    # capacitiesExcludingSystemData: capacitiesExcludingSystemData_object = None
    # compressionRate: int = None
    # duplicationRate: int = None
    # isMainframe: bool = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if kwargs.get("poolName"):
            self.name = kwargs.get("poolName")


@dataclass
class VSPPfrestStoragePoolList(BaseDataClass):
    data: List[VSPPfrestStoragePool] = None


@dataclass
class VSPPfrestLdev(SingleBaseClass):
    ldevId: int = None
    blockCapacity: int = None
    resourceGroupId: int = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@dataclass
class VSPPfrestLdevList(BaseDataClass):
    data: List[VSPPfrestLdev] = None


@dataclass
class VSPDpVolume(SingleBaseClass):
    logicalUnitId: int = None
    size: int = None


@dataclass
class VSPStoragePool(SingleBaseClass):
    dpVolumes: List[VSPDpVolume] = None
    resourceId: str = None
    name: str = None
    poolId: int = None
    name: str = None
    type: str = None
    status: str = None
    utilizationRate: int = None
    freeCapacity: int = None
    freeCapacityInUnits: str = None
    free_capacity_in_mb: str = None
    totalCapacity: int = None
    totalCapacityInUnit: str = None
    total_capacity_in_mb: str = None
    warningThresholdRate: int = None
    depletionThresholdRate: int = None
    subscriptionLimitRate: int = None
    virtualVolumeCount: int = None
    subscriptionRate: int = None
    ldevIds: List[int] = None
    deduplicationEnabled: bool = None
    subscriberId: str = None
    partnerId: str = None
    entitlementStatus: str = None
    isEncrypted: bool = None
    resourceGroupId: int = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dpVolumes = kwargs.get("dpVolumes", None)
        if dpVolumes:
            self.dpVolumes = [VSPDpVolume(**dp) for dp in dpVolumes]
        pool_type = kwargs.get("type", None)
        self.type = "HRT" if pool_type == "RT" else pool_type

    def to_dict(self) -> dict:
        """
        Convert the dataclass instance to a dictionary with snake_case keys,
        replacing None values with default fillers based on data type.
        """

        result = {}
        for field in fields(self):
            value = getattr(self, field.name)
            snake_case_key = camel_to_snake(field.name)

            # Determine default filler based on data type
            if value is None or value == "null":
                value = (
                    -1
                    if field.type == int
                    else (
                        ""
                        if field.type == str
                        else (
                            False
                            if field.type == bool
                            else [] if field.type == List else None
                        )
                    )
                )
            elif field.type == List[VSPDpVolume]:
                if value is not None:
                    value = [item.camel_to_snake_dict() for item in value]
                else:
                    value = []
            result[snake_case_key] = value

        return result


@dataclass
class VSPStoragePools(BaseDataClass):
    data: List[VSPStoragePool] = None


@dataclass
class UAIGStoragePool(SingleBaseClass):

    resourceId: str = None
    name: str = None
    type: str = None
    poolId: int = None
    status: str = None
    utilizationRate: int = None
    freeCapacity: int = None
    freeCapacityInUnits: str = None
    totalCapacity: int = None
    totalCapacityInUnit: str = None
    warningThresholdRate: int = None
    depletionThresholdRate: int = None
    subscriptionLimitRate: int = None
    virtualVolumeCount: int = None
    subscriptionRate: int = None
    ldevIds: List[int] = None
    dpVolumes: List[VSPDpVolume] = None
    deduplicationEnabled: bool = None
    entitlementStatus: str = None
    partnerId: str = None
    subscriberId: str = None
    resourceGroupId: int = None
    replicationDataReleasedRate: int = None
    warningThresholdRate: int = None
    virtualVolumeCount: int = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pool_info = kwargs.get("storagePoolInfo")
        if pool_info:
            self.type = pool_info.get("poolType", None)
            self.name = pool_info.get("poolName", None)
            self.dpVolumes = pool_info.get("dpVolumes", [])
            self.deduplicationEnabled = pool_info.get("isDeduplicationEnabled", None)
            self.depletionThresholdRate = pool_info.get("depletionThresholdRate", None)
            for field in self.__dataclass_fields__.keys():
                if not getattr(self, field):
                    setattr(self, field, pool_info.get(field, None))


class UAIGStoragePools(BaseDataClass):
    data: List[UAIGStoragePool] = None


@dataclass
class JournalVolumeSpec:
    journal_id: int = None
    startLdevId: int = None
    endLdevId: int = None
    data_overflow_watchIn_seconds: int = None
    mp_blade_id: int = None
    is_cache_mode_enabled: bool = None
    ldev_ids: List[int] = None
    mirror_unit_number: int = None
    copy_pace: str = None
    path_blockade_watch_in_minutes: int = None


@dataclass
class JournalVolumeFactSpec:
    journal_id: Optional[int] = None
    is_free_journal_pool_id: Optional[bool] = None
    free_journal_pool_id_count: Optional[int] = None
    is_mirror_not_used: Optional[bool] = None
