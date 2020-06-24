import pygame
from pygame.sprite import Sprite


class Brick(Sprite):

    def __init__(self, game):
        super().__init__()
        self.game_screen = game.screen
        self.game_rect = self.game_screen.get_rect()

        self.image = pygame.image.load('images/brick.png')
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.y = 100

    def blitme(self):
        self.game_screen.blit(self.image, self.rect)