from dataclasses import dataclass
from typing import Optional

try:
    from .common_base_models import SingleBaseClass

except ImportError:
    from .common_base_models import SingleBaseClass


@dataclass
class VSPCmdDevSpec(SingleBaseClass):
    ldev_id: Optional[int] = None
    # is_command_device_enabled: Optional[bool] = None
    is_security_enabled: Optional[bool] = None
    is_user_authentication_enabled: Optional[bool] = None
    is_device_group_definition_enabled: Optional[bool] = None
