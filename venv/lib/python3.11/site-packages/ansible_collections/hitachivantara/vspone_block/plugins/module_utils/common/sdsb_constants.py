import logging


class SDSBlockEndpoints(object):
    GET_SERVERS = "v1/objects/servers"
    POST_SERVERS = "v1/objects/servers"
    GET_SERVER_BY_ID = "v1/objects/servers/{}"
    GET_SERVERS_AND_QUERY_NICKNAME = "v1/objects/servers?nickname={}"
    GET_SERVERS_AND_QUERY_NICKNAMES = "v1/objects/servers?nicknames={}"
    GET_SERVERS_AND_QUERY_HBA_NAME = "v1/objects/servers?hbaName={}"
    DELETE_SERVERS = "v1/objects/servers/{}"
    PATCH_SERVERS = "v1/objects/servers/{}"
    GET_VOLUME_SERVER_CONNECTIONS_AND_ID = (
        "v1/objects/volume-server-connections?serverId={}"
    )
    DELETE_VOLUMES = "v1/objects/volumes/{}"
    POST_HBAS = "v1/objects/servers/{}/hbas"
    GET_HBAS = "v1/objects/servers/{}/hbas"
    DELETE_HBAS = "v1/objects/servers/{}/hbas/{}"
    GET_PORTS = "v1/objects/ports"
    GET_PORT_BY_ID = "v1/objects/ports/{}"
    GET_PORT_BY_NAME = "v1/objects/ports?name={}"
    GET_PORTS_AND_QUERY = "v1/objects/ports?{}={}"
    GET_PATHS = "v1/objects/servers/{}/paths"
    POST_PATHS = "v1/objects/servers/{}/paths"
    DELETE_PATHS = "v1/objects/servers/{}/paths/{},{}"
    GET_POOLS = "v1/objects/pools"
    GET_POOLS_AND_ID = "v1/objects/pools/{}"
    GET_POOLS_AND_QUERY = "v1/objects/pools?name={}"
    GET_VOLUMES = "v1/objects/volumes"
    POST_VOLUMES = "v1/objects/volumes"
    GET_VOLUMES_AND_QUERY = "v1/objects/volumes?{}={}"
    GET_VOLUMES_AND_NICKNAME = "v1/objects/volumes?nickname={}"
    GET_VOLUMES_AND_SERVERID = "v1/objects/volumes?serverId={}"
    GET_VOLUMES_BY_ID = "v1/objects/volumes/{}"
    PATCH_VOLUMES = "v1/objects/volumes/{}"
    POST_VOLUME_SERVER_CONNECTIONS = "v1/objects/volume-server-connections"
    DELETE_VOLUME_SERVER_CONNECTIONS = "v1/objects/volume-server-connections/{},{}"
    GET_VOLUME_SERVER_CONNECTIONS_FOR_SERVERID = (
        "v1/objects/volume-server-connections?serverId={}"
    )
    GET_VOLUME_SERVER_CONNECTIONS_FOR_VOLUMEID = (
        "v1/objects/volume-server-connections?volumeId={}"
    )
    POST_VOLUMES_EXPAND = "v1/objects/volumes/{}/actions/expand/invoke"
    GET_CHAP_USERS = "v1/objects/chap-users"
    GET_CHAP_USER_BY_ID = "v1/objects/chap-users/{}"
    GET_CHAP_USERS_AND_QUERY = "v1/objects/chap-users?targetChapUserName={}"
    POST_CHAP_USERS = "v1/objects/chap-users"
    DELETE_CHAP_USERS = "v1/objects/chap-users/{}"
    PATCH_CHAP_USERS = "v1/objects/chap-users/{}"
    GET_PORT_AUTH_SETTINGS = "v1/objects/port-auth-settings/{}"
    PATCH_PORT_AUTH_SETTINGS = "v1/objects/port-auth-settings/{}"
    GET_PORT_AUTH_SETTINGS_CHAP_USERS = "v1/objects/port-auth-settings/{}/chap-users"
    POST_PORT_AUTH_SETTINGS_CHAP_USERS = "v1/objects/port-auth-settings/{}/chap-users"
    DELETE_PORT_AUTH_SETTINGS_CHAP_USERS = (
        "v1/objects/port-auth-settings/{}/chap-users/{}"
    )
    GET_JOBS = "v1/objects/jobs/{}"
    GET_STORAGE_NODES_AND_QUERY = "v1/objects/storage-nodes?protectionDomainId={}"
    GET_DRIVES = "v1/objects/drives"
    POST_POOLS_EXPAND = "v1/objects/pools/{}/actions/expand/invoke"
    GET_STORAGE_CONTROLLERS = "v1/objects/storage-controllers"
    GET_STORAGE_CLUSTER = "v1/objects/storage"
    GET_HEALTH_STATUS = "v1/objects/health-status"

    GET_VPS = "v1/objects/virtual-private-storages"
    GET_VPS_BY_ID = "v1/objects/virtual-private-storages/{}"
    DELETE_VPS = "v1/objects/virtual-private-storages/{}"
    POST_VPS = "v1/objects/virtual-private-storages"
    UPDATE_VPS = "v1/objects/virtual-private-storages/{}"


class Http(object):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    BASE_URL = "/ConfigurationManager/simple/"
    CONTENT_TYPE = "Content-Type"
    APPLICATION_JSON = "application/json"
    HEADERS_JSON = {CONTENT_TYPE: APPLICATION_JSON}
    HTTP = "http://"
    HTTPS = "https://"
    DEFAULT_PORT = 443
    DEFAULT_SSL_PORT = 443
    OPEN_URL_TIMEOUT = 300
    USER_AGENT = "automation-module"


