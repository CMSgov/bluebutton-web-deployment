from typing import Dict, Any

try:
    from ..gateway.gateway_factory import GatewayFactory
    from ..common.hv_constants import GatewayClassTypes
    from ..common.uaig_utils import UAIGResourceID
    from ..common.hv_constants import ConnectionTypes
    from ..common.vsp_constants import VolumePayloadConst, DEFAULT_NAME_PREFIX
    from ..common.hv_log import Log
    from ..common.ansible_common import (
        log_entry_exit,
        convert_decimal_size_to_bytes,
    )
    from ..message.vsp_true_copy_msgs import VSPTrueCopyValidateMsg, TrueCopyFailedMsg
    from ..model.vsp_true_copy_models import (
        VSPTrueCopyPairInfoList,
    )
    from ..model.vsp_volume_models import CreateVolumeSpec


except ImportError:
    from gateway.gateway_factory import GatewayFactory
    from common.hv_constants import GatewayClassTypes
    from common.uaig_utils import UAIGResourceID
    from common.hv_constants import ConnectionTypes
    from common.vsp_constants import VolumePayloadConst, DEFAULT_NAME_PREFIX
    from common.hv_log import Log
    from common.ansible_common import (
        log_entry_exit,
        convert_decimal_size_to_bytes,
    )
    from message.vsp_true_copy_msgs import VSPTrueCopyValidateMsg, TrueCopyFailedMsg
    from model.vsp_true_copy_models import (
        VSPTrueCopyPairInfoList,
    )
    from model.vsp_volume_models import CreateVolumeSpec

logger = Log()


