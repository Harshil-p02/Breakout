import pygame
import sys
import time

from settings import Settings
from paddle import Paddle
from ball import Ball
from brick import Brick
from levels import Levels
from button import Button

# ----------------Make the atari version---------------------
class Breakout:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption('Breakout!')
        icon = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon)

        # Initialize game objects
        self.paddle = Paddle(self)
        self.ball = Ball(self)
        self.brick = Brick(self)
        self.bricks = pygame.sprite.Group()

        self.level = Levels()
        self._create_level()

        self.hacks_active = False
        self.game_running = False

        self.play_button = Button(self, 'Play')

    def run_game(self):
        '''Main Game Loop'''

        while True:
            if self.game_running:
                pygame.mouse.set_visible(False)
                self._check_hacks()
                self._update_ball()
                if not self.hacks_active:
                    self.paddle.update()
            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # sys.exit()
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        if self.play_button.rect.collidepoint(mouse_pos) and not self.game_running:
            time.sleep(0.5)
            self.game_running = True

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.paddle.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.paddle.moving_left = True
        elif event.key == pygame.K_p:
            self.game_running = True
        elif event.key == pygame.K_ESCAPE:
            self.game_running = not self.game_running
        if self.hacks_active:
            if event.key == pygame.K_RIGHT:
                self.ball.moving_right = True
            elif event.key == pygame.K_LEFT:
                self.ball.moving_left = True
            elif event.key == pygame.K_UP:
                self.ball.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.ball.moving_down = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.paddle.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.paddle.moving_left = False
        if self.hacks_active:
            if event.key == pygame.K_RIGHT:
                self.ball.moving_right = False
            elif event.key == pygame.K_LEFT:
                self.ball.moving_left = False
            elif event.key == pygame.K_UP:
                self.ball.moving_up = False
            elif event.key == pygame.K_DOWN:
                self.ball.moving_down = False

    def _check_hacks(self):
        keys = pygame.key.get_pressed()
        mods = pygame.key.get_mods()
        if keys[pygame.K_DELETE] and keys[pygame.K_SPACE]:
            if self.settings.ball_speed_y < 0:
                self.settings.ball_speed_y = -1
            else:
                self.settings.ball_speed_y = 1

        # ---------Move ball via keys------
        if mods & pygame.KMOD_SHIFT and mods & pygame.KMOD_CTRL:
            self.hacks_active = True
        else:
            self.hacks_active = False

    # ------Replaced by self._create_level()-----
    # def _create_wall(self):
    #     brick = Brick(self)
    #     brick_width, brick_height = brick.rect.size
    #     num_bricks = math.ceil(self.screen.get_rect().width / brick_width)
    #     for num in range(num_bricks):
    #         self._create_brick(num)

    def _create_level(self):
        levels = self.level.levels
        present_level = levels[self.settings.present_level_num]

        for row_num, row in enumerate(present_level):
            for pos_num, present in enumerate(row):
                if present:
                    self._create_brick(row_num, pos_num)

    def _create_brick(self, row, num):
        brick = Brick(self)
        brick.rect.x = num * brick.rect.width
        brick.rect.y = 80 + self.brick.rect.height * row
        self.bricks.add(brick)

    def _update_ball(self):
        # print(self.settings.ball_speed_x, self.settings.ball_speed_y)
        if not self.hacks_active:
            self.ball.update()
            self.collide()
        else:
            self.ball.hacked_ball()

        self._ball_brick_collision()

        if self.ball.rect.bottom - self.ball.rect.width / 2 > self.screen.get_rect().height:
            print(f'{self.settings.max_tries} tries remaining\t{len(self.bricks.sprites())} bricks left')
            self.restart()

    def collide(self):
        # Collision with paddle
        if self.ball.rect.colliderect(self.paddle.rect):
            self.settings.ball_speed_y *= -1.1
            self._get_collision_coords()
        # Collision with game window
        elif self.ball.rect.right >= self.screen.get_rect().right:
            self.settings.ball_speed_x *= -1
        elif self.ball.rect.left <= 0:
            self.settings.ball_speed_x *= -1
        elif self.ball.rect.top <= 0:
            self.settings.ball_speed_y *= -1

    def _get_collision_coords(self):
        # print(self.paddle.rect.x, self.ball.rect.x)
        self._change_x_vel(self.paddle.rect.x, self.ball.rect.x)

    def _change_x_vel(self, paddle_x, ball_x):
        change = ball_x - paddle_x - self.settings.paddle_width / 2
        # print(change)
        if change > 0:
            self.settings.ball_speed_x = 1 + change / 75
        else:
            self.settings.ball_speed_x = -1 + change / 75

    def _ball_brick_collision(self):
        for brick in self.bricks.sprites():
            if brick.rect.colliderect(self.ball.rect):
                self.bricks.remove(brick)
                if not self.hacks_active:
                    self.settings.ball_speed_y *= -1
        self._change_level()

    def _change_level(self):
        if not self.bricks.sprites():
            self.settings.present_level_num += 1
            if self.settings.present_level_num > len(self.level.levels):
                sys.exit()
            time.sleep(0.5)
            self.reset_game()

    def restart(self):
        self.settings.max_tries -= 1
        if self.settings.max_tries:
            self.reset_game()
        else:
            sys.exit()

    def reset_game(self):
        time.sleep(1)
        self.ball.center_ball()
        self.settings.ball_speed_x = 1
        self.settings.ball_speed_y = 1
        self.paddle.center_paddle()
        self.bricks.empty()

        self._create_level()

    def _update_screen(self):
        self.screen.fill((75, 75, 75))
        self.paddle.draw_paddle()
        self.ball.blitme()
        self.bricks.draw(self.screen)

        if not self.game_running:
            self.play_button.draw_button()

        pygame.display.flip()





if __name__ == '__main__':
    game = Breakout()
    game.run_game()