import copy
import random

import numpy as np
from Creature import Creature
import Settings

def NextGen(population):
    nextPop = []
    sortedPop = sorted(population, key=lambda x: x.fitness, reverse=True)
    elites = sortedPop[:int(len(population) * 0.20)]
    for elite in elites: nextPop.append(Creature(id=len(nextPop), DNA=elite.neuralNetwork.DNA))

    while len(nextPop) < len(population):
        newDNA = CrossParents(elites)
        mutatedDNA = Mutate(newDNA)
        child = Creature(len(nextPop), DNA=mutatedDNA)
        nextPop.append(child)

    return nextPop

def Mutate(DNA):
    if np.random.uniform() >= Settings.mutationChance: return DNA

    randomDNAIndex = np.random.randint(len(DNA))
    mutationWeight = Settings.mutationWeight
    diviation = np.random.uniform(-1, 1) * mutationWeight
    DNA[randomDNAIndex] += diviation

    return DNA

def CrossParents(population):
    father = BattleGenetics(population, 1)
    mother = BattleGenetics(population, 1)
    splitPoint = np.random.randint(len(father.neuralNetwork.DNA))
    #splitPoint = int(len(father.neuralNetwork.DNA))/2)
    halfFatherDNA = father.neuralNetwork.DNA[:splitPoint]
    halfMotherDNA = mother.neuralNetwork.DNA[splitPoint:]
    newDNA = np.concatenate((halfFatherDNA, halfMotherDNA))
    return newDNA
    #return father.neuralNetwork.DNA

def BattleGenetics(population, arenaSize):
    arena = []
    while len(arena) < arenaSize:
        randomParent = np.random.choice(population)
        if randomParent in arena: continue
        if not randomParent.alive: randomParent.fitness = -100
        mean = np.mean([pop.fitness for pop in population])
        #if mean > 0 and randomParent.fitness == 0: continue
        arena.append(randomParent)
    sortedArena = sorted(arena, key=lambda x: x.fitness, reverse=True)
    winner = sortedArena[0]
    return winner

if __name__ == "__main__":
    population = [Creature() for _ in range(2)]
    for creature in population:
        print(creature)
    population = NextGen(population)
    for creature in population:
        print(creature)