class VSPTrueCopyProvisioner:

    def __init__(self, connection_info, serial):
        self.gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_TRUE_COPY
        )
        self.vol_gw = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_VOLUME
        )
        self.cg_gw = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_COPY_GROUPS
        )
        self.connection_info = connection_info
        self.serial = serial
        self.gateway.set_storage_serial_number(serial)

    @log_entry_exit
    def get_all_replication_pairs(self, serial=None):
        return self.gateway.get_all_replication_pairs(self.serial)

    @log_entry_exit
    def get_tc_for_primary_vol_id(self, primary_vol_id):
        logger.writeDebug(f"PROV:60 :self.serial= {self.serial}")
        all_tc_pairs = self.gateway.get_all_true_copy_pairs(self.serial)
        for tc in all_tc_pairs.data:
            # logger.writeDebug(f"PROV:60 tc= {tc}")
            if hasattr(tc, "ldevId"):
                if tc.ldevId == primary_vol_id:
                    return tc
            if hasattr(tc, "primaryVolumeId"):
                if int(tc.primaryVolumeId) == int(primary_vol_id):
                    return tc
        return None

    def get_tc_for_secondary_vol_id(self, svol):
        logger.writeDebug(f"PROV:60 :self.serial= {self.serial}")
        all_tc_pairs = self.gateway.get_all_true_copy_pairs(self.serial)
        for tc in all_tc_pairs.data:
            logger.writeDebug(f"PROV:60 tc= {tc}")
            if hasattr(tc, "secondaryVolumeId"):
                if int(tc.secondaryVolumeId) == int(svol):
                    return tc
        return None

    @log_entry_exit
    def get_tc_by_cp_group_and_primary_vol_id(self, spec):
        tc = self.cg_gw.get_tc_by_cp_group_and_primary_vol_id(spec)
        logger.writeDebug(f"PROV:get_tc_by_cp_group_and_primary_vol_id:tc= {tc}")
        spec.secondary_storage_serial_number = self.gateway.get_secondary_serial(spec)
        return tc

    @log_entry_exit
    def get_true_copy_facts(self, spec=None, serial=None):
        tc_pairs = self.get_all_tc_pairs_direct(spec=spec)
        logger.writeDebug(f"PV:: pairs=  {tc_pairs}")
        if tc_pairs is None:
            return tc_pairs
        if spec is None:
            return tc_pairs
        else:
            ret_tc_pairs = self.apply_filters(tc_pairs, spec)
            return VSPTrueCopyPairInfoList(data=ret_tc_pairs)

    @log_entry_exit
    def get_all_tc_pairs_direct(self, serial=None, spec=None):
        if serial is None:
            serial = self.serial
        if spec is None:
            ret_list = self.gateway.get_all_true_copy_pairs(serial)
            logger.writeDebug(
                f"PROV:get_all_tc_pairs:ret_list= {ret_list} serial = {serial}"
            )
            return ret_list
        if self.connection_info.connection_type == ConnectionTypes.DIRECT:
            # First we check if there is a copy group name present in the spec
            spec.secondary_storage_serial_number = self.gateway.get_secondary_serial(
                spec
            )

            if (
                spec.copy_group_name
                and spec.copy_pair_name
                and spec.local_device_group_name
                and spec.remote_device_group_name
            ):
                return self.cg_gw.get_remote_copy_pair_by_id(spec)

            if spec.copy_group_name and spec.copy_pair_name:
                return self.cg_gw.get_remote_pairs_by_copy_group_and_copy_pair_name(
                    spec
                )

            if spec.copy_group_name:
                return self.cg_gw.get_remote_pairs_for_a_copy_group(spec)

            if spec.primary_volume_id:
                return self.cg_gw.get_remote_pairs_by_pvol(spec)

            if spec.secondary_volume_id:
                return self.cg_gw.get_remote_pairs_by_svol(spec)

            # ret_list = self.cg_gw.get_all_copy_pairs(spec)
            ret_list = self.cg_gw.get_all_remote_pairs_from_copy_groups(spec)
            return ret_list
            # return DirectCopyPairInfoList(data=ret_list)

    @log_entry_exit
    def apply_filters(self, tc_pairs, spec):
        result = tc_pairs
        if spec.primary_volume_id is not None:
            result = self.apply_filter_pvol(result, spec.primary_volume_id)
        if spec.secondary_volume_id is not None:
            result = self.apply_filter_svol(result, spec.secondary_volume_id)

        return result

    @log_entry_exit
    def apply_filter_pvol(self, tc_pairs, primary_vol_id):
        ret_val = []
        for tc in tc_pairs:
            if tc.pvolLdevId == primary_vol_id or tc.svolLdevId == primary_vol_id:
                ret_val.append(tc)
        return ret_val

    @log_entry_exit
    def apply_filter_svol(self, tc_pairs, secondary_vol_id):
        ret_val = []

        for tc in tc_pairs:
            if tc.svolLdevId == secondary_vol_id or tc.pvolLdevId == secondary_vol_id:
                ret_val.append(tc)
        return ret_val

    @log_entry_exit
    def get_tc_copypairs(self, pair):

        if isinstance(pair, list):
            return self.get_tc_copypairs_from_list(pair)

        tc_pairs = []

        logger.writeDebug("sng20241115 :pair={}", pair)
        copyPairs = pair.copyPairs
        if copyPairs is None:
            return

        for copyPair in copyPairs:
            if copyPair.replicationType == "TC":
                tc_pairs.append(copyPair)

        return tc_pairs

    @log_entry_exit
    def get_tc_copypairs_from_list(self, cgList):
        tc_pairs = []

        for cg in cgList:
            if cg is None:
                continue
            logger.writeDebug("sng20241115 :cg={}", cg)
            copyPairs = cg.copyPairs
            if copyPairs is None:
                continue

            for copyPair in copyPairs:
                if copyPair.replicationType == "TC":
                    tc_pairs.append(copyPair)

        return tc_pairs

    def get_tc_pair_by_pvol_new(self, copyPairs, volume_id):
        logger.writeDebug("sng20241115 :copyPairs={}", copyPairs)
        if copyPairs is None:
            return
        if not isinstance(copyPairs, list):
            copyPairs = [copyPairs]
        for copyPair in copyPairs:
            if copyPair.pvolLdevId == volume_id:
                # just return the first one for now
                logger.writeDebug("sng20241115 found copyPair={}", copyPair)
                return copyPair

    @log_entry_exit
    def get_replication_pair_by_id(self, pair_id):
        device_id = UAIGResourceID().storage_resourceId(self.serial)
        return self.gateway.get_replication_pair_by_id(device_id, pair_id)

    @log_entry_exit
    def delete_true_copy_pair(self, spec=None):
        self.connection_info.changed = False
        comment = None

        # tc_pair_id = "remoteStorageDeviceId,copyGroupName,localDeviceGroupName,remoteDeviceGroupName,copyPairName"
        # If we have both copy_group_name and copy_pair_name, we can delete the pair directly
        if spec.copy_group_name and spec.copy_pair_name:
            tc = self.cg_gw.get_remote_pairs_by_copy_group_and_copy_pair_name(spec)
            pair_id = self.gateway.delete_true_copy_pair_by_pair_id(spec)
            if spec.should_delete_svol is True:
                if tc is not None and len(tc) > 0:
                    for tc_pair in tc:
                        if tc_pair.copyPairName == spec.copy_pair_name:
                            spec.secondary_volume_id = tc_pair.svolLdevId
                rr_prov = RemoteReplicationHelperForSVol(
                    spec.secondary_connection_info, spec.secondary_storage_serial_number
                )
                rr_prov.delete_volume_and_all_mappings(spec.secondary_volume_id)
            self.connection_info.changed = True
            return pair_id, comment

        # Deleting TC by primary_volume_id is only supported for VSP One
        if spec.primary_volume_id:
            # secondary_storage_info = self.gateway.get_secondary_storage_info(spec.secondary_connection_info)
            # storage_model = secondary_storage_info["model"]
            storage_model = self.get_storage_model(spec)
            if "VSP One" not in storage_model:
                comment = VSPTrueCopyValidateMsg.DELETE_TC_BY_PRIMARY_VOLUME_ID_NOT_SUPPORTED.value.format(
                    storage_model
                )
                return None, comment
            else:
                comment = None
                if spec.copy_group_name:
                    copy_group = self.get_copy_group_by_name(spec)
                    logger.writeDebug(
                        f"PV:delete_true_copy_pair:copy_group={copy_group}"
                    )
                    if copy_group:
                        self.connection_info.changed = True
                        return (
                            self.gateway.delete_true_copy_pair_by_copy_group_and_pvol_id(
                                spec.primary_volume_id
                            ),
                            comment,
                        )
                    else:
                        comment = VSPTrueCopyValidateMsg.COPY_GROUP_NAME_NOT_FOUND.value.format(
                            spec.copy_group_name
                        )
                        return None, comment
                else:
                    self.connection_info.changed = True
                    return (
                        self.gateway.delete_true_copy_pair_by_primary_volume_id(
                            self.cg_gw, spec
                        ),
                        comment,
                    )

    @log_entry_exit
    def get_copy_group_by_name(self, spec):
        return self.cg_gw.get_copy_group_by_name(spec)

    @log_entry_exit
    def get_storage_model(self, spec):
        secondary_storage_info = self.gateway.get_secondary_storage_info(
            spec.secondary_connection_info
        )
        storage_model = secondary_storage_info["model"]
        return storage_model

    @log_entry_exit
    def resync_true_copy_pair(self, spec=None):
        tc = None

        pair_id = None
        # if we have copy_group_name and copy_pair_name, we can directly resync the
        # pair and return the pair information
        if spec.copy_group_name and spec.copy_pair_name:
            tc = self.cg_gw.get_remote_pairs_by_copy_group_and_copy_pair_name(spec)
            if (
                tc is not None
                and len(tc) > 0
                and tc[0].svolStatus == "PAIR"
                and tc[0].pvolStatus == "PAIR"
            ):
                return tc[0]
            else:
                pair_id = self.gateway.resync_true_copy_pair(spec)
                logger.writeDebug(f"PV:resync_true_copy_pair: pair_id=  {pair_id}")
                if pair_id:
                    pair = self.cg_gw.get_one_copy_pair_by_id(
                        pair_id, spec.secondary_connection_info
                    )
                    self.connection_info.changed = True
                    return pair
        if spec.primary_volume_id:
            if spec.copy_group_name:
                copy_group = self.get_copy_group_by_name(spec)
                logger.writeDebug(f"PV:delete_true_copy_pair:copy_group={copy_group}")
                if copy_group:
                    self.connection_info.changed = True
                    pair_id = (
                        self.gateway.resync_true_copy_pair_by_copy_group_and_pvol_id(
                            self.cg_gw, spec
                        )
                    )
                else:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_RESYNC_FAILED.value
                        + VSPTrueCopyValidateMsg.COPY_GROUP_NAME_NOT_FOUND.value.format(
                            spec.copy_group_name
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)
            else:
                storage_model = self.get_storage_model(spec)
                if "VSP One" not in storage_model:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_RESYNC_FAILED.value
                        + VSPTrueCopyValidateMsg.RESYNC_TC_BY_PRIMARY_VOLUME_ID_NOT_SUPPORTED.value.format(
                            storage_model
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)
                else:
                    self.connection_info.changed = True
                    pair_id = self.gateway.resync_true_copy_pair_by_primary_volume_id(
                        self.cg_gw, spec
                    )
        if pair_id is None:
            err_msg = (
                TrueCopyFailedMsg.PAIR_RESYNC_FAILED.value
                + VSPTrueCopyValidateMsg.NO_TC_PAIR_FOUND_FOR_INPUTS.value
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)

        pair = self.cg_gw.get_one_copy_pair_by_id(
            pair_id, spec.secondary_connection_info
        )
        self.connection_info.changed = True
        return pair

    @log_entry_exit
    def swap_resync_true_copy_pair(self, spec=None):
        tc = None
        pair_id = None
        # if we have copy_group_name and copy_pair_name, we directly swap_resync the
        # pair and return the pair information
        if spec.copy_group_name and spec.copy_pair_name:
            tc = self.cg_gw.get_remote_pairs_by_copy_group_and_copy_pair_name(spec)
            if (
                tc is not None
                and len(tc) > 0
                and tc[0].svolStatus == "PAIR"
                and tc[0].pvolStatus == "PAIR"
            ):
                return tc[0]
            else:
                pair_id = self.gateway.swap_resync_true_copy_pair(spec)
                logger.writeDebug(f"PV:swap_resync_true_copy_pair: pair_id=  {pair_id}")
                if pair_id:
                    pair = self.cg_gw.get_one_copy_pair_by_id(
                        pair_id, spec.secondary_connection_info
                    )
                    self.connection_info.changed = True
                    return pair

        if spec.primary_volume_id:
            if spec.copy_group_name:
                copy_group = self.get_copy_group_by_name(spec)
                if copy_group:
                    self.connection_info.changed = True
                    pair_id = self.gateway.swap_resync_true_copy_pair_by_copy_group_and_pvol_id(
                        self.cg_gw, spec
                    )
                else:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_SWAP_RESYNC_FAILED.value
                        + VSPTrueCopyValidateMsg.COPY_GROUP_NAME_NOT_FOUND.value.format(
                            spec.copy_group_name
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)
            else:
                storage_model = self.get_storage_model(spec)
                if "VSP One" not in storage_model:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_SWAP_RESYNC_FAILED.value
                        + VSPTrueCopyValidateMsg.RESYNC_TC_BY_PRIMARY_VOLUME_ID_NOT_SUPPORTED.value.format(
                            storage_model
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)
                else:
                    self.connection_info.changed = True
                    pair_id = (
                        self.gateway.swap_resync_true_copy_pair_by_primary_volume_id(
                            self.cg_gw, spec
                        )
                    )
        if pair_id is None:
            err_msg = (
                TrueCopyFailedMsg.PAIR_SWAP_RESYNC_FAILED.value
                + VSPTrueCopyValidateMsg.NO_TC_PAIR_FOUND_FOR_INPUTS.value
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)
        # DO NOT NEED THIS FUNCTION AS WE ARE NOW DIRECTLY RUNNING FROM SECONDARY
        # swap_pair_id =  self.gateway.swap_resync_true_copy_pair(spec)
        # pair_id = self.gateway.get_pair_id_from_swap_pair_id(swap_pair_id, spec.secondary_connection_info)
        # logger.writeDebug(f"PV:swap_resync_true_copy_pair: swap_pair_id = {swap_pair_id} pair_id = {pair_id}")
        pair = self.cg_gw.get_one_copy_pair_by_id(
            pair_id, spec.secondary_connection_info
        )
        self.connection_info.changed = True
        return pair

    @log_entry_exit
    def split_true_copy_pair(self, spec=None):
        tc = None
        pair_id = None
        if spec.copy_group_name and spec.copy_pair_name:
            # if we have copy_group_name and copy_pair_name, we directly split the
            # pair and return the pair information
            tc = self.cg_gw.get_remote_pairs_by_copy_group_and_copy_pair_name(spec)
            logger.writeDebug(f"PV:split_true_copy_pair: tc=  {tc}")
            if (
                tc is not None
                and len(tc) > 0
                and tc[0].svolStatus == "SSUS"
                and tc[0].pvolStatus == "PSUS"
            ):
                return tc[0]
            else:
                pair_id = self.gateway.split_true_copy_pair(spec)
                logger.writeDebug(f"PV:split_true_copy_pair: pair_id=  {pair_id}")
                if pair_id:
                    pair = self.cg_gw.get_one_copy_pair_by_id(
                        pair_id, spec.secondary_connection_info
                    )
                    self.connection_info.changed = True
                    return pair

        if spec.primary_volume_id:
            if spec.copy_group_name:
                copy_group = self.get_copy_group_by_name(spec)
                logger.writeDebug(f"PV:delete_true_copy_pair:copy_group={copy_group}")
                if copy_group:
                    self.connection_info.changed = True
                    pair_id = (
                        self.gateway.split_true_copy_pair_by_copy_group_and_pvol_id(
                            self.cg_gw, spec
                        )
                    )
                else:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_SPLIT_FAILED.value
                        + VSPTrueCopyValidateMsg.COPY_GROUP_NAME_NOT_FOUND.value.format(
                            spec.copy_group_name
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)

            else:
                storage_model = self.get_storage_model(spec)
                if "VSP One" not in storage_model:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_SPLIT_FAILED.value
                        + VSPTrueCopyValidateMsg.SPLIT_TC_BY_PRIMARY_VOLUME_ID_NOT_SUPPORTED.value.format(
                            storage_model
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)
                else:
                    self.connection_info.changed = True
                    pair_id = self.gateway.split_true_copy_pair_by_primary_volume_id(
                        self.cg_gw, spec
                    )
        if pair_id is None:
            err_msg = (
                TrueCopyFailedMsg.PAIR_SPLIT_FAILED.value
                + VSPTrueCopyValidateMsg.NO_TC_PAIR_FOUND_FOR_INPUTS.value
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)
        pair = self.cg_gw.get_one_copy_pair_by_id(
            pair_id, spec.secondary_connection_info
        )
        self.connection_info.changed = True
        return pair

    @log_entry_exit
    def swap_split_true_copy_pair(self, spec=None):
        tc = None

        pair_id = None
        # if we have copy_group_name and copy_pair_name, we directly swap_split the
        # pair and return the pair information
        if spec.copy_group_name and spec.copy_pair_name:
            tc = self.cg_gw.get_remote_pairs_by_copy_group_and_copy_pair_name(spec)
            if tc:
                logger.writeDebug(f"PV:swap_split_true_copy_pair: tc=  {tc}")
            if (
                tc is not None
                and len(tc) > 0
                and tc[0].svolStatus == "SSWS"
                and tc[0].pvolStatus == "PSUS"
            ):
                return tc[0]
            else:
                pair_id = self.gateway.swap_split_true_copy_pair(spec)
                logger.writeDebug(f"PV:swap_split_true_copy_pair: pair_id=  {pair_id}")
                if pair_id:
                    pair = self.cg_gw.get_one_copy_pair_by_id(
                        pair_id, spec.secondary_connection_info
                    )
                    self.connection_info.changed = True
                    return pair

        if spec.primary_volume_id:
            if spec.copy_group_name:
                copy_group = self.get_copy_group_by_name(spec)
                logger.writeDebug(f"PV:delete_true_copy_pair:copy_group={copy_group}")
                if copy_group:
                    self.connection_info.changed = True
                    pair_id = self.gateway.swap_split_true_copy_pair_by_copy_group_and_pvol_id(
                        self.cg_gw, spec
                    )
                else:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_SWAP_SPLIT_FAILED.value
                        + VSPTrueCopyValidateMsg.COPY_GROUP_NAME_NOT_FOUND.value.format(
                            spec.copy_group_name
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)
            else:
                storage_model = self.get_storage_model(spec)
                if "VSP One" not in storage_model:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_SWAP_SPLIT_FAILED.value
                        + VSPTrueCopyValidateMsg.SPLIT_TC_BY_PRIMARY_VOLUME_ID_NOT_SUPPORTED.value.format(
                            storage_model
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)
                else:
                    self.connection_info.changed = True
                    pair_id = (
                        self.gateway.swap_split_true_copy_pair_by_primary_volume_id(
                            self.cg_gw, spec
                        )
                    )
        if pair_id is None:
            err_msg = (
                TrueCopyFailedMsg.PAIR_SWAP_SPLIT_FAILED.value
                + VSPTrueCopyValidateMsg.NO_TC_PAIR_FOUND_FOR_INPUTS.value
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)
        # swap_pair_id =  self.gateway.swap_split_true_copy_pair(spec)
        # pair_id = self.gateway.get_pair_id_from_swap_pair_id(swap_pair_id, spec.secondary_connection_info)
        # logger.writeDebug(f"PV:swap_resync_true_copy_pair: swap_pair_id = {swap_pair_id} pair_id = {pair_id}")

        pair = self.cg_gw.get_one_copy_pair_by_id(
            pair_id, spec.secondary_connection_info
        )
        self.connection_info.changed = True
        return pair

    @log_entry_exit
    def is_resize_needed(self, volume_data, spec):
        size_in_bytes = convert_decimal_size_to_bytes(spec.new_volume_size)
        if volume_data.blockCapacity > size_in_bytes:
            logger.writeDebug(
                "PV:resize_true_copy_copy_pair: Shrink/reduce volume size is not supported."
            )
            return False

        expand_val = size_in_bytes - (
            volume_data.blockCapacity if volume_data.blockCapacity else 0
        )
        if expand_val > 0:
            return True
        return False

    @log_entry_exit
    def resize_true_copy_copy_pair(self, spec=None):
        tc = None
        pair_id = None
        if spec.copy_group_name and spec.copy_pair_name:
            tc = self.cg_gw.get_remote_pairs_by_copy_group_and_copy_pair_name(spec)
            logger.writeDebug(
                f"PV:resize_true_copy_copy_pair: tc= {tc} len _tc= {len(tc)}"
            )
            if tc is not None and len(tc) > 0:
                pvol_id = tc[0].pvolLdevId
                pvol_data = self.vol_gw.get_volume_by_id(pvol_id)
                if pvol_data is None:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_RESIZE_FAILED.value
                        + VSPTrueCopyValidateMsg.NO_PRIMARY_VOLUME_FOUND.value.format(
                            spec.primary_volume_id
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)

                if pvol_data.emulationType == "NOT DEFINED":
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_RESIZE_FAILED.value
                        + VSPTrueCopyValidateMsg.INVALID_EMULATION_TYPE.value.format(
                            pvol_data.emulationType
                        )
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)

                resize_needed = self.is_resize_needed(pvol_data, spec)
                if resize_needed is False:
                    err_msg = (
                        TrueCopyFailedMsg.PAIR_RESIZE_FAILED.value
                        + VSPTrueCopyValidateMsg.REDUCE_VOLUME_SIZE_NOT_SUPPORTED.value
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)

                else:
                    pair_id = self.gateway.resize_true_copy_pair(tc[0], spec)
                    logger.writeDebug(
                        f"PV:resize_true_copy_copy_pair: pair_id=  {pair_id}"
                    )
                    pair = self.gateway.get_replication_pair(spec)
                    self.connection_info.changed = True
                    return pair
            else:
                err_msg = (
                    TrueCopyFailedMsg.PAIR_RESIZE_FAILED.value
                    + VSPTrueCopyValidateMsg.NO_TC_PAIR_FOUND_FOR_INPUTS.value
                )
                logger.writeError(err_msg)
                raise ValueError(err_msg)

    @log_entry_exit
    def create_true_copy(self, spec) -> Dict[str, Any]:
        tc_exits = self.get_tc_by_cp_group_and_primary_vol_id(spec)
        if tc_exits:
            return tc_exits
        copy_group = self.get_copy_group_by_name(spec)
        if copy_group is None:
            spec.is_new_group_creation = True
        else:
            spec.is_new_group_creation = False

        pvol = self.get_volume_by_id(spec.primary_volume_id)
        logger.writeDebug(f"PV:create_true_copy: pvol = {pvol}")
        if pvol is None:
            err_msg = (
                TrueCopyFailedMsg.PAIR_CREATION_FAILED.value
                + VSPTrueCopyValidateMsg.NO_PRIMARY_VOLUME_FOUND.value.format(
                    spec.primary_volume_id
                )
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)

        if pvol.emulationType == "NOT DEFINED":
            err_msg = (
                TrueCopyFailedMsg.PAIR_CREATION_FAILED.value
                + VSPTrueCopyValidateMsg.INVALID_EMULATION_TYPE.value.format(
                    str(pvol.emulationType)
                )
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)
        secondary_connection_info = spec.secondary_connection_info
        secondary_connection_info.connection_type = ConnectionTypes.DIRECT
        rr_prov = RemoteReplicationHelperForSVol(
            secondary_connection_info, spec.secondary_storage_serial_number
        )
        secondary_vol_id = None
        try:
            if spec.secondary_nvm_subsystem is not None:
                secondary_vol_id = rr_prov.get_secondary_volume_id_when_nvme(pvol, spec)
            elif spec.secondary_iscsi_targets is not None:
                secondary_vol_id = rr_prov.get_secondary_volume_id(pvol, spec, True)
            else:
                secondary_vol_id = rr_prov.get_secondary_volume_id(pvol, spec, False)
            spec.secondary_volume_id = secondary_vol_id
            spec.is_data_reduction_force_copy = pvol.isDataReductionShareEnabled
            result = self.gateway.create_true_copy(spec)
            logger.writeDebug(f"create_true_copy: {result}")
            pair = self.cg_gw.get_one_copy_pair_by_id(
                result, spec.secondary_connection_info
            )
            self.connection_info.changed = True
            return pair
        except Exception as ex:
            # if the TC creation fails, delete the secondary volume if it was created
            if secondary_vol_id:
                if spec.secondary_nvm_subsystem is not None:
                    rr_prov.delete_volume_when_nvme(
                        secondary_vol_id,
                        pvol.nvmSubsystemId,
                        spec.secondary_nvm_subsystem,
                        pvol.namespaceId,
                    )
                    rr_prov.delete_volume(secondary_vol_id)
            err_msg = TrueCopyFailedMsg.PAIR_CREATION_FAILED.value + str(ex)
            logger.writeError(err_msg)
            raise ValueError(err_msg)

    @log_entry_exit
    def get_volume_by_id(self, primary_volume_id):

        volume = self.vol_gw.get_volume_by_id(primary_volume_id)
        # return vol_gw.get_volume_by_id(device_id, primary_volume_id)
        logger.writeDebug(f"PROV:get_volume_by_id:volume: {volume}")

        return volume


