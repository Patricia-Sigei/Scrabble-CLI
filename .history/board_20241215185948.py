from game import play_game
from board import create_board, append_special_tiles, print_board, is_valid_move, place_word


def main():
    # Initialize the board and add special tiles
    board = create_board()
    board = append_special_tiles(board)

    # Initialize player racks
    player_rack = draw_tiles(TILE_BAG, 7)
    computer_rack = draw_tiles(TILE_BAG, 7)

    print("\nInitial Board with Special Tiles:")
    print_board(board)

    print(f"Your tiles: {' '.join(player_rack)}")
    print("The game begins!")

    while True:
        # Player's Turn
        print("\nYour turn!")
        word = input("Enter a word to place (or 'q' to quit): ").upper()
        if word == "Q":
            print("Game over!")
            break

        # Validate word against player's rack
        if not all(player_rack.count(letter) >= word.count(letter) for letter in word):
            print("You don't have the tiles to form this word. Try again.")
            continue

        # Get position and direction
        try:
            start_row = int(input("Enter start row (0-14): "))
            start_col = int(input("Enter start column (0-14): "))
            direction = input("Enter direction ('H' for horizontal, 'V' for vertical): ").upper()
            if direction not in ("H", "V"):
                raise ValueError("Invalid direction!")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        # Validate and place the word
        if is_valid_move(board, word, start_row, start_col, direction):
            place_word(board, word, start_row, start_col, direction)
            print("\nUpdated Board After Your Turn:")
            print_board(board)
            
            # Update player's rack
            for letter in word:
                player_rack.remove(letter)
            
            # Replenish rack
            player_rack += draw_tiles(TILE_BAG, 7 - len(player_rack))
        else:
            print("Invalid move! Try again.")
            continue

        # Computer's Turn (placeholder)
        print("\nComputer's turn...")
        # Example: Computer places the word "HELLO" at a fixed position
        if is_valid_move(board, "HELLO", 10, 10, "H"):
            place_word(board, "HELLO", 10, 10, "H")
            print("\nUpdated Board After Computer's Turn:")
            print_board(board)
        else:
            print("Computer couldn't place a word.")

        # Check for endgame condition
        if not TILE_BAG and not player_rack and not computer_rack:
            print("No more tiles. Game over!")
            break


if __name__ == "__main__":
    main()
def create_board():
    """Creates a 15x15 Scrabble board."""
    return [[" " for _ in range(15)] for _ in range(15)]

def append_special_tiles(board):
    SPECIAL_TILES = {
        "DL": [(1, 2), (2, 1), (3, 2), (2, 3), (1, 12), (2, 13), (3, 12), (2, 11), (12, 1), (13, 2), (12, 3), (11, 2), (12, 13), (13, 12), (12, 11), (11, 12)],
        "TL": [(0, 6), (0, 8), (2, 6), (2, 8), (3, 7), (6, 0), (6, 14), (8, 0), (8, 14), (12, 6), (12, 8), (14, 6), (14, 8), (7, 3), (7, 11)],
        "DW": [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13),(9, 1), (9, 5), (9, 9), (9, 13), (13, 5), (13, 9)],
        "TW": [(0, 0), (0, 14), (7, 0), (7, 14), (14, 0), (14, 14)],
        "*": [(7, 7)]
    }
    for tile_type, positions in SPECIAL_TILES.items():
        for row, col in positions:
            board[row][col] = tile_type
         
    print("\nDebug: Special tiles added to the board.")  # Debugging line  
    return board

def print_board(board):
    """Prints the board in a readable format."""
    print("    " + " "+"   ".join(f"{i:2}" for i in range(15)))
    print("   " + "-" * 76)
    for i, row in enumerate(board):
        print(f"{i:2} | " + " | ".join(f"{cell:2}" if len(cell) == 1 else f"{cell}" for cell in row) + " |")
        print("   " + "-" * 76)


def place_word(board, word, start_row, start_col, direction):
    """
    Places a word on the board.
    direction: 'H' for horizontal, 'V' for vertical
    """
    if direction == "H":
        for i, letter in enumerate(word):
            board[start_row][start_col + i] = letter
    elif direction == "V":
        for i, letter in enumerate(word):
            board[start_row + i][start_col] = letter

def is_valid_move(board, word, start_row, start_col, direction):
    """
    Validates if the word can be placed on the board.
    Returns True if valid, False otherwise.
    """
    print(f"Debug: Validating move for '{word}' at ({start_row}, {start_col}) going {direction}")
    
    if direction == "H":
        if start_col + len(word) > 15:
            print("Debug: Word goes out of horizontal bounds.")
            return False
        for i, letter in enumerate(word):
            current_cell = board[start_row][start_col + i]
            # Allow placement on empty spaces or special tiles
            if current_cell not in (" ", "DL", "TL", "DW", "TW", "*", letter):  
                print(f"Debug: Cell conflict at ({start_row}, {start_col + i}). Cell: '{current_cell}', Letter: '{letter}'")
                return False
    elif direction == "V":
        if start_row + len(word) > 15:
            print("Debug: Word goes out of vertical bounds.")
            return False
        for i, letter in enumerate(word):
            current_cell = board[start_row + i][start_col]
            if current_cell not in (" ", "DL", "TL", "DW", "TW", "*", letter):
                print(f"Debug: Cell conflict at ({start_row + i}, {start_col}). Cell: '{current_cell}', Letter: '{letter}'")
                return False
    return True

if __name__ == "__main__":
    board = create_board()
    board = append_special_tiles(board)
    print_board(board)
    
    word = "HELLO"
    start_row, start_col = 7, 7
    direction = "H"
    
    if is_valid_move(board, word, start_row, start_col, direction):
        place_word(board, word, start_row, start_col, direction)
    else:
        print("Invalid move")
    
    print_board(board)                        # tiles.py
import random

TILE_BAG = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9,
    "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
    "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1, " ": 2  # Blank tiles
}

LETTER_POINTS = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, " ": 0
}

def draw_tiles(tile_bag, num=7):
    """Draws tiles from the tile bag."""
    tiles = []
    for _ in range(num):
        if not tile_bag:
            break
        tile = random.choice(list(tile_bag.keys()))
        tiles.append(tile)
        tile_bag[tile] -= 1
        if tile_bag[tile] == 0:
            del tile_bag[tile]
    return tiles


def calculate_score(word):
    """Calculates the score of a given word."""
    return sum(LETTER_POINTS[letter] for letter in word.upper())

