class Settings:

    def __init__(self):
        self.screen_width = 1440
        self.screen_height = 1000

        self.paddle_width, self.paddle_height = (150, 10)
        self.paddle_color = (255, 0, 0)
        self.paddle_speed = 2

        self.ball_speed_x = 1
        self.ball_speed_y = 1

        self.max_tries = 3

        self.present_level_num = 1