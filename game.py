import requests
from menu import *
from level import *
from units import *


class Game:
    def __init__(self):
        """ Initialize the game screen """
        pygame.init()
        self.running, self.playing = True, False                                                # opens game
        self.tutorial_yes, self.tutorial_no = False, False
        self.english_yes, self.spanish_yes = False, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False  # iterate through menu
        self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT = 640, 640
        self.display = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        self.window = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT))
        # self.font_name = 'VCR_OSD_MONO_1.001.TTF'
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.languages = LanguagesMenu(self)
        self.difficulty = DifficultyLevelMenu(self)
        self.lake_menu = TutorialEndMenu(self)
        self.tutorial = TutorialMenu(self)
        self.curr_menu = self.main_menu
        self.began_level = False
        self.beat_level = False
        self.lost_level = False
        self.picking_destination = False
        self.old_pos = [0, 0]
        self.text_archive = Text()
        self.text_archive.reset()

    def game_loop(self):
        if self.tutorial_yes:
            # PRE-GAME TEXT----------------------------------------
            while self.playing:                                                            # checks what player inputs
                self.check_events_pregame()
                if self.START_KEY:
                    self.playing = False
                self.display.fill(self.BLACK)
                self.draw_text(self.text_archive.tutorial_yes_1, 20,
                               self.DISPLAY_WIDTH/2, self.DISPLAY_HEIGHT/2 - 10)     # txt, size, pos
                self.draw_text(self.text_archive.tutorial_yes_2, 20,
                               self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 + 20)  # txt, size, pos
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()
            self.began_level = True
            self.tutorial_yes = False
        elif self.tutorial_no:
            while self.playing:                                                            # checks what player inputs
                self.check_events_pregame()
                if self.START_KEY:
                    self.playing = False
                self.display.fill(self.BLACK)
                self.draw_text(self.text_archive.tutorial_no_1, 20,
                               self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 - 10)  # txt, size, pos
                self.draw_text(self.text_archive.tutorial_no_2, 20,
                               self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 + 20)  # txt, size, pos
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()
            self.began_level = True
            self.tutorial_no = False
        # LEVEL BEGINS -------------------------------------------------------------------------------------------
        if self.began_level:
            self.playing = True
            level = Level(self)
            level.load_tutorial_level()                               # LOADS LEVEL !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            while self.playing:
                self.check_events_gameplay()
                if self.UP_KEY:
                    if level.cursor[1] > 0:
                        level.cursor[1] -= 1
                if self.DOWN_KEY:
                    if level.cursor[1] < level.row_num - 1:
                        level.cursor[1] += 1
                if self.LEFT_KEY:
                    if level.cursor[0] > 0:
                        level.cursor[0] -= 1
                if self.RIGHT_KEY:
                    if level.cursor[0] < level.column_num - 1:
                        level.cursor[0] += 1
                if self.START_KEY:
                    space = level.char_board[level.cursor[1]][level.cursor[0]]
                    if not self.picking_destination:
                        if space != '':
                            if space.player_unit:
                                self.picking_destination = True
                                self.old_pos = [level.cursor[0], level.cursor[1]]
                    else:
                        if space == '' and level.terrain_board[level.cursor[1]][level.cursor[0]] != 'w':
                            level.char_board[level.cursor[1]][level.cursor[0]] = level.char_board[self.old_pos[1]][self.old_pos[0]]
                            level.char_board[self.old_pos[1]][self.old_pos[0]] = ''
                            self.picking_destination = False
                        if not level.char_board[level.cursor[1]][level.cursor[0]].player_unit:
                            monster = level.char_board[level.cursor[1]][level.cursor[0]]
                            player_unit = level.char_board[self.old_pos[1]][self.old_pos[0]]
                            self.attack(player_unit, [self.old_pos[0], self.old_pos[1]], monster, [level.cursor[0], level.cursor[1]], level.char_board)
                self.display.fill(self.WHITE)
                level.draw_board()
                if self.lost_level:
                    break
                elif self.beat_level:
                    self.curr_menu = self.lake_menu
                    break
                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()

    def check_events_pregame(self):
        """ Check player input in the menus """
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

    def check_events_gameplay(self):
        """ Check player input during gameplay """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_keys(self):
        """ If player is not clicking a key, prevents continuous input  """
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY, = False, False, False, False, False, False

    def draw_text(self, text, size, x, y):
        """ Displays text """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def attack(self, attacker, attacker_coord, target, target_coord, board):
        damage = attacker.physical_atk - target.physical_def
        target.hp = target.hp - damage
        if target.hp <= 0:
            board[target_coord[1]][target_coord[0]] = ''
            return
        damage = target.physical_atk - attacker.physical_def
        attacker.hp = attacker.hp - damage
        if attacker.hp <= 0:
            board[attacker_coord[1]][attacker_coord[0]] = ''


