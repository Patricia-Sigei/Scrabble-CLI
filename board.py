class Board:
    def __init__(self):
        self.grid = [[" " for _ in range(15)] for _ in range(15)]  # 15x15 grid

    def display(self):
        for row in self.grid:
            print(" | ".join(row))
        print("\n")

    def place_tiles(self, word, start_pos, direction, player):
        """
        Place a word on the board, handling blank tiles correctly.
        """
        row, col = start_pos
        for i, letter in enumerate(word):
            if letter in player.tiles or letter == '_':
                if letter == '_':
                    assigned_letter = input(f"Enter the letter for blank tile at ({row}, {col}): ").strip().upper()
                    player.assign_blank_tile(assigned_letter)
                    self.grid[row][col] = assigned_letter.upper()
                else:
                    self.grid[row][col] = letter.upper()
                    player.tiles.remove(letter)

            # Adjust position for word placement
            if direction == 'horizontal':
                col += 1
            elif direction == 'vertical':
                row += 1
