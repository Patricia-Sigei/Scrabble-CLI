 # Update player's rack, skipping letters that were on the board
                    for letter in word:
                        if letter in player_rack:
                            player_rack.remove(letter)
                    player_rack = replenish_rack(player_rack)