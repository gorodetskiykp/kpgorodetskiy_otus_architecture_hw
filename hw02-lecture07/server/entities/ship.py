from ..core.vector import Position, Velocity
from ..core.mixins import TransformMixin, MovementMixin, StateMixin
from ..core.interfaces import Movable


class Ship(TransformMixin, MovementMixin, StateMixin):
    def __init__(self, position: Position, velocity: Velocity, ship_id: int = None):
        super().__init__(position=position, velocity=velocity, initial_state=True)
        self.ship_id = ship_id or id(self)
    
    def move(self):
        if not self.is_alive:
            return
        super().move()

    def set_velocity(self, new_velocity: Velocity):
        self.transform.velocity = new_velocity
