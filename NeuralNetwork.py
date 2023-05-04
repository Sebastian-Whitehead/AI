import numpy as np
import pygame

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

    def ShowNN(self, originalScreen):

        # Circle and line attributes
        circle_line_width = 2
        circle_radius = 10
        circle_margin_width = 20
        circle_margin_height = 5
        total_circle_line_width = circle_radius * 2 + circle_margin_width * 2
        total_circle_height = circle_radius * 2 + circle_margin_height * 2
        line_width_scale = 5

        # Colors
        circle_color = (0, 0, 0)
        positive_weight_color = (0, 255, 0)
        negative_weight_color = (255, 0, 0)
        white = [255] * 3

        # set screen size
        width, height = 200, 150
        screen = pygame.Surface((width, height))
        screen.fill(white)  # Fill the background with white

        center = (width / 2, height / 2)
        layers = len(self.structure)
        layerstest = []
        for layer, nodes in enumerate(self.structure):
            layertest = []
            for node in range(nodes):
                xOffSet = -(layers * total_circle_line_width) / 2
                xOffSet += layer * total_circle_line_width
                xOffSet += total_circle_line_width / 2

                yOffSet = (nodes * total_circle_height) / 2
                yOffSet -= node * total_circle_height
                yOffSet -= total_circle_height / 2

                coor = (center[0] + xOffSet, center[1] + yOffSet)

                layertest.append(coor)
            layerstest.append(layertest)

        for layer, nodes in enumerate(layerstest):
            for i, node in enumerate(nodes):
                if layer + 1 >= len(layerstest): continue
                nextNodes = layerstest[layer + 1]
                nodes_weights = np.transpose(np.array(self.layers[layer][0]))[i]

                for j, nextNode in enumerate(nextNodes):
                    weight_value = nodes_weights[j]
                    weight_value = int(weight_value * line_width_scale)
                    weight_color = positive_weight_color if weight_value >= 0 else negative_weight_color
                    pygame.draw.line(screen, weight_color, node, nextNode, abs(weight_value))

        for layer, nodes in enumerate(layerstest):
            for i, node in enumerate(nodes):
                pygame.draw.circle(screen, white, node, circle_radius, 0)
                pygame.draw.circle(screen, circle_color, node, circle_radius, circle_line_width)

        originalScreenWidth = pygame.display.get_surface().get_size()[0]
        originalScreen.blit(screen, (originalScreenWidth - width - 10, 10))


if __name__ == "__main__":

    nodes = 0
    structure = NeuralNetwork.structure
    for i in range(len(structure) - 1):
        out = structure[i + 1]
        nodes += structure[i] * out + out
    randomDNA = np.random.random(nodes)

    #DNA = ["w1", "w2", "b1", "w3", "w4", "b2", "w5", "w6", "b3", "w7", "w8", "w9", "b4", "w10", "w11", "w12", "b5"]
    nn = NeuralNetwork(randomDNA)
    print(nn)
    print(nn.calculateNetwork([0.2, 0.1]))

    pygame.init() # initialize pygame
    screen = pygame.display.set_mode([800] * 2)  # Set up the drawing window
    pygame.display.set_caption('Show neural network')
    nn.ShowNN(screen)
    pygame.display.update()

    running = True # run the game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False

    pygame.quit()  # quit pygame


