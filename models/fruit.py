import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.snake import Snake
    from models.game import SnakeGame


class Fruit:
    position: list[int] | None = None

    def is_eaten(self, snake: "Snake") -> bool:
        # check if the head_position of the snake == fruit position
        if snake.head_position == self.position:
            return True
        return False

    def generate_fruit_position(self, game: "SnakeGame"):
        self.position = [
            random.randrange(1, (game.window_x // 10)) * 10,
            random.randrange(1, (game.window_y // 10)) * 10,
        ]
