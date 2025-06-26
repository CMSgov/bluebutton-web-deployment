import os
import functools
import re
import string
import random
from typing import List


try:
    from .vsp_constants import PEGASUS_MODELS, DEFAULT_NAME_PREFIX
    from .hv_constants import TARGET_SUB_DIRECTORY
    from .ansible_common_constants import (
        ANSIBLE_LOG_PATH,
        LOGFILE_NAME,
        # REGISTRATION_FILE_NAME,
        # REGISTRATION_FILE_PATH,
        USER_CONSENT_FILE_PATH,
        CONSENT_FILE_NAME,
    )
    from ..message.common_msgs import CommonMessage
except ImportError:
    from .hv_constants import TARGET_SUB_DIRECTORY
    from .vsp_constants import PEGASUS_MODELS, DEFAULT_NAME_PREFIX
    from .ansible_common_constants import (
        ANSIBLE_LOG_PATH,
        LOGFILE_NAME,
        # REGISTRATION_FILE_NAME,
        # REGISTRATION_FILE_PATH,
        USER_CONSENT_FILE_PATH,
        CONSENT_FILE_NAME,
    )
    from message.common_msgs import CommonMessage


def get_logger_file():
    return os.path.join(ANSIBLE_LOG_PATH, LOGFILE_NAME)  # nosec


def get_logger_dir():
    return ANSIBLE_LOG_PATH


def snake_to_camel_case(string):
    # Split the string into words using '_' as delimiter
    parts = string.split("_")
    # Capitalize the first letter of each word except the first one
    camel_case_string = parts[0] + "".join(
        word.capitalize() for word in parts[1:]
    )  # nosec
    # camel_case_string = ''.join([word.capitalize() for word in words])
    return camel_case_string


def camel_to_snake_case(string):
    # Use regular expressions to find all occurrences of capital letters
    # followed by lowercase letters or digits
    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    # Replace the capital letters with '_' followed by lowercase letters
    # using re.sub() function
    snake_case_string = pattern.sub("_", string).lower()
    return snake_case_string


def camel_array_to_snake_case(a):
    newArr = []
    for i in a:
        if isinstance(i, list):
            newArr.append(camel_array_to_snake_case(i))
        elif isinstance(i, dict):
            newArr.append(camel_dict_to_snake_case(i))
        else:
            newArr.append(i)
    return newArr


def camel_dict_to_snake_case(j):
    out = {}
    for k in j:
        newK = camel_to_snake_case(k)
        if isinstance(j[k], dict):
            out[newK] = camel_dict_to_snake_case(j[k])
        elif isinstance(j[k], list):
            out[newK] = camel_array_to_snake_case(j[k])
        else:
            out[newK] = j[k]
    return out


def convert_hex_to_dec(hex):
    if ":" in hex:
        hex = hex.replace(":", "")
    try:
        return int(hex, 16)
    except ValueError:
        return None


def dicts_to_dataclass_list(data: List[dict], clsName: type) -> List:
    if data is not None:
        return [clsName(**item) for item in data]
    return None


def convert_block_capacity(bytes_size: int, block_size=512) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    factor = 1024
    size = bytes_size * block_size

    for unit in units:
        if size < factor:
            return f"{size:.2f}{unit}"
        size /= factor
    return f"{size:.2f}PB"  # If the size exceeds TB, assume it's in petabytes


def convert_to_bytes(size_str: str, block_size=512) -> int:
    size_str = (
        size_str.strip().upper()
    )  # Convert the string to uppercase for case-insensitivity
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}

    # Split the size string into value and unit
    value, unit = size_str[:-2], size_str[-2:]
    try:
        value = int(value)
        return (value * units[unit]) / block_size
    except (ValueError, KeyError):
        raise ValueError("Invalid size format")


def convert_mb_to_gb(size_str: str):
    size_str = size_str.strip().upper()

    value, unit = size_str[:-2], size_str[-2:]
    if unit == "MB":
        return f"{float('{:.2f}'.format(int(value) / 1024))}GB"
    else:
        return size_str


