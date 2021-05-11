import pygame
from game import *
from menu import *

g = Game()

# ----------- GAME LOOP ----------- #
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()

