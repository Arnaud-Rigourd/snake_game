import math
from typing import TYPE_CHECKING, Self

import numpy as np
import pygame
from pygame.event import Event

if TYPE_CHECKING:
    from models.game import SnakeGame
    from ML.models.individual import Individual
    from models.fruit import Fruit
from utils import DirectionEnum

INITIAL_HEAD_POSITION = [30, 10]

SNAKE_BODY = [
    [*INITIAL_HEAD_POSITION],
    [20, 10],
    [10, 10],
]

SPEED = 10

FRUIT_REWARD = 200
COLLISION_AVOIDED_REWARD = 20
FORBIDDEN_MOVE_PENALTY = -10
FRUIT_DISTANCE_REWARD = 10
FRUIT_DISTANCE_PENALTY = -5
MOVE_CONSISTENCY_REWARD = 50
EXPLORATION_REWARD = 2
MOVE_REWARD = 5


FORBIDDEN_MOVE_MAP = {
    DirectionEnum.UP: DirectionEnum.DOWN,
    DirectionEnum.DOWN: DirectionEnum.UP,
    DirectionEnum.RIGHT: DirectionEnum.LEFT,
    DirectionEnum.LEFT: DirectionEnum.RIGHT,
}


MOVE_MAP = {
    DirectionEnum.UP: -10,
    DirectionEnum.DOWN: 10,
    DirectionEnum.RIGHT: 10,
    DirectionEnum.LEFT: -10,
}


class Snake:
    def __init__(
        self,
        game: "SnakeGame",
        body: list[list[int]],
        head_position: list[int],
        direction: DirectionEnum | None = DirectionEnum.RIGHT,
        speed: int | None = SPEED,
    ):
        self.game = game
        self.body = body
        self.head_position = head_position
        self.direction = direction
        self.speed = speed

    @classmethod
    def create_default(cls, game: "SnakeGame") -> Self:
        return cls(
            game=game,
            body=[*SNAKE_BODY],
            head_position=[*INITIAL_HEAD_POSITION],
            speed=SPEED,
        )

    def move(self) -> None:
        """
        Update the position of the snake, and return relevant information to adjust the score:
        - new move
        - fruit eaten
        - new direction consistency
        - avoided collision
        """
        initial_distance = self.get_distance_from_fruit(self.game.fruit)
        initial_head_position = self.head_position
        initial_fruit_position = self.game.fruit.position
        match self.direction:
            case DirectionEnum.UP:
                self.head_position[1] += MOVE_MAP[DirectionEnum.UP]
            case DirectionEnum.DOWN:
                self.head_position[1] += MOVE_MAP[DirectionEnum.DOWN]
            case DirectionEnum.RIGHT:
                self.head_position[0] += MOVE_MAP[DirectionEnum.RIGHT]
            case DirectionEnum.LEFT:
                self.head_position[0] += MOVE_MAP[DirectionEnum.LEFT]

        self.body.insert(0, [*self.head_position])

        if self.head_position == initial_fruit_position:
            self.game.fruit.generate_fruit_position(self.game)
        else:
            self.body.pop()

        self.adjust_score(
            initial_distance, initial_head_position, initial_fruit_position
        )

    def adjust_score(
        self,
        initial_distance: float,
        initial_position: list[int],
        initial_fruit_position: list[int],
    ) -> None:
        self.game.score += MOVE_REWARD

        new_distance = self.get_distance_from_fruit(self.game.fruit)
        if new_distance < initial_distance:
            self.game.score += FRUIT_DISTANCE_REWARD
            if (
                self.head_position[0] == self.game.fruit.position[0]
                or self.head_position[1] == self.game.fruit.position[1]
            ):
                self.game.score += MOVE_CONSISTENCY_REWARD
        elif new_distance > initial_distance:
            self.game.score += FRUIT_DISTANCE_PENALTY

        if self.head_position == initial_fruit_position:
            self.game.score += FRUIT_REWARD
            self.game.fruit_eaten += 1

        if self.is_collision_avoided(initial_position):
            self.game.score += COLLISION_AVOIDED_REWARD

    def is_collision_avoided(self, initial_position: list[int]) -> bool:
        # check body position
        # check wall position or distance -> game.window_x and y
        # if the distance is less than 1 block, then reward

        return False

    def get_distance_from_fruit(self, fruit: "Fruit") -> float:
        """Get the Euclidean distance between the snake and the fruit"""
        return math.sqrt(
            (self.head_position[0] - fruit.position[0]) ** 2
            + (self.head_position[1] - fruit.position[1]) ** 2
        )

    def get_forecasted_next_move(self, individual: "Individual") -> np.int64:
        next_move = None
        for i in range(3):
            state = self.get_state()
            hidden = np.maximum(0, np.dot(state, individual.W1))
            output = np.dot(hidden, individual.W2)

            # enum.auto begins at 1
            next_move = np.argmax(output) + 1
            if DirectionEnum(next_move) == FORBIDDEN_MOVE_MAP[self.direction]:
                # try to give a legit move if next_move is forbidden (3 try before moving on)
                self.game.score += FORBIDDEN_MOVE_PENALTY
                self.game.forbidden_move_count += 1
            else:
                break
        return next_move

    def get_state(self) -> np.array:
        """Define the current state of the game by returning the snake direction and the relative position of the fruit"""
        fruit_direction = (
            np.sign(self.game.fruit.position[0] - self.head_position[0]),
            np.sign(self.game.fruit.position[1] - self.head_position[1]),
        )
        return np.array(
            [self.direction.value] + list(fruit_direction), dtype=np.float32
        )

    def update_direction(self, new_direction: int | np.int64) -> None:
        match new_direction:
            case (
                pygame.K_UP
                | DirectionEnum.UP.value
            ) if self.direction != DirectionEnum.DOWN:
                self.direction = DirectionEnum.UP
            case (
                pygame.K_DOWN
                | DirectionEnum.DOWN.value
            ) if self.direction != DirectionEnum.UP:
                self.direction = DirectionEnum.DOWN
            case (
                pygame.K_RIGHT
                | DirectionEnum.RIGHT.value
            ) if self.direction != DirectionEnum.LEFT:
                self.direction = DirectionEnum.RIGHT
            case (
                pygame.K_LEFT
                | DirectionEnum.LEFT.value
            ) if self.direction != DirectionEnum.RIGHT:
                self.direction = DirectionEnum.LEFT

    def update_direction_from_keyboard_event(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.update_direction(new_direction=event.key)
