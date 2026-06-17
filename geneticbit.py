#next the idea is to create a version where we transform the number to a float 
# and numbers with lower indicies are more likel to mutate 1/x *k 
# whislt higher indices are more likley to mutate. Maybe keeping an overall chempion is a good idea?
import struct
import numpy as np
from random import choices, randint,randrange, random
from MinimaFunction import minimum_finder

def genetic_finderb(problem, sample, termination=None, seed=None, **kwargs):
    
    
    
    def generate_population(size):
        narray =  np.random.uniform(problem.bounds[0], problem.bounds[1],size)
        return normaliser(narray, problem)
    
    def fitness(x):
        return problem._evaluate(denormaliser(x,problem))
    
    def selection_pair(population , fitness_func):
        population = np.array(population)
        fit = problem._evaluate(denormaliser(population,problem)) 
        worst = max(fit) # I think that if we use for genome in population menas going torugh each element of the lsit its not literarlly the worst.
        return choices(
            population = population,
            weights = worst - fit+ 1e-9,
            k=2
        )
        
    
    # def crossover(a,b):
    #     a = float_to_bits(a)
    #     b = float_to_bits(b)
    #     x = randint(1,63)
    #     return bits_to_float(a[0:x] +b[x:]) , bits_to_float(b[:x] + a[x:])
    def crossover(a , b):
        alpha = np.random.rand()
        x1,x2 = alpha*denormaliser(a,problem) + (1-alpha)*denormaliser(b,problem), (1-alpha)*denormaliser(a,problem) + alpha*denormaliser(b,problem)
        return normaliser(x1,problem), normaliser(x2,problem) #keeps the list as normalised.

    def mutation(a, current, max ): #we exepct an a which is alredy  normilsed, remmebr to check this in case it is not.
        if(a >= 1):
            a = 0.99999999999999
        last_values = int(f"{a:.15f}".split('.')[1])
        a = to_n_array(last_values)
        k = (8/max*current)+1
        b=1/200
        for i in range(len(a)): # starts from 0 index of the new numebr so we want to change the smaller numbers at the ened muhc more
            if random() < b+(1-b)*(i/49)**k:
                a[i] = abs(a[i]-1)
        return np.clip(to_n_value(a) / 10**15, 0.0, 1.0) # note that this does take our current value and devides it by 10 to the 15 first before retuning it and does not return before division (must complete all operations first)
        

    def run_evolution(
    populate_func,
    fitness_func,
    new_population_size,
    selection_func,
    crossover_func,
    mutation_func,
    generation_limit,
    ):
        population = populate_func(new_population_size)
        for i in range(generation_limit):
            fit = np.asarray(fitness_func(population), dtype=float)
            order = np.argsort(fit)
            population = np.asarray(population)[order]
            fit = fit[order]
            next_generation = population[0:2].tolist()
            num_pairs = int(np.ceil((new_population_size - 2) / 2))
            for j in range(num_pairs):
                paretns = selection_func(population, fit)
                offspring_a , offspring_b = crossover_func(paretns[0],paretns[1])
                offspring_a = mutation_func(offspring_a, i,generation_limit) 
                offspring_b = mutation_func(offspring_b, i,generation_limit)
                next_generation += [offspring_a, offspring_b]
            population = np.asarray(next_generation[:new_population_size])
        fit = np.asarray(fitness_func(population), dtype=float)
        order = np.argsort(fit)
        population = np.asarray(population)[order]
        
    
        best = minimum_finder(population[0], fitness)
        return denormaliser(best,problem), fitness(best)   
    
    
    x_coordinate, y_coordinate = run_evolution(generate_population, fitness ,sample, selection_pair, crossover , mutation , 100)
                                               
    return x_coordinate,y_coordinate





def normaliser(x,problem):
    return (x-problem.bounds[0])/(problem.bounds[1]-problem.bounds[0])



def denormaliser(xnorm,problem):
    return  (xnorm*(problem.bounds[1]-problem.bounds[0]))+problem.bounds[0]


def to_n_array(value):
    arr = np.zeros(50, dtype=int)
    for i in range(49,-1,-1):
        if value>=2**i:
            arr[49-i] = 1
            value = value - 2**i
        if value == 0:
            break
    return arr

def to_n_value(array):
    return sum(array * 2**np.arange(49, -1, -1))





