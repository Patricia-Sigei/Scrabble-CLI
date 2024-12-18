class ScrabbleBoard:
    def __init__(self):
        self.board = [[" " for _ in range(15)] for _ in range(15)]

    def display(self):
        for row in self.board:
            print(" | ".join(row))
        print("\n")

    def place_tile(self, row, col, tile):
        self.board[row][col] = tile


class ScrabbleGame:
    def __init__(self):
        self.board = ScrabbleBoard()
        self.player_tiles = ['A', '_', 'T', 'E', 'R', 'N']

    def display_game_state(self):
        print("Current Board:")
        self.board.display()
        print(f"Your Tiles: {', '.join(self.player_tiles)}\n")

    def handle_blank_tile(self, word, position):
        """
        Handle blank tiles when placing a word on the board.
        """
        for i, letter in enumerate(word):
            if letter not in self.player_tiles:
                # Check if the letter can be substituted by a blank tile
                if '_' in self.player_tiles:
                    print(f"Blank tile detected for letter '{letter}'.")
                    confirm_letter = input(f"Do you want to use a blank tile as '{letter}'? (y/n): ").strip().lower()
                    if confirm_letter == 'y':
                        self.player_tiles.remove('_')
                        print(f"Blank tile set as '{letter}'.")
                    else:
                        print("Move canceled. You chose not to use the blank tile.")
                        return False
                else:
                    print(f"You do not have the tile '{letter}' to play this word.")
                    return False

            # Simulate placing the tile on the board
            row, col = position
            self.board.place_tile(row, col + i, letter)

        return True

    def play_turn(self):
        """
        Allow the player to play a turn.
        """
        self.display_game_state()
        word = input("Enter the word you want to play: ").strip().upper()
        row = int(input("Enter the starting row (0-14): "))
        col = int(input("Enter the starting column (0-14): "))

        if self.handle_blank_tile(word, (row, col)):
            print("Word placed successfully!\n")
        else:
            print("Word placement failed.\n")


# Main game loop
if __name__ == "__main__":
    game = ScrabbleGame()

    while True:
        game.play_turn()
        continue_game = input("Do you want to play another turn? (y/n): ").strip().lower()
        if continue_game != 'y':
            print("Thanks for playing!")
            break
