import pygame

import Settings
from Creature import *
from Food import *
from Walls import *
import GeneticAlgorithm


def Simulation(screen, generation, population, simSec):
    foodList = [Food() for _ in range(Settings.foodCount)]
    walls = []
    font = pygame.font.Font('freesansbold.ttf', 32)

    # Run until the user asks to quit
    running = True
    TotElapsedFrames = 0
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
        screen.fill([255] * 3)  # Fill the background with white

        for food in foodList:
            food.update()
            food.draw(screen)

        walls = drawWall(walls)
        for wall in walls:
            wall.draw(screen)

        for creature in population:
            if not creature.alive: continue
            creature.eyes(foodList, screen)
            creature.update(screen)
            creature.collide(walls)
            creature.eat(foodList)
            creature.draw(screen)
            creature.CalculateFitness()

        best = sorted(population, key=lambda x: x.fitness, reverse=True)[0]
        best.DrawBest(screen)
        secText = font.render(f'Best: {best.fitness}', True, (0, 0, 0))
        screen.blit(secText, (20, 100))

        genText = font.render(f'Gen: {generation}', True, (0, 0, 0))
        screen.blit(genText, (20, 20))

        FramesCountDown = simSec * Settings.FrameRate * generation
        TotElapsedFrames += 1
        elapsedSec = round(FramesCountDown - TotElapsedFrames, 2)
        secText = font.render(f'Frames: {elapsedSec}', True, (0, 0, 0))
        screen.blit(secText, (20, 60))

        pygame.display.flip()  # Flip the display
        pygame.display.update()

        if elapsedSec >= 0: continue
        # pygame.quit()  # Done! Time to quit.
        return


def main():
    population = [Creature(i) for i in range(Settings.populationSize)]
    center = [Settings.screenSize / 2, Settings.screenSize / 2]
    for creature in population: creature.location = center

    pygame.init()
    screen = pygame.display.set_mode([Settings.screenSize] * 2)  # Set up the drawing window
    pygame.display.set_caption('Show Text')

    for generation in range(Settings.maxGenerations):
        Simulation(screen, generation, population, simSec=15)
        average = np.mean([pop.fitness for pop in population])
        print(f'Gen {generation} mean: {average}')
        population = GeneticAlgorithm.NextGen(population)


if __name__ == "__main__":
    main()
