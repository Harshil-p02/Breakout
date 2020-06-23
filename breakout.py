import pygame
import sys

from settings import Settings
from paddle import Paddle
from ball import Ball


class Breakout:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Breakout!')
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)

        self.paddle = Paddle(self)

        self.ball = Ball(self)

    def run_game(self):
        while True:
            self._check_events()
            self.paddle.update()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.paddle.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.paddle.moving_left = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.paddle.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.paddle.moving_left = False

    def _update_screen(self):
        self.screen.fill((75, 75, 75))
        self.paddle.draw_paddle()
        self.ball.blitme()
        pygame.display.flip()



if __name__ == '__main__':
    game = Breakout()
    game.run_game()