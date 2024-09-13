import random
from itertools import islice

import numpy as np

from ML.models.brain import Brain
from ML.models.individual import Individual, INPUT_SHAPE


def generate_new_generation(
    unsorted_elements: dict[Individual, tuple[float, int]],
    *,
    generation_size: int,
    mutation_rate: float,
    neuron_count: int,
) -> list[Individual]:
    actual_population_size = len(unsorted_elements)
    # sort players by score and keep x% of the best
    sorted_parents = get_sorted_elements(unsorted_elements)
    granted_parents = sorted_parents[: int(actual_population_size * 0.1)]

    # sorted_parents_map = dict(sorted(unsorted_elements.items(), key=lambda item: item[1], reverse=True))
    # granted_parents_map = dict(islice(sorted_parents_map.items(), int(actual_population_size * 0.1)))

    elite_children = create_children(
        granted_parents, neuron_count, mutation_rate, int(actual_population_size * 0.5)
    )
    # elite_children = create_children_with_weight(granted_parents_map, neuron_count, mutation_rate, int(actual_population_size * 0.5))
    # keep x% of random of the generation, no matter there reward
    random_parents = random.choices(
        sorted_parents[len(granted_parents) :], k=int(actual_population_size * 0.8)
    )
    granted_parents.extend(random_parents)
    # random_parents_map = dict(islice(sorted_parents_map.items(), int(actual_population_size * 0.9)))
    # granted_parents_map = granted_parents_map | random_parents_map
    random_children = create_children(
        granted_parents, neuron_count, mutation_rate, int(actual_population_size * 0.4)
    )
    # random_children = create_children_with_weight(granted_parents_map, neuron_count, mutation_rate, int(actual_population_size * 0.4))
    new_generation = elite_children + random_children

    # fill the new generation with completely new elements
    new_elements = Individual.create_generation(
        generation_size - len(new_generation), neuron_count=neuron_count
    )
    new_generation.extend(new_elements)

    return new_generation


def create_children_with_weight(
    parents: dict[Individual, float],
    neuron_count: int,
    mutation_rate: float,
    count: int,
) -> list[Individual]:
    children = []
    fitnesses = [max(fitness, 0) for fitness in parents.values()]
    for _ in range(count):
        parent_1, parent_2 = random.choices(
            list(parents.keys()), weights=fitnesses, k=2
        )
        child = crossover(parent_1, parent_2, neuron_count)
        add_mutation(child, mutation_rate)
        children.append(child)
    return children


def create_children(
    parents: list[Individual], neuron_count: int, mutation_rate: float, count: int
) -> list[Individual]:
    children = []
    for _ in range(count):
        parent_1, parent_2 = random.sample(parents, 2)
        child = crossover(parent_1, parent_2, neuron_count)
        add_mutation(child, mutation_rate)
        children.append(child)
    return children


def get_sorted_elements(unsorted_elements: dict[Individual, tuple[float, int]]) -> list[Individual]:
    """sort elements by the fitness score"""
    return [
        element
        for element, fitness_score in sorted(
            unsorted_elements.items(), key=lambda item: item[1][0], reverse=True
        )
    ]


def crossover(
    parent_1: Individual, parent_2: Individual, neuron_count: int
) -> Individual:
    """
    To select randomly genes from parents to the child, we first Create a copy / mask of the shape of the parent weight
    matrix, and fill it with random float numbers (0 to 1). Then, we replace them by a bool to determine which parent
    should give its gene
    """
    mask_w1 = np.random.rand(*parent_1.W1.shape) > 0.5
    child_w1 = np.where(mask_w1, parent_1.W1, parent_2.W1)
    mask_w2 = np.random.rand(*parent_1.W2.shape) > 0.5
    child_w2 = np.where(mask_w2, parent_1.W2, parent_2.W2)
    return Individual(
        W1=child_w1,
        W2=child_w2,
        brain=Brain.create_model(input_shape=INPUT_SHAPE, neuron_count=neuron_count),
    )


def add_mutation(individual: Individual, mutation_rate: float) -> None:
    """add small random mutation on the weight"""
    mutation_mask_w1 = np.random.rand(*individual.W1.shape) < mutation_rate
    individual.W1 += mutation_mask_w1 * np.random.randn(*individual.W1.shape)

    mutation_mask_w2 = np.random.rand(*individual.W2.shape) < mutation_rate
    individual.W2 += mutation_mask_w2 * np.random.randn(*individual.W2.shape)
