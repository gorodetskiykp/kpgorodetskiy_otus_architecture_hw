from abc import ABC, abstractmethod
from .vector import Position, Velocity
from dataclasses import dataclass


@dataclass
class Transform:
    position: Position
    velocity: Velocity


class Movable(ABC):
    @abstractmethod
    def move(self):
        pass


class MovementSystemInterface(ABC):
    @abstractmethod
    def move(self, transform: Transform):
        pass


class StateInterface(ABC):
    @abstractmethod
    def annihilate(self):
        pass
    
    @property
    @abstractmethod
    def is_alive(self) -> bool:
        pass


class HasTransform(ABC):
    @property
    @abstractmethod
    def transform(self) -> Transform:
        pass


class ShipFactoryInterface(ABC):
    @abstractmethod
    def create_ships(self, count: int) -> list['Ship']:
        pass


class GameInitializerInterface(ABC):
    @abstractmethod
    def initialize(self, ships_per_player: int) -> tuple[list, list]:
        pass
