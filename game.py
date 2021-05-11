import pygame
from menu import *


class Game():
    def __init__(self):
        """ Initialize the game screen """
        pygame.init()
        self.running, self.playing = True, False                                                # opens game
        self.tutorial_yes, self.tutorial_no = False, False
        self.english_yes, self.spanish_yes = False, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False  # iterate through menu
        self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT = 640, 480
        self.display = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.window = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        # self.font_name = 'VCR_OSD_MONO_1.001.TTF'
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.languages = LanguagesMenu(self)
        self.difficulty = DifficultyLevelMenu(self)
        self.tutorial = TutorialMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        if self.tutorial_yes:
            while self.playing:                                                            # checks what player inputs
                self.check_events()
                if self.START_KEY:
                    self.playing = False
                self.display.fill(self.BLACK)
                self.draw_text('As you and your team gathered your belongings,', 20,
                               self.DISPLAY_WIDTH/2, self.DISPLAY_HEIGHT/2 - 10)     # txt, size, pos
                self.draw_text('you were suddenly ambushed by mud mucks!', 20,
                               self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 + 20)  # txt, size, pos
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()
        elif self.tutorial_no:
            while self.playing:                                                            # checks what player inputs
                self.check_events()
                if self.START_KEY:
                    self.playing = False
                self.display.fill(self.BLACK)
                self.draw_text('Miraculously, you were able to avoid the mud mucks,', 20,
                               self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 - 10)  # txt, size, pos
                self.draw_text('Your party continued to travel to the swamp.', 20,
                               self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 + 20)  # txt, size, pos
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()

    def check_events(self):
        """ Check player input """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                               # player wants to close window
                self.running, self.playing = False, False
                self.curr_menu.run_display = False                                      # stop w/e menu from being run
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        """ If player is not clicking a key, prevents continuous input  """
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, = False, False, False, False

    def draw_text(self, text, size, x, y):
        """ Displays text """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

