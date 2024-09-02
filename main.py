import pygame.event

from models.fruit import Fruit
from models.snake_game import SnakeGame
from models.snake import Snake
from utils import black, green, red, white



INITIAL_HEAD_POSITION = [30, 10]

SNAKE_BODY = [
    [*INITIAL_HEAD_POSITION],
    [20, 10],
    [10, 10],
]

game = SnakeGame(window_x=80, window_y=80, fps=pygame.time.Clock())
snake = Snake(body=SNAKE_BODY, head_position=INITIAL_HEAD_POSITION, speed=10)
fruit = Fruit()


while True:
    game.window.fill(black)
    for event in pygame.event.get():
        snake.update_direction(event)
    snake.move()

    if snake.head_position == fruit.position or fruit.position is None:
        fruit.generate_fruit_position(game)
        game.score += 1
    else:
        snake.body.pop()

    # draw the fruit
    pygame.draw.rect(game.window, white, pygame.Rect(fruit.position[0], fruit.position[1], 10, 10))

    # draw the snake body in the window
    for body in snake.body:
        pygame.draw.rect(game.window, green, pygame.Rect(body[0], body[1], 10, 10))

    game.show_score()
    game.check_game_over(snake)
    pygame.display.update()
    game.fps.tick(snake.speed)
