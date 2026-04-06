from ..core.interfaces import GameInitializerInterface, ShipFactoryInterface
from ..factories.ship_factory import ShipFactory


class GameInitializer(GameInitializerInterface):
    def __init__(self, factory: ShipFactoryInterface = None):
        self.factory = factory or ShipFactory()
    
    def initialize(self, ships_per_player: int) -> tuple[list, list]:
        return (
            self.factory.create_ships(ships_per_player),
            self.factory.create_ships(ships_per_player),
        )