class Text:
    """ Allows translation implementation """
    def reset(self):
        """ Resets the text to English """
        self.main_title = 'Adventure Game'
        self.main_start = 'Start Game'
        self.main_options = 'Options'
        # ----------------------------------------
        self.option_title = 'Options'
        self.option_diff = 'Difficulty Level'
        self.option_lang = 'Language'
        # ----------------------------------------
        self.display_lang = 'Language'
        self.display_eng = 'English'
        self.display_spn = 'Spanish'
        self.display_set = 'Language set to Spanish'
        # ----------------------------------------
        self.diff_lvl = 'Difficulty Level'
        self.casual = 'Casual'
        self.experienced = 'Experienced'
        # ----------------------------------------
        self.tutorial_menu = 'Do you want to be shown how to play?'
        self.tutorial_yes = 'Yes'
        self.tutorial_no = 'No'
        # ----------------------------------------
        self.tutorial_yes_1 = 'As you and your team gathered your belongings,'
        self.tutorial_yes_2 = 'you were suddenly ambushed by mud monsters.'
        self.tutorial_no_1 = 'Miraculously, you were able to avoid the mud monsters,'
        self.tutorial_no_2 = 'Your party continued to travel to the lake.'
        # ----------------------------------------
        self.lake_text_1 = 'After defeating the mud monsters, your party'
        self.lake_text_2 = 'continued to travel to the lake.'

    def spanish(self):
        self.main_title = self.post_translate(self.main_title)
        self.main_start = self.post_translate(self.main_start)
        self.main_options = self.post_translate(self.main_options)
        # ----------------------------------------
        self.option_title = self.post_translate(self.option_title)
        self.option_diff = self.post_translate(self.option_diff)
        self.option_lang = self.post_translate(self.option_lang)
        # ----------------------------------------
        self.display_lang = self.post_translate(self.display_lang)
        self.display_eng = self.post_translate(self.display_eng)
        self.display_spn = self.post_translate(self.display_spn)
        self.display_set = self.post_translate(self.display_set)
        # ----------------------------------------
        self.diff_lvl = self.post_translate(self.diff_lvl)
        self.casual = self.post_translate(self.casual)
        self.experienced = self.post_translate(self.experienced)
        # ----------------------------------------
        self.tutorial_menu = self.post_translate(self.tutorial_menu)
        self.tutorial_yes = self.post_translate(self.tutorial_yes)
        self.tutorial_no = self.post_translate(self.tutorial_no)
        # ----------------------------------------
        self.tutorial_yes_1 = self.post_translate(self.tutorial_yes_1)
        self.tutorial_yes_2 = self.post_translate(self.tutorial_yes_2)
        self.tutorial_no_1 = self.post_translate(self.tutorial_no_1)
        self.tutorial_no_2 = self.post_translate(self.tutorial_no_2)
        # ----------------------------------------
        self.lake_text_1 = self.post_translate(self.lake_text_1)
        self.lake_text_2 = self.post_translate(self.lake_text_2)

    def post_translate(self, text):
        my_obj = {"destLang": "Spanish", "translate_text": text}
        response = requests.post('http://flip1.engr.oregonstate.edu:1992/post/', json=my_obj)
        my_dict = response.json()
        return my_dict["translation"]