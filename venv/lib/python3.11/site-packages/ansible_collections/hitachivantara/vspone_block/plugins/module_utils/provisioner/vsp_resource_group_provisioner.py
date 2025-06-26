try:
    from ..gateway.gateway_factory import GatewayFactory
    from ..common.hv_constants import GatewayClassTypes, ConnectionTypes
    from ..common.hv_log import Log
    from ..common.ansible_common import log_entry_exit
    from ..model.vsp_resource_group_models import (
        DisplayResourceGroup,
        DisplayResourceGroupList,
        HostGroupInfo,
        UaigResourceGroupInfo,
        UaigResourceGroupInfoList,
    )
    from ..model.vsp_iscsi_target_models import IscsiTargetFactSpec
    from .vsp_storage_port_provisioner import VSPStoragePortProvisioner


except ImportError:
    from gateway.gateway_factory import GatewayFactory
    from common.hv_constants import GatewayClassTypes, ConnectionTypes
    from common.hv_log import Log
    from common.ansible_common import log_entry_exit
    from model.vsp_resource_group_models import (
        DisplayResourceGroup,
        DisplayResourceGroupList,
        HostGroupInfo,
        UaigResourceGroupInfo,
        UaigResourceGroupInfoList,
    )
    from model.vsp_iscsi_target_models import IscsiTargetFactSpec

    from .vsp_storage_port_provisioner import VSPStoragePortProvisioner


logger = Log()


