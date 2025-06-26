from enum import Enum


class VSPVolumeMessage(Enum):
    pass


class VSPVolValidationMsg(Enum):
    NOT_POOL_ID_OR_PARITY_ID = (
        "either pool_id or parity_group or external_parity_group should be provided."
    )
    LUN_REQUIRED = "ldev_id is required for absent state to delete."
    COUNT_VALUE = "The parameter 'count' must be a whole number greater than zero."
    END_LDEV_AND_COUNT = "Ambiguous parameters, count and end_ldev_id cannot co-exist."
    POOL_ID_OR_PARITY_ID = "pool_id or parity_group is mandatory for new ldev creation."
    SIZE_REQUIRED = "size is mandatory for new ldev creation."
    SIZE_INT_REQUIRED = (
        "provide integer value for the size with unit. e.g. 5GB, 2TB, etc."
    )
    VALID_SIZE = "size is less than actual volume size of the ldev, Please provide with more than the actual size."
    LDEV_ID_OUT_OF_RANGE = "ldev id is out of range to create, Please specify within the range of 0 to 65535."
    VLDEV_ID_OUT_OF_RANGE = (
        "vldev id is out of range, Please specify within the range of 0 to 65279."
    )
    MAX_LDEV_ID_OUT_OF_RANGE = (
        "ldev id is out of range, Please specify within the range of 0 to 65535."
    )
    START_LDEV_LESS_END = "end_ldev_id can't be less then start_ldev_id."
    BOTH_API_TOKEN_USER_DETAILS = (
        "either api_token or user credential is required, both can't be provided"
    )
    BOTH_PARITY_GRP_TIERING = (
        "Tiering policy is not applicable if volume is not dynamic pool"
    )
    VLDEVID_META_RSRC = "Volume is in meta resource, vldev_id is not applicable."
    NOT_API_TOKEN_USER_DETAILS = "api_token is required"
    DIRECT_API_TOKEN_ERROR = (
        "api_token should not be present when connection type is 'direct'"
    )
    VOLUME_NOT_FOUND = "Volume not found for the given ldev id {}"
    VOLUME_NOT_FOUND_BY_NAME = "Volume not found for the given ldev name {}"
    POOL_ID_PARITY_GROUP = "pool_id, parity_group and external_parity_group are mutually exclusive for volume creation. Please provide only one of them."
    POOL_ID_OR_PARITY_GROUP = (
        "Either pool id or parity group is required for volume creation."
    )
    BOTH_PARITY_GROUPS_SPECIFIED = "Both parity_group and external_parity_group are specified. Please provide only one of them."
    NO_FREE_LDEV = "No free ldevs available in the storage meta."
    PATH_EXIST = "A path is defined in the volume. Use force=true in the spec to delete a volume with a path."

    SUBSCRIBER_ID_NOT_NUMERIC = "subscriber_id should have only numeric values."

    NVM_SUBSYSTEM_DOES_NOT_EXIST = "NVM subsystem {} does not exist."
    CONTRADICT_INFO = "Contradicting information provided in the spec. Volume name does not exist in the system, and spec.state is set to remove_host_nqn."
    VOLUME_HAS_PATH = (
        "This ldev can't be deleted. It might be connected to host groups or "
        "might be added to the NVM Subsystem as a namespace. Use force=true to "
        "delete this ldev."
    )
    LDEV_NOT_FOUND_IN_NVM = "Did not find ldev_id {} in NVM subsystem {}."
    INVALID_LDEV_NAME_LEN = "Invalid volume name length. Number of characters in volume name should be between 1 to 24."
    VOL_NOT_FOUND = "Volume not found."
    QUERY_NOT_LIST = "Query must be provided as a list of strings."
    INVALID_QUERY = "Invalid query provided: {}. Supported values are {}."
    INVALID_CAPACITY_SAVING = (
        "Invalid capacity_saving value '{}' provided. Supported values are {}."
    )
    INVALID_START_LDEV_ID = (
        "Invalid start_ldev_id provided. Supported values are 0 to 65278."
    )
    END_LDEV_ID_REQUIRED = "end_ldev_id is required when start_ldev_id is provided."
    INVALID_END_LDEV_ID = (
        "Invalid end_ldev_id provided. Supported values are 1 to 65279."
    )
    END_LDEV_LESS_START_LDEV = "end_ldev_id should be greater than start_ldev_id."
    START_LDEV_ID_REQUIRED = "start_ldev_id is required when end_ldev_id is provided."

    PARALLEL_EXE_LDEV_ID_NOT_ALLOWED = "ldev_id attribute cannot be specified at the same time as the is_parallel_execution_enabled attribute."
    PARALLEL_EXE_PG_ID_NOT_ALLOWED = "parity_group_id attribute cannot be specified at the same time as the is_parallel_execution_enabled attribute."
    PARALLEL_EXE_EXT_PG_ID_NOT_ALLOWED = "external_parity_group attribute cannot be specified at the same time as the is_parallel_execution_enabled attribute."
    LDEV_ID_NOT_IN_START_END_LDEV = (
        "ldev_id should be in the range of start_ldev_id and end_ldev_id."
    )
