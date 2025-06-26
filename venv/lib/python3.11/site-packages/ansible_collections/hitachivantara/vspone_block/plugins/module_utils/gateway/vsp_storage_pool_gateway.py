try:
    from ..common.vsp_constants import Endpoints
    from .gateway_manager import VSPConnectionManager
    from ..common.ansible_common import dicts_to_dataclass_list, log_entry_exit
    from ..model.vsp_storage_pool_models import (
        VSPPfrestStoragePoolList,
        VSPPfrestStoragePool,
        VSPPfrestLdevList,
        VSPPfrestLdev,
    )
    from ..common.uaig_constants import StoragePoolPayloadConst
    from ..common.hv_constants import PoolType

except ImportError:
    from common.vsp_constants import Endpoints
    from .gateway_manager import VSPConnectionManager
    from common.ansible_common import dicts_to_dataclass_list, log_entry_exit
    from model.vsp_storage_pool_models import (
        VSPPfrestStoragePoolList,
        VSPPfrestStoragePool,
        VSPPfrestLdevList,
        VSPPfrestLdev,
    )
    from common.uaig_constants import StoragePoolPayloadConst
    from common.hv_constants import PoolType


class VSPStoragePoolDirectGateway:

    def __init__(self, connection_info):
        self.connectionManager = VSPConnectionManager(
            connection_info.address,
            connection_info.username,
            connection_info.password,
            connection_info.api_token,
        )

    @log_entry_exit
    def get_all_storage_pools(self):
        endPoint = Endpoints.GET_POOLS
        storagePoolsDict = self.connectionManager.get(endPoint)
        return VSPPfrestStoragePoolList(
            dicts_to_dataclass_list(storagePoolsDict["data"], VSPPfrestStoragePool)
        )

    @log_entry_exit
    def get_storage_pool_by_id(self, pool_id):
        endPoint = Endpoints.GET_POOL.format(pool_id)
        poolDict = self.connectionManager.get(endPoint)
        return VSPPfrestStoragePool(**poolDict)

    @log_entry_exit
    def get_ldevs(self, ldevs_query):
        endPoint = Endpoints.GET_LDEVS.format(ldevs_query)
        rest_dpvolumes = self.connectionManager.get(endPoint)
        return VSPPfrestLdevList(
            dicts_to_dataclass_list(rest_dpvolumes["data"], VSPPfrestLdev)
        )

    @log_entry_exit
    def create_storage_pool(self, spec):
        endPoint = Endpoints.POST_POOL
        payload = {}
        payload[StoragePoolPayloadConst.POOL_ID] = spec.pool_id
        payload[StoragePoolPayloadConst.POOL_NAME] = spec.name
        payload[StoragePoolPayloadConst.POOL_TYPE] = (
            PoolType.HDT if spec.type.upper() == PoolType.HRT else spec.type.upper()
        )

        if isinstance(spec.warning_threshold_rate, int):
            payload[StoragePoolPayloadConst.WARNING_THRESHOLD] = (
                spec.warning_threshold_rate
            )
        if isinstance(spec.depletion_threshold_rate, int):
            payload[StoragePoolPayloadConst.DEPLETION_THRESHOLD] = (
                spec.depletion_threshold_rate
            )
        if spec.ldev_ids:
            payload[StoragePoolPayloadConst.LDEV_IDS] = spec.ldev_ids
        if spec.should_enable_deduplication:
            payload[StoragePoolPayloadConst.IS_ENABLE_DEDUPLICATION] = (
                spec.duplication_ldev_ids
            )

        url = self.connectionManager.post(endPoint, payload)
        pool_id = url.split("/")[-1]
        if spec.type.upper() == PoolType.HRT:
            spec.type = PoolType.RT
            try:
                self.change_storage_pool_settings(pool_id, spec)
            except Exception as e:
                self.delete_storage_pool(pool_id)
                raise e
        return pool_id

    @log_entry_exit
    def delete_storage_pool(self, pool_id):
        endPoint = Endpoints.GET_POOL.format(pool_id)
        return self.connectionManager.delete(endPoint)

    @log_entry_exit
    def update_storage_pool(self, pool_id, spec):
        endPoint = Endpoints.POOL_EXPAND.format(pool_id)
        payload = {
            StoragePoolPayloadConst.PARAMETERS: {
                StoragePoolPayloadConst.LDEV_IDS: spec.ldev_ids
            }
        }

        return self.connectionManager.post(endPoint, payload)

    @log_entry_exit
    def change_storage_pool_settings(self, pool_id, spec):
        endPoint = Endpoints.GET_POOL.format(pool_id)
        payload = {}
        # will add more parameters as needed

        if spec.type:
            payload[StoragePoolPayloadConst.POOL_TYPE] = spec.type

        unused = self.connectionManager.patch(endPoint, payload)
        return pool_id
