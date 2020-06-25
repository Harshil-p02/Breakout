import pygame.font


class Button:

    def __init__(self, game, msg):
        self.game_screen = game.screen
        self.game_rect = game.screen.get_rect()

        self.width, self.height = 200, 100
        self.button_color = (0, 0, 255)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('Algerian', 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.game_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.game_screen.fill(self.button_color, self.rect)
        self.game_screen.blit(self.msg_image, self.msg_image_rect)