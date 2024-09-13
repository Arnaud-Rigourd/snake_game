import enum
import signal
from enum import Enum

import pygame

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


class AutoEnum(Enum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name


class DirectionEnum(enum.Enum):
    UP = enum.auto()
    DOWN = enum.auto()
    RIGHT = enum.auto()
    LEFT = enum.auto()


class TimeoutException(Exception):
    pass


def alarm_handler(signum, frame):
    raise TimeoutException("The function reached the timeout: consider investigate")


def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator
