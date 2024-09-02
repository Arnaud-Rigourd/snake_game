import uuid
from typing import Self

import numpy as np

from ML.models.brain import Brain
from models.game import SnakeGame

INPUT_SHAPE = (3,)
INPUT_SIZE = 3
OUTPUT_SIZE = 4


class Individual:
    id: uuid.UUID
    brain: Brain
    W1: np.ndarray
    W2: np.ndarray

    def __init__(self, **kwargs):
        self.id = uuid.uuid4()
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def create_generation(cls, generation_size: int, neuron_count: int) -> list[Self]:
        return [
            cls.create_individual(hidden_size=neuron_count)
            for _ in range(generation_size)
        ]

    @classmethod
    def create_individual(cls, hidden_size: int) -> Self:
        return cls(
            W1=np.random.randn(INPUT_SIZE, hidden_size),
            W2=np.random.randn(hidden_size, OUTPUT_SIZE),
            brain=Brain.create_model(input_shape=INPUT_SHAPE),
        )

    @staticmethod
    def fitness(game: SnakeGame) -> float:
        return float(round(game.score / game.life_time, 3))

    def __repr__(self):
        return "Individual"
