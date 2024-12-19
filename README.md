# Scrabble CLI

This is a command-line interface (CLI) application for playing Scrabble.
Phase 3 final project.

## Setup

1. Clone the repository:
    ```sh
    git clone git@github.com:Patricia-Sigei/Scrabble-CLI.git
    cd Scrabble-CLI
    ```

2. Create a Python environment using `pipenv`:
    ```sh
    pipenv install
    ```

3. Install the required dependencies:
    ```sh
    pipenv run pip install requests
    ```

---

## Usage

To start the application, run:
```sh
pipenv run python main.py
```

---

## Features

- **Valid Word Verification**: Ensures words are valid using a Scrabble dictionary.
- **Bonus Tiles**: Includes `TW` (Triple Word), `DW` (Double Word), `TL` (Triple Letter), and `DL` (Double Letter) tiles.
- **Adjacency Rules**: Ensures new words are adjacent to existing tiles.
- **Crossword Validation**: Verifies all newly formed words.
- **Computer AI**: A computer player intelligently selects and places valid words.

---

## How to Play

1. Run the game using the command:
    ```sh
    pipenv run python main.py
    ```

2. Follow the prompts:
    - Choose a game mode (e.g., Human vs. Computer).
    - Input your word, start position, and direction during your turn.

3. Example game flow:
    ```
    Welcome to Scrabble!
    Choose game mode:
    1. Human vs Computer
    2. Human vs Human
    3. Two Humans vs Computer
    Enter 1, 2, or 3: 1

    Game begins! The first word must cover the center tile (7,7).
    Human's turn. Your rack: A E T R S T N
    Enter a word to place (or 's' to skip, 'q' to quit): START
    Enter start row (0-14): 7
    Enter start column (0-14): 7
    Enter direction (H for horizontal, V for vertical): H
    ```

---

## Game Logic

### Board Setup
- The board is a 15x15 grid.
- Special tiles (`TW`, `DW`, `TL`, `DL`) and a center star tile (`*`) are added.

### Word Validation
- Words must be valid according to the dictionary.
- New words must connect with existing tiles or cover the center tile during the first move.
- Adjacent crosswords are also validated.

### Scoring
- Each letter has a predefined value.
- Special tiles multiply scores for letters or words.

### Computer AI
- The computer generates valid moves by scanning the board for anchor points and selecting words from its rack.

---

## Development Steps

1. **Board Creation**:
    - Created a 15x15 grid.
    - Added special score tiles like `TW`, `DW`, `TL`, `DL`.

2. **Wordlist Integration**:
    - Downloaded a Scrabble wordlist.
    - Loaded the wordlist into a set for efficient lookup.

3. **Validation Logic**:
    - Ensured words fit the board and adhere to adjacency rules.
    - Validated primary words and crosswords.

4. **Game Modes**:
    - Developed Human vs. Computer, Human vs. Human, and Two Humans vs. Computer.

5. **Scoring**:
    - Implemented point calculations for letters and bonus tiles.

---

## Contributors

For questions, suggestions, or issues, please reach out to:

- GitHub:  
  [Emily](https://github.com/Emily-art3)  
  [Patricia](https://github.com/Patricia-Sigei)  
  [Anita](https://github.com/awangui)  
  [Wilson](https://github.com/willisntannpc)  
  [Victor](https://github.com/flakegotgame)  

---

## License

This project is licensed under the MIT License.
