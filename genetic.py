#https://www.youtube.com/watch?v=nhT56blfRpE
#https://www.youtube.com/watch?v=uQj5UNhCPuo
#https://www.youtube.com/watch?v=-kpcAa-qKwY


#next the idea is to create a version where we transform the number to a float 
# and numbers with lower indicies are more likel to mutate 1/x *k 
# whislt higher indices are more likley to mutate. Maybe keeping an overall chempion is a good idea?
import numpy as np
from random import choices 
from MinimaFunction import minimum_finder

def genetic_findera(problem, sample, termination=None, seed=None, **kwargs):
    
    def generate_population(size):
        return np.random.uniform(problem.bounds[0], problem.bounds[1],size)
    
    def fitness(x):
        return problem._evaluate(x)
    
    def selection_pair(population , fitness_func):
        population = np.array(population)
        fit = problem._evaluate(population) 
        worst = max(fit) # I think that if we use for genome in population menas going torugh each element of the lsit its not literarlly the worst.
        return choices(
            population = population,
            weights = worst - fit+ 1e-9,
            k=2
        )
        
    def crossover(a , b):
        alpha = np.random.rand()
        return alpha*a + (1-alpha)*b, (1-alpha)*a + alpha*b
    
    
    def mutation(a, num, startIndex, endIndex):
        for _ in range(num):
            a += np.random.uniform(startIndex, endIndex)
            a = np.clip(a, problem.bounds[0], problem.bounds[1])
        return a 
    
    def run_evolution(
    populate_func,
    fitness_func,
    new_population_size,
    selection_func,
    crossover_func,
    mutation_func,
    generation_limit,
    ):
        width = problem.bounds[1] - problem.bounds[0]
        step = width / 20
        population = populate_func(new_population_size)
        for i in range(generation_limit):
            # if i%1000 == 0:
            #     print(i)
            population = sorted(
                population,
                key = fitness_func,
            )
            next_generation = population[0:2]
            for j in range(int(len(population)/2)-1):
                paretns = selection_func(population, fitness_func)
                offspring_a , offspring_b = crossover_func(paretns[0],paretns[1])
                offspring_a = mutation_func(offspring_a, 1, -step, step)
                offspring_b = mutation_func(offspring_b, 1, -step, step)
                next_generation += [offspring_a, offspring_b]
            population = next_generation
        population = sorted(
                population,
                key = fitness_func,
            )
        population[0] = minimum_finder(population[0],fitness)
        return population[0], fitness(population[0])
    
    
    x_coordinate, y_coordinate = run_evolution(generate_population, fitness ,sample, selection_pair, crossover , mutation , 100)
                                               
    
    return x_coordinate,y_coordinate