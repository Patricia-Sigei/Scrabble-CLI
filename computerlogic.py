import random
from itertools import permutations
from board import create_board, print_board, append_special_tiles
from tiles import draw_tiles  # Import the draw_tiles function

TILE_BAG = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9,
    "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
    "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1, " ": 2
}

def load_word_list(file_path="valid_words.txt"):
    try:
        with open(file_path, "r") as file:
            return {line.strip().lower() for line in file if line.strip()}
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return set()

def is_word_valid(word, word_list):
    return word.lower() in word_list

def get_best_word(rack, word_list):
    max_word = ""
    for size in range(1, len(rack) + 1):
        for perm in permutations(rack, size):
            possible_word = "".join(perm)
            if is_word_valid(possible_word, word_list) and len(possible_word) > len(max_word):
                max_word = possible_word
    return max_word

def can_place_word(board, word, start_row, start_col, direction):
    if direction == "H":
        if start_col + len(word) > 15:
            return False
        for i in range(len(word)):
            if board[start_row][start_col + i] not in (" ", word[i]) and not (start_row == 7 and start_col == 7 and i == 0):
                return False
    elif direction == "V":
        if start_row + len(word) > 15:
            return False
        for i in range(len(word)):
            if board[start_row + i][start_col] not in (" ", word[i]) and not (start_row == 7 and start_col == 7 and i == 0):
                return False
    return True

def place_word_on_board(board, word, start_row, start_col, direction):
    if direction == "H":
        for i in range(len(word)):
            board[start_row][start_col + i] = word[i]
    elif direction == "V":
        for i in range(len(word)):
            board[start_row + i][start_col] = word[i]

def find_start_positions(board):
    positions = [(random.randint(0, 14), random.randint(0, 14))]
    return positions

def computer_play(board, rack):
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
        random.shuffle(directions)
        for direction in directions:
            if can_place_word(board, best_word, start_row, start_col, direction):
                place_word_on_board(board, best_word, start_row, start_col, direction)
                print(f"Computer played: {best_word} at ({start_row}, {start_col}) ({direction})")
                return

    print("Computer could not place the word on the board.")

if __name__ == "__main__":
    board = create_board()
    append_special_tiles(board)
    rack = draw_tiles(TILE_BAG)
    print(f"Computer's rack: {rack}")
    print_board(board)
    computer_play(board, rack)
    print_board(board)
