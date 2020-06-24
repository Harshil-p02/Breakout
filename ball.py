import pygame


class Ball:

    def __init__(self, game):
        self.game_screen = game.screen
        self.game_rect = self.game_screen.get_rect()
        self.settings = game.settings

        self.image = pygame.image.load('images/ball.png')
        self.rect = self.image.get_rect()
        self.rect.center = self.game_rect.center

        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x += self.settings.ball_speed_x
        self.y += self.settings.ball_speed_y

        self.rect.x = self.x
        self.rect.y = self.y

    def hacked_ball(self):
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        if self.moving_right and self.rect.right < self.game_rect.right:
            self.x += abs(self.settings.ball_speed_x)
        if self.moving_left and self.rect.x > 0:
            self.x -= abs(self.settings.ball_speed_x)
        if self.moving_down and self.rect.bottom < self.game_rect.height:
            self.y += abs(self.settings.ball_speed_y)
        if self.moving_up and self.rect.top > 0:
            self.y -= abs(self.settings.ball_speed_y)

        self.rect.x = self.x
        self.rect.y = self.y

    def center_ball(self):
        self.rect.center = self.game_rect.center

    def blitme(self):
        self.game_screen.blit(self.image, self.rect)