class ModuleArgs(object):
    CONNECTION_ADDRESS = "connection_address"
    NULL = "None"
    CHECK_MODE = "check_mode"
    SERVER = "management_address"
    SERVER_PORT = "management_port"
    USER = "user"
    PASSWORD = "password"
    SERVER_NICKNAME = "server_nickname"
    OS_TYPE = "os_type"
    ISCSI_NAME = "iscsi_name"
    TARGET_PORT_NAME = "target_port_name"
    POOL_NAME = "pool_name"
    CAPACITY = "capacity_mb"
    NUMBER = "number"
    BASE_NAME = "base_name"
    START_NUMBER = "start_number"
    NUMBER_OF_DIGIT = "number_of_digit"
    VOLUME_NAME = "volume_name"
    TARGET_CHAP_USER_NAME = "target_chap_user_name"
    TARGET_CHAP_SECRET = "target_chap_secret"
    INITIATOR_CHAP_USER_NAME = "initiator_chap_user_name"
    INITIATOR_CHAP_USER_SECRET = "initiator_chap_secret"
    POOL_EXPAND_CAPACITY = "pool_expand_capacity"
    EXPAND_POOL_PROCESS1_INFO = "expand_pool_process1_info"
    DEVICE_COUNT = "device_count"
    EC2_INSTANCE_INFO = "ec2_instance_info"
    SYSTEM_CONFIGRATION_FILE = "system_configuration_file"
    VM_CONFIGRATION_FILE = "vm_configuration_file"
    DRIVE_COUNT_IN_NODE = "drive_count_in_node"
    ADDITINAL_DRIVE_COUNT_IN_NODE = "additional_drive_count_in_node"
    ADD_STORAGENODE_PROCESS1_INFO = "add_storagenode_process1_info"
    TIME_A = "time_a"
    TIME_B = "time_b"
    TIME_C = "time_c"
    TIME_D = "time_d"


class AutomationConstants(object):
    PORT_NUMBER_MIN = 0
    PORT_NUMBER_MAX = 49151
    NAME_PARAMS_MIN = 1
    NAME_PARAMS_MAX = 256
    MIN_SIZE_ALLOWED = 1
    MAX_SIZE_ALLOWED = 999999999999
    MAX_TIME_ALLOWED = 999
    MIN_TIME_ALLOWED = 1
    CHAP_SECRET_MIN = 12
    CHAP_SECRET_MAX = 32
    QOS_UPPER_LIMIT_IOPS_MIN = 100
    QOS_UPPER_LIMIT_IOPS_MAX = 2147483647
    QOS_UPPER_LIMIT_XFER_RATE_MIN = 1
    QOS_UPPER_LIMIT_XFER_RATE_MAX = 2097151
    QOS_UPPER_ALERT_ALLOWABLE_TIME_OUT_MIN = 1
    QOS_UPPER_ALERT_ALLOWABLE_TIME_OUT_MAX = 600


class ErrorMessages(object):
    INVALID_PORT_NUMBER_ERR = (
        "The specified value is invalid"
        + " ({}: {}). Specify the value within a valid range (min: "
        + str(AutomationConstants.PORT_NUMBER_MIN)
        + ", max: "
        + str(AutomationConstants.PORT_NUMBER_MAX)
        + ")."
    )
    HTTP_4xx_ERRORS = (
        "Invalid request sent by the client."
        + " API responded with client error code ({}). Reason: {}"
    )
    HTTP_5xx_ERRORS = (
        "The server encountered an unexpected "
        + "condition. API responded with server error code ({}). Reason: {}"
    )
    API_COMMUNICATION_ERR = (
        "Communication with the target server" + " failed. Reason: {}"
    )
    NOT_AVAILABLE = "Not Available."
    REQUIRED_VALUE_ERR = (
        "The value for the parameter is" + " required. ({}) Specify a valid value."
    )
    API_TIMEOUT_ERR = (
        "A timeout occurred because no response" + " was received from the server."
    )
    INVALID_TYPE_VALUE = (
        "The specified value is not an integer"
        + " type ({}: {}). Specify an integer value."
    )
    INVALID_NAME_SIZE = (
        "The argument of the parameter name length is invalid"
        + " ({}: {}). Specify in a valid range characters"
    )
    INVALID_SIZE_VALUE = (
        "The specified size argument has an invalid range"
        + " ({}: {}). Specify in a valid range."
    )
    INVALID_TIME_VALUE = (
        "The specified time argument has an invalid range"
        + " ({}: {}). Specify in a valid range."
    )
    INVALID_SECRET_SIZE = (
        "The specified value is invalid" + " ({}: {}). Secret should be 12 to 32 chars."
    )


class LogMessages(object):
    ENTER_METHOD = "Enter method: {}"
    LEAVE_METHOD = "Leave method: {}"
    API_REQUEST_START = "API Request: {} {}"
    API_RESPONSE = "API Response: {}"


class Log(object):
    SYSLOG_IDENTIFIER = "SYSLOG_IDENTIFIER"
    PRIORITY = "PRIORITY"
    # There is no applicable level in Python for following priorities
    # 0(Emergency), 1(Alert), 5(Notice)
    ARGS = {
        logging.DEBUG: {PRIORITY: 7},
        logging.INFO: {PRIORITY: 6},
        logging.WARNING: {PRIORITY: 4},
        logging.ERROR: {PRIORITY: 3},
        logging.CRITICAL: {PRIORITY: 2},
    }
