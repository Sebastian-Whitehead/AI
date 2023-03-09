from Creature import *
from Food import *

population = []
for i in range(Settings.populationSize):
    creature = Creature()
    population.append(creature)

foodList = []
for i in range(Settings.foodCount):
    food = Food()
    foodList.append(food)

pygame.init()

screen = pygame.display.set_mode([Settings.screenSize] * 2)  # Set up the drawing window

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

    for creature in population:
        creature.update()
        creature.eat(foodList)
        creature.draw(screen)

    pygame.display.flip()  # Flip the display

pygame.quit()  # Done! Time to quit.
