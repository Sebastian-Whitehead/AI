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
        self.action = np.random.random(2) * 2 - 1

    def update(self):
        if not self.alive: return
        # self.location = list(pygame.mouse.get_pos()) # Set position to mouse
        self.move()
        self._BoundInsideFrame()
        self._BoxCollider()

    def _BoundInsideFrame(self):
        self.location[0] = max(self.location[0], 0)  # West border
        self.location[0] = min(self.location[0], Settings.screenSize)  # East border
        self.location[1] = max(self.location[1], 0)  # Nord border
        self.location[1] = min(self.location[1], Settings.screenSize)  # South border

    def _BoxCollider(self):
        colliderSize = [self.size * 2] * 2
        colliderLocation = np.subtract(self.location, colliderSize[0] / 2)
        self.collider = pygame.Rect(colliderLocation, colliderSize)

    def draw(self, screen):
        if not self.alive: return
        # pygame.draw.rect(screen, (255, 0, 0), self.collider) # Show collider
        pygame.draw.circle(screen, self.color, self.location, self.size)  # Show creature

    def eyes(self, foodList: list, screen):
        targetFood = targetDistance = None
        foodSize = foodList[0].size[0]
        for food in foodList:
            if food.eaten: continue
            foodX, foodY = food.location[0], food.location[1]
            foodX, foodY = foodX + foodSize / 2, foodY + foodSize / 2
            creatureX, creatureY = self.location[0], self.location[1]
            dx, dy = foodX - creatureX, foodY - creatureY
            distance = np.sqrt(np.power(dx, 2) + np.power(dy, 2))

            if targetDistance == None or distance < targetDistance:
                targetFood = food
                targetDistance = distance

        # Draw line from Creature to Food
        foodX, foodY = targetFood.location[0], targetFood.location[1]
        foodX, foodY = foodX + foodSize / 2, foodY + foodSize / 2
        pygame.draw.line(screen, (0, 0, 0), self.location, (foodX, foodY))

        targetDirection = 0 # Calculate direction to food
        targetFood = [targetDirection, targetDistance] 
        
        self.action = self.neuralNetwork.calculateNetwork(targetFood)

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

    def move(self):
        # TODO: MAP VALUES
        x = np.sin(self.action[0]) * self.action[1]
        y = np.cos(self.action[0]) * self.action[1]
        newLocation = [x, y]
        self.location = np.add(self.location, newLocation)

if __name__ == "__main__":
    creature = Creature()
