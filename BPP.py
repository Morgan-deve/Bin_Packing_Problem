import numpy as np
import random



########################## Read Data####################


def readInstances(instanceFile: str):
    instanceSet = open(instanceFile, "r")
    itemsLen = int(instanceSet.readline())
    binSize = int(instanceSet.readline())
    itemsIndex = []
    items = {}
    for i in range(itemsLen):
        items[i] = int(instanceSet.readline())
        itemsIndex.append(i)

    return itemsLen, binSize, items, itemsIndex


def initialize():
    random.shuffle()
    return


def fitness(individual, items, bin_capacity):
    
    num_bins_used = 0
    unique_bins = np.unique(individual)
    
    for bin_id in unique_bins:
        
        total_weight = sum([items[i] for i in range(len(items)) if individual[i] == bin_id])
        if total_weight > bin_capacity:
            return float('inf') 
        num_bins_used += 1
    
    return num_bins_used  

# population = initialize_population(5, items, bin_capacity)
# for i, individual in enumerate(population):
#     print(f"Individual {i+1}: {individual} - Fitness: {fitness(individual, items, bin_capacity)}")



def tournament_selection(population, fitness, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        competitors = np.random.choice(population, tournament_size)
        selected.append(max(competitors, key=lambda ind: fitness(ind)))
    return selected

            ############cycle crossover#########


def cycle_crossover(parent1, parent2):
    """ Perform Cycle Crossover (CX) between two parent permutations. """
    
    # Initialize offspring with None values
    size = len(parent1)
    offspring1, offspring2 = [None]*size, [None]*size
    
    # Helper function to find cycles
    def create_cycle(p1, p2):
        cycle = []
        index = 0
        while index not in cycle:
            cycle.append(index)
            index = p1.index(p2[index])
        return cycle
    
    # Step 1: Find cycle starting from position 0
    cycle = create_cycle(parent1, parent2)
    
    # Step 2: Copy the cycle elements from parent1 to offspring1, and parent2 to offspring2
    for i in cycle:
        offspring1[i] = parent1[i]
        offspring2[i] = parent2[i]
    
    # Step 3: Fill in the remaining positions with the opposite parent's genes
    for i in range(size):
        if offspring1[i] is None:
            offspring1[i] = parent2[i]
        if offspring2[i] is None:
            offspring2[i] = parent1[i]
    
    return offspring1, offspring2

# Example usage
parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
parent2 = [4, 1, 2, 8, 7, 6, 5, 3]

offspring1, offspring2 = cycle_crossover(parent1, parent2)
print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Offspring 1:", offspring1)
print("Offspring 2:", offspring2)


                ########order crossover#########


import numpy as np

def ox_crossover(parent1, parent2):
    """ Perform Order Crossover (OX) between two parent permutations. """
    
    # Length of the parent chromosomes
    size = len(parent1)
    
    # Initialize offspring with None values
    offspring1, offspring2 = [None]*size, [None]*size
    
    # Randomly select two crossover points
    cx_point1, cx_point2 = sorted(np.random.choice(range(size), 2, replace=False))
    
    # Step 1: Copy the segment between crossover points
    offspring1[cx_point1:cx_point2] = parent1[cx_point1:cx_point2]
    offspring2[cx_point1:cx_point2] = parent2[cx_point1:cx_point2]
    
    # Step 2: Fill the remaining positions from the other parent in order
    def fill_offspring(offspring, parent, cx_point1, cx_point2):
        current_position = cx_point2 % size
        for gene in parent:
            if gene not in offspring:
                offspring[current_position] = gene
                current_position = (current_position + 1) % size
                
    # Fill offspring1 with remaining genes from parent2
    fill_offspring(offspring1, parent2, cx_point1, cx_point2)
    # Fill offspring2 with remaining genes from parent1
    fill_offspring(offspring2, parent1, cx_point1, cx_point2)
    
    return offspring1, offspring2

# Example usage
parent1 = [1, 2, 3, 4, 5, 6, 7, 8]
parent2 = [4, 1, 2, 8, 7, 6, 5, 3]

offspring1, offspring2 = ox_crossover(parent1, parent2)
print("Parent 1:", parent1)
print("Parent 2:", parent2)
print("Offspring 1:", offspring1)
print("Offspring 2:", offspring2)

