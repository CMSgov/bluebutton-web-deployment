try:
    from ..common.ansible_common import (
        log_entry_exit,
        convert_mb_to_gb,
    )
    from ..common.hv_log import Log
    from ..provisioner.vsp_storage_pool_provisioner import VSPStoragePoolProvisioner
    from ..gateway.vsp_storage_system_gateway import VSPStorageSystemDirectGateway
    from ..model.vsp_storage_pool_models import StoragePoolSpec
    from ..common.hv_constants import StateValue

except ImportError:
    from common.ansible_common import (
        log_entry_exit,
        convert_mb_to_gb,
    )
    from common.hv_log import Log
    from provisioner.vsp_storage_pool_provisioner import VSPStoragePoolProvisioner
    from gateway.vsp_storage_system_gateway import VSPStorageSystemDirectGateway
    from model.vsp_storage_pool_models import StoragePoolSpec
    from common.hv_constants import StateValue

logger = Log()


class VSPStoragePoolReconciler:

    def __init__(self, connection_info, serial=None):
        self.connection_info = connection_info
        self.provisioner = VSPStoragePoolProvisioner(self.connection_info)
        self.serial = serial
        if self.serial is None:
            self.serial = self.get_storage_serial_number()

    @log_entry_exit
    def storage_pool_reconcile(self, state: str, spec: StoragePoolSpec):
        #  reconcile the storage pool based on the desired state in the specification
        state = state.lower()
        if state == StateValue.ABSENT:
            return self.delete_storage_pool(spec)
        elif state == StateValue.PRESENT:
            ret_value = self.create_update_storage_pool(spec).to_dict()
            if ret_value is None:
                return None
            free_capacity_mb = ret_value.get("free_capacity_in_units")
            total_capacity_mb = ret_value.get("total_capacity_in_units")
            if free_capacity_mb:
                ret_value["free_capacity_in_units"] = convert_mb_to_gb(free_capacity_mb)
            if total_capacity_mb:
                ret_value["total_capacity_in_units"] = convert_mb_to_gb(
                    total_capacity_mb
                )
            return ret_value
            # return self.create_update_storage_pool(spec).to_dict()

    @log_entry_exit
    def get_storage_serial_number(self):
        storage_gw = VSPStorageSystemDirectGateway(self.connection_info)
        storage_system = storage_gw.get_current_storage_system_info()
        return storage_system.serialNumber

    @log_entry_exit
    def create_update_storage_pool(self, spec):
        pool = self.provisioner.get_storage_pool_by_name_or_id_only(spec.name, spec.id)
        if pool is None:
            return self.provisioner.create_storage_pool(spec)
        else:
            return self.provisioner.update_storage_pool(spec, pool)

    @log_entry_exit
    def delete_storage_pool(self, spec):

        return self.provisioner.delete_storage_pool(spec)

    @log_entry_exit
    def storage_pool_facts(self, pool_fact_spec):

        pools = self.provisioner.get_storage_pool(pool_fact_spec)
        return None if not pools else pools.to_dict()
