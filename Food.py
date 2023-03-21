import Settings
import numpy as np
import pygame


class Food:
    def __init__(self, location: list = None) -> None:
        randomLocation = np.random.randint(0, Settings.screenSize, size=(2))
        self.location = location if location else randomLocation
        self.color = Settings.foodColor
        self.size = [Settings.foodSize] * 2
        self.eaten = False

    def update(self):
        self.rect = pygame.Rect(self.location, self.size)  # Create rectangle

    def draw(self, screen):
        if self.eaten: return  # Don't show if eaten
        pygame.draw.rect(screen, self.color, self.rect)  # Draw food
