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
        self.char_board = [[]]
        self.cursor = [0, 0]
        self.tile = pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num)
        self.unit = pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num)
        self.cursor_rects = [pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num/10),
                             pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num/10, self.game.DISPLAY_HEIGHT/self.row_num),
                             pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num, self.game.DISPLAY_HEIGHT/self.row_num/10),
                             pygame.Rect(0, 0, self.game.DISPLAY_WIDTH/self.column_num/10, self.game.DISPLAY_HEIGHT/self.row_num)]

    def draw_board(self):
        monster_count = 0
        hero_count = 0
        for i in range(self.row_num):
            for j in range(self.column_num):
                # DRAW TILES-----------------------------------------------------------------------------------------
                cur_rect = self.tile
                cur_rect.update(self.game.DISPLAY_WIDTH / self.column_num * j,
                                self.game.DISPLAY_HEIGHT / self.row_num * i,
                                self.game.DISPLAY_WIDTH / self.column_num, self.game.DISPLAY_HEIGHT / self.row_num)
                if self.terrain_board[i][j] == 'g':
                    pygame.draw.rect(self.game.display, (0, 255, 0), cur_rect)
                if self.terrain_board[i][j] == 'd':
                    pygame.draw.rect(self.game.display, (200, 200, 100), cur_rect)
                if self.terrain_board[i][j] == '^':
                    pygame.draw.rect(self.game.display, (255, 0, 0), cur_rect)
                if self.terrain_board[i][j] == 's':
                    pygame.draw.rect(self.game.display, (100, 100, 100), cur_rect)
                if self.terrain_board[i][j] == 'f':
                    pygame.draw.rect(self.game.display, (0, 175, 0), cur_rect)
                if self.terrain_board[i][j] == 'c':
                    pygame.draw.rect(self.game.display, (50, 50, 50), cur_rect)
                if self.terrain_board[i][j] == 'w':
                    pygame.draw.rect(self.game.display, (0, 0, 255), cur_rect)
                # DRAW UNITS-----------------------------------------------------------------------------------------
                center = (self.game.DISPLAY_WIDTH / self.column_num * j + self.game.DISPLAY_WIDTH / self.column_num/2,
                          self.game.DISPLAY_HEIGHT / self.row_num * i + self.game.DISPLAY_HEIGHT / self.row_num/2)
                radius = (self.game.DISPLAY_HEIGHT / self.row_num)/2 - ((self.game.DISPLAY_HEIGHT / self.row_num)/16)
                # HERO UNITS -----------------------------------------------------------------
                if self.char_board[i][j] != '':
                    if self.char_board[i][j].symbol == 'H':                        # hero character
                        pygame.draw.circle(self.game.display, (230, 10, 0), center, radius)
                        hero_count += 1
                    if self.char_board[i][j].symbol == 'M':                        # mage character
                        pygame.draw.circle(self.game.display, (0, 100, 0), center, radius)
                        hero_count += 1
                    if self.char_board[i][j].symbol == 'A':                        # archer character
                        pygame.draw.circle(self.game.display, (0, 0, 100), center, radius)
                        hero_count += 1
                    if self.char_board[i][j].symbol == 'T':                        # knight character
                        pygame.draw.circle(self.game.display, (0, 50, 50), center, radius)
                        hero_count += 1
                    # MONSTER UNITS ----------------------------------------------------------------
                    if self.char_board[i][j].symbol == 'U':                        # mud mucks
                        pygame.draw.circle(self.game.display, (0, 0, 0), center, radius)
                        monster_count += 1
                    if self.char_board[i][j].symbol == 'I':                        # slimes
                        pygame.draw.circle(self.game.display, (100, 0, 50), center, radius)
                        monster_count += 1
                    if self.char_board[i][j].symbol == 'K':                        # skeletons
                        pygame.draw.circle(self.game.display, (20, 40, 60), center, radius)
                        monster_count += 1
                    if self.char_board[i][j].symbol == 'O':                        # ogres
                        pygame.draw.circle(self.game.display, (50, 10, 10), center, radius)
                        monster_count += 1
                # CURSOR -----------------------------------------------------------------------
                if j == self.cursor[0] and i == self.cursor[1]:
                    self.cursor_rects[0].update(self.game.DISPLAY_WIDTH / self.column_num * j,
                                                self.game.DISPLAY_HEIGHT / self.row_num * i,
                                                self.game.DISPLAY_WIDTH / self.column_num,
                                                self.game.DISPLAY_HEIGHT / self.row_num / 10)
                    pygame.draw.rect(self.game.display, (255, 255, 255), self.cursor_rects[0])
                    self.cursor_rects[1].update(self.game.DISPLAY_WIDTH / self.column_num * j + (self.game.DISPLAY_WIDTH / self.column_num / 10) * 9,
                                                self.game.DISPLAY_HEIGHT / self.row_num * i,
                                                self.game.DISPLAY_WIDTH / self.column_num / 10,
                                                self.game.DISPLAY_HEIGHT / self.row_num)
                    pygame.draw.rect(self.game.display, (255, 255, 255), self.cursor_rects[1])
                    self.cursor_rects[2].update(self.game.DISPLAY_WIDTH / self.column_num * j,
                                                self.game.DISPLAY_HEIGHT / self.row_num * i + (self.game.DISPLAY_WIDTH / self.column_num / 10) * 9,
                                                self.game.DISPLAY_WIDTH / self.column_num,
                                                self.game.DISPLAY_HEIGHT / self.row_num / 10)
                    pygame.draw.rect(self.game.display, (255, 255, 255), self.cursor_rects[2])
                    self.cursor_rects[3].update(self.game.DISPLAY_WIDTH / self.column_num * j,
                                                self.game.DISPLAY_HEIGHT / self.row_num * i,
                                                self.game.DISPLAY_WIDTH / self.column_num / 10,
                                                self.game.DISPLAY_HEIGHT / self.row_num)
                    pygame.draw.rect(self.game.display, (255, 255, 255), self.cursor_rects[3])
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
        self.char_board = [['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '']]
        self.char_board[1][4] = MudMuck()
        self.char_board[4][3] = Hero()
        """self.char_board = [['', '', '', '', '', '', '', ''],
                           ['', '', '', '', 'U', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', 'T', 'M', '', '', '', ''],
                           ['', '', '', 'H', 'A', '', '', ''],
                           ['', '', '', '', '', 'U', '', ''],
                           ['U', '', 'U', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', 'U']]"""

    def load_level_1(self):
        self.terrain_board = [['g', 'g', 'g', 'g', 'g', 'g', 'g', '^'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['g', 'g', 'w', 'w', 'w', 'g', 'g', 'g'],
                              ['g', 'w', 'w', 'w', 'w', 'w', 'g', 'g'],
                              ['g', 'w', 'w', 'w', 'w', '^', '^', 'g'],
                              ['g', 'g', 'w', 'w', '^', 'g', 'g', 'g'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['^', 'g', 'g', 'g', 'g', 'g', 'g', '^']]
        self.char_board = [['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', ''],
                            ['', '', '', '', '', '', '', '']]
        self.char_board[0][0] = MudMuck()
        self.char_board[7][7] = Hero()

    def load_final_level(self):
        self.terrain_board = [['^', '^', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['^', 'g', 'c', 'c', 'c', 'c', 'c', 'g'],
                              ['g', 'g', 'c', 'c', 'c', 'c', 'c', 'g'],
                              ['g', 'g', 'f', 'g', 'g', 'g', 'f', 'g'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'f', 'f'],
                              ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'],
                              ['g', 'g', 'g', 'g', 'g', 'f', 'f', 'g'],
                              ['f', 'g', 'g', 'g', 'g', 'g', 'g', 'g']]
        self.char_board = [['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', ''],
                           ['', '', '', '', '', '', '', '']]
        self.char_board[0][0] = MudMuck()
        self.char_board[7][7] = Hero()
