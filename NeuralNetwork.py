import numpy as np


class NeuralNetwork:
    inputNeurons = 2
    hiddenLayers = 2
    hiddenNeurons = 3
    outputNeurons = 2

    artic = [2, 3, 3, 2]

    def __init__(self):

        self.make()

    def make(self):
        self.layers = list()
        self.weights = list()
        self.biases = list()

        for i, test in enumerate(self.artic):
            if i >= len(self.artic) - 2: break
            neurons = self.artic[i + 1]
            weights = np.random.random((neurons, test))
            self.weights.append(weights)
            bias = np.random.random((neurons, 1))
            self.biases.append(bias)

    def see(self, eyes):
        pass

    def calculate(self, input, weights, bias):
        layer = np.multiply(input, weights)
        layer = np.add(layer, bias)
        layer = np.sum(layer, axis=1)
        layer = np.transpose(layer)
        layer = 1 / (1 + np.exp(-layer))

        self.layers.append(layer)

        return layer

    def PrintLayers(self):
        for layer in self.layers:
            print(layer)

    def __str__(self):
        for weights, bias in zip(self.weights, self.biases):
            print("*")
            print(weights)
            print("+")
            print(bias)
            print("=")
            #print(layer)
        return ""


if __name__ == "__main__":
    neuralNetwork = NeuralNetwork()
    print(neuralNetwork)
