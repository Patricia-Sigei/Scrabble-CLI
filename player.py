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
        from board import place_word, is_valid_move
        from tiles import calculate_score

        if is_valid_move(board, word, start_row, start_col, direction):
            place_word(board, word, start_row, start_col, direction)
            self.score += calculate_score(word)
            for letter in word.upper():
                if letter in self.rack:
                    self.rack.remove(letter)
            return True
        return False
