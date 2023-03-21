import numpy as np
import pygame


class Wall:
    size = np.array([20] * 2)

    def __init__(self, location):
        self.location = location - np.divide(self.size, 2)

    def draw(self, screen):
        self.rect = pygame.Rect(self.location, self.size)  # Create rectangle
        pygame.draw.rect(screen, [0] * 3, self.rect)  # Draw wall


def drawWall(walls: list):
    if np.any(pygame.mouse.get_pressed(3)):
        mousePos = pygame.mouse.get_pos()
        walls.append(Wall(mousePos))
    return walls
