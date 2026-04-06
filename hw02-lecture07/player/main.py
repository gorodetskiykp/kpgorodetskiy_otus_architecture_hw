from server import Game, GameInitializer 


def display_tick(game: Game, tick_number: int):
    print(f"\n=== Tick {tick_number} ===")
    
    positions = game.get_ships_positions()
    
    for i, ship in enumerate(positions, 1):
        player = "Player 1" if ship['player'] == 1 else "Player 2"
        status = "ALIVE" if ship['alive'] else "DESTROYED"
        print(f"  Ship {i} ({player}): ({ship['x']:3d}, {ship['y']:3d}) - {status}")


def main():
    game = Game(GameInitializer())
    
    for tick in range(1, 4):
        display_tick(game, tick)
        game.tick()


if __name__ == "__main__":
    main()
