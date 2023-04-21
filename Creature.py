import math

import numpy as np
import Settings
import pygame
import NeuralNetwork


class Creature:

    def __init__(self,
                 id: int,
                 location: list = None,
                 size: int = Settings.creatureSize,
                 color: list = None,
                 DNA: list = None):
        self.id = id
        if location: self.location = location
        else: self.RandomLocation()
        self.size = size
        randomColor = np.random.randint(0, 255, size=(3))
        self.color = color if color else randomColor
        self.neuralNetwork = NeuralNetwork.NeuralNetwork(DNA)
        self.alive = True
        self.action = np.random.random(2) * 2 - 1
        self.eaten = 0
        self.energi = 0
        self.fitness = 0
        self.stomich = []
        self.targetDistance = []
        self.rotation = 0
        self.speed = 5

    def RandomLocation(self):
        randomLocation = np.random.randint(0, Settings.screenSize, size=(2))
        self.location = randomLocation

    def update(self, screen):
        if not self.alive: return
        # self.location = list(pygame.mouse.get_pos()) # Set position to mouse
        self.move(screen)
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
        # pygame.draw.rect(screen, (255, 0, 0), self.collider) # Show collider
        pygame.draw.circle(screen, self.color, self.location, self.size)  # Show creature

    def eyes(self, foodList: list, screen):
        targetFood = targetDistance = None
        foodSize = foodList[0].size[0]
        for food in foodList:
            if food.eaten: continue
            if food in self.stomich: continue
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
        pygame.draw.line(screen, [200] * 3, self.location, (foodX, foodY))

        p1x, p1y = self.location
        p2x, p2y = targetFood.location
        targetDirection = math.degrees(math.atan2(p2y - p1y, p2x - p1x)) - self.rotation
        #if targetDirection <= 0: targetDirection = 1
        #else: targetDirection = -1
        if abs(targetDirection) > 180: targetDirection += 360
        targetDirection = targetDirection / 180
        #print(f'{targetDirection=}')
        targetFood = [targetDirection] #, targetDistance]
        #if self.id == 0: print("Input:", targetFood)
        self.action = self.neuralNetwork.calculateNetwork(targetDirection)
        #self.action = self.neuralNetwork.calculateNetwork(targetFood)
        #if self.id == 0: print("Output:", self.action)

        self.targetDistance.append(targetDistance)

    def eat(self, foodList: list):
        for food in foodList:
            if food in self.stomich: continue
            if food.eaten: continue
            checkFoodCollision = pygame.Rect.colliderect(self.collider, food.rect)
            if not checkFoodCollision: continue
            #food.eaten = True
            self.eaten += 1
            self.stomich.append(food)

    def collide(self, wallList: list):
        for wall in wallList:
            checkWallCollision = pygame.Rect.colliderect(self.collider, wall.rect)
            if not checkWallCollision: continue
            self.alive = False

    def move(self, screen):
        #direction = self.action[0] * math.pi
        #if self.id == 0: print(self.action)
        #direction = 0 * math.pi
        self.rotation += math.degrees(self.action[0]) * 720 * 0.04
        direction = self.rotation
        #self.speed += self.action[1] * 0.04
        speed = self.speed
        speed = min(speed, 2)
        x = np.cos(math.radians(direction))
        y = np.sin(math.radians(direction))
        newLocation = [x, y]
        newLocation = np.multiply(newLocation, speed)
        self.location = np.add(self.location, newLocation)

        # Draw go to line
        x = np.cos(direction) * speed * 20
        y = np.sin(direction) * speed * 20
        goTo = np.add(self.location, [x, y])
        #pygame.draw.line(screen, [200, 0, 0], self.location, goTo)

        center = [Settings.screenSize / 2, Settings.screenSize / 2]
        distance = np.subtract(self.location, center)
        self.energi = math.sqrt(sum(v**2 for v in distance))
        self.energi = abs(speed)
        #if self.id == 0: print(goTo)
        #if self.id == 0: print(self.action)

        #if self.id == 0: print(self.location)
        #if self.location[0] <= self.size + 5: self.alive = False
        #if self.location[1] <= self.size + 5: self.alive = False
        #if self.location[0] >= Settings.screenSize - self.size - 5: self.alive = False
        #if self.location[1] >= Settings.screenSize - self.size - 5: self.alive = False

    def DrawBest(self, screen):
        if not self.alive: return
        pygame.draw.circle(screen, [200, 0, 0], self.location, self.size + 2, width=0)

    def CalculateFitness(self):
        #self.fitness = self.eaten / self.energi
        self.fitness = round(self.fitness, 5)
        self.fitness = self.eaten
        #self.fitness = np.mean(self.targetDistance) * .5 / (self.eaten + 1)

if __name__ == "__main__":
    creature = Creature()
