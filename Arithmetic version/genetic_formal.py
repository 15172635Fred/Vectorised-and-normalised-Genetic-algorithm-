#https://www.youtube.com/watch?v=nhT56blfRpE
#https://www.youtube.com/watch?v=uQj5UNhCPuo
#https://www.youtube.com/watch?v=-kpcAa-qKwY


#next the idea is to create a version where we transform the number to a float 
# and numbers with lower indicies are more likel to mutate 1/x *k 
# whislt higher indices are more likley to mutate. Maybe keeping an overall chempion is a good idea?
import numpy as np
from random import choices, randint,randrange,random
from typing import List, Callable, Tuple
from collections import namedtuple


def genetic_finder(problem, termination=None, seed=None, **kwargs):
    
    Population = List[float]
    FitnessFunc = Callable[[float], float]
    PopulateFunc = Callable[[] , Population]
    SelectionFunc = Callable[[Population, FitnessFunc], tuple[float, float]]
    CrossoverFunc = Callable[[float, float], Tuple[float, float]]
    MutationFunc = Callable[[float], float]
    
    def generate_population(size:int) -> Population:
        return [np.random.uniform(problem.bounds[0], problem.bounds[1]) for _ in range(size)]
    
    def fitness(x:float) -> float:
        return problem._evaluate(x)
    
    def selection_pair(population: Population , fitness_func: FitnessFunc) -> Population:
        worst = max(fitness_func(genome) for genome in population)
        return choices(
            population = population,
            weights = [(worst - fitness_func(genome)+ 1e-9) for genome in population],
            k=2
        )
        
    def crossover(a : float , b : float) -> Tuple[float,float]:
        alpha = np.random.rand()
        return alpha*a + (1-alpha)*b, (1-alpha)*a + alpha*b
    
    
    def mutation(a: float, num:int , startIndex: int, endIndex: int  ) ->float:
        for _ in range(num):
            a += np.random.uniform(startIndex, endIndex)
            a = np.clip(a, problem.bounds[0], problem.bounds[1])
        return a 
    
    def run_evolution(
    populate_func: PopulateFunc,
    fitness_func: FitnessFunc,
    new_population_size : int,
    selection_func: SelectionFunc = selection_pair,
    crossover_func: CrossoverFunc = crossover,
    mutation_func: MutationFunc = mutation,
    generation_limit: int = 100,
    
):
        population = populate_func(new_population_size)
        for i in range(generation_limit):
            if i%1000 == 0:
                print(i)
            population = sorted(
                population,
                key = fitness_func,
            )
            next_generation = population[0:2]
            for j in range(int(len(population)/2)-1):
                paretns = selection_func(population, fitness_func)
                offspring_a , offspring_b = crossover_func(paretns[0],paretns[1])
                offspring_a = mutation_func(offspring_a, 1, -20,20)
                offspring_b = mutation_func(offspring_b, 1, -20,20)
                next_generation += [offspring_a, offspring_b]
            population = next_generation
        population = sorted(
                population,
                key = fitness_func,
            )
        return population[0], fitness(population[0])
    
    
    x_coordinate, y_coordinate = run_evolution(generate_population, fitness ,200, selection_pair, crossover , mutation , 1000)
                                               
    
    return x_coordinate,y_coordinate