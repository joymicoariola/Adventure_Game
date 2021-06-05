import pygame
from units import *


class Level:
    """ Creates game Level """
    def __init__(self, game):
        self.game = game
        self.mid_width, self.mid_height = self.game.DISPLAY_WIDTH / 2, self.game.DISPLAY_HEIGHT / 2
        self.run_display = True
        self.offset = -100
        self.column_num = 8
        self.row_num = 8
        self.terrain_board = [[]]
        self.terrain_board_sprites = [[]]
        self.char_board = [[]]
        self.cursor = [0, 0]
        self.cursor_sprite = Cursor()
        self.tile = pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num)
        self.unit = pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num)
        self.cursor_rects = [pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num/10),
                             pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num/10, self.game.DISPLAY_HEIGHT/self.row_num),
                             pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num/10),
                             pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num/10, self.game.DISPLAY_HEIGHT/self.row_num)]

    def draw_board(self):
        monster_count = 0
        hero_count = 0
        tile_group = pygame.sprite.Group()
        sprites = pygame.sprite.Group()
        for i in range(self.row_num):
            for j in range(self.column_num):
                # DRAW TILES-----------------------------------------------------------------------------------------
                position = (self.game.DISPLAY_WIDTH / self.column_num * j,
                            self.game.DISPLAY_HEIGHT / self.row_num * i)
                if self.terrain_board[i][j] == 'g' or self.terrain_board[i][j] == 'd' or self.terrain_board[i][j] == '^'\
                        or self.terrain_board[i][j] == 's' or self.terrain_board[i][j] == 'f'\
                        or self.terrain_board[i][j] == 'c' or self.terrain_board[i][j] == 'w':
                    self.terrain_board_sprites[i][j].sprite.rect = position
                    tile_group.add(self.terrain_board_sprites[i][j].sprite)
                tile_group.draw(self.game.display)
                # HERO UNITS -----------------------------------------------------------------
                if self.char_board[i][j] != '':
                    position = (self.game.DISPLAY_WIDTH / self.column_num * j,
                                self.game.DISPLAY_HEIGHT / self.row_num * i)
                    if self.char_board[i][j].symbol == 'H' or self.char_board[i][j].symbol == 'M' or\
                            self.char_board[i][j].symbol == 'A' or self.char_board[i][j].symbol == 'T':
                        self.char_board[i][j].sprite.rect = position
                        sprites.add(self.char_board[i][j].sprite)
                        hero_count += 1
                    # MONSTER UNITS ----------------------------------------------------------------
                    if self.char_board[i][j].symbol == 'U' or self.char_board[i][j].symbol == 'I' or\
                            self.char_board[i][j].symbol == 'K' or self.char_board[i][j].symbol == 'O':
                        self.char_board[i][j].sprite.rect = position
                        sprites.add(self.char_board[i][j].sprite)
                        monster_count += 1
                # CURSOR -----------------------------------------------------------------------
                if j == self.cursor[0] and i == self.cursor[1]:
                    self.cursor_sprite.sprite.rect = position
                    sprites.add(self.cursor_sprite.sprite)
        sprites.draw(self.game.display)
        if hero_count == 0:
            self.game.lost_level = True
        if monster_count == 0:
            self.game.beat_level = True

    def load_tutorial_level(self):
        self.terrain_board = [['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd'],
                              ['d', 's', 's', 'd', 'd', 'd', 'd', 'd'],
                              ['d', 's', 'd', 'd', 'd', 'd', 'd', 'd'],
                              ['d', 'd', 'd', 'd', 'd', 's', 's', 'd'],
                              ['d', 'd', 'd', 'd', 'd', 's', 's', 'd'],
                              ['d', 'd', 'd', 'd', 'd', 'd', 'd', 'd'],
                              ['d', 's', 'd', 'd', 'd', 'd', 'd', 'd'],
                              ['s', 's', 'd', 'd', 'd', 'd', 'd', 'd']]
        self.terrain_board_sprites = [['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', '']]
        for i in range(len(self.terrain_board)):
            for j in range(len(self.terrain_board)):
                if self.terrain_board[i][j] == 'g':
                    self.terrain_board_sprites[i][j] = Grass()
                elif self.terrain_board[i][j] == 'd':
                    self.terrain_board_sprites[i][j] = Mud()
                elif self.terrain_board[i][j] == '^':
                    self.terrain_board_sprites[i][j] = Mountain()
                elif self.terrain_board[i][j] == 'f':
                    self.terrain_board_sprites[i][j] = Forest()
                elif self.terrain_board[i][j] == 's':
                    self.terrain_board_sprites[i][j] = Stone()
                elif self.terrain_board[i][j] == 'c':
                    self.terrain_board_sprites[i][j] = Castle()
                elif self.terrain_board[i][j] == 'w':
                    self.terrain_board_sprites[i][j] = Water()
        self.char_board = [['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '']]
        self.char_board[2][5] = MudMuck()
        self.char_board[5][5] = MudMuck()
        self.char_board[6][0] = MudMuck()
        self.char_board[6][3] = MudMuck()
        self.char_board[7][7] = MudMuck()
        # ------------------------------------------------------
        self.char_board[4][3] = Hero()
        self.char_board[4][4] = Archer()
        self.char_board[3][3] = Mage()
        self.char_board[3][2] = Knight()

    def load_level_1(self):
        self.terrain_board = [['g', 'g', 'g', 'g', 'g', 'g', 'g', '^'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['g', 'g', 'w', 'w', 'w', 'g', 'g', 'g'],
                              ['g', 'w', 'w', 'w', 'w', 'w', 'g', 'g'],
                              ['g', 'w', 'w', 'w', 'w', '^', '^', 'g'],
                              ['g', 'g', 'w', 'w', '^', 'g', 'g', 'g'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['^', 'g', 'g', 'g', 'g', 'g', 'g', '^']]
        self.terrain_board_sprites = [['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', '']]
        for i in range(len(self.terrain_board)):
            for j in range(len(self.terrain_board)):
                if self.terrain_board[i][j] == 'g':
                    self.terrain_board_sprites[i][j] = Grass()
                elif self.terrain_board[i][j] == 'd':
                    self.terrain_board_sprites[i][j] = Mud()
                elif self.terrain_board[i][j] == '^':
                    self.terrain_board_sprites[i][j] = Mountain()
                elif self.terrain_board[i][j] == 'f':
                    self.terrain_board_sprites[i][j] = Forest()
                elif self.terrain_board[i][j] == 's':
                    self.terrain_board_sprites[i][j] = Stone()
                elif self.terrain_board[i][j] == 'c':
                    self.terrain_board_sprites[i][j] = Castle()
                elif self.terrain_board[i][j] == 'w':
                    self.terrain_board_sprites[i][j] = Water()
        self.char_board = [['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '']]
        self.char_board[0][6] = Skeletons()
        self.char_board[1][6] = Skeletons()
        self.char_board[2][1] = Slimes()
        self.char_board[3][0] = Slimes()
        self.char_board[4][0] = Slimes()
        self.char_board[5][1] = Slimes()
        self.char_board[7][6] = Skeletons()
        # --------------------------------------------------------
        self.char_board[6][5] = Hero()
        self.char_board[6][4] = Knight()
        self.char_board[5][5] = Mage()
        self.char_board[5][6] = Archer()

    def load_final_level(self):
        self.terrain_board = [['^', '^', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['^', 'g', 'c', 'c', 'c', 'c', 'c', 'g'],
                              ['g', 'g', 'c', 'c', 'c', 'c', 'c', 'g'],
                              ['g', 'g', 'f', 'g', 'g', 'g', 'f', 'g'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'f', 'f'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['g', 'g', 'g', 'g', 'g', 'f', 'f', 'g'],
                              ['f', 'g', 'g', 'g', 'g', 'g', 'g', 'g']]
        self.terrain_board_sprites = [['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', ''],
                                      ['', '', '', '', '', '', '', '']]
        for i in range(len(self.terrain_board)):
            for j in range(len(self.terrain_board)):
                if self.terrain_board[i][j] == 'g':
                    self.terrain_board_sprites[i][j] = Grass()
                elif self.terrain_board[i][j] == 'd':
                    self.terrain_board_sprites[i][j] = Mud()
                elif self.terrain_board[i][j] == '^':
                    self.terrain_board_sprites[i][j] = Mountain()
                elif self.terrain_board[i][j] == 'f':
                    self.terrain_board_sprites[i][j] = Forest()
                elif self.terrain_board[i][j] == 's':
                    self.terrain_board_sprites[i][j] = Stone()
                elif self.terrain_board[i][j] == 'c':
                    self.terrain_board_sprites[i][j] = Castle()
                elif self.terrain_board[i][j] == 'w':
                    self.terrain_board_sprites[i][j] = Water()
        self.char_board = [['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', '']]
        self.char_board[2][7] = Slimes()
        self.char_board[3][1] = Slimes()
        self.char_board[6][0] = Slimes()
        self.char_board[3][3] = Skeletons()
        self.char_board[3][4] = Skeletons()
        self.char_board[3][5] = Skeletons()
        self.char_board[1][3] = Ogres()
        self.char_board[1][4] = Ogres()
        self.char_board[1][5] = Ogres()
        # -------------------------------------------
        self.char_board[6][2] = Hero()
        self.char_board[6][3] = Knight()
        self.char_board[7][2] = Archer()
        self.char_board[7][3] = Mage()
