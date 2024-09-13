import time

import pygame
from pygame.time import Clock

from models.fruit import Fruit
from models.snake import Snake
from utils import red, black, green, timeout

COLLISION_PENALTY = 500


class SnakeGame:
    def __init__(self, window_x: int, window_y: int, fps: Clock, display_game=True):
        self.window_x = window_x
        self.window_y = window_y
        self.window = (
            pygame.display.set_mode((window_x, window_y)) if display_game else None
        )
        self.score = 0
        self.fruit_eaten = 0
        self.forbidden_move_count = 0
        self.start_time = time.time()
        self.stop_time = None
        self.fps = fps
        self.snake = Snake.create_default(game=self)
        self.fruit = Fruit()
        # create the first fruit on a random position
        self.fruit.generate_fruit_position(self)

        self.display = display_game
        if self.display:
            pygame.init()
            pygame.font.init()

    @timeout(2)
    def play(self, individual, hard_quit=True, display_game=True) -> None:
        while True:
            next_move = self.snake.get_forecasted_next_move(individual)
            self.snake.update_direction(next_move)
            self.snake.move()

            if display_game:
                self.draw()
                self.show_score()

            if self.check_collision() is True:
                self.score -= COLLISION_PENALTY
                self.game_over(hard_quit=hard_quit)
                break

            if display_game:
                pygame.display.update()
                self.fps.tick(self.snake.speed)

    def get_game_kpi(self) -> tuple:
        return self.score, self.life_time

    @property
    def life_time(self) -> float:
        if self.stop_time is None:
            raise ValueError(f"{self.stop_time} should not be None at this point")
        return self.stop_time - self.start_time

    def check_collision(self) -> bool:
        if (
            self.snake.head_position[0] < 0
            or self.snake.head_position[0] > self.window_x - 10
        ):
            return True
        if (
            self.snake.head_position[1] < 0
            or self.snake.head_position[1] > self.window_y - 10
        ):
            return True

        for body_position in self.snake.body[1:]:
            if (
                self.snake.head_position[0] == body_position[0]
                and self.snake.head_position[1] == body_position[1]
            ):
                return True
        return False

    def game_over(self, hard_quit: bool = True):
        self.stop_time = time.time()
        if hard_quit:
            pygame.quit()
            quit()

    def show_score(self):
        score_font = pygame.font.SysFont("times new roman", 15)
        score_surface = score_font.render("Score : " + str(self.score), True, red)
        score_rect = score_surface.get_rect()

        self.window.blit(score_surface, score_rect)

    def draw(self):
        self.window.fill(black)
        # draw the fruit
        pygame.draw.rect(
            self.window,
            red,
            pygame.Rect(self.fruit.position[0], self.fruit.position[1], 10, 10),
        )
        # draw the snake body in the window
        for body in self.snake.body:
            pygame.draw.rect(self.window, green, pygame.Rect(body[0], body[1], 10, 10))
