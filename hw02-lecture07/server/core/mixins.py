from typing import Optional
from .interfaces import Movable, HasTransform, Transform, MovementSystemInterface, StateInterface
from .vector import Position, Velocity
from ..systems.movement import MovementSystem


class TransformMixin(HasTransform):
    def __init__(self, position: Position, velocity: Velocity, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._transform = Transform(position, velocity)
    
    @property
    def transform(self) -> Transform:
        return self._transform 
    
    @property
    def position(self):
        return self._transform.position
    
    @position.setter
    def position(self, value):
        self._transform.position = value


class MovementMixin(Movable):
    def __init__(self, movement_system: Optional[MovementSystemInterface] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not isinstance(self, HasTransform):
            raise TypeError("MovementMixin requires HasTransform")
        self.movement_system = movement_system or MovementSystem()
    
    def move(self):
        self.movement_system.move(self.transform)


class StateMixin(StateInterface):
    def __init__(self, initial_state: bool = True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state = initial_state
    
    def annihilate(self):
        self._state = False
    
    @property
    def is_alive(self) -> bool:
        return self._state
