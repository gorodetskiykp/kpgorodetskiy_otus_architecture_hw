import time
import random
from server import Game


class GameAgent:
    def __init__(self, game: Game, name: str = "Agent"):
        self.game = game
        self.name = name
        self.last_shot_tick = {}  
        self.favorite_ships = []  
        
    def get_all_ships(self):
        return self.game.ships
    
    def decide_commands(self):
        commands = []
        all_ships = self.get_all_ships()
        alive_ships = [s for s in all_ships if s.is_alive]
        
        if not alive_ships:
            return commands
        
        for ship in random.sample(alive_ships, min(3, len(alive_ships))): 
            vel_cmd = self.decide_velocity(ship)
            if vel_cmd:
                commands.append(vel_cmd)
            
            if self.should_shoot(ship):
                shoot_cmd = self.decide_shoot(ship)
                if shoot_cmd:
                    commands.append(shoot_cmd)
        
        return commands
    
    def decide_velocity(self, ship):
        if random.random() < 0.3:
            new_vx = ship.transform.velocity.x + random.randint(-2, 2)
            new_vy = ship.transform.velocity.y + random.randint(-2, 2)
            
            new_vx = max(-5, min(5, new_vx))
            new_vy = max(-5, min(5, new_vy))
            
            return {
                'type': 'set_velocity',
                'data': {
                    'ship_id': ship.ship_id,
                    'vx': new_vx,
                    'vy': new_vy
                }
            }
        return None
    
    def should_shoot(self, ship):
        last_shot = self.last_shot_tick.get(ship.ship_id, 0)
        if self.game.tick_count - last_shot < 2:
            return False
        
        return random.random() < 0.3
    
    def decide_shoot(self, ship):
        self.last_shot_tick[ship.ship_id] = self.game.tick_count
        
        return {
            'type': 'shoot',
            'data': {
                'from_ship_id': ship.ship_id
            }
        }
    
    def send_commands(self):
        commands = self.decide_commands()
        for cmd in commands:
            self.game.add_command(cmd)
        
        if commands:
            vel_cmds = [c for c in commands if c['type'] == 'set_velocity']
            shoot_cmds = [c for c in commands if c['type'] == 'shoot']
            
            ship_ids = set()
            for cmd in commands:
                ship_ids.add(cmd['data'].get('ship_id') or cmd['data'].get('from_ship_id'))
            
            ships_str = ', '.join([f"Ship {sid}" for sid in ship_ids])
            
            if vel_cmds:
                print(f"  [AGENT {self.name}] Changed velocity for {ships_str}")
            if shoot_cmds:
                print(f"  [AGENT {self.name}] 🔫 Shot from {ships_str}")


