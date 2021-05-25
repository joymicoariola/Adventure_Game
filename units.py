import pygame


class Unit:
    def __init__(self):
        """ Creates base stats """
        self.symbol = ''
        self.physical_atk = 0
        self.physical_def = 0
        self.magic_atk = 0
        self.magic_def = 0
        self.movement = 0
        self.hp = 0
        self.ranged = False
        self.player_unit = False


# HERO UNITS --------------------------------------


class Hero(Unit):
    def __init__(self):
        """ Creates base hero stats """
        self.symbol = 'H'
        self.physical_atk = 25
        self.physical_def = 10
        self.magic_atk = 0
        self.magic_def = 8
        self.movement = 1                                           # maybe change movement to 2 ?
        self.hp = 30
        self.ranged = False
        self.player_unit = True


class Knight(Unit):
    def __init__(self):
        """ Creates base knight stats """
        self.symbol = 'T'
        self.physical_atk = 20
        self.physical_def = 15
        self.magic_atk = 0
        self.magic_def = 3
        self.movement = 1
        self.hp = 45
        self.ranged = False
        self.player_unit = True


class Archer(Unit):
    def __init__(self):
        """ Creates base knight stats """
        self.symbol = 'A'
        self.physical_atk = 15
        self.physical_def = 8
        self.magic_atk = 0
        self.magic_def = 10
        self.movement = 1
        self.hp = 25
        self.ranged = False
        self.player_unit = True


class Mage(Unit):
    def __init__(self):
        """ Creates base knight stats """
        self.symbol = 'M'
        self.physical_atk = 0
        self.physical_def = 7
        self.magic_atk = 30
        self.magic_def = 15
        self.movement = 1
        self.hp = 20
        self.ranged = False
        self.player_unit = True

# MONSTER UNITS --------------------------------------


class MudMuck(Unit):
    def __init__(self):
        """ Creates base mud muck stats """
        self.symbol = 'U'
        self.physical_atk = 10
        self.physical_def = 3
        self.magic_atk = 0
        self.magic_def = 8
        self.movement = 1
        self.hp = 10
        self.ranged = False
        self.player_unit = False


class Slimes(Unit):
    def __init__(self):
        """ Creates base slimes stats """
        self.symbol = 'I'
        self.physical_atk = 15
        self.physical_def = 7
        self.magic_atk = 0
        self.magic_def = 10
        self.movement = 1
        self.hp = 20
        self.ranged = False
        self.player_unit = False


class Skeletons(Unit):
    def __init__(self):
        """ Creates base skeleton stats """
        self.symbol = 'K'
        self.physical_atk = 0
        self.physical_def = 8
        self.magic_atk = 20
        self.magic_def = 15
        self.movement = 1
        self.hp = 15
        self.ranged = False
        self.player_unit = False


class Ogres(Unit):
    def __init__(self):
        """ Creates base ogre stats """
        self.symbol = 'O'
        self.physical_atk = 25
        self.physical_def = 18
        self.magic_atk = 0
        self.magic_def = 10
        self.movement = 1
        self.hp = 40
        self.ranged = False
        self.player_unit = False