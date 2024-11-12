from numpy import average
import random
import matplotlib.pyplot as plt






populationsize = 50
maxRounds = 5000
crossoverProbability = 0.8
mutationProbability = 0.05



########################## Read Data####################


def readInstances(instanceFile: str):
    instanceSet = open(instanceFile, "r")
    instancelen = int(instanceSet.readline())
    binSize = int(instanceSet.readline())
    itemsindex = []
    items = {}
    for i in range(instancelen):
        items[i] = int(instanceSet.readline())
        itemsindex.append(i)

    return instancelen, binSize, items, itemsindex

                ############fitnes###########
                
def bin_count(itemsindex: list, items: object):
    bins = 1
    bin_capacity = 0
    fitness = 0
    
    for i in itemsindex:
        if (bin_capacity + items[i] > binSize):
            fitness += fitnessbin(bin_capacity)
            bins += 1
            bin_capacity = items[i]
            
        else:
            bin_capacity += items[i]
            
        fitness += fitnessbin(bin_capacity)
        
    return fitness, bins

def fitnessbin(binFilledcapacity: int):
    return (binFilledcapacity/binSize)**4

            

                    #######initialization######
                    

def initialize(itemsindex:list, items:object):
    population = []
    for _ in range(populationsize):
        random.shuffle(itemsindex)
        fitness, bins = bin_count(itemsindex, items)
        population.append({'genotype': itemsindex[:],  'fitness': fitness,'bin_count': bins})
    return sorted(population, key=lambda geno: -geno['fitness'])

                                                        #######parents selection####

def rouletselection(poluation: list):
    fitness_sum= sum(p['fitness'] for p in poluation)
    index = random.random() * fitness_sum
    
    fitness =0 
    for genotype in population:
        fitness += genotype['fitness']
        if (fitness > index):
            return genotype


                                                    #######mutation selection####

def insert_mutation(child: list):
    if (random.random() > mutationProbability):
        return child
    randomindex = random.sample(range(len(child)), 2)
    gen2 = child[randomindex[1]]
    child.remove(gen2)
    child.insert(randomindex[0], gen2)
    
    return child


def inversion_mutation(child: list):
    if (random.random() > mutationProbability):
        return child
    
    randomindex = random.sample(range(len(child)), 2)
    randomindex.sort()
    
    rep1 = child[: randomindex[0]]
    rep2 = child[randomindex[0]: randomindex[1]+1]
    rep2.reverse()
    rep3 = child[randomindex[1]+1:]
    
    child = rep1 + rep2 + rep3
    
    return child

def swap_mutation(child: list):
    if (random.random() > mutationProbability):
        return child
    
    randomindex = random.sample(range(len(child)), 2)
    rep1 = child[randomindex[0]]
    rep2 = child[randomindex[1]]
    child[randomindex[0]] = rep2
    child[randomindex[1]] = rep1
    
    return child

                                                ######crossover###########
                                                
                      
                                                
def ox_crossover(parents1, parents2):
    if (random.random() > crossoverProbability):
        return parents1, parents2
    
    point1 = random.randint(0, instancelen - 2)
    point2 = random.randint(point1 +1, instancelen - 1)
    
    child1 = [None]*instancelen
    child2 = [None]*instancelen
    
    child1[point1: point2] = parents1[point1: point2]
    child2[point1: point2] = parents2[point1: point2]
    
    child1_index = point2
    child2_index = point2
    
    for i in range(instancelen):
        index = i+point2
        if (index >= instancelen):
            index -= instancelen
            
        if (parents2[index] not in child1):
            child1[child1_index] = parents2[index]
            child1_index += 1
            if (child1_index >= instancelen):
                child1_index -= instancelen
                
        if (parents1[index] not in child2):
            child2[child2_index] = parents1[index]
            child2_index += 1
            if (child2_index >= instancelen):
                child2_index -= instancelen
                
    return child1, child2

def caf_crossover(parents1, parents2):                  #cut and fill crossover
    if (random.random() > crossoverProbability):
        return [parents1, parents2]
    
    point = random.randint(1, instancelen -1)
    child1 = parents1[0:point]
    child2 = parents2[0:point]
    
    for i in range(len(parents1)):
        index = i + point
        
        if (index >= instancelen):
            index -= instancelen
        if parents1[index] not in child2:
            child2.append(parents1[index])
        if parents2[index] not in child1:
            child1.append(parents2[index])
    
    return child1, child2
 
   
                                                    ##### elitism ####


