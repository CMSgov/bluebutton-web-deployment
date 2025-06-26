from dataclasses import dataclass, field, asdict
from typing import Optional, List, get_type_hints, get_origin
import re


@dataclass
class ConnectionInfo:
    """_summary_"""

    address: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    api_token: Optional[str] = None
    subscriber_id: Optional[str] = None
    connection_type: str = field(
        default="direct", metadata={"field": "connection_type"}
    )
    changed: bool = field(default=False, metadata={"field": "changed"})


@dataclass
class StorageSystemInfo:
    serial: int


@dataclass
class TaskLevel:
    state: str


@dataclass
class TenantInfo:
    partnerId: Optional[str] = None
    subscriberId: Optional[str] = None


def camel_to_snake(name: str) -> str:
    """
    Convert a camel case string to snake case, handling consecutive capital letters and acronyms properly.
    """
    # Replace transitions where a lowercase letter is followed by uppercase letters
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)

    # Replace transitions where an acronym (multiple uppercase) is followed by a lowercase letter
    name = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)

    return name.lower()


# Define a parent class with the common functionality
class BaseDataClass:

    def __init__(self, data=None):
        self.data = data if data is not None else []

    def data_to_list(self):
        return [item.to_dict() for item in self.data]

    def data_to_snake_case_list(self):
        return [item.camel_to_snake_dict() for item in self.data]

    def __setattr__(self, name, value):
        if name == "data":
            super().__setattr__(name, value)
        else:
            raise AttributeError("Cannot set attribute directly")

    def to_dict(self):
        return [item.to_dict() for item in self.data]

    def dump_to_object(self, bulk_data):
        #  Direct call from the list data class
        """
        Must use below way to declare the data class list

        data: List[<DataClassName>}] = None
        """
        bulk_data = bulk_data["data"]
        self.data = [
            self.__dataclass_fields__["data"].type.__args__[0](**item)
            for item in bulk_data
        ]
        return self


class SingleBaseClass:

    def __init__(self, **kwargs):
        for ds_field in self.__dataclass_fields__.keys():
            setattr(self, ds_field, kwargs.get(ds_field, None))

    def to_dict(self):
        return asdict(self)

    def snake_to_camel(self, name: str) -> str:
        """
        Convert a snake case string to camel case.
        """
        return "".join(word.title() for word in name.split("_"))

    def camel_to_snake_dict(self) -> dict:
        """
        Convert a camel case string to snake case and include type-based default values.
        """
        new_dict = {}
        type_hints = get_type_hints(type(self))

        for key, unused in self.__dataclass_fields__.items():
            value = getattr(self, key)
            cased_key = camel_to_snake(key)

            # Determine the value to use
            if value is None:
                origin = type_hints.get(key)
                field_type = get_origin(origin)
                if origin == str:
                    value = ""
                elif origin == int:
                    value = -1
                elif origin == float:
                    value = -1.0
                elif origin == bool:
                    value = None
                elif field_type == list:
                    value = []
                elif field_type == dict:
                    value = {}
                else:
                    value = None  # Default for unsupported types

            if (
                isinstance(value, list)
                and len(value) > 0
                and isinstance(value[0], SingleBaseClass)
            ):
                value = [item.camel_to_snake_dict() for item in value]
            if isinstance(value, dict) or isinstance(value, SingleBaseClass):
                value = value.camel_to_snake_dict()
            new_dict[cased_key] = value

        return new_dict


@dataclass
class VSPStorageDevice:
    storageDeviceId: str
    model: str
    ip: str
    serialNumber: int
    ctl1Ip: str
    ctl2Ip: str
    dkcMicroVersion: str
    isSecure: bool

    def __init__(self, **kwargs):
        for key in self.__annotations__.keys():
            setattr(self, key, kwargs.get(key, None))


@dataclass
class VSPCommonInfo:
    serialNumber: str
    model: str
    firstWWN: str
    deviceID: int


def fix_bad_camel_to_snake_conversion(key):
    new_key = key.replace("v_s_m", "vsm")
    return new_key


def base_dict_converter(object):
    result = {}
    for ds_field in object.__dataclass_fields__.values():
        value = getattr(object, ds_field.name)
        snake_case_key = camel_to_snake(ds_field.name)
        if "v_s_m" in snake_case_key:
            snake_case_key = fix_bad_camel_to_snake_conversion(snake_case_key)

        # Determine default filler based on data type
        if value is None or value == "null":
            value = (
                -1
                if ds_field.type == int
                else (
                    ""
                    if ds_field.type == str
                    else (
                        False
                        if ds_field.type == bool
                        else [] if ds_field.type == List else None
                    )
                )
            )
        result[snake_case_key] = value

    return result


@dataclass
class APIGRequestModel(SingleBaseClass):
    module_name: Optional[str] = None
    operation_name: Optional[str] = None
    site: Optional[str] = None
    storage_model: Optional[str] = None
    storage_serial: Optional[int] = None
    storage_type: Optional[int] = None
    connection_type: Optional[int] = None
    operation_status: Optional[int] = None
    process_time: Optional[float] = None
