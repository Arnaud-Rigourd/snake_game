import random
from uuid import UUID

import numpy as np

from ML.models.brain import Brain
from ML.models.individual import Individual, INPUT_SHAPE


def generate_new_generation(
    unsorted_elements: dict[Individual, float],
    *,
    generation_size: int,
    mutation_rate: float,
    neuron_count: int,
):
    new_generation = []
    granted_parents = []
    # sort players by score and keep x% of the best
    sorted_parents = get_sorted_elements(unsorted_elements)
    granted_parents.extend(sorted_parents[: int(len(unsorted_elements) * 0.3)])
    # keep x% of random of the generation, no matter there reward
    random_parents = random.choices(
        sorted_parents[len(granted_parents) :], k=int(len(unsorted_elements) * 0.2)
    )
    granted_parents.extend(random_parents)
    # create new player from granted parents
    for _ in range(int(len(granted_parents) / 2)):
        parent_1, parent_2 = random.sample(granted_parents, 2)
        for parent in {parent_1, parent_2}:
            granted_parents.remove(parent)
        child = crossover(parent_1, parent_2)
        add_mutation(child, mutation_rate)
        new_generation.append(child)

    # fill the new generation with completely new elements
    new_elements = Individual.create_generation(
        generation_size - len(new_generation), neuron_count=neuron_count
    )
    new_generation.extend(new_elements)


def get_sorted_elements(unsorted_elements: dict[Individual, float]) -> list[Individual]:
    """sort elements by the fitness score"""
    return [
        element
        for element, fitness_score in sorted(
            unsorted_elements.items(), key=lambda item: item[1]
        )
    ]


def crossover(parent_1: Individual, parent_2: Individual) -> Individual:
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
        W1=child_w1, W2=child_w2, brain=Brain.create_model(input_shape=INPUT_SHAPE)
    )


def add_mutation(individual: Individual, mutation_rate: float) -> None:
    """add small random mutation on the weight"""
    mutation_mask_w1 = np.random.rand(*individual.W1.shape) < mutation_rate
    individual.W1 += mutation_mask_w1 * np.random.randn(*individual.W1.shape)

    mutation_mask_w2 = np.random.rand(*individual.W2.shape) < mutation_rate
    individual.W2 += mutation_mask_w1 * np.random.randn(*individual.W2.shape)
