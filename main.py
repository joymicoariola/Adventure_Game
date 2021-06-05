from game import *

g = Game()

# ----------- GAME LOOP ----------- #
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
