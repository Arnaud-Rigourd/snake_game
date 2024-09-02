import pygame.event

from models.fruit import Fruit
from models.game import SnakeGame
from models.snake import Snake


INITIAL_HEAD_POSITION = [30, 10]

SNAKE_BODY = [
    [*INITIAL_HEAD_POSITION],
    [20, 10],
    [10, 10],
]

game = SnakeGame(window_x=300, window_y=300, fps=pygame.time.Clock())
game.snake.speed = 5

while True:
    for event in pygame.event.get():
        game.snake.update_direction_from_keyboard_event(event)
    game.snake.move()

    if game.snake.head_position == game.fruit.position:
        game.fruit.generate_fruit_position(game)
        game.score += 1
    else:
        game.snake.body.pop()

    game.draw()
    game.show_score()
    if game.check_collision() is True:
        game.game_over()
    pygame.display.update()
    game.fps.tick(game.snake.speed)
