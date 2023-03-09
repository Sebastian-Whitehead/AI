import Settings
import numpy as np
import pygame

class Food:
    def __init__(self, location=None):
        randomLocation = np.random.randint(0, Settings.screenSize, size=(2))
        self.location = location if location else randomLocation
        self.color = Settings.foodColor
        self.size = [Settings.foodSize] * 2
        self.eaten = False

    def update(self):
        self.rect = pygame.Rect(self.location, self.size)

    def draw(self, screen):
        if self.eaten: return
        pygame.draw.rect(screen, self.color, self.rect)