def create_agent_strategy(strategy_type: str = "random"):
    
    class RandomAgent(GameAgent):
        def decide_velocity(self, ship):
            if random.random() < 0.3:
                return {
                    'type': 'set_velocity',
                    'data': {
                        'ship_id': ship.ship_id,
                        'vx': random.randint(-5, 5),
                        'vy': random.randint(-5, 5)
                    }
                }
            return None
        
        def should_shoot(self, ship):
            last_shot = self.last_shot_tick.get(ship.ship_id, 0)
            if self.game.tick_count - last_shot < 3:
                return False
            return random.random() < 0.2
    
    class ChaoticAgent(GameAgent):
        def decide_commands(self):
            commands = []
            all_ships = self.get_all_ships()
            alive_ships = [s for s in all_ships if s.is_alive]
            
            # Хаотичный агент может управлять МНОГИМИ кораблями
            for ship in alive_ships:  # Все корабли!
                if random.random() < 0.4:  # 40% шанс на каждый
                    vel_cmd = {
                        'type': 'set_velocity',
                        'data': {
                            'ship_id': ship.ship_id,
                            'vx': random.randint(-5, 5),
                            'vy': random.randint(-5, 5)
                        }
                    }
                    commands.append(vel_cmd)
                
                if random.random() < 0.3:  # 30% шанс выстрелить
                    self.last_shot_tick[ship.ship_id] = self.game.tick_count
                    shoot_cmd = {
                        'type': 'shoot',
                        'data': {
                            'from_ship_id': ship.ship_id
                        }
                    }
                    commands.append(shoot_cmd)
            
            return commands
    
    class TacticalAgent(GameAgent):
        """Тактический агент - выбирает одну стратегию и придерживается её"""
        def __init__(self, game, name="Tactical"):
            super().__init__(game, name)
            self.strategy = random.choice(['speed_demon', 'gunslinger', 'controller'])
        
        def decide_commands(self):
            commands = []
            all_ships = self.get_all_ships()
            alive_ships = [s for s in all_ships if s.is_alive]
            
            if self.strategy == 'speed_demon':
                # Фокус на изменении скоростей
                for ship in random.sample(alive_ships, min(2, len(alive_ships))):
                    if random.random() < 0.7:
                        commands.append({
                            'type': 'set_velocity',
                            'data': {
                                'ship_id': ship.ship_id,
                                'vx': random.randint(-3, 3),
                                'vy': random.randint(-3, 3)
                            }
                        })
            
            elif self.strategy == 'gunslinger':
                # Фокус на стрельбе
                for ship in random.sample(alive_ships, min(3, len(alive_ships))):
                    if random.random() < 0.6:
                        self.last_shot_tick[ship.ship_id] = self.game.tick_count
                        commands.append({
                            'type': 'shoot',
                            'data': {
                                'from_ship_id': ship.ship_id
                            }
                        })
            
            else:  # controller
                # Пытается контролировать конкретные корабли
                if not self.favorite_ships:
                    self.favorite_ships = random.sample(alive_ships, min(2, len(alive_ships)))
                
                for ship in self.favorite_ships:
                    if ship.is_alive:
                        # Всегда меняет скорость любимых кораблей
                        commands.append({
                            'type': 'set_velocity',
                            'data': {
                                'ship_id': ship.ship_id,
                                'vx': random.randint(-2, 2),
                                'vy': random.randint(-2, 2)
                            }
                        })
                        
                        # И часто стреляет с них
                        if random.random() < 0.5:
                            self.last_shot_tick[ship.ship_id] = self.game.tick_count
                            commands.append({
                                'type': 'shoot',
                                'data': {
                                    'from_ship_id': ship.ship_id
                                }
                            })
            
            return commands
    
    strategies = {
        'random': RandomAgent,
        'chaotic': ChaoticAgent,
        'tactical': TacticalAgent
    }
    
    return strategies.get(strategy_type, RandomAgent)


def run_agent_demo():
    """Демонстрация работы агентов"""
    from server import Game, GameInitializer
    
    print("=" * 60)
    print("ЗАПУСК ДЕМОНСТРАЦИИ АГЕНТОВ")
    print("=" * 60)
    print("Агенты могут управлять ЛЮБЫМИ кораблями на поле!")
    print("=" * 60)
    
    # Создаем игру
    game = Game(GameInitializer(), ships_count=4)  # 4 корабля у каждого игрока
    
    # Создаем агентов разных типов
    AgentClass1 = create_agent_strategy("chaotic")
    AgentClass2 = create_agent_strategy("tactical")
    AgentClass3 = create_agent_strategy("random")
    
    agent1 = AgentClass1(game, "Chaotic")
    agent2 = AgentClass2(game, "Tactical")
    agent3 = AgentClass3(game, "Random")
    
    agents = [agent1, agent2, agent3]
    
    # Запускаем 20 тиков
    for tick in range(1, 21):
        print(f"\n--- Tick {tick} ---")
        
        # Агенты принимают решения и отправляют команды
        for agent in agents:
            agent.send_commands()
        
        # Сервер обрабатывает команды и двигает корабли
        game.tick()
        
        # Показываем состояние
        state = game.get_game_state()
        
        alive_ships = [s for s in state['ships'] if s['alive']]
        print(f"\n  Ships alive: {len(alive_ships)}/{len(state['ships'])}")
        
        for ship in state['ships']:
            status = "💀" if not ship['alive'] else "✅"
            print(f"    Ship {ship['id']}: "
                  f"pos=({ship['x']:2d}, {ship['y']:2d}) "
                  f"vel=({ship['vx']:2d}, {ship['vy']:2d}) "
                  f"{status}")
        
        if state['bombs']:
            print(f"\n  Active bombs: {len(state['bombs'])}")
            for i, bomb in enumerate(state['bombs']):
                print(f"    Bomb {i+1}: at ({bomb['x']:2d}, {bomb['y']:2d}) "
                      f"fuse: {bomb['fuse']}")
        
        time.sleep(1)


if __name__ == "__main__":
    run_agent_demo()