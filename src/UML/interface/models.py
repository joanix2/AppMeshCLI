from dataclasses import dataclass, asdict
from typing import List
import json

@dataclass
class ParameterDTO:
    protection: str
    name: str
    type: str

@dataclass
class ModelDTO:
    name: str
    parameters: List[ParameterDTO]

    def to_json(self) -> str:
        """Convert the ModelDTO instance to a JSON string."""
        return json.dumps(asdict(self), indent=4)