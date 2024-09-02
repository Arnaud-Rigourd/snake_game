from typing import Self

from keras import layers, models

from train import NEURON_COUNT


class Brain(models.Sequential):
    @classmethod
    def create_model(cls, input_shape: tuple) -> Self:
        model = cls()
        model.add(
            layers.Dense(NEURON_COUNT, activation="relu", input_shape=input_shape)
        )
        model.add(layers.Dense(NEURON_COUNT, activation="relu"))
        model.add(layers.Dense(4, activation="softmax"))
        return model