def log_entry_exit(func):
    try:
        from .hv_log import Log
    except ImportError:
        from hv_log import Log

    logger = Log()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        module_name = func.__module__
        func_name = func.__name__

        logger.writeEnter(f"{module_name}:{func_name}")
        # result = func(*args, **kwargs)

        try:
            #  202408 - common break point
            result = func(*args, **kwargs)
        except Exception as e:
            logger.writeError(f"Exception in {module_name}:{func_name} - {e}")
            raise
        logger.writeExit(f"{module_name}:{func_name}")
        return result

    return wrapper


def process_size_string(size_str: str) -> str:
    size_str = size_str.upper()  # Convert to uppercase for case-insensitivity
    size_str = size_str.replace(" ", "")  # Remove white spaces
    if "MB" in size_str or "GB" in size_str or "TB" in size_str:
        size_str = size_str.replace("B", "")  # Remove 'B' if present
    else:
        size_str += "M"  # Append 'M' if none of MB, GB, TB are present
    return size_str


def get_response_key(response, *keys):
    for key in keys:
        response_key = response.get(key)
        if response_key is not None:
            return response_key
    return None


def get_default_value(value_type):
    return (
        ""
        if value_type == str
        else (
            -1
            if value_type == int
            else [] if value_type == list else (None if value_type == bool else False)
        )
    )


def get_ansible_home_dir():
    # Define the base directories to check
    ansible_base_dirs = [
        os.path.expanduser("~/.ansible/collections"),
        "/usr/share/ansible/collections",
    ]

    # Define the target subdirectory to look for

    # Iterate over the base directories to find the target subdirectory
    for base_dir in ansible_base_dirs:
        target_dir = os.path.join(base_dir, TARGET_SUB_DIRECTORY)  # nosec
        if os.path.exists(target_dir):
            return target_dir

    # Fallback to determining the directory from the current file's location
    abs_path = os.path.dirname(os.path.abspath(__file__))
    split_path = abs_path.split("plugins")[0]

    for base in ansible_base_dirs:
        target_dir = os.path.join(base, split_path)  # nosec
        if os.path.exists(target_dir):
            return target_dir

    # If none of the directories exist, return the default user-specific directory
    return os.path.join(ansible_base_dirs[0], TARGET_SUB_DIRECTORY)  # nosec


def operation_constants(state):
    if state == "present":
        return "created/updated"
    elif state == "absent":
        return "deleted"
    elif state == "defragment":
        return "defragmented"
    else:
        return state


def volume_id_to_hex_format(vol_id):

    if vol_id is None:
        return ""

    hex_format = None

    # Split the hex value to string
    hex_value = format(vol_id, "06x")
    # Convert hexadecimal to 00:00:00 format
    part1_hex = hex_value[:2]
    part2_hex = hex_value[2:4]
    part3_hex = hex_value[4:6]

    # Combine the hexadecimal values into the desired format
    hex_format = f"{part1_hex}:{part2_hex}:{part3_hex}"

    return hex_format.upper()


def is_pegasus_model(storage_info) -> bool:
    return any(sub in storage_info.model for sub in PEGASUS_MODELS)


