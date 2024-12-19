import random

TILE_BAG = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12, "F": 2, "G": 3, "H": 2, "I": 9,
    "J": 1, "K": 1, "L": 4, "M": 2, "N": 6, "O": 8, "P": 2, "Q": 1, "R": 6,
    "S": 4, "T": 6, "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2, "Z": 1, "@": 2  
}

LETTER_POINTS = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "@": 0
}

def draw_tiles(tile_bag, num=7):
    """Draws tiles from the tile bag."""
    tiles = []
    for _ in range(num):
        if not tile_bag:
            break
        tile = random.choice(list(tile_bag.keys()))
        tiles.append(tile)
        tile_bag[tile] -= 1
        if tile_bag[tile] == 0:
            del tile_bag[tile]
    return tiles



#function to calculate score
   
def calculate_score(word):

  score = 0
  letter_values = {
      'a': 1, 'e': 1, 'i': 1, 'o': 1, 'u': 1, 
      'l': 1, 'n': 1, 'r': 1, 's': 1, 't': 1, 
      'd': 2, 'g': 2, 
      'b': 3, 'c': 3, 'm': 3, 'p': 3, 
      'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 
      'k': 5, '@':0,
      'j': 8, 'x': 8, 
      'q': 10, 'z': 10,
  }

  for letter in word.lower():
    if letter in letter_values:
      score += letter_values[letter]

    return sum(LETTER_POINTS[letter] for letter in word.upper())

# # Example usage
# word = "HELLO"
# score = scrabble_score(word)
# print(f"The score of '{word}' is: {score}")