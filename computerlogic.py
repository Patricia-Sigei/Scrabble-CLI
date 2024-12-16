import random
import itertools  # For generating permutations
from board import is_valid_move, place_word  # Ensure board-related functions are imported from board.py
from game import load_wordlist  # Import load_wordlist to access the wordlist

# Load the wordlist globally (you can load it once when the game starts)
WORDLIST = load_wordlist()

def computer_turn(board, computer_player):
    """Determines and plays the computer's move."""
    print(f"{computer_player.name}'s turn:")
    
    # Generate all possible words that can be formed with the computer's rack
    possible_words = generate_possible_words(computer_player.rack)
    
    for word in possible_words:
        if is_valid_word(word):  # Check if the word is valid
            # Try all valid positions for the word on the board
            for row in range(15):
                for col in range(15):
                    for direction in ['H', 'V']:
                        if is_valid_move(board, word, row, col, direction):
                            place_word(board, word, row, col, direction)
                            computer_player.rack = update_rack(computer_player.rack, word)
                            print(f"Computer played '{word}' at ({row}, {col}) going {direction}.")
                            return  # End after playing one valid word
    print("Computer could not play a word this turn.")

def generate_possible_words(rack):
    """Generates possible words from the player's rack using permutations."""
    possible_words = []
    # Generate permutations of all lengths from 2 to 7 (max word length in Scrabble)
    for i in range(2, 8):
        for combo in itertools.permutations(rack, i):
            word = ''.join(combo)
            possible_words.append(word.upper())
    return possible_words

def update_rack(rack, word):
    """Updates the rack by removing the letters used in the word."""
    updated_rack = rack.copy()
    for letter in word:
        updated_rack.remove(letter)
    # Add new tiles to the rack (simulating drawing new tiles after the word is played)
    # Here, you can use the draw_tiles function, similar to how it's done in the game loop
    return updated_rack

def is_valid_word(word):
    """Checks if a word is valid by comparing it against the wordlist."""
    return word in WORDLIST  # Check if the word exists in the pre-loaded wordlist
