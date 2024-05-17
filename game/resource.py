from dataclasses import dataclass

from .enums import ResourceType, ResourceBoundaryValueType
from .decorators import non_negative


class Resource:

    @non_negative
    def __init__(self, resource_type: ResourceType, value: int):
        self._resource_type = resource_type
        self._value = value

    def __string__(self):
        return f"{self._resource_type}: {self._value}"

    @property
    def resource_type(self):
        return self._resource_type

    @property
    def value(self):
        return self._value

    @value.setter
    @non_negative
    def value(self, value):
        self._value = value

    @non_negative
    def increase_value(self, value: int):
        self.value += value

    @non_negative
    def decrease_value(self, value: int):
        self.value = max(self._value - value, 0)


@dataclass(frozen=True)
class ResourceBoundaryValue:

    resource_type: ResourceType
    resource_boundary_value_type: ResourceBoundaryValueType
    value: int