class RemoteReplicationHelperForSVol:

    DEFAULT_HOSTGROUP_NAME = "ANSIBLE_DEFAULT_HOSTGROUP"
    DEFAULT_HOST_MODE = "VMWARE_EXTENSION"  # "STANDARD"

    def __init__(self, connection_info, serial):
        self.hg_gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_HOST_GROUP
        )
        self.sp_gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.STORAGE_PORT
        )
        self.vol_gateway = GatewayFactory.get_gateway(
            connection_info, GatewayClassTypes.VSP_VOLUME
        )
        if connection_info.connection_type.lower() == ConnectionTypes.DIRECT:
            self.nvme_gateway = GatewayFactory.get_gateway(
                connection_info, GatewayClassTypes.VSP_NVME_SUBSYSTEM
            )
            self.iscsi_gateway = GatewayFactory.get_gateway(
                connection_info, GatewayClassTypes.VSP_ISCSI_TARGET
            )
        self.connection_info = connection_info
        self.serial = serial
        self.hg_gateway.set_serial(serial)
        self.sp_gateway.set_serial(serial)
        self.vol_gateway.set_serial(serial)

    @log_entry_exit
    def delete_volume(self, secondary_vol_id, volume=None):
        if volume is None:
            volume = self.vol_gateway.get_volume_by_id(secondary_vol_id)
        if volume.ports is not None and len(volume.ports) > 0:
            for port in volume.ports:
                logger.writeDebug("PROV:delete_volume:port = {}", port)
                self.vol_gateway.delete_lun_path(port)

        force_execute = (
            True
            if volume.dataReductionMode
            and volume.dataReductionMode.lower() != VolumePayloadConst.DISABLED
            else None
        )
        try:
            self.vol_gateway.delete_volume(secondary_vol_id, force_execute)
            self.connection_info.changed = False
            return
        except Exception as e:
            err_msg = TrueCopyFailedMsg.SEC_VOLUME_DELETE_FAILED.value + str(e)
            logger.writeError(err_msg)
            raise ValueError(err_msg)

    @log_entry_exit
    def select_secondary_volume_id(self, pvol_id, spec=None):
        if spec is None:
            free_vol_info = self.vol_gateway.get_free_ldev_matching_pvol(pvol_id)
            logger.writeDebug(
                "PROV:select_secondary_volume_id:free_vol_info = {}", free_vol_info
            )
            return free_vol_info.data[0].ldevId
        else:
            if (
                spec.begin_secondary_volume_id is not None
                and spec.end_secondary_volume_id is not None
            ):
                # Select the first free volume in the range
                free_vol_info = self.vol_gateway.get_free_ldev_matching_svol_range(
                    spec.begin_secondary_volume_id, spec.end_secondary_volume_id
                )
                logger.writeDebug(
                    "PROV:select_secondary_volume_id:for range:free_vol_info = {}",
                    free_vol_info,
                )
                if free_vol_info.data:
                    for free_vol in free_vol_info.data:
                        if free_vol.resourceGroupId == 0:
                            if (
                                free_vol.ldevId > spec.begin_secondary_volume_id
                                and free_vol.ldevId < spec.end_secondary_volume_id
                            ):
                                return free_vol.ldevId
                            else:
                                logger.writeDebug(
                                    "PROV:select_secondary_volume_id:free_vol = {}",
                                    free_vol,
                                )

                err_msg = VSPTrueCopyValidateMsg.NO_FREE_LDEV_IN_RANGE.value.format(
                    spec.begin_secondary_volume_id, spec.end_secondary_volume_id
                )
                logger.writeError(err_msg)
                raise ValueError(err_msg)
            else:
                # If no range is specified, get the first free volume
                free_vol_info = self.vol_gateway.get_free_ldev_matching_pvol(pvol_id)
                logger.writeDebug(
                    "PROV:select_secondary_volume_id:free_vol_info = {}", free_vol_info
                )
                if free_vol_info.data:
                    return free_vol_info.data[0].ldevId
                else:
                    err_msg = VSPTrueCopyValidateMsg.NO_FREE_LDEV_FOUND.value.format(
                        pvol_id
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)

    @log_entry_exit
    def get_secondary_volume_id(self, vol_info, spec, is_iscsi=False):
        logger.writeDebug("PROV:get_secondary_volume_id:vol_info = {}", vol_info)

        # check if pvol is iscsi
        if is_iscsi:
            if vol_info.ports is not None and len(vol_info.ports) > 0:
                port = vol_info.ports[0]
                if isinstance(port, dict) and port.get("hostGroupNumber") is None:
                    err_msg = VSPTrueCopyValidateMsg.PVOL_ISCSI_MISSING.value.format(
                        vol_info.ldevId
                    )
                    logger.writeError(err_msg)
                    raise ValueError(err_msg)

        # Before creating the secondary volume check if secondary hostgroup exists
        if is_iscsi:
            host_group = self.get_secondary_hostgroup(
                spec.secondary_iscsi_targets, is_iscsi
            )
        else:
            host_group = self.get_secondary_hostgroup(spec.secondary_hostgroups)
        if host_group is None:
            err_msg = None
            if is_iscsi:
                err_msg = VSPTrueCopyValidateMsg.NO_REMOTE_ISCSI_FOUND.value.format(
                    spec.secondary_iscsi_targets[0].name,
                    spec.secondary_iscsi_targets[0].port,
                )
            else:
                err_msg = VSPTrueCopyValidateMsg.NO_REMOTE_HG_FOUND.value.format(
                    spec.secondary_hostgroups[0].name, spec.secondary_hostgroups[0].port
                )
            logger.writeError(err_msg)
            raise ValueError(err_msg)

        svol_id = self.select_secondary_volume_id(vol_info.ldevId, spec)
        secondary_pool_id = spec.secondary_pool_id
        sec_vol_spec = CreateVolumeSpec()
        sec_vol_spec.pool_id = secondary_pool_id

        sec_vol_spec.size = self.get_size_from_byte_format_capacity(
            vol_info.byteFormatCapacity
        )
        sec_vol_spec.capacity_saving = vol_info.dataReductionMode
        if vol_info.dataReductionMode != VolumePayloadConst.DISABLED:
            sec_vol_spec.is_compression_acceleration_enabled = (
                vol_info.isCompressionAccelerationEnabled
            )

        sec_vol_id = self.vol_gateway.create_volume(sec_vol_spec)

        # the name change is done in the update_volume method
        if vol_info.label is not None and vol_info.label != "":
            sec_vol_name = vol_info.label
        else:
            sec_vol_name = f"{DEFAULT_NAME_PREFIX}-{vol_info.ldevId}"

        try:
            self.vol_gateway.change_volume_settings(sec_vol_id, label=sec_vol_name)
            if is_iscsi:
                self.iscsi_gateway.add_luns_to_iscsi_target(
                    host_group,
                    [sec_vol_id],
                    None,
                    (
                        spec.secondary_iscsi_targets[0].lun_id
                        if spec.secondary_iscsi_targets[0].lun_id is not None
                        else None
                    ),
                )
            else:
                self.hg_gateway.add_luns_to_host_group(
                    host_group,
                    [sec_vol_id],
                    (
                        spec.secondary_hostgroups[0].lun_id
                        if spec.secondary_hostgroups[0].lun_id is not None
                        else None
                    ),
                )
        except Exception as ex:
            err_msg = TrueCopyFailedMsg.SEC_VOLUME_OPERATION_FAILED.value + str(ex)
            logger.writeError(err_msg)
            # if setting the volume name fails, delete the secondary volume
            # if attaching the volume to the host group fails, delete the secondary volume
            self.delete_volume(sec_vol_id)
            raise ValueError(err_msg)

        logger.writeDebug(
            "PROV:get_secondary_volume_id:sec_vol_name = {}", sec_vol_name
        )
        # logger.writeDebug("PROV:get_secondary_volume_id:spec = {}", spec)
        # logger.writeDebug("PROV:get_secondary_volume_id:host_group = {}", host_group)

        # self.hg_gateway.add_luns_to_host_group(host_group, [sec_vol_id])
        return sec_vol_id

    @log_entry_exit
    def get_secondary_hostgroup(self, secondary_hostgroup, is_iscsi=False):
        hostgroups_list = self.validate_secondary_hostgroups(
            secondary_hostgroup, is_iscsi
        )
        logger.writeDebug(
            "PROV:get_secondary_hostgroup:hostgroups_list = {}", hostgroups_list
        )
        return hostgroups_list[0]

    @log_entry_exit
    def parse_hostgroup(self, hostgroup):
        hostgroup.port = hostgroup.portId
        return hostgroup

    @log_entry_exit
    def get_size_from_byte_format_capacity(self, byte_format):
        logger.writeDebug(
            "PROV:get_size_from_byte_format_capacity:hgs = {}", byte_format
        )
        value = byte_format.split(" ")[0]
        unit = byte_format.split(" ")[1]
        int_value = value.split(".")[0]
        return f"{int_value}{unit}"

    def get_secondary_hostgroups_payload(self, secondary_hostgroups):
        hostgroups_list = self.validate_secondary_hostgroups(secondary_hostgroups)
        payload = self.create_secondary_hgs_payload(hostgroups_list)
        return payload

    def validate_secondary_hostgroups(self, secondary_hgs, is_iscsi=False):
        logger.writeDebug("PROV:validate_secondary_hostgroups:hgs = {}", secondary_hgs)
        logger.writeDebug(
            "PROV:validate_secondary_hostgroups:connection_info = {}",
            self.connection_info,
        )

        hostgroup_list = []
        for hg in secondary_hgs:
            hostgroup = self.get_hg_by_name_port(hg.name, hg.port, is_iscsi)
            if hostgroup is None:
                err_msg = None
                if is_iscsi:
                    err_msg = VSPTrueCopyValidateMsg.NO_REMOTE_ISCSI_FOUND.value.format(
                        hg.name, hg.port
                    )
                else:
                    err_msg = VSPTrueCopyValidateMsg.NO_REMOTE_HG_FOUND.value.format(
                        hg.name, hg.port
                    )
                logger.writeError(err_msg)
                raise ValueError(err_msg)

            hostgroup_list.append(hostgroup)

        logger.writeDebug(
            f"PROV:validate_secondary_hostgroups:hostgroup_list = {hostgroup_list}"
        )

        for hg in secondary_hgs:
            port = self.get_port_by_name(hg.port)
            if port is None:
                err_msg = VSPTrueCopyValidateMsg.SEC_PORT_NOT_FOUND.value.format(
                    hg.port
                )
                logger.writeError(err_msg)
                raise ValueError(err_msg)

            # if port.portInfo["portType"] != "FIBRE" or port.portInfo["mode"] != "SCSI":
            #     raise ValueError(VSPTrueCopyValidateMsg.WRONG_PORT_PROVIDED.value.format(port.resourceId, port.portInfo["portType"], port.portInfo["mode"]))

        return hostgroup_list

    @log_entry_exit
    def get_hg_by_name_port(self, name, port, is_iscsi=False):
        hg = {}
        if is_iscsi is True:
            hg = self.iscsi_gateway.get_one_iscsi_target(port, name)
        else:
            hg = self.hg_gateway.get_one_host_group(port, name)
        logger.writeDebug("PROV:get_hg_by_name_port:hgs = {}", hg)
        if hg is None:
            return None
        return hg.data

    @log_entry_exit
    def get_port_by_name(self, port):
        return self.sp_gateway.get_single_storage_port(port)

    @log_entry_exit
    def create_secondary_hgs_payload(self, hgs):
        ret_list = []
        for hg in hgs:
            item = {}
            item["hostGroupID"] = hg.hostGroupInfo["hostGroupId"]
            item["name"] = hg.hostGroupInfo["hostGroupName"]
            item["port"] = hg.hostGroupInfo["port"]
            item["resourceGroupID"] = hg.hostGroupInfo["resourceGroupId"] or 0
            ret_list.append(item)
        return ret_list

    @log_entry_exit
    def get_secondary_volume_id_when_nvme(self, vol_info, spec):
        logger.writeDebug(
            "PROV:get_secondary_volume_id_when_nvme:vol_info = {}", vol_info
        )
        # capture namespace ID
        pvolNameSpaceId = vol_info.namespaceId
        # pvolNvmSubsystemId = vol_info.nvmSubsystemId

        if pvolNameSpaceId is None or pvolNameSpaceId == "":
            err_msg = VSPTrueCopyValidateMsg.PVOL_NAMESPACE_MISSING.value.format(
                vol_info.ldevId
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)

        logger.writeDebug("PROV: nvmesubsystem spec = {}", spec.secondary_nvm_subsystem)
        # Before creating the secondary volume check if secondary hostgroup exists
        # host_group = self.get_secondary_hostgroup(spec.secondary_hostgroups)
        nvme_subsystem = self.get_nvmesubsystem_by_name(spec.secondary_nvm_subsystem)
        if nvme_subsystem is None:
            err_msg = VSPTrueCopyValidateMsg.NO_REMOTE_NVME_FOUND.value.format(
                spec.secondary_nvm_subsystem.name
            )
            logger.writeError(err_msg)
            raise ValueError(err_msg)

        # if int(nvme_subsystem.nvmSubsystemId) != int(pvolNvmSubsystemId):
        #     err_msg = VSPTrueCopyValidateMsg.NVMSUBSYSTEM_DIFFER.value.format(
        #         nvme_subsystem.nvmSubsystemId, pvolNvmSubsystemId
        #     )
        #     logger.writeError(err_msg)
        #     raise ValueError(err_msg)

        svol_id = self.select_secondary_volume_id(vol_info.ldevId, spec)
        secondary_pool_id = spec.secondary_pool_id
        sec_vol_spec = CreateVolumeSpec()
        sec_vol_spec.pool_id = secondary_pool_id

        sec_vol_spec.size = self.get_size_from_byte_format_capacity(
            vol_info.byteFormatCapacity
        )
        sec_vol_spec.capacity_saving = vol_info.dataReductionMode
        sec_vol_spec.ldev_id = svol_id

        sec_vol_id = self.vol_gateway.create_volume(sec_vol_spec)

        # the name change is done in the update_volume method
        if vol_info.label is not None and vol_info.label != "":
            sec_vol_name = vol_info.label
        else:
            sec_vol_name = f"{DEFAULT_NAME_PREFIX}-{vol_info.ldevId}"

        try:
            self.vol_gateway.change_volume_settings(sec_vol_id, label=sec_vol_name)
            ns_id = self.create_namespace_for_svol(
                nvme_subsystem.nvmSubsystemId, sec_vol_id, None
            )
            ns_id = ns_id.split(",")[-1]
            self.create_namespace_paths(
                nvme_subsystem.nvmSubsystemId,
                ns_id,
                spec.secondary_nvm_subsystem,
            )
        except Exception as ex:
            err_msg = TrueCopyFailedMsg.SEC_VOLUME_OPERATION_FAILED.value + str(ex)
            logger.writeError(err_msg)
            # if setting the volume name fails, delete the secondary volume
            # if attaching the volume to the host group fails, delete the secondary volume
            self.delete_volume_when_nvme(
                sec_vol_id,
                nvme_subsystem.nvmSubsystemId,
                spec.secondary_nvm_subsystem,
                pvolNameSpaceId,
            )
            raise ValueError(err_msg)

        logger.writeDebug(
            "PROV:get_secondary_volume_id:sec_vol_name = {}", sec_vol_name
        )
        # logger.writeDebug("PROV:get_secondary_volume_id:spec = {}", spec)
        # logger.writeDebug("PROV:get_secondary_volume_id:host_group = {}", host_group)

        # self.hg_gateway.add_luns_to_host_group(host_group, [sec_vol_id])
        return sec_vol_id

    @log_entry_exit
    def get_nvmesubsystem_by_name(self, nvmsubsystem):
        nvme_subsystems = self.nvme_gateway.get_nvme_subsystems()
        for nvme in nvme_subsystems.data:
            if nvme.nvmSubsystemName == nvmsubsystem.name:
                logger.writeDebug("PROV:get_nvmesubsystem_by_name:nvme = {}", nvme)
                return nvme
        return None

    @log_entry_exit
    def create_namespace_for_svol(self, nvm_subsystem_id, ldev_id, ns_id):
        ns_id = self.nvme_gateway.create_namespace(nvm_subsystem_id, ldev_id, ns_id)
        logger.writeDebug("PROV:add_svol_to_nvmesubsystem:ns_id = {}", ns_id)
        return ns_id

    @log_entry_exit
    def create_namespace_paths(self, nvm_subsystem_id, namespace_id, nvmsubsystem):
        nqns = []
        if nvmsubsystem.paths is not None:
            nqns = nvmsubsystem.paths
        else:
            host_nqns = self.nvme_gateway.get_host_nqns(nvm_subsystem_id)
            nqns = [nqn.hostNqn for nqn in host_nqns.data]

        for nqn in nqns:
            host_ns_path_id = self.nvme_gateway.set_host_namespace_path(
                nvm_subsystem_id, nqn, namespace_id
            )
            logger.writeDebug(
                "PROV:create_namespace_paths:host_ns_path_id = {}", host_ns_path_id
            )
        return None

    @log_entry_exit
    def delete_volume_when_nvme(
        self, secondary_vol_id, nvm_id, nvmsubsystem, namespaceId, volume=None
    ):
        if volume is None:
            volume = self.vol_gateway.get_volume_by_id(secondary_vol_id)
        if nvm_id is None:
            nvm_id = volume.nvmSubsystemId
        if namespaceId is None:
            namespaceId = volume.namespaceId
        nqns = []
        if nvmsubsystem is not None and nvmsubsystem.paths is not None:
            nqns = nvmsubsystem.paths
        else:
            host_nqns = self.nvme_gateway.get_host_nqns(nvm_id)
            nqns = [nqn.hostNqn for nqn in host_nqns.data]

        for nqn in nqns:
            self.nvme_gateway.delete_host_namespace_path(nvm_id, nqn, namespaceId)
        self.nvme_gateway.delete_namespace(nvm_id, namespaceId)
        force_execute = (
            True
            if volume.dataReductionMode
            and volume.dataReductionMode.lower() != VolumePayloadConst.DISABLED
            else None
        )
        try:
            self.vol_gateway.delete_volume(secondary_vol_id, force_execute)
            self.connection_info.changed = False
            return
        except Exception as e:
            err_msg = TrueCopyFailedMsg.SEC_VOLUME_DELETE_FAILED.value + str(e)
            logger.writeError(err_msg)
            raise ValueError(err_msg)

    @log_entry_exit
    def get_secondary_hg_payload(self, hg):
        ret_list = []
        item = {}
        item["hostGroupID"] = hg.hostGroupInfo["hostGroupId"]
        item["name"] = hg.hostGroupInfo["hostGroupName"]
        item["port"] = hg.hostGroupInfo["port"]
        item["resourceGroupID"] = hg.hostGroupInfo["resourceGroupId"] or 0
        ret_list.append(item)
        return ret_list

    @log_entry_exit
    def delete_volume_and_all_mappings(self, secondary_volume_id):
        logger.writeDebug(
            f"delete_svol_force: secondary_volume_id: {secondary_volume_id}"
        )
        volume = self.vol_gateway.get_volume_by_id(secondary_volume_id)
        if volume.namespaceId is not None:
            self.delete_volume_when_nvme(secondary_volume_id, None, None, None, volume)
        else:
            self.delete_volume(secondary_volume_id, volume)
