from dataclasses import dataclass, asdict
from typing import List

try:
    from .common_base_models import BaseDataClass, SingleBaseClass
except ImportError:
    from common_base_models import BaseDataClass, SingleBaseClass


@dataclass
class CapacityManageInfo:
    usedCapacityRate: int
    maximumReserveRate: int
    thresholdWarning: int
    thresholdDepletion: int
    thresholdStorageControllerDepletion: int


@dataclass
class SavingEffectsInfo:
    efficiencyDataReduction: int
    preCapacityDataReduction: int
    postCapacityDataReduction: int
    totalEfficiencyStatus: str
    dataReductionWithoutSystemDataStatus: str
    totalEfficiency: int
    dataReductionWithoutSystemData: int
    preCapacityDataReductionWithoutSystemData: int
    postCapacityDataReductionWithoutSystemData: int
    calculationStartTime: str
    calculationEndTime: str


@dataclass
class RebuildCapacityResourceSettingInfo:
    numberOfTolerableDriveFailures: int


@dataclass
class RebuildableResourcesInfo:
    numberOfDrives: int


@dataclass
class SDSBPoolInfo(SingleBaseClass):
    id: str
    name: str
    protectionDomainId: str
    statusSummary: str
    status: str
    totalCapacity: int
    totalRawCapacity: int
    totalRawCapacity: int
    usedCapacity: int
    freeCapacity: int
    totalPhysicalCapacity: int
    metaDataPhysicalCapacity: int
    reservedPhysicalCapacity: int
    usablePhysicalCapacity: int
    blockedPhysicalCapacity: int
    capacityManage: CapacityManageInfo
    savingEffects: SavingEffectsInfo
    numberOfVolumes: int
    redundantPolicy: str
    redundantType: str
    dataRedundancy: int
    storageControllerCapacitiesGeneralStatus: str
    totalVolumeCapacity: int
    provisionedVolumeCapacity: int
    otherVolumeCapacity: int
    temporaryVolumeCapacity: int
    rebuildCapacityPolicy: str
    rebuildCapacityResourceSetting: RebuildCapacityResourceSettingInfo
    rebuildCapacityStatus: str
    rebuildableResources: RebuildableResourcesInfo
    encryptionStatus: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def to_dict(self):
        return asdict(self)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     if "capacityManage" in kwargs:
    #         self.capacityManage = CapacityManageInfo(**kwargs.get("capacityManage"))
    #     if "savingEffects" in kwargs:
    #         self.savingEffects = SavingEffectsInfo(**kwargs.get("savingEffects"))
    #     if "rebuildCapacityResourceSetting" in kwargs:
    #         self.rebuildCapacityResourceSetting = RebuildCapacityResourceSettingInfo(**kwargs.get("rebuildCapacityResourceSetting"))
    #     if "rebuildableResources" in kwargs:
    #         self.rebuildableResources = RebuildCapacityResourceSettingInfo(**kwargs.get("rebuildableResources"))


@dataclass
class SDSBPoolsInfo(BaseDataClass):
    data: List[SDSBPoolInfo]
