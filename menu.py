import pygame
import requests


class Menu:
    """ Creates menu """
    def __init__(self, game):
        self.game = game
        self.mid_width, self.mid_height = self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)                               # x, y, width, height
        self.offset = -100

    def draw_cursor(self):
        """ Helper function """
        self.game.draw_text('>', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        """ Helper function """
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    """ Main Menu that inherits from menu class """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.start_x, self.start_y, = self.mid_width, self.mid_height + 30
        self.options_x, self.options_y = self.mid_width, self.mid_height + 50
        self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)        # initial position for the cursor

    def display_menu(self):
        """ Displays the menu """
        self.run_display = True
        while self.run_display:
            self.game.check_events_pregame()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(self.game.text_archive.main_title, 40, self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2 - 30)
            self.game.draw_text(self.game.text_archive.main_start, 20, self.start_x, self.start_y)
            self.game.draw_text(self.game.text_archive.main_options, 20, self.options_x, self.options_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        """ Helper function """
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.options_x + self.offset, self.options_y)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.start_x + self.offset, self.start_y)
                self.state = 'Start'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.curr_menu = self.game.tutorial
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            self.run_display = False


class OptionsMenu(Menu):
    """ Initializes options menu """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Difficulty Level'
        self.diff_x, self.diff_y = self.mid_width, self.mid_height + 20
        self.lang_x, self.lang_y = self.mid_width, self.mid_height + 40
        self.cursor_rect.midtop = (self.diff_x + self.offset, self.diff_y)

    def display_menu(self):
        """ Displays the options menu """
        self.run_display = True
        while self.run_display:
            self.game.check_events_pregame()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text(self.game.text_archive.option_title, 30, self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2 - 30)
            self.game.draw_text(self.game.text_archive.option_diff, 20, self.diff_x, self.diff_y)
            self.game.draw_text(self.game.text_archive.option_lang, 20, self.lang_x, self.lang_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        """ Checks player input """
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Difficulty Level':
                self.state = 'Languages'
                self.cursor_rect.midtop = (self.lang_x + self.offset, self.lang_y)
            elif self.state == 'Languages':
                self.state = 'Difficulty Level'
                self.cursor_rect.midtop = (self.diff_x + self.offset, self.diff_y)
        if self.game.START_KEY:
            if self.state == 'Difficulty Level':
                self.game.curr_menu = self.game.difficulty
            elif self.state == 'Languages':
                self.game.curr_menu = self.game.languages
            self.run_display = False


class LanguagesMenu(Menu):
    """ Initializes languages menu """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'English'
        self.eng_x, self.eng_y = self.mid_width, self.mid_height + 20
        self.spn_x, self.spn_y = self.mid_width, self.mid_height + 40
        self.cursor_rect.midtop = (self.eng_x + self.offset, self.eng_y)

    def display_menu(self):
        """ Displays the languages menu """
        self.run_display = True
        while self.run_display:
            self.game.check_events_pregame()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text(self.game.text_archive.display_lang, 30, self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2 - 30)
            self.game.draw_text(self.game.text_archive.display_eng, 20, self.eng_x, self.eng_y)
            self.game.draw_text(self.game.text_archive.display_spn, 20, self.spn_x, self.spn_y)
            if self.game.english_yes:
                self.game.draw_text('Language set to English', 20, self.game.DISPLAY_WIDTH / 2,
                                    self.game.DISPLAY_HEIGHT / 2 - 90)
                self.game.text_archive.reset()
                self.game.english_yes = False
            elif self.game.spanish_yes:
                self.game.draw_text(self.game.text_archive.display_set, 20, self.game.DISPLAY_WIDTH / 2,
                                    self.game.DISPLAY_HEIGHT / 2 - 90)               # Language set to Spanish
                self.game.text_archive.spanish()
                self.game.spanish_yes = False
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        """ Checks player input """
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'English':
                self.state = 'Spanish'
                self.cursor_rect.midtop = (self.spn_x + self.offset, self.spn_y)
            elif self.state == 'Spanish':
                self.state = 'English'
                self.cursor_rect.midtop = (self.eng_x + self.offset, self.eng_y)
        if self.game.START_KEY:
            if self.state == 'English':
                self.game.english_yes = True
            elif self.state == 'Spanish':
                self.game.spanish_yes = True
            self.run_display = False


class DifficultyLevelMenu(Menu):
    """ Initializes difficulty menu """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Casual'
        self.casual_x, self.casual_y = self.mid_width, self.mid_height + 20
        self.exp_x, self.exp_y = self.mid_width, self.mid_height + 40
        self.cursor_rect.midtop = (self.casual_x + self.offset, self.casual_y)

    def display_menu(self):
        """ Displays the difficulty menu """
        self.run_display = True
        while self.run_display:
            self.game.check_events_pregame()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text(self.game.text_archive.diff_lvl, 30, self.game.DISPLAY_WIDTH/2, self.game.DISPLAY_HEIGHT/2 - 30)
            self.game.draw_text(self.game.text_archive.casual, 20, self.casual_x, self.casual_y)
            self.game.draw_text(self.game.text_archive.experienced, 20, self.exp_x, self.exp_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        """ Checks player input """
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Casual':
                self.state = 'Experienced'
                self.cursor_rect.midtop = (self.exp_x + self.offset, self.exp_y)
            elif self.state == 'Experienced':
                self.state = 'Casual'
                self.cursor_rect.midtop = (self.casual_x + self.offset, self.casual_y)


class TutorialMenu(Menu):
    """ Initializes tutorial menu """
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Yes'
        self.yes_x, self.yes_y = self.mid_width, self.mid_height + 20
        self.no_x, self.no_y = self.mid_width, self.mid_height + 40
        self.cursor_rect.midtop = (self.yes_x + self.offset, self.yes_y)

    def display_menu(self):
        """ Displays the tutorial menu """
        self.run_display = True
        while self.run_display:
            self.game.check_events_pregame()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text(self.game.text_archive.tutorial_menu, 17, self.game.DISPLAY_WIDTH/2,
                                self.game.DISPLAY_HEIGHT/2 - 30)
            self.game.draw_text(self.game.text_archive.tutorial_yes, 20, self.yes_x, self.yes_y)
            self.game.draw_text(self.game.text_archive.tutorial_no, 20, self.no_x, self.no_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        """ Checks player input """
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Yes':
                self.state = 'No'
                self.cursor_rect.midtop = (self.no_x + self.offset, self.no_y)
            elif self.state == 'No':
                self.state = 'Yes'
                self.cursor_rect.midtop = (self.yes_x + self.offset, self.yes_y)
        if self.game.START_KEY:
            if self.state == 'Yes':
                self.game.tutorial_yes = True
                self.game.playing = True
            elif self.state == 'No':
                self.game.tutorial_no = True
                self.game.playing = True
            self.run_display = False

class TutorialEndMenu(Menu):
    """ Initializes the dialogue/next level screen once tutorial is completed """
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        """ Displays the lake menu dialogue/level screen """
        self.run_display = True
        while self.run_display:
            self.game.check_events_pregame()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(self.game.text_archive.lake_text_1, 20,
                                self.game.DISPLAY_WIDTH / 2, self.game.DISPLAY_HEIGHT / 2 - 10)
            self.game.draw_text(self.game.text_archive.lake_text_2, 20,
                                self.game.DISPLAY_WIDTH / 2, self.game.DISPLAY_HEIGHT / 2 + 20)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        """ Checks player input """
        if self.game.START_KEY:
            pass