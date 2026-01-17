from __future__ import annotations

import copy
from typing import Dict, Any
from abc import ABC, abstractmethod

from edgevisionx.utils.logger import EVXLogger


class Node(ABC):
    """Base node class"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.name = config.get("name", self.__class__.__name__)
        self._initialized = False
        self._metrics = {}
        self.logger = EVXLogger.get_logger(self.name)

    @abstractmethod
    def setup(self) -> None:
        """Initialize resources"""
        pass

    @abstractmethod
    def __call__(self, input: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing logic"""
        pass

    def teardown(self):
        pass

    def validate_input(self, input: Dict) -> bool:
        pass

    def clone(self):
        return copy.deepcopy(self)
