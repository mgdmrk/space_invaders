import pygame

class Assets:
    """Class is storing resources."""


    @staticmethod
    def load():
        """Loading resources from drive."""
        Assets.SPACE_SHIP = pygame.transform.scale((pygame.image.load('assets/images/space_ship.png')), (50,50))
        Assets.ENEMY1 = pygame.transform.scale((pygame.image.load('assets/images/enemy1.png')), (50,50))
        Assets.ENEMY2 = pygame.transform.scale((pygame.image.load('assets/images/enemy2.png')), (50,50))
        Assets.ENEMY_BULLET = pygame.transform.scale((pygame.image.load('assets/images/enemy_bullet.png')), (5,5))
        Assets.SHIP_BULLET = pygame.transform.scale((pygame.image.load('assets/images/ship_bullet.png')), (5,5))
        Assets.EXPLOSION1 = pygame.image.load('assets/images/explosion1.png')
        Assets.EXPLOSION2 = pygame.image.load('assets/images/explosion2.png')
        Assets.FONT = pygame.font.Font('assets/font/yoster.ttf', 50)
        Assets.BACKGROUND = pygame.transform.scale((pygame.image.load('assets/images/background.jpg')), (800, 600))
        Assets.ICON = pygame.image.load("assets/images/icon.png")
