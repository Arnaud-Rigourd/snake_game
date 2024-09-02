import enum

import pygame
from pygame.event import Event

from utils import AutoEnum


class DirectionEnum(AutoEnum):
    UP = enum.auto()
    DOWN = enum.auto()
    RIGHT = enum.auto()
    LEFT = enum.auto()


MOVE_MAP = {
    DirectionEnum.UP: -10,
    DirectionEnum.DOWN: 10,
    DirectionEnum.RIGHT: 10,
    DirectionEnum.LEFT: -10,
}


class Snake:
    def __init__(
            self,
            body: list[list[int]],
            head_position: list[int],
            direction: DirectionEnum | None = DirectionEnum.RIGHT,
            speed: int | None = 15
    ):
        self.body = body
        self.head_position = head_position
        self.direction = direction
        self.speed = speed

    def move(self) -> None:
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

    def update_direction(self, event: Event) -> None:
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP if self.direction != DirectionEnum.DOWN:
                    self.direction = DirectionEnum.UP
                case pygame.K_DOWN if self.direction != DirectionEnum.UP:
                    self.direction = DirectionEnum.DOWN
                case pygame.K_RIGHT if self.direction != DirectionEnum.LEFT:
                    self.direction = DirectionEnum.RIGHT
                case pygame.K_LEFT if self.direction != DirectionEnum.RIGHT:
                    self.direction = DirectionEnum.LEFT
