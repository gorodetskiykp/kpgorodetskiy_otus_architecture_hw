from ..core.interfaces import GameInitializerInterface
from ..core.vector import Position, Velocity
from ..entities.bomb import Bomb


class Game:
    def __init__(self, initializer: GameInitializerInterface, ships_count: int = 3):
        result = initializer.initialize(ships_count)
        if not isinstance(result, tuple) or len(result) != 2:
            raise TypeError("Initializer must return a tuple of two lists")
        
        self.player_1_ships, self.player_2_ships = result
        self.ships = self.player_1_ships + self.player_2_ships
        self.bombs = []
        self.tick_count = 0

        self.command_queue = []

    def add_command(self, command: dict):
        self.command_queue.append(command)

    def process_commands(self):
        for command in self.command_queue:
            self._execute_command(command)
        self.command_queue.clear()

    def _find_ship_by_id(self, ship_id: int):
        for ship in self.ships:
            if ship.ship_id == ship_id:
                return ship
        return None

    def _execute_command(self, command: dict):
        cmd_type = command.get('type')
        data = command.get('data', {})
        
        if cmd_type == 'set_velocity':
            ship_id = data.get('ship_id')
            target_ship = self._find_ship_by_id(ship_id)
            
            if target_ship and target_ship.is_alive:
                new_vel = Velocity(data.get('vx', 0), data.get('vy', 0))
                target_ship.set_velocity(new_vel)
                print(f"  [SERVER] Ship {ship_id} velocity -> ({new_vel.x}, {new_vel.y})")
        
        elif cmd_type == 'shoot':
            from_ship_id = data.get('from_ship_id')
            from_ship = self._find_ship_by_id(from_ship_id)
            
            if from_ship and from_ship.is_alive:
                bomb = Bomb(
                    position=Position(from_ship.position.x, from_ship.position.y),
                    velocity=from_ship.transform.velocity
                )
                
                self.bombs.append(bomb)
                print(f"  [SERVER] Ship {from_ship_id} fired a bomb!")
    
    def process_bombs(self):
        exploded_bombs = []
        things_to_destroy = set() 
        
        for bomb in self.bombs:
            if not bomb.is_alive:
                exploded_bombs.append(bomb)
                continue
            
            exploded = bomb.move()
            
            if exploded:
                print(f"  [SERVER] 💥 BOOM! Bomb exploded at ({bomb.position.x}, {bomb.position.y})")
                
                for ship in self.ships:
                    if ship.is_alive:
                        distance = abs(bomb.position.x - ship.position.x) + abs(bomb.position.y - ship.position.y)
                        if distance < 10:
                            things_to_destroy.add(ship)
                            print(f"  [SERVER] 💀 Ship {ship.ship_id} caught in explosion!")
                
                for other_bomb in self.bombs:
                    if other_bomb != bomb and other_bomb.is_alive:
                        distance = abs(bomb.position.x - other_bomb.position.x) + abs(bomb.position.y - other_bomb.position.y)
                        if distance < 10:
                            things_to_destroy.add(other_bomb)
                            other_bomb.fuse = 0
                            print(f"  [SERVER] 💥 Other bomb detonated by explosion!")
                
                exploded_bombs.append(bomb)
        
        for thing in things_to_destroy:
            thing.annihilate()
        
        self.bombs = [b for b in self.bombs if b not in exploded_bombs]

    def tick(self):
        self.process_commands()

        self.tick_count += 1
        for ship in self.ships:
            ship.move()

        self.process_bombs()
    
    def get_game_state(self):
        """Вернуть состояние игры"""
        ships_data = []
        for ship in self.ships:
            ships_data.append({
                'id': ship.ship_id,
                'x': ship.position.x,
                'y': ship.position.y,
                'vx': ship.transform.velocity.x,
                'vy': ship.transform.velocity.y,
                'alive': ship.is_alive
            })
        
        bombs_data = []
        for bomb in self.bombs:
            bombs_data.append({
                'x': bomb.position.x,
                'y': bomb.position.y,
                'fuse': bomb.fuse
            })
        
        return {
            'tick': self.tick_count,
            'ships': ships_data,
            'bombs': bombs_data
        }
