import time

import pygame
from pygame.time import Clock

from models.snake import Snake
from utils import red


class SnakeGame:
    def __init__(self, window_x: int, window_y: int, fps: Clock):
        self.window_x = window_x
        self.window_y = window_y
        self.window = pygame.display.set_mode((window_x, window_y))
        self.score = -1
        self.fps = fps

        pygame.init()
        pygame.font.init()

    @staticmethod
    def game_over():
        # game_over_surface = self.font.render('Your Score is : ' + str(score), True, red)
        # game_over_rect = game_over_surface.get_rect()

        # setting position of the text
        # game_over_rect.midtop = (window_x / 2, window_y / 4)

        # blit will draw the text on screen
        # game_window.blit(game_over_surface, game_over_rect)
        # pygame.display.flip()

        time.sleep(1)

        # deactivating pygame library
        pygame.quit()

        # quit the program
        quit()

    def check_game_over(self, snake: Snake) -> None:
        if snake.head_position[0] < 0 or snake.head_position[0] > self.window_x - 10:
            self.game_over()
        if snake.head_position[1] < 0 or snake.head_position[1] > self.window_y - 10:
            self.game_over()

        for body_position in snake.body[1:]:
            if (
                snake.head_position[0] == body_position[0]
                and snake.head_position[1] == body_position[1]
            ):
                self.game_over()

    def show_score(self):
        score_font = pygame.font.SysFont("times new roman", 15)
        score_surface = score_font.render("Score : " + str(self.score), True, red)
        score_rect = score_surface.get_rect()

        self.window.blit(score_surface, score_rect)
