# Vectorised and normalised genetic algorithm

## Setup

This project uses [uv](https://docs.astral.sh/uv/). With uv installed:

```bash
uv sync          # create the virtual environment and install dependencies
uv run runner.py # run the benchmark and generate the error plots in figures/
```

To define or change a problem you make a new Problem class (similar to the pymoo problem class). It needs three methods:

```python
def __init__(self):      # constructor that defines the bounds of the domain
def _evaluate(self, x):  # returns the y value of the function for a given x
def solution(self):      # returns the x and y of the global minimum as a tuple, used for comparison
```

## Overview

A genetic algorithm is a program that copies biological evolution to solve hard problems. In our case it finds the absolute minimum of a function inside a given range. The implementation is made to work together with the pymoo library, following the same idea of starting from the definition of a problem. The function gives back both the x and the y coordinate of the minimum point, and it can be extended to work on other problems too.

Inside our repo there are 4 main files.

### runner.py

This is the file you actually run.

- At the top we set up NSGA-III, one of the most common genetic algorithm from the famous pymoo library.
- After that a set of problems that are commonly used as benchmarks are defined, for example Rastrigin, Schwefel, Griewank and Ackley, plus a couple of my own harder functions. These are the kind of functions that are often used to test this type of algorithm.
- Then come the tests. For each problem we run through a set of different populations [5, 10, 20, 50, 100, 150, 200], and for each of our 3 genetic function (the arithmetic one, the bit one and NSGA-III, the last two are explained later) we draw, on a logarithmic scale graph, the difference between the x we get and the x we expect. I use the x error because for these functions the x coordinate decides the y coordinate (it is one to one, or at worst many to one). Every setup is run a few times (5) and the error is averaged, so one lucky or unlucky run does not change everything. The nested loop makes sure that each problem has its own graph with the 3 genetic function on it.

### MinimaFunction.py

This file uses the numerical definition of a derivative, the rate of change / slope over an infinitesimally small interval, to compute an approximation of the first and second derivative at a certain point. The functions for this are:

- `d_fun(x, func)`: takes an x coordinate and the function and computes the first derivative at that coordinate using the central difference method, which gives a more accurate approximation.
- `d2_fun(x, func)`: same thing for the second derivative, again with the central difference method.
- `minimum_finder(starting_guess, func, depth=0)`: a function that uses Newton's method to find the next value, by subtracting from the current value the ratio between the derivative at the current value and the second derivative at the current value (if you are not familiar with Newton's method I would suggest watching the blackpenredpen video on it, it turned out to be very useful). Note that the function returns the next value when the change between the current value and the next value is less than 10 decimal places. Note also that on its own the algorithm might get stuck in local minima or inflection points, because it might think it is already at a minimum, and an inflection point might cause a division by 0 (there is a check that stops this). The function has a depth, so the recursive algorithm can only call itself a few times (it stops once the depth goes past 2) before stopping.

### genetic.py (arithmetic version)

(image made by me on Freeform)

<img width="1000" height="997" alt="image" src="https://github.com/user-attachments/assets/eaabd279-e693-4bfb-a9c4-6e569ef599fa" />

- `def genetic_findera(problem, sample, termination=None, seed=None, **kwargs)`: the function returns the x coordinate and the y coordinate of the optimal point, which are found by calling run_evolution. run_evolution is another method inside the function. The function takes the parameters problem and sample, where problem defines the bounds and the evaluation function (see the problem class above) and sample is the size of the population that we are going to use.

- run_evolution takes 7 parameters: populate_func, fitness_func, new_population_size, selection_func, crossover_func, mutation_func, generation_limit. The method starts by defining a step, by dividing the width (difference between the end of the domain and the start of the domain) by 20. This is used to move across the function in a less random way. Then by calling populate_func and passing in the size given by sample we create a new population (see the other methods below). We then start a loop that goes from 0 up until the generation limit. We start each loop by sorting the population using the fitness function. We then keep for the next population our two best results from the current population (the ones with the lowest value). Then, starting from 0 up until (n/2 - 1), because one pair was already kept, we use selection_func to select a pair of parents. We then use the crossover function on them to make two offspring, and finally we apply the mutation function to each child before adding it to the next generation. When the population is back to its original size we restart the loop, until we hit generation_limit. (if you are wondering about the name of this variable, it is because in other uses of the genetic algorithm this is actually a limit, but the algorithm could stop before this). We then sort the population one last time and take the first element, which is the x of the lowest y we got. We then make the last decimal places more accurate by passing our x into minimum_finder (which on its own would get stuck in local minima or maxima or inflection points) to refine the decimals. We then return its x coordinate and its matching y coordinate.

In this version the mutation handles variation by shifting the current float by a random value, inside a range you can set (here from -step to step), and the crossover is a blend of the two parents.

### geneticbit.py (bit / normalised version)

This is the second version and the main new idea of this repo. It works on a normalised list of x coordinates and then uses bit operations to change the decimal part in a more controlled way. The structure of genetic_finderb is the same as the arithmetic one (populate, fitness, selection, crossover, mutation, run_evolution), so here I will only talk about what is different.

