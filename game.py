import random
import itertools  # For generating permutations
from board import create_board, print_board, is_valid_move, place_word
from tiles import TILE_BAG, draw_tiles
from player import Player

def load_wordlist():
    """Loads the wordlist from a file."""
    with open("wordlist.txt", "r") as file:
        return set(word.strip().upper() for word in file)

WORDLIST = load_wordlist()  # Preload wordlist globally for validation

def play_game():
    """Main game loop."""
    # Initialize board and players
    board = create_board()
    tile_bag = TILE_BAG.copy()
    players = [Player("Human"), Player("Computer")]

    # Draw initial tiles for both players
    for player in players:
        player.rack = draw_tiles(tile_bag, 7)

    current_player = 0

    while tile_bag or any(player.rack for player in players):
        player = players[current_player]
        print_board(board)
        print(f"{player.name}'s turn. Rack: {player.rack}")

        if player.name == "Human":
            # Human turn
            word = input("Enter a word: ").upper()
            start_row = int(input("Enter start row (0-14): "))
            start_col = int(input("Enter start column (0-14): "))
            direction = input("Direction (H/V): ").upper()

            if is_valid_move(board, word, start_row, start_col, direction):
                place_word(board, word, start_row, start_col, direction)
                player.rack = update_rack(player.rack, word)
                print(f"Word played: {word}")
            else:
                print("Invalid move.")
        else:
            # Computer turn
            print("Computer is thinking...")
            computer_turn(board, player)

        # Replenish tiles after the turn (only if there are tiles in the bag)
        if tile_bag:
            player.rack += draw_tiles(tile_bag, 7 - len(player.rack))

        current_player = (current_player + 1) % 2  # Switch turns

    # Game Over
    print("Game Over!")
    for player in players:
        print(f"{player.name} Score: {player.score}")
    winner = max(players, key=lambda p: p.score)
    print(f"{winner.name} wins!")

def update_rack(player_rack, word):
    """Updates the player's rack after a word is played."""
    for letter in word:
        if letter in player_rack:
            player_rack.remove(letter)
    return player_rack

def computer_turn(board, computer_player):
    """Determines and plays the computer's move."""
    print(f"{computer_player.name}'s turn:")
    
    # Generate all possible words that can be formed with the computer's rack
    possible_words = generate_possible_words(computer_player.rack)
    
    if not possible_words:
        print("Computer can't form any words, swapping tiles...")
        swap_tiles(computer_player.rack)
        return
    
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
    """Generates possible valid words from the player's rack using permutations."""
    possible_words = set()
    for i in range(2, 8):  # Length of words from 2 to 7
        for combo in itertools.permutations(rack, i):
            word = ''.join(combo).upper()
            if word in WORDLIST:  # Only add valid words from the wordlist
                possible_words.add(word)
    return list(possible_words)

def is_valid_word(word):
    """Checks if a word is valid by comparing it against the wordlist."""
    return word in WORDLIST  # Check if the word exists in the pre-loaded wordlist

def swap_tiles(rack):
    """Simulates the computer swapping tiles."""
    print("Swapping tiles...")
    global TILE_BAG
    # Swap a certain number of tiles
    for _ in range(min(7, len(rack))):
        TILE_BAG.append(rack.pop())  # Add tile back to the bag
    rack += draw_tiles(TILE_BAG, 7 - len(rack))  # Replenish the rack with new tiles
