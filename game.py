import random
import itertools  
from board import create_board, print_board, is_valid_move, place_word
from tiles import TILE_BAG, draw_tiles
from player import Player

def load_wordlist():
    """Loads the wordlist from a file."""
    with open("wordlist.txt", "r") as file:
        return set(word.strip().upper() for word in file)

WORDLIST = load_wordlist()  

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

        current_player = (current_player + 1) % 2  

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

    # game.py (or similar file handling game logic)
def play_turn(player_tiles):
    print(f"Your current tiles: {player_tiles}")
    
    # Check if player has blank tiles
    if '@' in player_tiles:
        print("You have blank tiles available to use.")
        blank_tile_index = player_tiles.index('@')
        chosen_letter = input("Enter the letter you want the blank tile to represent: ").upper()

        # Ensure the letter is valid
        if len(chosen_letter) == 1 and chosen_letter.isalpha():
            player_tiles[blank_tile_index] = chosen_letter
            print(f"You used a blank tile as '{chosen_letter}'")
        else:
            print("Invalid letter. Please enter a valid single letter.")
            return play_turn(player_tiles)  

    word = input("Enter the word to play: ").upper()
    return word, player_tiles

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
        if is_valid_word(word):  
            for row in range(15):
                for col in range(15):
                    for direction in ['H', 'V']:
                        if is_valid_move(board, word, row, col, direction):
                            place_word(board, word, row, col, direction)
                            computer_player.rack = update_rack(computer_player.rack, word)
                            print(f"Computer played '{word}' at ({row}, {col}) going {direction}.")
                            return  
    print("Computer could not play a word this turn.")

def generate_possible_words(rack):
    """Generates possible valid words from the player's rack using permutations."""
    possible_words = set()
    for i in range(2, 8):  
        for combo in itertools.permutations(rack, i):
            word = ''.join(combo).upper()
            if word in WORDLIST:  
                possible_words.add(word)
    return list(possible_words)

def is_valid_word(word):
    return word in WORDLIST 

def swap_tiles(rack):
    print("Swapping tiles...")
    global TILE_BAG
    for _ in range(min(7, len(rack))):
        TILE_BAG.append(rack.pop())  
    rack += draw_tiles(TILE_BAG, 7 - len(rack))  

def play_turn(player_tiles):
    print(f"Your current tiles: {player_tiles}")
    
    if '@' in player_tiles:
        print("You have blank tiles available to use.")
        blank_tile_index = player_tiles.index('@')
        chosen_letter = input("Enter the letter you want the blank tile to represent: ").upper()

        if len(chosen_letter) == 1 and chosen_letter.isalpha():
            player_tiles[blank_tile_index] = chosen_letter
            print(f"You used a blank tile as '{chosen_letter}'")
        else:
            print("Invalid letter. Please enter a valid single letter.")
            return play_turn(player_tiles)  

    word = input("Enter the word to play: ").upper()
    return word, player_tiles
