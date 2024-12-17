# board.py

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
         
    return board

def print_board(board):
    """Prints the board in a readable format."""
    print("    " + " "+"   ".join(f"{i:2}" for i in range(15)))
    print("   " + "-" * 76)
    for i, row in enumerate(board):
        print(f"{i:2} | " + " | ".join(f"{cell:2}" if len(cell) == 1 else f"{cell}" for cell in row) + " |")
        print("   " + "-" * 76)

def is_connected(board, start_row, start_col, word, direction):
    """Checks if the word connects to existing tiles or is the first word covering the center tile."""
    connected = False
    if direction == "H":
        for i in range(len(word)):
            row = start_row
            col = start_col + i
            # Check if the current position overlaps with existing tiles
            if board[row][col] != ' ':
                connected = True
            # Check if the current position is adjacent to an existing tile
            if (
                (row > 0 and board[row - 1][col] != ' ') or
                (row < 14 and board[row + 1][col] != ' ') or
                (col > 0 and board[row][col - 1] != ' ') or
                (col < 14 and board[row][col + 1] != ' ')
            ):
                connected = True

    elif direction == "V":
        for i in range(len(word)):
            row = start_row + i
            col = start_col
            # Check if the current position overlaps with existing tiles
            if board[row][col] != ' ':
                connected = True
            # Check if the current position is adjacent to an existing tile
            if (
                (row > 0 and board[row - 1][col] != ' ') or
                (row < 14 and board[row + 1][col] != ' ') or
                (col > 0 and board[row][col - 1] != ' ') or
                (col < 14 and board[row][col + 1] != ' ')
            ):
                connected = True

    # Check if the word covers the center tile for the first word
    if not connected and board[7][7] == '*':
        if direction == "H" and start_row == 7 and start_col <= 7 < start_col + len(word):
            connected = True
        elif direction == "V" and start_col == 7 and start_row <= 7 < start_row + len(word):
            connected = True

    return connected

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
            current_cell = board[start_row][start_col + i]
            if current_cell not in (" ", "DL", "TL", "DW", "TW", "*", letter):  
                return False
    elif direction == "V":
        if start_row + len(word) > 15:
            return False
        for i, letter in enumerate(word):
            current_cell = board[start_row + i][start_col]
            if current_cell not in (" ", "DL", "TL", "DW", "TW", "*", letter):
                return False
    return True
