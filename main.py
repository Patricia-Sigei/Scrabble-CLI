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


def is_valid_word(word, wordlist):
    """Checks if a word is valid using the wordlist."""
    return word in wordlist


def replenish_rack(rack):
    """Replenishes the player's or computer's rack to maintain seven tiles."""
    while len(rack) < 7 and TILE_BAG:
        rack += draw_tiles(TILE_BAG, 1)
    return rack


def human_turn(player, board, wordlist, first_move):
    """Handles the human player's turn."""
    print(f"\n{player.name}'s turn. Your rack: {' '.join(player.rack)}")
    while True:
        word = input("Enter a word to place (or 'pass' to skip, 'q' to quit): ").upper()
        if word == "PASS":
            print(f"{player.name} passed the turn.")
            return first_move

        if word == "Q":
            print("You chose to quit the game.")
            return True  # Return True to indicate the game should end

        if not is_valid_word(word, wordlist):
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

                return False  # First move is now done
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Try again.")


def computer_turn(player, board, wordlist, first_move):
    """Handles the computer player's turn."""
    print(f"\n{player.name}'s turn (Computer). Thinking...")
    possible_words = []

    if first_move:
        possible_words = [word for word in wordlist if all(word.count(l) <= player.rack.count(l) for l in word)]
    else:
        possible_words = find_possible_words_from_board(player, board, wordlist)

    if not possible_words:
        print("Computer cannot form a word and passes its turn.")
        return first_move

    random.shuffle(possible_words)
    for word in possible_words:
        for row in range(15):
            for col in range(15):
                for direction in ['H', 'V']:
                    if first_move and not (row == 7 and col == 7):
                        continue
                    if is_valid_move(board, word, row, col, direction):
                        place_word(board, word, row, col, direction)
                        print(f"Computer placed '{word}' at ({row}, {col}) going {direction}.")
                        print_board(board)

                        # Update computer's rack and score
                        player.score += calculate_score(word)
                        for letter in word:
                            player.rack.remove(letter)
                        replenish_rack(player.rack)

                        return False  # First move is now done
    print("Computer couldn't place any word and passes.")
    return first_move


def find_possible_words_from_board(player, board, wordlist):
    """Finds possible words the computer can build from the existing board."""
    possible_words = []
    
    # Iterate over all possible word placements on the board (horizontally and vertically)
    for row in range(15):
        for col in range(15):
            # Try to form possible words horizontally and vertically
            for direction in ['H', 'V']:
                word = ""
                if direction == 'H':
                    # Get horizontal word
                    for c in range(col, 15):
                        if board[row][c] != '-':
                            word += board[row][c]
                        else:
                            break
                elif direction == 'V':
                    # Get vertical word
                    for r in range(row, 15):
                        if board[r][col] != '-':
                            word += board[r][col]
                        else:
                            break
                
                # Check if the word can be formed using the player's rack
                if word and all(word.count(l) <= player.rack.count(l) for l in word):
                    if word in wordlist:
                        possible_words.append(word)

    return possible_words


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
            first_move = computer_turn(current_player, board, wordlist, first_move)
        else:
            first_move = human_turn(current_player, board, wordlist, first_move)
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