def elitism(population, childs):
    for geno in population:
        if(childs['fitness'] >= geno['fitness']):
            population[population.index(geno)] = childs
        break
    return sorted(population, key=lambda geno: geno['fitness'])

                                                    ####### main ######
            
round = 0

instancelen, binSize, items, itemsindex = readInstances("./instance_sets/5.txt")
population = initialize(itemsindex, items)

generationsfitness = []
generationsbins = []
while round < maxRounds:
                        ####parents selections #####
    generationsfitness.append([i['fitness'] for i in population])
    generationsbins.append([i['bin_count'] for i in population])
    
    #roulet selections 
    parents1 = rouletselection(population)
    parents2 = rouletselection(population)
    
    
                        #### crossover####
    
    #ox crosover
    child1, child2 = ox_crossover(parents1['genotype'], parents2['genotype'])
    
    #cut and fill crossover
    # child1, child2 = caf_crossover(parents1['genotype'], parents2['genotype'])
    
                        ##### mutation####
            

    #insert mutation
    # mutatedchild1 = insert_mutation(child1)
    # mutatedchild2 = insert_mutation(child2)
    
    #inversion mutation
    # mutatedchild1 = inversion_mutation(child1)
    # mutatedchild2 = inversion_mutation(child2)
     
    #swap mutation
    mutatedchild1 = swap_mutation(child1)
    mutatedchild2 = swap_mutation(child2)
    
    #check fitness
    fitness1, bins1 = bin_count(child1, items)
    fitness2, bins2 = bin_count(child2, items)
    
    #elitism
    population = elitism(population, {'genotype': mutatedchild1, 'fitness': fitness1,'bin_count': bins1})
    population = elitism(population, {'genotype': mutatedchild2, 'fitness': fitness2,'bin_count': bins2})
    
    round +=1
    
# print(population)
# print (items)

bins_counts = []
for chromosome in population:
    bins_counts.append(chromosome['bin_count'])
    
    
plt.figure(figsize=(10, 6))
plt.hist(bins_counts, color='skyblue', align='mid')
plt.title('Frequency of Bin Counts in Population')
plt.xlabel('Number of Bins')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

def result(items: object, ind: object, binSize: int, name: str):
    def printList(l: list):
        return " ".join(map(str, l))
    
    bincount = ind["bin_count"]
     
    with open(name, 'w') as file:
        file.write(f"{bincount}\n")
        itemList = []
        bin_capacity = 0
        for item in ind["genotype"]:
            if ( bin_capacity + items[item] <= binSize):
                itemList.append(item +1)
                bin_capacity += items[item]
            else:
                x = printList(itemList)
                file.write(f"{x}\n")
                itemList = [item +1]
                bin_capacity = items[item]
                
        x = printList(itemList)
        file.write(f"{x}\n")
        
# result(items, population[0], 10000, 'instance5.txt')

def max_mean_fitness(generationsfitness: list, generationCount: int, title: str ):
    maxFitness = []
    meanFitness = []
    plt.figure()
    allGen = []
    for i in range(generationCount):
        allGen.append(i)

    for fitnessList in generationsfitness:
        maxFitness.append(max(fitnessList))
        meanFitness.append(average(fitnessList))

    plt.plot(allGen, meanFitness, label='Average Fitness',
             color='r', linestyle='dashed')
    plt.plot(allGen, maxFitness, label='Best Fitness', color='b')

    plt.xlabel('Generation')
    plt.ylabel('Fitness')

    plt.title(f'Fitness Generations :\n {title}')

    plt.legend()
    plt.grid()

    plt.show()

# max_mean_fitness(generationsfitness, 5000, 'fitness_cut and fill_crossover-swap mutation')


def max_mean_bins(generationsbins: list, generationCount: int, title: str):
    minBin = []
    meanBin = []
    plt.figure()
    allGen = []
    for i in range(generationCount):
        allGen.append(i)

    for binsList in generationsbins:
        minBin.append(min(binsList))
        meanBin.append(average(binsList))

    plt.plot(allGen, meanBin, label='Average Bins',
             color='r', linestyle='dashed')
    plt.plot(allGen, minBin, label='Best Bins', color='b')

    plt.xlabel('Generation')
    plt.ylabel('Bins')

    plt.title(f'Bins Generations :\n {title}')

    plt.legend()
    plt.grid()

    plt.show()
    
    
# max_mean_bins(generationsbins, 5000, 'bins_cut and fill_crossover-swap mutation' )

