class Player:
    def __init__(self, name):
        self.name = name
        self.tiles = []  # Player's current tiles

    def assign_blank_tile(self, target_letter):
        """
        Replace a blank tile ('_') in the player's tiles with the specified letter.
        """
        if '_' in self.tiles:
            self.tiles.remove('_')
            self.tiles.append(target_letter.upper())  # Assign the blank tile
            print(f"Blank tile successfully assigned as '{target_letter}'.")
        else:
            print("No blank tiles available to assign.")

    def display_tiles(self):
        print(f"{self.name}'s tiles: {', '.join(self.tiles)}")
