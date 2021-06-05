import requests
from menu import *
from level import *
from units import *


class Game:
    def __init__(self):
        """ Initialize the game screen """
        pygame.init()
        self.running, self.is_playing = True, False
        self.tutorial_yes, self.tutorial_no = False, False
        self.english_yes, self.spanish_yes = False, False
        self.diff_experienced = False
        self.casual_yes, self.experienced_yes = False, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False  # iterate through menu
        self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT = 640, 640
        self.BAR_WIDTH, self.BAR_HEIGHT = 640, 150
        self.display = pygame.Surface((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT + self.BAR_HEIGHT))
        self.window = pygame.display.set_mode((self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT + self.BAR_HEIGHT))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.languages = LanguagesMenu(self)
        self.difficulty = DifficultyLevelMenu(self)
        self.lake_menu = TutorialEndMenu(self)
        self.tutorial = TutorialMenu(self)
        self.curr_menu = self.main_menu
        self.curr_level = "Menus"
        self.began_level, self.beat_level, self.lost_level = False, False, False
        self.picking_destination = False
        self.picking_target = False
        self.old_pos = [0, 0]
        self.text_archive = Text()
        self.text_archive.reset()
        self.terrain_info, self.unit_info = "No terrain", "No unit"
        self.help_text = "Select a unit to command."

    def game_loop(self):
        if self.tutorial_yes:
            # PRE-GAME TEXT----------------------------------------
            self.curr_level = "Tutorial Level"
            while self.is_playing:                                                            # checks what player inputs
                self.check_events_pregame()
                if self.START_KEY:
                    self.is_playing = False
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
            self.curr_level = "Level 1"
            while self.is_playing:
                # checks what player inputs
                self.check_events_pregame()
                if self.START_KEY:
                    self.is_playing = False
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
            level = Level(self)
            while self.curr_level != "Game Completed":
                if self.curr_level == "Tutorial Level":
                    level.load_tutorial_level()
                elif self.curr_level == "Level 1":
                    level.load_level_1()
                elif self.curr_level == "Final Level":
                    level.load_final_level()
                if self.diff_experienced:
                    self.apply_difficulty(level.char_board)
                self.is_playing = True
                while self.is_playing:
                    self.check_events_gameplay()
                    if self.UP_KEY:
                        if level.cursor[1] > 0 and self.allow_cursor("Up", level.cursor, self.old_pos, self.picking_destination, self.picking_target, level.char_board):
                            level.cursor[1] -= 1
                    if self.DOWN_KEY:
                        if level.cursor[1] < level.row_num - 1 and self.allow_cursor("Down", level.cursor, self.old_pos, self.picking_destination, self.picking_target, level.char_board):
                            level.cursor[1] += 1
                    if self.LEFT_KEY:
                        if level.cursor[0] > 0 and self.allow_cursor("Left", level.cursor, self.old_pos, self.picking_destination, self.picking_target, level.char_board):
                            level.cursor[0] -= 1
                    if self.RIGHT_KEY:
                        if level.cursor[0] < level.column_num - 1 and self.allow_cursor("Right", level.cursor, self.old_pos, self.picking_destination, self.picking_target, level.char_board):
                            level.cursor[0] += 1
                    if self.START_KEY:
                        space = level.char_board[level.cursor[1]][level.cursor[0]]
                        if not self.picking_destination:
                            if space != '':
                                if space.player_unit:
                                    self.picking_destination = True
                                    self.old_pos = [level.cursor[0], level.cursor[1]]
                        else:
                            if space == '' and level.terrain_board[level.cursor[1]][level.cursor[0]] == 'w':
                                pass
                            elif space == '':
                                level.char_board[level.cursor[1]][level.cursor[0]] = level.char_board[self.old_pos[1]][self.old_pos[0]]
                                level.char_board[self.old_pos[1]][self.old_pos[0]] = ''
                                self.picking_destination = False
                            elif not level.char_board[level.cursor[1]][level.cursor[0]].player_unit:
                                monster = level.char_board[level.cursor[1]][level.cursor[0]]
                                player_unit = level.char_board[self.old_pos[1]][self.old_pos[0]]
                                self.attack(player_unit, [self.old_pos[0], self.old_pos[1]], monster, [level.cursor[0], level.cursor[1]], level.char_board)
                                self.picking_destination = False
                    if self.BACK_KEY:
                        if self.picking_destination:
                            self.picking_destination = False
                    if not self.picking_destination:
                        self.help_text = self.text_archive.help_unit
                    else:
                        self.help_text = self.text_archive.help_dest
                    self.display.fill(self.BLACK)
                    level.draw_board()
                    # Tutorial Instructions -------------------------------------------------------------
                    if self.curr_level == 'Tutorial Level':
                        self.draw_text(self.text_archive.instructions_controls1, 15, self.DISPLAY_WIDTH / 2, 16)
                        self.draw_text(self.text_archive.instructions_controls2, 15, self.DISPLAY_WIDTH / 2, 33)
                        self.draw_text(self.text_archive.instructions_controls3, 15, self.DISPLAY_WIDTH / 2, 48)
                        self.draw_text(self.text_archive.instructions_goal, 15, self.DISPLAY_WIDTH / 2, 63)
                        self.draw_text(self.text_archive.instructions_phymag, 15, self.DISPLAY_WIDTH / 2, 78)
                    # -----------------------------------------------------------------------------------
                    if self.lost_level:
                        self.intermission_screen("Game Over")
                        self.beat_level = False
                        self.lost_level = False
                        self.is_playing = False
                    elif self.beat_level:
                        if self.curr_level == "Tutorial Level":
                            self.intermission_screen("Tutorial Level")
                            self.curr_level = "Level 1"
                            self.beat_level = False
                        elif self.curr_level == "Level 1":
                            self.intermission_screen("Level 1")
                            self.curr_level = "Final Level"
                            self.beat_level = False
                        elif self.curr_level == "Final Level":
                            self.intermission_screen("Final Level")
                        self.is_playing = False
                    self.get_tile_info(level.cursor[0], level.cursor[1], level.terrain_board, level.char_board)
                    self.draw_text(self.help_text, 20, self.BAR_WIDTH/2 - 100, self.DISPLAY_HEIGHT + self.BAR_HEIGHT/2)
                    self.window.blit(self.display, (0, 0))
                    pygame.display.update()
                    self.reset_keys()

    def intermission_screen(self, beaten_level):
        """ Display an intermission screen """
        freeze_game = False
        message1 = "ERROR"
        message2 = "ERROR"
        if beaten_level == "Tutorial Level":
            message1 = self.text_archive.lake_text_1
            message2 = self.text_archive.lake_text_2
        elif beaten_level == "Level 1":
            message1 = self.text_archive.castle_text_1
            message2 = self.text_archive.castle_text_2
        elif beaten_level == "Final Level":
            message1 = self.text_archive.final_text_1
            message2 = self.text_archive.final_text_2
            freeze_game = True
        elif beaten_level == "Game Over":
            message1 = self.text_archive.game_over_1
            message2 = self.text_archive.game_over_2
        looping = True
        self.reset_keys()
        while looping:
            # checks what player inputs
            self.check_events_pregame()
            if self.START_KEY and not freeze_game:
                looping = False
            self.display.fill(self.BLACK)
            self.draw_text(message1, 15,
                           self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 - 10)  # txt, size, pos
            self.draw_text(message2, 15,
                           self.DISPLAY_WIDTH / 2, self.DISPLAY_HEIGHT / 2 + 20)  # txt, size, pos
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def check_events_pregame(self):
        """ Check player input in the menus """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                               # player wants to close window
                self.running, self.is_playing = False, False
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
                self.running, self.is_playing = False, False
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
        """ Have a unit attack another unit """
        if attacker.name == "Mage":
            damage = attacker.magic_atk - target.magic_def
            target.hp = target.hp - damage
            if target.hp <= 0:
                board[target_coord[1]][target_coord[0]] = ''
                return
            if target.name == "Skeleton":
                damage = target.magic_atk - attacker.magic_def
                attacker.hp = attacker.hp - damage
            else:
                damage = target.physical_atk - attacker.physical_def
                attacker.hp = attacker.hp - damage
        else:
            damage = attacker.physical_atk - target.physical_def
            target.hp = target.hp - damage
            if target.hp <= 0:
                board[target_coord[1]][target_coord[0]] = ''
                return
            if target.name == "Skeleton":
                damage = target.magic_atk - attacker.magic_def
                attacker.hp = attacker.hp - damage
            else:
                damage = target.physical_atk - attacker.physical_def
                attacker.hp = attacker.hp - damage
        if attacker.hp <= 0:
            board[attacker_coord[1]][attacker_coord[0]] = ''

    def allow_cursor(self, direction, cursor_pos, old_pos, picking_destination, picking_target, char_board):
        """ Returns a boolean representing whether the cursor is allowed to make the proposed move """
        if picking_destination:
            if direction == "Up":
                if abs(old_pos[0] - cursor_pos[0]) + abs(old_pos[1] - (cursor_pos[1] - 1)) <= char_board[old_pos[1]][old_pos[0]].movement:
                    return True
                else:
                    return False
            elif direction == "Down":
                if abs(old_pos[0] - cursor_pos[0]) + abs(old_pos[1] - (cursor_pos[1] + 1)) <= char_board[old_pos[1]][old_pos[0]].movement:
                    return True
                else:
                    return False
            elif direction == "Left":
                if abs(old_pos[0] - (cursor_pos[0] - 1)) + abs(old_pos[1] - cursor_pos[1]) <= char_board[old_pos[1]][old_pos[0]].movement:
                    return True
                else:
                    return False
            elif direction == "Right":
                if abs(old_pos[0] - (cursor_pos[0] + 1)) + abs(old_pos[1] - cursor_pos[1]) <= char_board[old_pos[1]][old_pos[0]].movement:
                    return True
                else:
                    return False
        return True

    def get_tile_info(self, x_pos, y_pos, terrain_board, char_board):
        """ Retrieve information about currently hovered tile """
        if terrain_board[y_pos][x_pos] == 'g':
            self.terrain_info = self.text_archive.terrain_header + self.text_archive.tile_grass
        elif terrain_board[y_pos][x_pos] == 'd':
            self.terrain_info = self.text_archive.terrain_header + self.text_archive.tile_mud
        elif terrain_board[y_pos][x_pos] == '^':
            self.terrain_info = self.text_archive.terrain_header + self.text_archive.tile_mountains
        elif terrain_board[y_pos][x_pos] == 's':
            self.terrain_info = self.text_archive.terrain_header + self.text_archive.tile_stone
        elif terrain_board[y_pos][x_pos] == 'f':
            self.terrain_info = self.text_archive.terrain_header + self.text_archive.tile_forest
        elif terrain_board[y_pos][x_pos] == 'c':
            self.terrain_info = self.text_archive.terrain_header + self.text_archive.tile_castle
        elif terrain_board[y_pos][x_pos] == 'w':
            self.terrain_info = self.text_archive.terrain_header + self.text_archive.tile_water
        # UNIT DESCRIPTIONS -----------------------------------------------------------
        if char_board[y_pos][x_pos] != '':
            unit = char_board[y_pos][x_pos]
            self.draw_text("HP: " + str(unit.hp), 20, self.BAR_WIDTH / 2 + 200, self.DISPLAY_HEIGHT + self.BAR_HEIGHT / 15 + 4)
            self.draw_text("P. Atk: " + str(unit.physical_atk), 20, self.BAR_WIDTH/ 2 + 200, self.DISPLAY_HEIGHT + self.BAR_HEIGHT / 15 + 28)
            self.draw_text("P. Def: " + str(unit.physical_def), 20, self.BAR_WIDTH / 2 + 200, self.DISPLAY_HEIGHT + self.BAR_HEIGHT / 15 + 52)
            self.draw_text("M. Atk: " + str(unit.magic_atk), 20, self.BAR_WIDTH / 2 + 200, self.DISPLAY_HEIGHT + self.BAR_HEIGHT / 15 + 76)
            self.draw_text("M. Def: " + str(unit.magic_def), 20, self.BAR_WIDTH / 2 + 200, self.DISPLAY_HEIGHT + self.BAR_HEIGHT / 15 + 100)
            if unit.symbol == 'H':
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_hero
            elif unit.symbol == "T":
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_knight
            elif unit.symbol == "A":
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_archer
            elif unit.symbol == "M":
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_mage
            elif unit.symbol == "U":
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_mud_monster
            elif unit.symbol == "I":
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_slime
            elif unit.symbol == "K":
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_skeleton
            elif unit.symbol == "O":
                self.unit_info = self.text_archive.unit_header + self.text_archive.unit_ogre
        else:
            self.unit_info = "Unit: " + self.text_archive.unit_none
        self.draw_text(self.unit_info, 20, self.BAR_WIDTH/2 - 192, self.DISPLAY_HEIGHT + self.BAR_HEIGHT/15 + 4)
        self.draw_text(self.terrain_info, 20, self.BAR_WIDTH/2 - 192, self.DISPLAY_HEIGHT + self.BAR_HEIGHT / 15 + 24)

    def apply_difficulty(self, char_board):
        """ Applies experienced difficulty (increases enemy HP) """
        for y in range(8):
            for x in range(8):
                if char_board[y][x] != '':
                    if not char_board[y][x].player_unit:
                        char_board[y][x].hp += 10

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
        self.casual_prompt = 'Difficulty set to Casual'
        self.experienced_prompt = ' Difficulty set to Experienced'
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
        self.tutorial_no_2 = 'Your party traveled towards the lake that neared the castle of ogres.'
        # ----------------------------------------
        self.lake_text_1 = 'After defeating the mud monsters, your party'
        self.lake_text_2 = 'continued to travel to the lake that neared the castle of ogres.'
        # ----------------------------------------
        self.castle_text_1 = 'You realized that the amount of monsters guarding the castle meant for'
        self.castle_text_2 = 'a difficult battle against the ogres. Despite that, your party continued traveling.'
        # ----------------------------------------
        self.final_text_1 = 'Together, your party defeated the group of ogres that attacked your village.'
        self.final_text_2 = 'Thanks to your efforts, you all lived peacefully... until the next adventure!'
        # ----------------------------------------
        self.game_over_1 = 'Game Over'
        self.game_over_2 = 'Press Enter key to retry'
        # ----------------------------------------
        self.tile_grass = "Grass"
        self.tile_mud = "Mud"
        self.tile_mountains = "Mountains"
        self.tile_stone = "Stone"
        self.tile_forest = "Forest"
        self.tile_castle = "Castle"
        self.tile_water = "Water"
        # ----------------------------------------
        self.unit_hero = "Hero"
        self.unit_knight = "Knight"
        self.unit_mage = "Mage"
        self.unit_archer = "Archer"
        self.unit_mud_monster = "Mud Monster"
        self.unit_slime = "Slime"
        self.unit_skeleton = "Skeleton"
        self.unit_ogre = "Ogre"
        self.unit_none = "No Unit"
        # ----------------------------------------
        self.unit_header = "Unit: "
        self.terrain_header = "Terrain: "
        self.help_unit = "Select a unit to command."
        self.help_dest = "Choose a destination or target."
        # ----------------------------------------
        self.instructions_controls1 = "Press arrow keys to move cursor"
        self.instructions_controls2 = "Press Enter to confirm selection"
        self.instructions_controls3 = "Press Backspace to undo"
        self.instructions_goal = "Defeat all enemies to complete the level"
        self.instructions_phymag = "All units use physical attack and defense, except for the Mage and Skeleton"

    def spanish(self):
        """ Translates all text to Spanish """
        print("Starting translation...")
        self.main_title = self.post_translate(self.main_title)
        print(self.main_title)
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
        self.casual_prompt = self.post_translate(self.casual_prompt)
        self.experienced_prompt = self.post_translate(self.experienced_prompt)
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
        # ----------------------------------------
        self.castle_text_1 = self.post_translate(self.castle_text_1)
        self.castle_text_2 = self.post_translate(self.castle_text_2)
        # ----------------------------------------
        self.final_text_1 = self.post_translate(self.final_text_1)
        self.final_text_2 = self.post_translate(self.final_text_2)
        # ----------------------------------------
        self.game_over_1 = self.post_translate(self.game_over_1)
        self.game_over_2 = self.post_translate(self.game_over_2)
        # ----------------------------------------
        self.tile_grass = self.post_translate(self.tile_grass)
        self.tile_mud = self.post_translate(self.tile_mud)
        self.tile_mountains = self.post_translate(self.tile_mountains)
        self.tile_stone = self.post_translate(self.tile_stone)
        self.tile_forest = self.post_translate(self.tile_forest)
        self.tile_castle = self.post_translate(self.tile_castle)
        self.tile_water = self.post_translate(self.tile_water)
        # ----------------------------------------
        self.unit_hero = self.post_translate(self.unit_hero)
        self.unit_knight = self.post_translate(self.unit_knight)
        self.unit_mage = self.post_translate(self.unit_mage)
        self.unit_archer = self.post_translate(self.unit_archer)
        self.unit_mud_monster = self.post_translate(self.unit_mud_monster)
        self.unit_slime = self.post_translate(self.unit_slime)
        self.unit_skeleton = self.post_translate(self.unit_skeleton)
        self.unit_ogre = self.post_translate(self.unit_ogre)
        self.unit_none = self.post_translate(self.unit_none)
        # ----------------------------------------
        self.unit_header = self.post_translate(self.unit_header)
        self.terrain_header = self.post_translate(self.terrain_header)
        self.help_unit = self.post_translate(self.help_unit)
        self.help_dest = self.post_translate(self.help_dest)
        # ----------------------------------------
        self.instructions_controls1 = self.post_translate(self.instructions_controls1)
        self.instructions_controls2 = self.post_translate(self.instructions_controls2)
        self.instructions_controls3 = self.post_translate(self.instructions_controls3)
        self.instructions_goal = self.post_translate(self.instructions_goal)
        self.instructions_phymag = self.post_translate(self.instructions_phymag)
        print("Translation complete!")

    def post_translate(self, text):
        my_obj = {"destLang": "Spanish", "translate_text": text}
        response = requests.post('http://flip1.engr.oregonstate.edu:1992/post/', json=my_obj)
        my_dict = response.json()
        return my_dict["translation"]