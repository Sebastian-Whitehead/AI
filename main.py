import pygame
from Creature import *
from Food import *
from Walls import *
import GeneticAlgorithm


def Simulation(screen, generation, population, simSec):
    for creature in population: creature.RandomLocation()
    foodList = [Food() for _ in range(Settings.foodCount)]
    walls = []
    font = pygame.font.Font('freesansbold.ttf', 32)

    # Run until the user asks to quit
    running = True
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
            creature.update()
            creature.collide(walls)
            creature.eyes(foodList, screen)
            creature.eat(foodList)
            creature.draw(screen)

        genText = font.render(f'Size: {len(population)}', True, (0, 0, 0))
        screen.blit(genText, (20, 20))

        genText = font.render(f'Gen: {generation}', True, (0, 0, 0))
        screen.blit(genText, (20, 60))

        SecondsCountDown = simSec * generation
        TotElapsedSec = pygame.time.get_ticks() / 1000
        elapsedSec = round(SecondsCountDown - TotElapsedSec, 2)
        secText = font.render(f'Sec: {elapsedSec}', True, (0, 0, 0))
        screen.blit(secText, (20, 100))

        pygame.display.flip()  # Flip the display
        pygame.display.update()

        if elapsedSec >= 0: continue
        # pygame.quit()  # Done! Time to quit.
        return


def main():
    population = [Creature() for _ in range(Settings.populationSize)]

    pygame.init()
    screen = pygame.display.set_mode([Settings.screenSize] * 2)  # Set up the drawing window
    pygame.display.set_caption('Show Text')

    for generation in range(10):
        Simulation(screen, generation, population, simSec=5)
        # GeneticAlgorithm


if __name__ == "__main__":
    main()
