import pygame


class Ball:

    def __init__(self, game):
        self.game_screen = game.screen
        self.game_rect = self.game_screen.get_rect()

        self.image = pygame.image.load('images/ball.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.game_rect.center

    def update(self):
        pass

    def blitme(self):
        self.game_screen.blit(self.image, self.rect)