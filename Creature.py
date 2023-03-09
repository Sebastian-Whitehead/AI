import numpy as np
import Settings
import pygame
import NeuralNetwork

class Creature:

    def __init__(self, location=None, size=Settings.creatureSize, color=None):
        randomLocation = np.random.randint(0, Settings.screenSize, size=(2))
        self.location = location if location else randomLocation
        self.size = size
        randomColor = np.random.randint(0, 255, size=(3))
        self.color = color if color else randomColor
        self.neuralNetwork = NeuralNetwork.NeuralNetwork()

    def update(self):
        self.location = list(pygame.mouse.get_pos())

        self.move()

        # Bound
        if self.location[0] < 0: self.location[0] = 0
        if self.location[0] > Settings.screenSize: self.location[0] = Settings.screenSize
        if self.location[1] < 0: self.location[1] = 0
        if self.location[1] > Settings.screenSize: self.location[1] = Settings.screenSize

        # Make box collider
        colliderSize = [self.size * 2] * 2
        colliderLocation = np.subtract(self.location, colliderSize[0] / 2)
        self.collider = pygame.Rect(colliderLocation, colliderSize)

    def draw(self, screen):
        # pygame.draw.rect(screen, (255, 0, 0), self.collider) # Show collider
        pygame.draw.circle(screen, self.color, self.location, self.size)

    def eat(self, foodList):
        for food in foodList:
            if not pygame.Rect.colliderect(self.collider, food.rect): continue
            food.eaten = True

    def move(self):
        pass


if __name__ == "__main__":
    Creature()
