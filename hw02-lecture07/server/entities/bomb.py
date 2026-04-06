from ..core.vector import Position, Velocity
from ..core.mixins import TransformMixin, MovementMixin, StateMixin


class Bomb(TransformMixin, MovementMixin, StateMixin):
    def __init__(self, position: Position, velocity: Velocity):
        doubled_velocity = Velocity(velocity.x * 2, velocity.y * 2)
        super().__init__(position=position, velocity=doubled_velocity, initial_state=True)
        self.fuse = 3
    
    def move(self):
        if not self.is_alive:
            return
        super().move()
        self.fuse -= 1
        if self.fuse <= 0:
            self.annihilate()
            return True
        return False
