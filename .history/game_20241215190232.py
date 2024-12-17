# game.py
from board import create_board, print_board
from tiles import TILE_BAG, draw_tiles
from player import Player

def play_game():
    """Main game loop."""
    # Initialize board and players
    board = create_board()
    tile_bag = TILE_BAG.copy()
    players = [Player("Human"), Player("Computer")]

    # Draw initial tiles for both players
    for player in players:
        player.rack = draw_tiles(tile_bag, 7)

    current_player = 0

    while tile_bag or any(player.rack for player in players):
        player = players[current_player]
        print_board(board)
        print(f"{player.name}'s turn. Rack: {player.rack}")
        if player.name == "Human":
            # Human turn
            word = input("Enter a word: ").upper()
            start_row = int(input("Enter start row (0-14): "))
            start_col = int(input("Enter start column (0-14): "))
            direction = input("Direction (H/V): ").upper()
            if player.play_word(board, word, start_row, start_col, direction):
                print(f"Word played: {word}")
            else:
                print("Invalid move.")
        else:
            # Computer turn (basic logic)
            print("Computer is thinking...")
            if player.rack:
                word = player.rack[0]
                player.play_word(board, word, 7, 7, "H")  # Example move
                print(f"Computer played: {word}")
            else:
                print("Computer passed.")

        # Replenish tiles
        player.rack += draw_tiles(tile_bag, 7 - len(player.rack))
        current_player = (current_player + 1) % 2

    # Game Over
    print("Game Over!")
    for player in players:
        print(f"{player.name} Score: {player.score}")
    winner = max(players, key=lambda p: p.score)
    print(f"{winner.name} wins!")
