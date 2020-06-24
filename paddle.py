import pygame


class Paddle:

    def __init__(self, game):
        self.game_screen = game.screen
        self.game_rect = game.screen.get_rect()
        self.settings = game.settings

        self.rect = pygame.Rect(0, 0, self.settings.paddle_width, self.settings.paddle_height)
        self.rect.x = self.game_rect.width / 2 - self.rect.width/2
        self.rect.y = self.game_rect.height - 30

        self.moving_right = False
        self.moving_left = False

        self.x = float(self.rect.x)

    def update(self):
        self.x = float(self.rect.x)
        if self.moving_right and self.rect.right < self.game_rect.right:
            self.x += self.settings.paddle_speed
        if self.moving_left and self.rect.x > 0:
            self.x -= self.settings.paddle_speed

        self.rect.x = self.x

    def center_paddle(self):
        self.rect.x = self.game_rect.width / 2 - self.rect.width / 2

    def draw_paddle(self):
        pygame.draw.rect(self.game_screen, self.settings.paddle_color, self.rect)