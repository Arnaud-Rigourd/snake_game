import random

import pygame
from pygame.event import Event

from models.fruit import Fruit
from models.game import SnakeGame
from models.snake import Snake, DirectionEnum

POSSIBLE_MOVES = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
POSSIBLE_MOVES_MAP = {
    DirectionEnum.UP: pygame.K_UP,
    DirectionEnum.DOWN: pygame.K_DOWN,
    DirectionEnum.RIGHT: pygame.K_RIGHT,
    DirectionEnum.LEFT: pygame.K_LEFT,
}


class Player:
    def __init__(self, id: int):
        self.id = id

    def prepare(self):
        pass

    @staticmethod
    def choose_random_move(snake_direction: DirectionEnum) -> Event:
        possible_moves = [*POSSIBLE_MOVES]
        possible_moves.remove(POSSIBLE_MOVES_MAP[snake_direction])
        move = random.choice(possible_moves)
        return pygame.event.Event(pygame.KEYDOWN, key=move)

    def play(self, game: SnakeGame, snake: Snake, fruit: Fruit) -> None:
        while True:
            event = self.choose_random_move(
                snake.direction
            )  # TODO: replace by the new brain of the snake
            snake.update_direction_from_keyboard_event(event)
            snake.move()

            if snake.head_position == fruit.position or fruit.position is None:
                fruit.generate_fruit_position(game)
                game.score += 1
            else:
                snake.body.pop()

            game.draw(snake, fruit)
            game.show_score()
            game.check_collision(snake)
            pygame.display.update()
            game.fps.tick(snake.speed)
