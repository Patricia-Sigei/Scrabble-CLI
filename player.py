# player.py

class Player:
    def __init__(self, name):
        self.name = name
        self.rack = []
        self.score = 0

    def play_word(self, board, word, start_row, start_col, direction):
        """
        Plays a word on the board. Updates score and rack.
        """
        from board import place_word, is_valid_move, is_connected
        from tiles import calculate_score

        word = word.upper()  # Ensure the word is uppercase for consistent processing
        print(f"Debug: {self.name} is attempting to play '{word}' at ({start_row}, {start_col}) in direction '{direction}'.")

        # Validate move
        if not is_valid_move(board, word, start_row, start_col, direction):
            print(f"Debug: Invalid move for '{word}'.")
            return False

        # Check if the word is connected to existing tiles or is the first word
        if not is_connected(board, start_row, start_col, word, direction):
            print(f"Debug: Word '{word}' is not connected to existing tiles.")
            return False

        # Place the word if valid
        place_word(board, word, start_row, start_col, direction)
        word_score = calculate_score(word)  # Adjusted for full scoring details
        self.score += word_score
        print(f"Debug: Word '{word}' placed successfully! Scored {word_score} points.")

        # Remove letters from the player's rack
        for letter in word:
            if letter in self.rack:
                self.rack.remove(letter)
            else:
                print(f"Debug: Error - Attempted to remove '{letter}' from rack, but it wasn't found.")

        return True
