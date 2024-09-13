import gc
from statistics import mean

import pygame

from ML.models.individual import Individual
from ML.services.generation import generate_new_generation
from models.game import SnakeGame
from utils import TimeoutException

# params
GENERATION_SIZE = 100
MUTATION_RATE = 0.1
NEURON_COUNT = 32
GAME_DIMENSION = 80

# settings
MAX_SCORE = GAME_DIMENSION * GAME_DIMENSION - 3

generation_count = 0
next_generation = []
while True:
    generation_count += 1
    print(f"========== generation {generation_count} ==========")

    fitness_fruit_per_element: dict[Individual, tuple[float, int]] = {}
    if not next_generation:
        print("First generation")
        # create the first generation
        next_generation = Individual.create_generation(
            generation_size=GENERATION_SIZE, neuron_count=NEURON_COUNT
        )

    for individual in next_generation:
        game = SnakeGame(
            window_x=GAME_DIMENSION,
            window_y=GAME_DIMENSION,
            fps=pygame.time.Clock(),
            display_game=False,
        )
        try:
            game.play(individual, hard_quit=False, display_game=game.display)
        except TimeoutException as exc:
            # TODO: log the error instead
            print(exc)
            continue

        fitness_fruit_per_element[individual] = (individual.fitness(game), game.fruit_eaten)
        # only for display
        print(".", end="", flush=True)

    # generate a report here
    sorted_by_fitness = dict(sorted(fitness_fruit_per_element.items(), key=lambda item: item[1][0], reverse=True))
    sorted_by_fruit_eaten = dict(sorted(fitness_fruit_per_element.items(), key=lambda item: item[1][1], reverse=True))
    print(
        f"\nmax fitness: {next(iter(sorted_by_fitness.values()))[0]} - related fruit {next(iter(sorted_by_fitness.values()))[1]} - max fruit {next(iter(sorted_by_fruit_eaten.values()))[1]} - related score {next(iter(sorted_by_fruit_eaten.values()))[0]} - mean score: {mean([fitness for fitness, fruit_eaten in fitness_fruit_per_element.values()])}\n"
    )
    if next(iter(sorted_by_fruit_eaten.values()))[1] >= 61:
        break

    next_generation = generate_new_generation(
        fitness_fruit_per_element,
        generation_size=GENERATION_SIZE,
        mutation_rate=MUTATION_RATE,
        neuron_count=NEURON_COUNT,
    )

    gc.collect()
