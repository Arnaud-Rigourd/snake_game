from typing import Self

from keras import layers, models


class Brain(models.Sequential):
    @classmethod
    def create_model(cls, input_shape: tuple, neuron_count: int) -> Self:
        model = cls()
        model.add(
            layers.Dense(neuron_count, activation="relu", input_shape=input_shape)
        )
        model.add(layers.Dense(neuron_count, activation="relu"))
        model.add(layers.Dense(4, activation="softmax"))
        return model
