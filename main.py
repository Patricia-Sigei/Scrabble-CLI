import requests
from board import create_board, append_special_tiles, print_board, is_valid_move, is_connected
from tiles import draw_tiles, TILE_BAG
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


def player_turn(board, player, first_move):
    """Handles the player's turn."""
    print("\nYour turn!")
    print(f"Your rack: {' '.join(player.rack)}")
    word = input("Enter a word to place (or 'q' to quit, 's' to skip turn): ").upper()

    if word == "Q":
        return "quit"

    if word == "S":
        print("You passed your turn.")
        return "skip"

    if not is_valid_word(word):
        print_board(board)
        print(f"'{word}' is not a valid word. Try again.")
        return "retry"

    temp_rack = player.rack[:]
    for letter in word:
        if letter in temp_rack:
            temp_rack.remove(letter)
        elif not any(letter in row for row in board):
            print_board(board)
            print(f"You don't have the tiles to form this word and it's not on the board. Try again.")
            return "retry"

    try:
        start_row = int(input("Enter start row (0-14): "))
        start_col = int(input("Enter start column (0-14): "))
        direction = input("Enter direction ('H' for horizontal, 'V' for vertical): ").upper()
        if direction not in ("H", "V"):
            raise ValueError("Invalid direction!")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return "retry"

    if first_move:
        if direction == "H" and not (start_row == 7 and start_col <= 7 and start_col + len(word) > 7):
            print("The first word must cover the center tile (7,7). Try again.")
            return "retry"
        elif direction == "V" and not (start_col == 7 and start_row <= 7 and start_row + len(word) > 7):
            print("The first word must cover the center tile (7,7). Try again.")
            return "retry"

    if is_valid_move(board, word, start_row, start_col, direction) and is_connected(board, start_row, start_col, word, direction):
        player.play_word(board, word, start_row, start_col, direction)
        print("\nUpdated Board After Your Turn:")
        print_board(board)
        player.rack = replenish_rack(player.rack)
        return "success"
    else:
        print("The word must connect to an existing tile. Try again.")
        return "retry"

def computer_turn(board, computer, first_move):
    """Handles the computer's turn."""
    print("\nComputer's turn!")
    computer_word = next(
        (w for w in ["HELLO", "WORLD", "PYTHON", "SCRABBLE", "AI", "CODE", "ARM", "SIT"]
         if all(computer.rack.count(l) >= w.count(l) for l in w)), None)

    if computer_word:
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
                computer.play_word(board, computer_word, start_row, start_col, direction)
                print(f"Computer placed '{computer_word}' at ({start_row}, {start_col}) going {direction}.")
                print("\nUpdated Board After Computer's Turn:")
                print_board(board)

                # Update computer's rack
                computer.rack = replenish_rack(computer.rack)
                return False
        else:
            print("Computer couldn't place a word.")
    else:
        print("Computer passed its turn.")

    return first_move

def main():
    # Download the wordlist
    wordlist_url = "https://github.com/jonbcard/scrabble-bot/raw/master/src/dictionary.txt"
    download_wordlist(wordlist_url)

    # Initialize the board and add special tiles
    board = create_board()
    board = append_special_tiles(board)

    # Initialize player and computer
    player = Player("Player")
    computer = Player("Computer")

    player.rack = draw_tiles(TILE_BAG, 7)
    computer.rack = draw_tiles(TILE_BAG, 7)

    print("\nLet's play Scrabble!".capitalize())
    print_board(board)

    print("The game begins!")

    print(f"Your tiles: {' '.join(player.rack)}")

    # Randomize starting player
    current_player = random.choice(["player", "computer"])
    print(f"{current_player.capitalize()} starts!")

    first_move = True

    while True:
        if current_player == "player":
            result = player_turn(board, player, first_move)
            if result == "quit":
                print("Game over!")
                if player.score > computer.score:
                    print(f"You win! Your score: {player.score}, Computer's score: {computer.score}")
                elif player.score < computer.score:
                    print(f"Computer wins! Your score: {player.score}, Computer's score: {computer.score}")
                break
            elif result == "skip":
                current_player = "computer"
            elif result == "retry":
                continue
            else:
                current_player = "computer"
                first_move = False
        else:
            first_move = computer_turn(board, computer, first_move)
            current_player = "player"

        # Endgame condition
        if not TILE_BAG and not player.rack and not computer.rack:
            print("No more tiles. Game over!")
            print(f"Final Scores - You: {player.score}, Computer: {computer.score}")
            break

if __name__ == "__main__":
    main()
