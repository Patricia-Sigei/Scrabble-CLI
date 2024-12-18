import random
import requests
from board import create_board, append_special_tiles, print_board, is_valid_move, place_word
from tiles import draw_tiles, TILE_BAG, calculate_score
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

def load_wordlist(filename="wordlist.txt"):
    """Loads the wordlist from a file."""
    with open(filename) as f:
        return set(word.strip().upper() for word in f)

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

def is_adjacent_to_existing(board, start_row, start_col, direction, word_length):
    """Checks if the word placement is adjacent to existing tiles on the board."""
    row, col = start_row, start_col
    for _ in range(word_length):
        # Check adjacent cells for existing letters
        if (
            (row > 0 and board[row - 1][col] != '-') or
            (row < 14 and board[row + 1][col] != '-') or
            (col > 0 and board[row][col - 1] != '-') or
            (col < 14 and board[row][col + 1] != '-')
        ):
            return True

        if direction == 'H':
            col += 1
        elif direction == 'V':
            row += 1

    return False

def is_first_move(board):
    """Checks if the game is still on the first move (board center empty)."""
    return board[7][7] == '-'

def validate_adjacent_words(board, word, start_row, start_col, direction, wordlist):
    """Validates that all new adjacent words formed are valid."""
    row, col = start_row, start_col
    for i, letter in enumerate(word):
        if board[row][col] == '-':  # Only validate for newly placed letters
            adjacent_word = ""
            if direction == "H":
                # Check vertical word
                r = row
                while r > 0 and board[r - 1][col] != "-":
                    r -= 1
                while r < 15 and board[r][col] != "-":
                    adjacent_word += board[r][col]
                    r += 1
            elif direction == "V":
                # Check horizontal word
                c = col
                while c > 0 and board[row][c - 1] != "-":
                    c -= 1
                while c < 15 and board[row][c] != "-":
                    adjacent_word += board[row][c]
                    c += 1

            if len(adjacent_word) > 1 and not is_valid_word(adjacent_word, wordlist):
                return False

        # Move to the next letter position
        if direction == "H":
            col += 1
        elif direction == "V":
            row += 1

    return True

def find_possible_moves(player, board, wordlist):
    """Finds all valid moves for the computer, ensuring words attach to the board."""
    moves = []

    # Find all anchor points (existing tiles on the board)
    for row in range(15):
        for col in range(15):
            if board[row][col] != '-':  # Tile exists here
                for direction in ['H', 'V']:
                    # Generate words using anchor tiles
                    for word in generate_candidate_words(player.rack, board[row][col], wordlist):
                        start_row, start_col = row, col
                        if direction == 'H':
                            start_col -= word.index(board[row][col])  # Adjust to fit anchor letter
                        elif direction == 'V':
                            start_row -= word.index(board[row][col])

                        # Validate the move
                        if is_valid_move(board, word, start_row, start_col, direction):
                            moves.append((word, start_row, start_col, direction))

    return moves

def generate_candidate_words(rack, anchor_letter, wordlist):
    """Generates all possible words using the rack and an anchor letter."""
    possible_words = []
    for word in wordlist:
        if anchor_letter in word and all(
            word.count(l) <= rack.count(l) + (1 if l == anchor_letter else 0) for l in word
        ):
            possible_words.append(word)
    return possible_words

def human_turn(player, board, wordlist, first_move, calculate_score):
    """Handles the human player's turn."""
    print(f"\n{player.name}'s turn. Your rack: {' '.join(player.rack)}")
    while True:
        word = input("Enter a word to place (or 's' to skip, 'q' to quit): ").upper()
        if word == "S":
            print(f"{player.name} passed the turn.")
            return first_move

        if word == "Q":
            print("You chose to quit the game.")
            return True  # Return True to indicate the game should end

        if not is_valid_word(word, "wordlist.txt", "two_letters.txt"):
            print(f"'{word}' is not a valid word. Try again.")
            continue

        try:
            start_row = int(input("Enter start row (0-14): "))
            start_col = int(input("Enter start column (0-14): "))
            direction = input("Enter direction (H for horizontal, V for vertical): ").upper()

            if first_move and not (start_row == 7 and start_col == 7):
                print("The first word must start at the center tile (7,7). Try again.")
                continue

            if is_valid_move(board, word, start_row, start_col, direction):
                place_word(board, word, start_row, start_col, direction)
                print("Updated Board:")
                print_board(board)

                # Update player's rack and score
                player.score += calculate_score(word)
                for letter in word:
                    if letter in player.rack:
                        player.rack.remove(letter)
                replenish_rack(player.rack)

                return False  
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Try again.")

def computer_turn(player, board, wordlist, first_move, calculate_score):
    """Handles the computer player's turn."""
    print(f"\n{player.name}'s turn (Computer). Thinking...")
    print(f"Computer's rack: {' '.join(player.rack)}")

    moves = find_possible_moves(player, board, wordlist)

    # Filter moves to only include those that form valid adjacent words
    valid_moves = []
    for word, start_row, start_col, direction in moves:
        if validate_adjacent_words(board, word, start_row, start_col, direction, wordlist):
            valid_moves.append((word, start_row, start_col, direction))

    if not valid_moves:
        print("Computer cannot form a valid word and passes its turn.")
        return first_move

    # Pick a random valid move
    word, start_row, start_col, direction = random.choice(valid_moves)
    place_word(board, word, start_row, start_col, direction)
    print(f"Computer placed '{word}' at ({start_row}, {start_col}) going {direction}.")
    print_board(board)

    # Update computer's rack and score
    player.score += calculate_score(word)
    for letter in word:
        if letter in player.rack:
            player.rack.remove(letter)
    replenish_rack(player.rack)

    return False  

def main():
    # Step 1: Download wordlist
    wordlist_url = "https://github.com/jonbcard/scrabble-bot/raw/master/src/dictionary.txt"
    download_wordlist(wordlist_url)
    wordlist = load_wordlist()

    # Step 2: Initialize board and players
    board = create_board()
    append_special_tiles(board)

    print("\nWelcome to Scrabble!")
    print("Choose game mode:")
    print("1. Human vs Computer")
    print("2. Human vs Human")
    print("3. Two Humans vs Computer")
    while True:
        choice = input("Enter 1, 2, or 3: ")
        if choice in ["1", "2", "3"]:
            break
        print("Invalid choice. Try again.")

    players = []
    if choice == "1":
        players = [Player("Human"), Player("Computer")]
    elif choice == "2":
        players = [Player("Player 1"), Player("Player 2")]
    else:
        players = [Player("Player 1"), Player("Player 2"), Player("Computer")]

    for player in players:
        player.rack = draw_tiles(TILE_BAG, 7)

        # Step 3: Randomize starting player
    current_player_idx = random.randint(0, len(players) - 1)
    first_move = True

    print("\nGame begins! The first word must cover the center tile (7,7).")
    while TILE_BAG or any(player.rack for player in players):
        current_player = players[current_player_idx]
        print_board(board)

        # Check if the current player chose to quit
        if current_player.name == "Computer":
            first_move = computer_turn(current_player, board, wordlist, first_move, calculate_score)
        else:
            first_move = human_turn(current_player, board, wordlist, first_move, calculate_score)
            if first_move:  # If the player chose to quit, exit the game
                break

        current_player_idx = (current_player_idx + 1) % len(players)

    # Game Over - Display results
    print("\nGame Over! Final Scores:")
    for player in players:
        print(f"{player.name}: {player.score} points")
    winner = max(players, key=lambda p: p.score)
    print(f"The winner is {winner.name} with {winner.score} points!")

if __name__ == "__main__":
    main()
