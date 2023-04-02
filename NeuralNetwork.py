import numpy as np


class NeuralNetwork:
    structure = [2, 3, 2]

    def __init__(self):
        self.construct() # Construct weights and baises 

    def construct(self):
        self.layers = list() # Declare layers list


        for i, startNeurons in enumerate(self.structure): # Loop structure
            layer = list() # Declare layer list
            if i >= len(self.structure) - 1: break # Break last iteration
            neurons = self.structure[i + 1] # End neurons size
            weights = np.random.random((neurons, startNeurons)) # Make random weights matrix
            layer.append(weights)
            bias = np.random.random((neurons, 1)) # Make random biases list
            layer.append(bias)
            self.layers.append(layer)

    def calculateNetwork(self, inputValues):
        layerValues = inputValues # Initialize layerValues to input
        for layer in self.layers: # Loop each layer
            weights, bias = layer[0], layer[1] # Initialize weights and biases
            layerValues = self.calculateLayer(layerValues, weights, bias)
        return layerValues # Return final layer

    def calculateLayer(self, inputValues, weights, bias): # Calculate layer (x*w+b=y)
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
    print(nn.calculateNetwork([0.2, 0.1]))
