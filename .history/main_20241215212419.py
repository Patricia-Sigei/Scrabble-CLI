import requests
from board import create_board, append_special_tiles, print_board, is_valid_move, place_word
from tiles import draw_tiles, TILE_BAG, calculate_score
import random

# Ensure this function is defined at the top before being used in main()
def download_wordlist(url, filename="wordlist.txt"):
    """Downloads a wordlist from the given URL and saves it to a file."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "w") as f:
            f.write(response.text)
        print(f"Wordlist downloaded and saved as '{filename}'.")
    except Exception as e:
        print(f"Error downloading wordlist: {e}")

# The rest of your function definitions go here

def is_valid_word(word, wordlist_file="wordlist.txt"):
    """Checks if a word is valid using the downloaded wordlist."""
    try:
        with open(wordlist_file) as f:
            valid_words = set(line.strip().upper() for line in f)
        return word in valid_words
    except FileNotFoundError:
        print("Error: Wordlist file not found. Please download it first.")
        return False
    except Exception as e:
        print(f"Error reading wordlist file: {e}")
        return False


def replenish_rack(rack):
    """Replenishes the player's or computer's rack to maintain seven tiles."""
    while len(rack) < 7 and TILE_BAG:
        rack += draw_tiles(TILE_BAG, 1)
    return rack


def computer_turn(board, computer_rack, wordlist_file="wordlist.txt"):
    """Let the computer try to place a valid word with strategic placement."""
    # Load wordlist
    try:
        with open(wordlist_file) as f:
            valid_words = set(line.strip().upper() for line in f)
    except Exception as e:
        print(f"Error loading wordlist: {e}")
        return False

    # Find all valid words the computer can form with its rack
    possible_words = [
        word for word in valid_words if all(computer_rack.count(letter) >= word.count(letter) for letter in word)
    ]

    # If no valid words can be formed, the computer passes its turn
    if not possible_words:
        print("Computer passes its turn.")
        return False

    # Sort words by length (longer words are generally better)
    possible_words.sort(key=len, reverse=True)

    # Try to place the first valid word with the highest score
    for word in possible_words:
        for _ in range(50):  # Try up to 50 random placements
            start_row, start_col = random.randint(0, 14), random.randint(0, 14)
            direction = random.choice(["H", "V"])

            # Check if the word can be placed at the generated position
            if is_valid_move(board, word, start_row, start_col, direction):
                place_word(board, word, start_row, start_col, direction)
                print(f"Computer placed '{word}' at ({start_row}, {start_col}) going {direction}.")
                print_board(board)

                # Calculate and update computer score
                word_score = calculate_score(word)
                computer_score = word_score  # Update the score immediately
                print(f"Computer scored {word_score} points! Total: {computer_score} points.")

                # Update computer's rack
                for letter in word:
                    computer_rack.remove(letter)
                computer_rack = replenish_rack(computer_rack)

                return True  # Successful placement

    # If no valid placement is found after 50 attempts, the computer passes
    print("Computer couldn't place a word.")
    return False


def main():
    # Download the wordlist
    wordlist_url = "https://github.com/jonbcard/scrabble-bot/raw/master/src/dictionary.txt"
    download_wordlist(wordlist_url)

    # Initialize the board and add special tiles
    board = create_board()
    board = append_special_tiles(board)

    # Initialize player and computer racks
    player_rack = draw_tiles(TILE_BAG, 7)
    computer_rack = draw_tiles(TILE_BAG, 7)

    player_score = 0
    computer_score = 0

    print("\nInitial Board with Special Tiles:")
    print_board(board)

    print(f"Your tiles: {' '.join(player_rack)}")
    print("The game begins!")

    while True:
        # --- Player's Turn ---
        print("\nYour turn!")
        print(f"Your rack: {' '.join(player_rack)}")
        word = input("Enter a word to place (or 'q' to quit, 'pass' to skip turn): ").upper()

        if word == "Q":
            print("Game over!")
            break

        if word == "PASS":
            print("You passed your turn.")
        else:
            if not word.isalpha():
                print(f"'{word}' is not a valid word. It should only contain alphabetic characters.")
                continue

            if not is_valid_word(word):
                print(f"'{word}' is not a valid word. Try again.")
                continue

            if not all(player_rack.count(letter) >= word.count(letter) for letter in word):
                print("You don't have the tiles to form this word. Try again.")
                continue

            # Handle row and column input with validation
            while True:
                try:
                    start_row = int(input("Enter start row (0-14): "))
                    start_col = int(input("Enter start column (0-14): "))
                    if not (0 <= start_row <= 14) or not (0 <= start_col <= 14):
                        raise ValueError("Row and column must be between 0 and 14.")
                    break  # Exit the loop if inputs are valid
                except ValueError as e:
                    print(f"Invalid input: {e}")
                    continue

        def is_valid_move(board, word, start_row, start_col, direction):
    "             ""Checks if a word can be placed at the given position on the board."""
                word_length = len(word)
    
                   # Check boundaries
                    if direction == "V":
                    if start_row + word_length > 14:  # Word doesn't fit vertically
                         print(f"Invalid move: Word doesn't fit vertically at {start_row}, {start_col}")
                     return False
    elif direction == "H":
        if start_col + word_length > 14:  # Word doesn't fit horizontally
            print(f"Invalid move: Word doesn't fit horizontally at {start_row}, {start_col}")
            return False

    # Check if the word overlaps with other tiles correctly
    for i in range(word_length):
        r, c = start_row + (i if direction == "V" else 0), start_col + (i if direction == "H" else 0)
        
        # Check if this position is already occupied with a tile or is valid for placing
        if board[r][c] != '.' and board[r][c] != word[i]:
            print(f"Invalid move: Tile at ({r}, {c}) is not empty and does not match the word.")
            return False
    
    return True

                print("\nUpdated Board After Your Turn:")
                print_board(board)

                # Calculate and update player score
                word_score = calculate_score(word)
                player_score += word_score
                print(f"You scored {word_score} points! Total: {player_score} points.")

                # Update player's rack
                for letter in word:
                    player_rack.remove(letter)
                player_rack = replenish_rack(player_rack)
            else:
                print("Invalid move! Try again.")
                continue

        # --- Computer's Turn ---
        if not computer_turn(board, computer_rack):
            print("Computer passed its turn.")
        
        # Endgame condition
        if not TILE_BAG and not player_rack and not computer_rack:
            print("No more tiles. Game over!")
            print(f"Final Scores - You: {player_score}, Computer: {computer_score}")
            break


if __name__ == "__main__":
    main()
