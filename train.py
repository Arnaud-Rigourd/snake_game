import random
from uuid import UUID

import pygame

from ML.models.individual import Individual
from ML.services.generation import generate_new_generation
from models.game import SnakeGame

# settings
MAX_SCORE = 3588

# params
GENERATION_SIZE = 100
MUTATION_RATE = 0.01
NEURON_COUNT = 16

generation_count = 0
while True:
    generation_count += 1
    print(f"=========={generation_count} generation==========")

    fitness_per_element: dict[Individual, float] = {}
    individuals = Individual.create_generation(
        generation_size=GENERATION_SIZE, neuron_count=NEURON_COUNT
    )
    generation_scores = []
    for individual in individuals:
        game = SnakeGame(
            window_x=300, window_y=300, fps=pygame.time.Clock(), display_game=False
        )
        game.play(individual, hard_quit=False, display_game=False)
        print(
            f"{individual.fitness(game)} - {game.life_time} - {round(game.score, 1)} - {game.fruit_eaten} - {game.forbidden_move_count}"
        )
        fitness_per_element[individual] = individual.fitness(game)
        generation_scores.append(game.score)

    if max(generation_scores) >= 40:
        break

    generate_new_generation(
        fitness_per_element,
        generation_size=GENERATION_SIZE,
        mutation_rate=MUTATION_RATE,
        neuron_count=NEURON_COUNT,
    )
