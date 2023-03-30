import numpy as np


class NeuralNetwork:
    structure = [2, 3, 2]

    def __init__(self):
        self.construct()

    def construct(self):
        self.layers = list()

        for i, startNeurons in enumerate(self.structure):
            layer = list()
            if i >= len(self.structure) - 1: break
            neurons = self.structure[i + 1]
            weights = np.random.random((neurons, startNeurons))
            layer.append(weights)
            bias = np.random.random((neurons, 1))
            layer.append(bias)
            self.layers.append(layer)

    def calculateNetwork(self, inputValues):
        layerValues = inputValues
        for layer in self.layers:
            weights, bias = layer[0], layer[1]
            layerValues = self.calculateLayer(layerValues, weights, bias)
        return layerValues

    def calculateLayer(self, inputValues, weights, bias):
        layer = np.multiply(inputValues, weights)
        layer = np.add(layer, bias)
        layer = np.sum(layer, axis=1)
        layer = np.transpose(layer)
        layer = 1 / (1 + np.exp(-layer))

        return layer

    def PrintLayers(self):
        for layer in self.layers:
            print(layer)

    def __str__(self):
        for weights, bias in self.layers:
            print("Weights")
            print(weights)
            print("Bias")
            print(bias)
        return ""


if __name__ == "__main__":
    nn = NeuralNetwork()
    print(nn)
    nn.calculateNetwork([0.2, 0.1])
