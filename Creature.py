import numpy as np
import Settings
import pygame
import NeuralNetwork


class Creature:

    def __init__(self, location: list = None, size: int = Settings.creatureSize, color: list = None):
        randomLocation = np.random.randint(0, Settings.screenSize, size=(2))
        self.location = location if location else randomLocation
        self.size = size
        randomColor = np.random.randint(0, 255, size=(3))
        self.color = color if color else randomColor
        self.neuralNetwork = NeuralNetwork.NeuralNetwork()
        self.alive = True

    def update(self):
        if not self.alive: return
        # self.location = list(pygame.mouse.get_pos()) # Set position to mouse
        self.move()

        # Bound in frame
        self.location[0] = max(self.location[0], 0)  # West border
        self.location[0] = min(self.location[0], Settings.screenSize)  # East border
        self.location[1] = max(self.location[1], 0)  # Nord border
        self.location[1] = min(self.location[1], Settings.screenSize)  # South border

        # Make box collider
        colliderSize = [self.size * 2] * 2
        colliderLocation = np.subtract(self.location, colliderSize[0] / 2)
        self.collider = pygame.Rect(colliderLocation, colliderSize)

    def draw(self, screen):
        if not self.alive: return
        # pygame.draw.rect(screen, (255, 0, 0), self.collider) # Show collider
        pygame.draw.circle(screen, self.color, self.location, self.size)  # Show creature

    def eat(self, foodList: list):
        for food in foodList:
            checkFoodCollision = pygame.Rect.colliderect(self.collider, food.rect)
            if not checkFoodCollision: continue
            food.eaten = True

    def collide(self, wallList: list):
        for wall in wallList:
            checkWallCollision = pygame.Rect.colliderect(self.collider, wall.rect)
            if not checkWallCollision: continue
            self.alive = False

    def moveRandom(self):
        randomVector = np.random.random(2) * 2 - 1
        newLocation = np.add(self.location, randomVector)
        self.location = newLocation

    def move(self):
        self.moveRandom()
        pass


if __name__ == "__main__":
    Creature()