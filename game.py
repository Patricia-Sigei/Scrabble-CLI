from board import Board
from player import Player
import random


class ScrabbleGame:
    def __init__(self):
        """
        Initialize the Scrabble game with a board and two players.
        Player 1 is the Computer, and Player 2 is the User.
        """
        self.board = Board()
        self.players = [Player("Computer"), Player("User")]
        self.current_player_idx = 0

    def display_game_state(self):
        """
        Display the current game state: the board and players' tiles.
        """
        print("\nCurrent Board:")
        self.board.display()
        print("\nPlayer Tiles:")
        for player in self.players:
            player.display_tiles()

    def play_turn(self):
        """
        Handles a single turn for the current player.
        """
        current_player = self.players[self.current_player_idx]

        if current_player.name == "Computer":
            self.computer_play()
        else:
            self.player_play(current_player)

        # Switch to the next player
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def computer_play(self):
        """
        Logic for the computer to play a word on the board.
        """
        print("\nComputer's Turn:")
        word = self.generate_computer_word(self.players[0].tiles)

        if not word:
            print("Computer has no valid moves. Skipping turn.")
            return

        # Randomly choose a starting position and direction
        row = random.randint(0, 14)
        col = random.randint(0, 14)
        direction = random.choice(["horizontal", "vertical"])

        print(f"Computer attempts to play '{word}' at ({row}, {col}) {direction}.")
        success = self.board.place_tiles(word, (row, col), direction, self.players[0])

        if success:
            print("Computer successfully placed its word!")
        else:
            print("Computer's move failed.")

    def generate_computer_word(self, tiles):
        """
        Generate a word from the computer's tiles using a simple strategy.
        """
        # Sample word dictionary (expand with a real dictionary for better gameplay)
        valid_words = {"CAT", "DOG", "BAT", "RAT", "TEAR", "WATER"}
        for word in valid_words:
            if all(letter in tiles or letter == "_" for letter in word):
                return word
        return None

    def player_play(self, player):
        """
        Handles the turn for a human player.
        """
        print(f"\n{player.name}'s Turn:")
        self.display_game_state()

        try:
            word = input("Enter the word you want to play: ").strip().upper()
            row = int(input("Enter the starting row (0-14): ").strip())
            col = int(input("Enter the starting column (0-14): ").strip())
            direction = input("Enter the direction ('horizontal' or 'vertical'): ").strip().lower()

            success = self.board.place_tiles(word, (row, col), direction, player)

            if success:
                print(f"{player.name} successfully placed the word '{word}'!")
            else:
                print("Invalid move. Please try again.")
        except ValueError:
            print("Invalid input. Please follow the instructions.")
