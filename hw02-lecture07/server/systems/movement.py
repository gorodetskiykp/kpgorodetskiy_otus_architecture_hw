from typing import Callable

from ..core.interfaces import MovementSystemInterface, Transform


class MovementSystem(MovementSystemInterface):
    def __init__(self, strategy: Callable = None):
        self.strategy = strategy or self._linear_move
    
    @staticmethod
    def _linear_move(transform: Transform):
        transform.position = transform.position + transform.velocity
    
    def move(self, transform: Transform):
        self.strategy(transform)
