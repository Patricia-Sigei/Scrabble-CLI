from game import ScrabbleGame

if __name__ == "__main__":
    game = ScrabbleGame()
    print("Welcome to Scrabble CLI!")

    while True:
        game.play_turn()
        continue_game = input("Do you want to continue playing? (y/n): ").strip().lower()
        if continue_game != 'y':
            print("Thanks for playing Scrabble CLI!")
            break


