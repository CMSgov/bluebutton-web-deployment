from dataclasses import dataclass
from typing import Optional


@dataclass
class ExternalParityGroupFactSpec:
    external_parity_group: Optional[int] = None