class VSPResourceGroupProvisioner:

    def __init__(self, connection_info, serial=None):
        self.gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_RESOURCE_GROUP
        )
        self.hg_gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_HOST_GROUP
        )
        self.iscsi_gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_ISCSI_TARGET
        )
        self.port_prov = VSPStoragePortProvisioner(connection_info)
        self.connection_info = connection_info

        self.serial = serial
        if serial:
            self.serial = serial
            self.gateway.set_serial(serial)
        self.spec = None

    @log_entry_exit
    def get_resource_groups(self, spec=None, refresh=None):

        return self.get_resource_groups_direct(spec)

    @log_entry_exit
    def get_resource_groups_gw(self, spec=None, refresh=None):
        if spec is None or spec.is_empty():
            resource_groups = self.gateway.get_resource_groups(spec, refresh)
            # logger.writeDebug("PV:resource_groups={}", resource_groups)
            # return resource_groups
            return self.convert_rg_list_to_display_rg_list(
                resource_groups.data, None, None
            )
        else:
            ret_list = []

            if spec.id:
                resource_group = self.get_resource_group_by_rg_id(spec.id)
                logger.writeDebug("PV:resource_group={}", resource_group)
                if resource_group is None:
                    return None
                display_rg = self.convert_rg_to_display_rg(
                    resource_group, None, spec.query
                )
                ret_list.append(display_rg)
                return DisplayResourceGroupList(data=ret_list)

            elif spec.name:
                resource_group = self.get_resource_group_by_name(spec.name)
                logger.writeDebug("PV:resource_group={}", resource_group)
                if resource_group is None:
                    return None
                display_rg = self.convert_rg_to_display_rg(
                    resource_group, None, spec.query
                )
                ret_list.append(display_rg)
                return DisplayResourceGroupList(data=ret_list)
            else:
                resource_groups = self.get_resource_groups_for_query(spec)
                if spec.is_locked is not None:
                    if spec.is_locked:
                        resource_groups = self.get_locked_resource_group_gw(
                            resource_groups
                        )
                    else:
                        resource_groups = self.get_unlocked_resource_group_gw(
                            resource_groups
                        )

                return self.convert_rg_list_to_display_rg_list(
                    resource_groups, None, spec.query
                )

    @log_entry_exit
    def get_resource_groups_direct(self, spec=None):
        if spec is None:
            resource_groups = self.gateway.get_resource_groups()
            # logger.writeDebug("PV:resource_groups={}", resource_groups)
            # return resource_groups
            return self.convert_rg_list_to_display_rg_list(
                resource_groups.data, None, None
            )
        else:
            ret_list = []
            sp_ids = None
            if spec.query and "storage_pool_ids" in spec.query:
                sp_ids = self.handle_storage_pools()
            if spec.id:
                try:
                    resource_group = self.gateway.get_resource_group_by_id(spec.id)
                    logger.writeDebug("PV:resource_group={}", resource_group)
                    if resource_group is None:
                        return None
                    sp_ids = self.handle_storage_pools()
                    display_rg = self.convert_rg_to_display_rg(
                        resource_group, sp_ids, spec.query
                    )
                    ret_list.append(display_rg)
                    return DisplayResourceGroupList(data=ret_list)
                except Exception as e:
                    logger.writeError(
                        f"An error occurred during get_resource_group_by_id call: {str(e)}"
                    )
                    return None

            elif spec.name:
                resource_group = self.get_resource_group_by_name(spec.name)
                logger.writeDebug("PV:resource_group={}", resource_group)
                if resource_group is None:
                    return None
                sp_ids = self.handle_storage_pools()
                display_rg = self.convert_rg_to_display_rg(
                    resource_group, sp_ids, spec.query
                )
                ret_list.append(display_rg)
                return DisplayResourceGroupList(data=ret_list)
            else:

                resource_groups = self.gateway.get_resource_groups(spec)
                return self.convert_rg_list_to_display_rg_list(
                    resource_groups.data, sp_ids, spec.query
                )

    @log_entry_exit
    def get_resource_group_by_name(self, name):
        resource_groups = self.gateway.get_resource_groups()
        for rg in resource_groups.data:
            if rg.resourceGroupName == name:
                return rg
        return None

    @log_entry_exit
    def get_locked_resource_group_gw(self, name):
        ret_list = []
        resource_groups = self.gateway.get_resource_groups()
        for rg in resource_groups.data:
            if rg.locked is True:
                ret_list.append(rg)
        return ret_list

    @log_entry_exit
    def get_unlocked_resource_group_gw(self, name):
        ret_list = []
        resource_groups = self.gateway.get_resource_groups()
        for rg in resource_groups.data:
            if rg.locked is False:
                ret_list.append(rg)
        return ret_list

    @log_entry_exit
    def get_resource_group_by_rg_id(self, rg_id):
        resource_groups = self.gateway.get_resource_groups()
        logger.writeDebug("PV:resource_groups={}", resource_groups)
        logger.writeDebug("PV:get_resource_group_by_rg_id:rg_id={}", rg_id)

        if isinstance(rg_id, str) and rg_id.startswith("resourcegroup-"):
            for rg in resource_groups.data:
                if rg.resourceId == rg_id:
                    return rg
            return None
        else:
            for rg in resource_groups.data:
                if rg.resourceGroupId == int(rg_id):
                    return rg
            return None

    @log_entry_exit
    def get_resource_groups_for_query(self, spec):
        resource_groups = self.gateway.get_resource_groups()
        if spec.query is None:
            return resource_groups
        ret_list = []
        include_volume = True if "ldevs" in spec.query else False
        include_parity_group = True if "parity_groups" in spec.query else False
        include_port = True if "ports" in spec.query else False
        include_host_group = True if "host_groups" in spec.query else False
        # include_iscsi_target = True if "iscsi_targets" in spec.query else False
        # include_nvm_subsystem = True if "nvm_subsystem_ids" in spec.query else False
        include_pool = True if "storage_pool_ids" in spec.query else False
        for rg in resource_groups.data:
            tmp_rg = UaigResourceGroupInfo(
                resourceId=None,
                resourceGroupName=rg.resourceGroupName,
                resourceGroupId=rg.resourceGroupId,
                virtualDeviceId=rg.virtualDeviceId,
                virtualDeviceType=rg.virtualDeviceType,
                locked=rg.locked,
                parityGroups=rg.parityGroups if include_parity_group else None,
                hostGroups=rg.hostGroups if include_host_group else None,
                volumes=rg.volumes if include_volume else None,
                ports=rg.ports if include_port else None,
                pools=rg.pools if include_pool else None,
                metaResourceSerial=rg.metaResourceSerial,
            )
            ret_list.append(tmp_rg)
        return ret_list

    @log_entry_exit
    def get_resource_group_by_id(self, id):
        try:
            resource_group = self.gateway.get_resource_group_by_id(id)
            logger.writeDebug("PV:resource_group={}", resource_group)
            return resource_group
        except Exception as e:
            logger.writeError(
                f"An error occurred during get_resource_group_by_id call: {str(e)}"
            )
            return None

    @log_entry_exit
    def get_pool_ldevs(self, pool_ids):
        return self.gateway.get_pool_ldevs(pool_ids)

    @log_entry_exit
    def convert_rg_list_to_display_rg_list(self, rg_list, sp_ids, query):
        display_rg_list = []
        logger.writeDebug("PV:220:rg_list={}", rg_list)
        if isinstance(rg_list, UaigResourceGroupInfoList):
            rg_list = rg_list.data
        for rg in rg_list:
            # don't do all this crap for meta resource groups
            if rg.resourceGroupId == 0:
                continue
            display_rg = self.convert_rg_to_display_rg(rg, sp_ids, query)
            display_rg_list.append(display_rg)
        return DisplayResourceGroupList(data=display_rg_list)

    @log_entry_exit
    def fill_vsm_info(self, rg):
        all_vsms = self.gateway.get_vsm_all()
        logger.writeDebug("PV:fill_vsm_info:all_vsms={}", all_vsms)
        for vsm in all_vsms.data:
            if rg.resourceGroupId in vsm.resourceGroupIds:
                rg.virtualStorageDeviceId = vsm.virtualStorageDeviceId
                rg.virtualSerialNumber = vsm.virtualSerialNumber
                rg.virtualModel = vsm.virtualModel
                return

    @log_entry_exit
    def convert_rg_to_display_rg(self, rg, sp_ids=None, query=None):
        if rg is None:
            return None

        return self.convert_rg_to_display_rg_direct(rg, sp_ids, query)

    @log_entry_exit
    def convert_rg_to_display_rg_direct(self, rg, sp_ids=None, query=None):

        if rg.virtualStorageId != 0:
            self.fill_vsm_info(rg)
        if rg.hostGroupIds is not None:
            host_group_ids, iscsi_target_ids = self.break_host_group_ids(
                rg.hostGroupIds
            )
            rg.hostGroupIds = host_group_ids
            rg.iscsiTargetIds = iscsi_target_ids

            if sp_ids and rg.resourceGroupId in sp_ids:
                return self.get_display_resource_groups(
                    rg,
                    host_group_ids,
                    iscsi_target_ids,
                    sp_ids[rg.resourceGroupId],
                    query,
                )
            else:
                return self.get_display_resource_groups(
                    rg, host_group_ids, iscsi_target_ids, None, query
                )
        else:
            if sp_ids and rg.resourceGroupId in sp_ids:
                return self.get_display_resource_groups(
                    rg, None, None, sp_ids[rg.resourceGroupId], query
                )
            else:
                return self.get_display_resource_groups(rg, None, None, None, query)

    @log_entry_exit
    def get_display_resource_groups(
        self, rg, host_group_ids, iscsi_target_ids, sp_ids=None, query=None
    ):

        display_rg = DisplayResourceGroup()
        display_rg.name = rg.resourceGroupName
        display_rg.id = rg.resourceGroupId
        display_rg.lockStatus = rg.lockStatus
        display_rg.virtualStorageId = rg.virtualStorageId
        if rg.virtualStorageId != 0:
            display_rg.virtualSerialNumber = rg.virtualSerialNumber
            display_rg.virtualModel = rg.virtualModel

        display_rg.selfLock = rg.selfLock if hasattr(rg, "selfLock") else None
        display_rg.lockOwner = rg.lockOwner if hasattr(rg, "lockOwner") else None
        display_rg.lockHost = rg.lockHost if hasattr(rg, "lockHost") else None
        display_rg.lockSessionId = (
            rg.lockSessionId if hasattr(rg, "lockSessionId") else None
        )
        if query is None:
            if sp_ids:
                display_rg.storagePoolIds = sp_ids
            display_rg.ldevs = rg.ldevIds
            display_rg.parityGroups = rg.parityGroupIds
            display_rg.ports = rg.portIds
            display_rg.hostGroups = self.get_display_host_groups(host_group_ids)
            display_rg.iscsiTargets = self.get_display_iscsi_targets(iscsi_target_ids)
            display_rg.nvmSubsystemIds = rg.nvmSubsystemIds
        else:
            if "ldevs" in query:
                if rg.ldevIds:
                    display_rg.ldevs = rg.ldevIds
                else:
                    display_rg.ldevs = []
            if "parity_groups" in query:
                if rg.parityGroupIds:
                    display_rg.parityGroups = rg.parityGroupIds
                else:
                    display_rg.parityGroups = []
            if "ports" in query:
                if rg.portIds:
                    display_rg.ports = rg.portIds
                else:
                    display_rg.ports = []
            if "host_groups" in query:
                if host_group_ids:
                    display_rg.hostGroups = self.get_display_host_groups(host_group_ids)
                else:
                    display_rg.hostGroups = []
            if "iscsi_targets" in query:
                if iscsi_target_ids:
                    display_rg.iscsiTargets = self.get_display_iscsi_targets(
                        iscsi_target_ids
                    )
                else:
                    display_rg.iscsiTargets = []
            if "nvm_subsystem_ids" in query:
                if rg.nvmSubsystemIds:
                    display_rg.nvmSubsystemIds = rg.nvmSubsystemIds
                else:
                    display_rg.nvmSubsystemIds = []
            if "storage_pool_ids" in query:
                if sp_ids:
                    display_rg.storagePoolIds = sp_ids
                else:
                    display_rg.storagePoolIds = []

        return display_rg

    @log_entry_exit
    def break_host_group_ids(self, hg_ids):
        iscsi_target_ids = []
        host_group_ids = []

        for host_group_id in hg_ids:
            tmp = host_group_id.split(",")
            port = tmp[0]
            id = tmp[1]
            port_type = self.port_prov.get_port_type(port)
            if port_type == "ISCSI":
                iscsi_target_ids.append(f"{port},{id}")
            elif port_type == "FIBRE":
                host_group_ids.append(f"{port},{id}")
            else:
                logger.writeError(
                    f"PROV:break_host_group_ids:Unsupported port type: {port_type}"
                )
        return host_group_ids, iscsi_target_ids

    @log_entry_exit
    def create_resource_group(self, spec):
        return self.gateway.create_resource_group(spec)

    @log_entry_exit
    def add_resource(self, rg, spec):
        if self.connection_info.connection_type == ConnectionTypes.DIRECT:
            try:
                ret_value = self.gateway.add_resource(rg.resourceGroupId, spec)
                logger.writeError("PV:add_resource:ret_value={}", ret_value)
                return ret_value
            except Exception as e:
                logger.writeError(
                    f"An error occurred during add_resource call: {str(e)}"
                )
                raise ValueError(str(e))
        else:
            return self.gateway.add_resource(rg.resourceId, spec)

    @log_entry_exit
    def get_host_group_id(self, port, name):
        hg = self.hg_gateway.get_one_host_group(port, name)
        if hg is None:
            return None
        return hg.data.hostGroupId if hg.data else None

    @log_entry_exit
    def get_hg_by_id(self, hg_id):
        resp = self.hg_gateway.get_hg_by_id(hg_id)
        port = resp["portId"]
        name = resp["hostGroupName"]
        id = resp["hostGroupNumber"]
        return HostGroupInfo(port=port, name=name, id=id)

    @log_entry_exit
    def get_iscsi_id(self, port, name):
        spec = IscsiTargetFactSpec(ports=[port])
        iscsi_targets = self.iscsi_gateway.get_iscsi_targets(spec)
        logger.writeDebug("PV:get_iscsi_id:iscsi_targets={}", iscsi_targets)
        for iscsi_target in iscsi_targets.data:
            if iscsi_target.iscsiName == name:
                return iscsi_target.iscsiId
        return None

    @log_entry_exit
    def get_display_host_groups(self, host_group_ids):
        hg_list = []
        if host_group_ids is None:
            return hg_list
        for hg_id in host_group_ids:
            host_group_one = self.get_hg_by_id(hg_id)
            # host_group = host_group_one.data
            # logger.writeDebug("PV:get_display_host_groups:hg={}", host_group)
            if host_group_one is None:
                continue
            hg_list.append(host_group_one)

        return hg_list

    @log_entry_exit
    def get_display_iscsi_targets(self, iscsi_target_ids):
        hg_list = []
        if iscsi_target_ids is None:
            return hg_list
        iscsi_targets_data = None
        port_set = set()
        id_set = set()
        id_to_port = {}
        for hg_id in iscsi_target_ids:
            ss = hg_id.split(",")
            port = ss[0]
            port_set.add(port)
            id = ss[1]
            id_set.add(id)
            id_to_port[id] = port

            spec = IscsiTargetFactSpec(ports=[port])
            iscsi_targets = self.iscsi_gateway.get_iscsi_targets(spec)
            # logger.writeDebug("PV:get_display_iscsi_targets:iscsi_targets={}", iscsi_targets)
            iscsi_targets_data = iscsi_targets.data
        if iscsi_targets_data is None:
            return hg_list
        for iscsi_target in iscsi_targets_data:
            if str(iscsi_target.iscsiId) in id_set:
                hg_list.append(
                    HostGroupInfo(
                        port=iscsi_target.portId,
                        name=iscsi_target.iscsiName,
                        id=iscsi_target.iscsiId,
                    )
                )
                id_set.remove(str(iscsi_target.iscsiId))

        remaining = list(id_set)
        for id in remaining:
            hg_list.append(HostGroupInfo(port=id_to_port[id], name="", id=id))

        return hg_list

    @log_entry_exit
    def remove_resource(self, rg, spec):
        if self.connection_info.connection_type == ConnectionTypes.DIRECT:
            return self.gateway.remove_resource(rg.resourceGroupId, spec)
        else:
            self.update_spec_for_removal_gw(rg, spec)
            logger.writeDebug("PV:remove_resource:updated_spec={}", spec)
            if self.is_update_needed(spec):
                return self.gateway.remove_resource(rg.resourceId, spec)
            return None

    @log_entry_exit
    def is_update_needed(self, spec):
        if (
            (spec.ldevs is None or len(spec.ldevs) == 0)
            and (spec.parity_groups is None or len(spec.parity_groups) == 0)
            and (spec.ports is None or len(spec.ports) == 0)
            and (spec.host_groups is None or len(spec.host_groups) == 0)
            and (spec.iscsi_targets is None or len(spec.iscsi_targets) == 0)
            and (spec.storage_pool_ids is None or len(spec.storage_pool_ids) == 0)
            and (spec.nvm_subsystem_ids is None or len(spec.nvm_subsystem_ids) == 0)
        ):
            return False
        return True

    @log_entry_exit
    def update_spec_for_removal_gw(self, rg, spec):
        if spec.ldevs:
            if rg.volumes:
                spec.ldevs = list(set(rg.volumes) & set(spec.ldevs))
            else:
                spec.ldevs = []
        if spec.parity_groups:
            if rg.parityGroups:
                spec.parity_groups = list(
                    set(rg.parityGroups) & set(spec.parity_groups)
                )
            else:
                spec.parity_groups = []
        if spec.ports:
            if rg.ports:
                spec.ports = list(set(rg.ports) & set(spec.ports))
            else:
                spec.ports = []
        if spec.host_groups:
            if rg.hostGroups:
                logger.writeDebug(
                    "PV:update_spec_for_removal_gw:rg.hostGroups={}", rg.hostGroups
                )
                logger.writeDebug(
                    "PV:update_spec_for_removal_gw:rg.spec.host_groups={}",
                    spec.host_groups,
                )
                hgs_to_remove = []
                for hg in rg.hostGroups:
                    for spec_hg in spec.host_groups:
                        if hg.get("hostGroupName") == spec_hg.get("name"):
                            hgs_to_remove.append(spec_hg)

                spec.host_groups = hgs_to_remove
            else:
                spec.host_groups = []
        if spec.iscsi_targets:
            if rg.iscsiTargets:
                iscsi_targets_to_remove = []
                for iscsi in rg.iscsiTargets:
                    for iscsi_target in spec.iscsi_targets:
                        if iscsi.get("iscsiName") == iscsi_target.get("name"):
                            iscsi_targets_to_remove.append(iscsi_target)

                spec.iscsi_targets = iscsi_targets_to_remove
            else:
                spec.iscsi_targets = []
        if spec.storage_pool_ids:
            if rg.pools:
                spec.storage_pool_ids = list(set(rg.pools) & set(spec.storage_pool_ids))
            else:
                spec.storage_pool_ids = []
        return

    @log_entry_exit
    def delete_resource_group(self, resource_group, spec):
        if self.connection_info.connection_type == ConnectionTypes.DIRECT:
            return self.gateway.delete_resource_group(resource_group.resourceGroupId)
        else:
            resource_id = resource_group.resourceId
            return self.gateway.delete_resource_group(resource_id, spec)

    @log_entry_exit
    def delete_resource_group_force(self, resource_group):
        return self.gateway.delete_resource_group_force(resource_group)

    @log_entry_exit
    def handle_storage_pools(self):
        dp_pools = self.gateway.get_dp_pools()
        logger.writeDebug("PV:handle_storage_pools:dp_pools={}", dp_pools)
        hti_pools = self.gateway.get_hti_pools()
        logger.writeDebug("PV:handle_storage_pools:hti_pools={}", hti_pools)

        pool_ldevs = {}
        for dp in dp_pools:
            pool_id = dp["poolId"]
            first_ldev = dp["firstLdevId"]
            pool_ldevs[pool_id] = first_ldev

        logger.writeDebug("PV:handle_storage_pools:ldevs={}", pool_ldevs)

        for hti in hti_pools:
            pool_id = hti["poolId"]
            first_ldev = hti["firstLdevId"]
            pool_ldevs[pool_id] = first_ldev

        rg_id_pool = {}
        for pool_id, ldev_id in pool_ldevs.items():
            rg_id = self.gateway.get_rg_id_from_ldev_id(ldev_id)
            if rg_id in rg_id_pool:
                pool_ids = rg_id_pool[rg_id]
                pool_ids.append(pool_id)
            else:
                rg_id_pool[rg_id] = [pool_id]

        logger.writeDebug("PV:handle_storage_pools:rg_id_pool={}", rg_id_pool)
        return rg_id_pool
