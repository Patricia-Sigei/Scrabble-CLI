import requests
from board import create_board, append_special_tiles, print_board, is_valid_move, place_word, is_connected
from tiles import draw_tiles, TILE_BAG, calculate_score
import random
from player import Player


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


def is_valid_word(word, wordlist_file="wordlist.txt", two_letter_file="two_letters.txt"):
    """Checks if a word is valid using the downloaded wordlist and a two-letter word list."""
    try:
        with open(wordlist_file) as f:
            valid_words = set(line.strip().upper() for line in f)
        with open(two_letter_file) as f:
            valid_two_letter_words = set(line.strip().upper() for line in f)
        return word in valid_words or word in valid_two_letter_words
    except FileNotFoundError as e:
        print(f"Error: {e.filename} file not found. Please download it first.")
        return False
    except Exception as e:
        print(f"Error reading wordlist files: {e}")
        return False


def replenish_rack(rack):
    """Replenishes the player's or computer's rack to maintain seven tiles."""
    while len(rack) < 7 and TILE_BAG:
        rack += draw_tiles(TILE_BAG, 1)
    return rack


def generate_possible_words(rack, wordlist_file="wordlist.txt"):
    """Generates all possible valid words from the current rack."""
    possible_words = []
    with open(wordlist_file) as f:
        valid_words = set(line.strip().upper() for line in f)

    # Generate possible words by trying all combinations of letters from the rack
    for word in valid_words:
        temp_rack = rack[:]
        valid = True
        for letter in word:
            if letter in temp_rack:
                temp_rack.remove(letter)
            else:
                valid = False
                break
        if valid:
            possible_words.append(word)

    return possible_words


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

    # Randomize starting player
    current_player = random.choice(["player", "computer"])
    print(f"{current_player.capitalize()} starts!")

    first_move = True

    while True:
        if current_player == "player":
            # --- Player's Turn ---
            print("\nYour turn!")
            print(f"Your rack: {' '.join(player_rack)}")
            word = input("Enter a word to place (or 'q' to quit, 's' to skip turn): ").upper()

            if word == "Q":
                print("Game over!")
                if player_score > computer_score:
                    print(f"You win! Your score: {player_score}, Computer's score: {computer_score}")
                elif player_score < computer_score:
                    print(f"Computer wins! Your score: {player_score}, Computer's score: {computer_score}")
                break

            if word == "S":
                print("You passed your turn.")
            else:
                if not is_valid_word(word):
                    print(f"'{word}' is not a valid word. Try again.")
                    continue

                temp_rack = player_rack[:]
                for letter in word:
                    if letter in temp_rack:
                        temp_rack.remove(letter)
                    elif not any(letter in row for row in board):
                        print(f"You don't have the tiles to form this word and it's not on the board. Try again.")
                        break
                else:
                    try:
                        start_row = int(input("Enter start row (0-14): "))
                        start_col = int(input("Enter start column (0-14): "))
                        direction = input("Enter direction ('H' for horizontal, 'V' for vertical): ").upper()
                        if direction not in ("H", "V"):
                            raise ValueError("Invalid direction!")
                    except ValueError as e:
                        print(f"Invalid input: {e}")
                        continue

                    if first_move:
                        if direction == "H":
                            if not (start_row == 7 and start_col <= 7 and start_col + len(word) > 7):
                                print("The first word must cover the center tile (7,7). Try again.")
                                continue
                        elif direction == "V":
                            if not (start_col == 7 and start_row <= 7 and start_row + len(word) > 7):
                                print("The first word must cover the center tile (7,7). Try again.")
                                continue

                    if is_valid_move(board, word, start_row, start_col, direction) and is_connected(board, start_row, start_col, word, direction):
                        place_word(board, word, start_row, start_col, direction)
                        print("\nUpdated Board After Your Turn:")
                        print_board(board)

                        # Calculate and update player score
                        word_score = calculate_score(word)
                        player_score += word_score
                        print(f"You scored {word_score} points! Total: {player_score} points.")

                        # Update player's rack, skipping letters that were on the board
                        for letter in word:
                            if letter in player_rack:
                                player_rack.remove(letter)
                        player_rack = replenish_rack(player_rack)
                        first_move = False
                    else:
                        print("Invalid move! Try again.")
                        continue

            current_player = "computer"

        else:
            # --- Computer's Turn ---
            print("\nComputer's turn!")

            # Get all valid words the computer can form with its rack
            computer_words = generate_possible_words(computer_rack)

            if computer_words:
                # Pick a word from the possible valid words
                computer_word = random.choice(computer_words)

                for _ in range(50):  # Attempt up to 50 random positions and directions
                    start_row, start_col = random.randint(0, 14), random.randint(0, 14)
                    direction = random.choice(["H", "V"])

                    if first_move:
                        start_row, start_col = 7, 7
                        direction = random.choice(["H", "V"])
                        if direction == "H":
                            start_col = random.randint(0, 7)
                        else:
                            start_row = random.randint(0, 7)

                    if is_valid_move(board, computer_word, start_row, start_col, direction) and is_connected(board, start_row, start_col, computer_word, direction):
                        place_word(board, computer_word, start_row, start_col, direction)
                        print(f"Computer placed '{computer_word}' at ({start_row}, {start_col}) going {direction}.")
                        print("\nUpdated Board After Computer's Turn:")
                        print_board(board)

                        # Calculate and update computer score
                        word_score = calculate_score(computer_word)
                        computer_score += word_score
                        print(f"Computer scored {word_score} points! Total: {computer_score} points.")

                        # Update computer's rack
                        for letter in computer_word:
                            computer_rack.remove(letter)
                        computer_rack = replenish_rack(computer_rack)
                        first_move = False
                        break
                else:
                    print("Computer couldn't place a word.")
            else:
                print("Computer passed its turn.")

            current_player = "player"

        # Endgame condition
        if not TILE_BAG and not player_rack and not computer_rack:
            print("No more tiles. Game over!")
            print(f"Final Scores - You: {player_score}, Computer: {computer_score}")
            break


if __name__ == "__main__":
    main()