def calculate_naid(wwn_any_port, serial_number, lun, array_family=7):
    wwn_any_port = int(wwn_any_port, 16)
    # Mask and adjustment based on array family
    wwn_mask_and = 0xFFFFFF00
    serial_number_mask_or = 0x00000000

    if array_family == 0:  # ARRAY_FAMILY_DF
        wwn_mask_and = 0xFFFFFFF0
    elif array_family == 2:  # ARRAY_FAMILY_HM700
        while serial_number > 99999:
            serial_number -= 100000
        serial_number_mask_or = 0x50200000
    elif array_family == 3:  # ARRAY_FAMILY_R800
        serial_number_mask_or = 0x00300000
    elif array_family == 4:  # ARRAY_FAMILY_HM800
        while serial_number > 99999:
            serial_number -= 100000
        serial_number_mask_or = 0x50400000
    elif array_family == 5:  # ARRAY_FAMILY_R900
        serial_number_mask_or = 0x00500000
    elif array_family == 6:  # ARRAY_FAMILY_HM900
        if 400000 <= serial_number < 500000:
            serial_number_mask_or = 0x50400000
        elif 700000 <= serial_number < 800000:
            serial_number_mask_or = 0x50700000
        else:
            serial_number_mask_or = 0x50600000
        while serial_number > 99999:
            serial_number -= 100000
    elif array_family == 7:  # ARRAY_FAMILY_HM2000
        serial_number_mask_or = 0x50800000
        while serial_number > 99999:
            serial_number -= 100000
    else:
        raise ValueError(f"Unsupported array family: {array_family}")

    # Apply masks
    wwn_part = wwn_any_port & 0xFFFFFFFF
    wwn_part &= wwn_mask_and
    serial_number |= serial_number_mask_or

    # Construct high bytes
    high_bytes = (
        (0x60 << 56)
        | (0x06 << 48)
        | (0x0E << 40)
        | (0x80 << 32)
        | ((wwn_part >> 24) & 0xFF) << 24
        | ((wwn_part >> 16) & 0xFF) << 16
        | ((wwn_part >> 8) & 0xFF) << 8
        | (wwn_part & 0xFF)
    )

    # Construct low bytes
    low_bytes = (
        ((serial_number >> 24) & 0xFF) << 56
        | ((serial_number >> 16) & 0xFF) << 48
        | ((serial_number >> 8) & 0xFF) << 40
        | (serial_number & 0xFF) << 32
        | 0x00 << 24
        | 0x00 << 16
        | ((lun >> 8) & 0xFF) << 8
        | (lun & 0xFF)
    )

    # Format NAID
    naid = f"naa.{high_bytes:012x}{low_bytes:016x}"

    return naid


def validate_ansible_product_registration():

    if not os.path.exists(
        os.path.join(USER_CONSENT_FILE_PATH, CONSENT_FILE_NAME)
    ):  # nosec
        return CommonMessage.USER_CONSENT_MISSING.value
    return


def convert_decimal_size_to_bytes(size_str, block_size=512):
    # Define a regular expression to capture the numeric value and the unit
    match = re.match(r"^([0-9.]+)([a-zA-Z]+)$", size_str)

    # If the regex didn't match, raise an error
    if not match:
        raise ValueError(f"Invalid size format: {size_str}")

    # Parse the numeric part (the size value)
    value = float(match.group(1))

    # Get the unit part (e.g., "GB", "MB")
    unit = match.group(2).upper()

    # Convert to bytes based on the unit
    if unit == "B":
        return int(value) / block_size
    elif unit == "KB":
        return int(value * 1024) / block_size
    elif unit == "MB":
        return int(value * 1024 * 1024) / block_size
    elif unit == "GB":
        return int(value * 1024 * 1024 * 1024) / block_size
    elif unit == "TB":
        return int(value * 1024 * 1024 * 1024 * 1024) / block_size
    else:
        raise ValueError(f"Unsupported unit: {unit}")


# this function is used to do auto name assignment,
# not cryptographic or security-sensitive usage
#
# this security scan error can be disregarded moving forward,
# name collisions are not a concern in this context and
# switching to secrets is not necessary
#
def generate_random_name_prefix_string(length=10):
    return f"{DEFAULT_NAME_PREFIX}-" + "".join(  # nosec
        random.choices(string.digits, k=length)  # nosec
    )  # nosec


def convert_to_mb(value):
    if isinstance(value, str):
        value = value.strip()  # Remove any extra spaces
        if "GB" in value:
            # Extract number part and convert to MB
            num = float(value.replace("GB", "").strip())
            return num * 1024
        elif "TB" in value:
            num = float(value.replace("TB", "").strip())
            return num * 1024 * 1024
        elif "MB" in value:
            return float(value.replace("MB", "").strip())
    elif isinstance(value, (int, float)):
        return value
    else:
        raise ValueError(
            "Invalid input format. Please provide a value in GB, TB, or MB."
        )


def check_range(arr, lower_bound, upper_bound):
    return all(lower_bound <= x <= upper_bound for x in arr)


def get_size_from_byte_format_capacity(byte_format):
    value = byte_format.split(" ")[0]
    unit = byte_format.split(" ")[1]
    int_value = value.split(".")[0]
    return f"{int_value}{unit}"
