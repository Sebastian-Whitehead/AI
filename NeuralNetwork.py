import numpy as np


class NeuralNetwork:
    # Input, hidden1, output
    structure = [1, 5, 2]

    def __init__(self, DNA=None):
        self.layers = list()  # Declare layers list
        self.DNA = np.array([])
        if DNA is None: self.constructRandomLayers()  # Construct weights and baises
        else: self.DNAToLayers(DNA)

    def constructRandomLayers(self):
        for i, startNeurons in enumerate(self.structure):  # Loop structure
            layer = list()  # Declare layer list
            if i >= len(self.structure) - 1: break  # Break last iteration
            neurons = self.structure[i + 1]  # End neurons size

            weights = np.random.random((neurons, startNeurons))  # Make random weights matrix
            weights = np.subtract(np.multiply(weights, 2), 1)  # Map weights from -1 to 1
            layer.append(weights)

            bias = np.random.random((neurons, 1))  # Make random biases list
            bias = np.subtract(np.multiply(bias, 2), 1)  # Map biases from -1 to 1
            layer.append(bias)
            self.layers.append(layer)

            # Make DNA string from layers
            group = np.concatenate((weights, bias), axis=1)
            self.DNA = np.concatenate((self.DNA, group.flatten()))

    def DNAToLayers(self, DNA):
        self.DNA = DNA
        DNA = np.array(DNA)
        for i, startNeurons in enumerate(self.structure):  # Loop structure
            if i >= len(self.structure) - 1: break  # Break last iteration
            startNeurons = self.structure[i]
            endNeurons = self.structure[i + 1]  # End neurons size
            layerSize = startNeurons * endNeurons + endNeurons
            layer = DNA[:layerSize]
            DNA = DNA[layerSize:]
            weightsCount = startNeurons * endNeurons
            width = int((weightsCount + endNeurons) / endNeurons)
            shape = (endNeurons, width)
            layer = layer.reshape(shape)

            newLayer = list()  # Declare layer list
            weights = layer[:,:-1]
            newLayer.append(weights)
            bias = layer[:,-1].reshape(endNeurons, 1)
            newLayer.append(bias)
            self.layers.append(newLayer)

    def calculateNetwork(self, inputValues):
        layerValues = inputValues  # Initialize layerValues to input
        for layer in self.layers:  # Loop each layer
            weights, bias = layer[0], layer[1]  # Initialize weights and biases
            layerValues = self.calculateLayer(layerValues, weights, bias)
        return layerValues  # Return final layer

    def calculateLayer(self, inputValues, weights, bias):  # Calculate layer (x*w+b=y)
        layer = np.multiply(inputValues, weights)
        layer = np.add(layer, bias)
        layer = np.sum(layer, axis=1)
        layer = np.transpose(layer)
        layer = self.sigmoid(layer)

        return layer

    def sigmoid(self, input):
        return 1 / (1 + np.exp(-input)) * 2 - 1

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
    DNA = [-0.83022046,  0.44317445, -0.65713954, -0.35838965, -0.73220725, -0.06549296,
      0.13006164, -0.61775492, -0.51673575,  0.40817964, -0.74359962,  0.94213346,
      0.4826172,   0.16676537, -0.21516564, -0.6917134,  -0.54550664]
    #DNA = ["w1", "w2", "b1", "w3", "w4", "b2", "w5", "w6", "b3", "w7", "w8", "w9", "b4", "w10", "w11", "w12", "b5"]
    nn = NeuralNetwork(DNA)
    print(nn)
    print(nn.calculateNetwork([0.2, 0.1]))
