import random
from itertools import permutations
from board import create_board, print_board, append_special_tiles

# Define Scrabble tile bag with letter frequencies
TILE_BAG = {
    "a": 9, "b": 2, "c": 2, "d": 4, "e": 12, "f": 2, "g": 3, "h": 2, "i": 9, "j": 1, 
    "k": 1, "l": 4, "m": 2, "n": 6, "o": 8, "p": 2, "q": 1, "r": 6, "s": 4, "t": 6, 
    "u": 4, "v": 2, "w": 2, "x": 1, "y": 2, "z": 1, " ": 2  # Blank tiles (space)
}

def load_word_list(file_path="valid_words.txt"):
    """Loads a dictionary of valid Scrabble words from a text file."""
    try:
        with open(file_path, "r") as file:
            # Read words, strip whitespace, and convert to lowercase
            return {line.strip().lower() for line in file if line.strip()}
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return set()

def is_word_valid(word, word_list):
    """Checks if a word is valid based on the loaded word list."""
    return word.lower() in word_list

def get_best_word(rack, word_list):
    """Generates the best valid word that can be formed from the given rack."""
    max_word = ""
    for size in range(1, len(rack) + 1):
        for perm in permutations(rack, size):
            possible_word = "".join(perm)
            if is_word_valid(possible_word, word_list) and len(possible_word) > len(max_word):
                max_word = possible_word
    return max_word

def can_place_word(board, word, start_row, start_col, direction):
    """Checks if the word can be placed on the board starting at the given position and direction."""
    if direction == "H":
        if start_col + len(word) > 15:
            return False
        for i in range(len(word)):
            # Check if the tile is empty or matches the character
            if board[start_row][start_col + i] not in (" ", word[i]) and not (start_row == 7 and start_col == 7 and i == 0):
                return False
    elif direction == "V":
        if start_row + len(word) > 15:
            return False
        for i in range(len(word)):
            # Check if the tile is empty or matches the character
            if board[start_row + i][start_col] not in (" ", word[i]) and not (start_row == 7 and start_col == 7 and i == 0):
                return False
    return True

def place_word_on_board(board, word, start_row, start_col, direction):
    """Places the word on the board starting at the given position and direction."""
    if direction == "H":
        for i in range(len(word)):
            board[start_row][start_col + i] = word[i]
    elif direction == "V":
        for i in range(len(word)):
            board[start_row + i][start_col] = word[i]

def find_start_positions(board):
    """Finds all potential start positions on the board."""
    positions = [(7, 7)]  # First move should always start from the center (7, 7)
    return positions

def draw_tile_rack():
    """Draws a random tile rack from the tile bag."""
    rack = []
    available_tiles = [tile for tile, count in TILE_BAG.items() for _ in range(count)]
    for _ in range(7):  # Draw 7 tiles for the rack
        tile = random.choice(available_tiles)
        rack.append(tile)
        available_tiles.remove(tile)  # Remove the tile from the available pool
    return rack

def computer_play(board, rack):
    """Main function for the computer's turn."""
    word_list = load_word_list()
    if not word_list:
        print("Error: No valid words loaded.")
        return

    best_word = get_best_word(rack, word_list)
    if not best_word:
        print("Computer could not form a valid word.")
        return

    start_positions = find_start_positions(board)
    if not start_positions:
        print("No valid starting positions found.")
        return

    directions = ["H", "V"]

    for start_row, start_col in start_positions:
        random.shuffle(directions)  # Randomize direction choice
        for direction in directions:
            if can_place_word(board, best_word, start_row, start_col, direction):
                place_word_on_board(board, best_word, start_row, start_col, direction)
                print(f"Computer played: {best_word} at ({start_row}, {start_col}) ({direction})")
                return

    print("Computer could not place the word on the board.")

if __name__ == "__main__":
    # Create and initialize the board
    board = create_board()

    # Add special tiles to the board
    append_special_tiles(board)

    # Draw a random tile rack for the computer to play with
    rack = draw_tile_rack()

    # Simulate computer's play
    print(f"Computer's rack: {rack}")
    print_board(board)
    computer_play(board, rack)
    print_board(board)
