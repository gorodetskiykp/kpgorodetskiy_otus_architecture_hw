from dataclasses import dataclass
from random import randint
from abc import ABC, abstractmethod


@dataclass
class Vector2D:
    x: int
    y: int
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return self.__class__(self.x + other.x, self.y + other.y)


class Randomizable(ABC):
    @classmethod
    @abstractmethod
    def random(cls, min_val: int, max_val: int):
        pass


class Position(Vector2D, Randomizable): 
    @classmethod
    def random(cls, min_val: int, max_val: int):
        return cls(randint(min_val, max_val), randint(min_val, max_val))
    
    def __str__(self):
        return f"({self.x}, {self.y})"


class Velocity(Vector2D, Randomizable):
    @classmethod
    def random(cls, min_val: int, max_val: int):
        return cls(randint(min_val, max_val), randint(min_val, max_val))
