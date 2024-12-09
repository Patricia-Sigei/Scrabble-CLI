# board.py

def create_board():
    """Creates a 15x15 Scrabble board."""
    return [[" " for _ in range(15)] for _ in range(15)]


def print_board(board):
    """Prints the board in a readable format."""
    print("    " + " ".join(f"{i:2}" for i in range(15)))
    print("   " + "-" * 45)
    for i, row in enumerate(board):
        print(f"{i:2} | " + " | ".join(row) + " |")
        print("   " + "-" * 45)


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
    if direction == "H":
        if start_col + len(word) > 15:
            return False
        for i, letter in enumerate(word):
            if board[start_row][start_col + i] not in (" ", letter):
                return False
    elif direction == "V":
        if start_row + len(word) > 15:
            return False
        for i, letter in enumerate(word):
            if board[start_row + i][start_col] not in (" ", letter):
                return False
    return True
