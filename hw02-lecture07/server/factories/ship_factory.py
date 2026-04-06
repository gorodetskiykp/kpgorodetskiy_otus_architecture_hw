from ..core.vector import Position, Velocity
from ..core.interfaces import ShipFactoryInterface
from ..entities.ship import Ship


class ShipFactory(ShipFactoryInterface):
    @staticmethod
    def create_ships(count: int) -> list[Ship]:
        return [Ship(
            position=Position.random(0, 100),
            velocity=Velocity.random(-5, 5),
            ship_id=i+1,
        ) for i in range(count)]
