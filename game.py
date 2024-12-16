import random
from player import Player
from board import create_board, append_special_tiles
from tiles import draw_tiles, TILE_BAG  # Import TILE_BAG from tiles.py
from computerlogic import computer_turn, is_valid_word  # Import the computer logic and word validation function

def display_board(board):
    """Prints the board in a readable format."""
    print("    " + "  ".join(f"{i:2}" for i in range(15)))
    print("   " + "-" * 76)
    for i, row in enumerate(board):
        print(f"{i:2} | " + " | ".join(f"{cell:2}" if len(cell) == 1 else f"{cell}" for cell in row) + " |")
        print("   " + "-" * 76)

def display_rack(player):
    """Displays the player's tile rack."""
    print(f"{player.name}'s Rack: ", end="")
    print(" ".join(player.rack))

def human_turn(board, human_player):
    """Prompts the human player to play a word."""
    print(f"{human_player.name}'s turn:")
    word = input("Enter a word to play: ").upper()
    start_row = int(input("Enter the row to start the word: "))
    start_col = int(input("Enter the column to start the word: "))
    direction = input("Enter the direction (H for horizontal, V for vertical): ").upper()

    if human_player.play_word(board, word, start_row, start_col, direction):
        print(f"Successfully played '{word}' at ({start_row}, {start_col}) going {direction}.")
    else:
        print("Invalid move. Try again.")

def main():
    """Main function to run the game loop."""
    # Create board and players
    board = create_board()
    board = append_special_tiles(board)

    human_player = Player("Human")
    computer_player = Player("Computer")

    # Draw random tiles for both players' racks, ensure the tile bag is updated for both
    human_player.rack = draw_tiles(TILE_BAG.copy(), num=7)  # Use copy of TILE_BAG for human
    computer_player.rack = draw_tiles(TILE_BAG.copy(), num=7)  # Use copy of TILE_BAG for computer

    # Show initial board state and human's rack
    display_board(board)
    display_rack(human_player)  # Display the human player's rack

    # Game loop
    while True:
        # Display the computer's rack before the computer's turn
        display_rack(computer_player)

        # Computer's turn using imported computer logic
        computer_turn(board, computer_player)  # This will use the logic defined in computerlogic.py
        display_board(board)

        # Human's turn
        human_turn(board, human_player)
        display_board(board)

        # Display the human player's updated rack after their turn
        display_rack(human_player)

        # Optional: Add some condition to break the loop, like a max number of turns or game over check
        play_again = input("Do you want to continue playing? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()

