import pygame


class Unit:
    def __init__(self):
        """ Creates base stats """
        self.name = ''
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
        self.name = "Hero"
        self.symbol = 'H'
        self.physical_atk = 25
        self.physical_def = 10
        self.magic_atk = 0
        self.magic_def = 8
        self.movement = 2                                           # maybe change movement to 2 ?
        self.hp = 30
        self.ranged = False
        self.player_unit = True
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/hero.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Knight(Unit):
    def __init__(self):
        """ Creates base knight stats """
        self.name = "Knight"
        self.symbol = 'T'
        self.physical_atk = 20
        self.physical_def = 15
        self.magic_atk = 0
        self.magic_def = 3
        self.movement = 1
        self.hp = 45
        self.ranged = False
        self.player_unit = True
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/knight.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Archer(Unit):
    def __init__(self):
        """ Creates base knight stats """
        self.name = "Archer"
        self.symbol = 'A'
        self.physical_atk = 15
        self.physical_def = 8
        self.magic_atk = 0
        self.magic_def = 10
        self.movement = 3
        self.hp = 25
        self.ranged = False
        self.player_unit = True
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/archer.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Mage(Unit):
    def __init__(self):
        """ Creates base knight stats """
        self.name = "Mage"
        self.symbol = 'M'
        self.physical_atk = 0
        self.physical_def = 7
        self.magic_atk = 30
        self.magic_def = 15
        self.movement = 1
        self.hp = 20
        self.ranged = False
        self.player_unit = True
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/mage.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))

# MONSTER UNITS --------------------------------------


class MudMuck(Unit):
    def __init__(self):
        """ Creates base mud muck stats """
        self.name = "Mud Monster"
        self.symbol = 'U'
        self.physical_atk = 10
        self.physical_def = 3
        self.magic_atk = 0
        self.magic_def = 8
        self.movement = 1
        self.hp = 10
        self.ranged = False
        self.player_unit = False
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/mudmonster.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Slimes(Unit):
    def __init__(self):
        """ Creates base slimes stats """
        self.name = "Slimes"
        self.symbol = 'I'
        self.physical_atk = 15
        self.physical_def = 7
        self.magic_atk = 0
        self.magic_def = 10
        self.movement = 1
        self.hp = 20
        self.ranged = False
        self.player_unit = False
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/slime.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Skeletons(Unit):
    def __init__(self):
        """ Creates base skeleton stats """
        self.name = "Skeleton"
        self.symbol = 'K'
        self.physical_atk = 0
        self.physical_def = 8
        self.magic_atk = 20
        self.magic_def = 15
        self.movement = 1
        self.hp = 15
        self.ranged = False
        self.player_unit = False
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/skeleton.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Ogres(Unit):
    def __init__(self):
        """ Creates base ogre stats """
        self.name = "Ogre"
        self.symbol = 'O'
        self.physical_atk = 20
        self.physical_def = 10
        self.magic_atk = 0
        self.magic_def = 10
        self.movement = 1
        self.hp = 40
        self.ranged = False
        self.player_unit = False
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/ogre.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Grass:
    def __init__(self):
        """ Creates a grass tile """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/grass.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Mud:
    def __init__(self):
        """ Creates a mud tile """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/mud.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Mountain:
    def __init__(self):
        """ Creates a mountain tile """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/mountain.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Forest:
    def __init__(self):
        """ Creates a forest tile """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/forest.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Stone:
    def __init__(self):
        """ Creates a stone tile """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/stone.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Castle:
    def __init__(self):
        """ Creates a castle tile """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/castle.png")                      # change to castle
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Water:
    def __init__(self):
        """ Creates a water tile """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/water.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))


class Cursor:
    def __init__(self):
        """ Creates a cursor object """
        self.sprite = pygame.sprite.Sprite()
        self.sprite.image = pygame.image.load("sprites/cursor.png")
        self.sprite.image = pygame.transform.scale(self.sprite.image, (80, 80))