- `generate_population(size)`: makes random values inside the bounds and then normalises them to the range [0, 1] with the normaliser function, so the whole population is kept normalised.
- `fitness(x)`: evaluates the problem on the denormalised value, so even if the population is normalised the score is still the real y value.
- `selection_pair`: same idea as before, it gives more weight to the better (lower) results, just working on the normalised population.
- `crossover(a, b)`: a blend crossover. It denormalises the two parents, mixes them with a random alpha, and normalises the two children back, so the list stays normalised.
- `mutation(a, current, max)`: this is where the bit operations happen. It takes a normalised value, keeps the decimal part to 15 places and turns it into an array of 50 bits (most significant bit first). For every bit it decides if it flips it or not, with a probability that depends on the position of the bit and on how far we are in the evolution. At the start the probability is more spread out, so even the more significant bits can flip and we get big jumps in the value, which helps exploration. As the generations go on (the current and max arguments control this with the exponent k) the flips move to the less significant bits, so the changes get smaller and the algorithm fine tunes. After flipping, the bits are turned back into a value, divided by 10^15 and clipped to [0, 1].
- `run_evolution`: same loop as the arithmetic version (keep the 2 best, make the pairs, crossover, mutate, repeat for generation_limit generations), but it is vectorised with numpy, and it passes the generation number into the mutation so the mutation knows how far we are. At the end it refines the best point with minimum_finder, denormalises it and returns the real x and y.
- helper functions: normaliser and denormaliser do the min-max scaling to [0, 1] and back, while to_n_array and to_n_value turn an integer into the 50 bit array and back.

So there are two versions. The arithmetic one handles variation by shifting the current float by a random value, inside a range the user can set. The second one first creates a normalised list of x coordinates and then uses bit operations on the decimal part, allowing big shifts in the value at the start of the loop to push exploration, while making the change in the "less" significant bits smaller as the program goes on, which lets it fine tune. Also note that both of these algorithms use the Newton-Raphson method too: on its own this method is very inefficient and gets stuck in local minima or maxima or inflection points for the test cases we are using, but here it is only used for fine tuning at the end, to slightly improve the accuracy of the lower decimal places that the genetic algorithm can struggle to find.

I also have to mention: this is the updated version of my other genetic algorithm. A lot of the errors were fixed, but here we also vectorised and normalised the project. Vectorisation through the numpy library makes the program run faster (which is important since it has to run many tests on different populations), and the normalisation stops the error we had in the previous version, where the program would end up out of bounds and get reset to the limit, which made it very inefficient. Note that this is compared to pymoo NSGA-III, which is built for multi objective problems, so using it on a one dimensional, single objective context like this is not what it was made for, so it is not a completely fair competition between the two.

## Tests

Here are some of the tests. For each problem I show the function and its domain. The result graph is the error plot from figures/. Each plot has the name of the problem as its title, so it is easy to match a graph to its function (I put them in order, but if one ends up under the wrong problem just move it by checking the title on the plot).

### Problem 1 (Rastrigin)

function: `f(x) = 10 + x^2 - 10*cos(2*pi*x)`   domain: `[-1, 6]`

graph of function: (to be inserted)

graph of result:

<img width="1421" height="921" alt="Problem1 result" src="https://github.com/user-attachments/assets/d106a06f-1318-4ad0-9228-2e7ce1e912bd" />
<img width="694" height="521" alt="image" src="https://github.com/user-attachments/assets/963d3cfa-83b4-48ff-a1e8-2788455cd003" />

### Problem 2

function: `f(x) = x^2 * sin(1/(x^2 + 0.001)) + 0.3*x^2 + cos(x^2/4)`   domain: `[0, 2]`

graph of function: (to be inserted)

graph of result:

<img width="1421" height="923" alt="Problem6 result" src="https://github.com/user-attachments/assets/461549cb-5f87-4a93-afd8-8f350f2bc586" />
<img width="694" height="522" alt="image" src="https://github.com/user-attachments/assets/0061c172-3612-462e-b5f2-e242f1ba65f0" />


### Problem 3

function: `f(x) = sin(x^2) + 0.05*x^2 - cos(3*x)`   domain: `[0, 10]`

graph of function: (to be inserted)

graph of result:

<img width="1420" height="923" alt="Problem3 result" src="https://github.com/user-attachments/assets/03705e1b-43c1-4427-9a25-97c2a955c6f6" />
<img width="696" height="521" alt="image" src="https://github.com/user-attachments/assets/d4263f41-f9cf-4bbe-808c-c92ac46f1340" />

### Problem 4 (Schwefel)

function: `f(x) = 418.9829 - x*sin(sqrt(|x|))`   domain: `[-500, 500]`

graph of function: (to be inserted)

graph of result:

<img width="1422" height="922" alt="Problem4 result" src="https://github.com/user-attachments/assets/f16b31af-f1df-44bb-91a4-bd6a4a87b005" />
<img width="693" height="523" alt="image" src="https://github.com/user-attachments/assets/2d914ed4-46ed-4351-a3da-57447f06a50f" />


### Problem 5 (Griewank)

function: `f(x) = 1 + x^2/4000 - cos(x)`   domain: `[-1, 12]`

graph of function: (to be inserted)

graph of result:

<img width="1418" height="920" alt="Problem5 result" src="https://github.com/user-attachments/assets/d4806b86-cbb6-4e01-849e-280dd67e1df0" />
<img width="695" height="521" alt="image" src="https://github.com/user-attachments/assets/91fef290-d5a9-457d-bc3b-58a932c2ab27" />


### Problem 6 (Ackley)

function: `f(x) = -20*exp(-0.2*sqrt(x^2)) - exp(cos(2*pi*x)) + 20 + e`   domain: `[-33, 33]`

graph of function: (to be inserted)

graph of result:

<img width="1423" height="924" alt="Problem2 result" src="https://github.com/user-attachments/assets/98c5e1d4-bd01-4d14-8f26-43ca85d8028b" />
<img width="694" height="523" alt="image" src="https://github.com/user-attachments/assets/6fb31667-c4dc-438e-8b9e-f6c04414e671" />

