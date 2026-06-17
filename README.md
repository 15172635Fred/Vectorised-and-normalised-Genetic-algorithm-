
## Setup

This project uses [uv](https://docs.astral.sh/uv/). With uv installed:

```bash
uv sync          # create the virtual environment and install dependencies
uv run runner.py # run the benchmark and generate error plots in figures/
```
to define or change a new problem define a new Problem class (similar to pymmo prolem class)

def __init__(self):    ---> constructor that defines bounds, function retrunts the y value of the fucniton at a sepcifci givne x value
def _evaluate(self, x) ---> function that returns the y coordinate for a given x coordinate 
def solution(self):    ---> function that retunrs the x and y solution of the global minima as a touple for comparison.


## Overview

A genetic algorithm is a computer program that mimics biological evolution to solve complex problems. In this case, it finds the absolute minimum of a function within a given range. The implementation is meant to integrate seamlessly with the pymoo library, following the same idea of starting from the definition of a problem. The function returns both the x and y coordinate of the minimum point, and it can be extended to work on other problems.


                                                        Within our repo we can see 4 main different classes


1) The third signifcant file is runner.py.
   
-At the top of the program we set up nsga III, one of the most ocmmon genetic algorithm from the famous pymoo library

- This si followed by a set of different problems which have been commonly used for benchamrks are defined, this inclue for example Rastrigin, Schwefel, Griewank and Ackley which are ofte used to test this type of function

-this is followed by the tests themeslves which for each problem run torugh a set of different popualtions [5,10,20,50,100,150,200] and using a logarithmic scale graph for each one of our 3 different genetic function (NSGA III and the other 2 will be disucssed later) the difference ebtween the resutling value for x and the expected vlaue for x (as this is a funcitont he x coordinate is determinsitic of the y-cooridnate as it is one:one or at worst many:one). The ensted loop will ensure tht at eahc problem has its own graph with the 3 set of genetic fucntion implemtned.


2) The second sginficant file is the MinimaFunction.py

- The function uses the nuemrical defintion of a derivative- the rate of change/slope over an infinitesimally small interval to compute an approximation of the derviative and second derivative at a certain point. The functions used to this are defined as
      -->d_fun(x, func)  : accepts an x-coordinate and the function and computes the first derivative at that coordinate by using the central difference method which gives a morte accurate
                           approximation
      -->d2_fun(x, func) : accepts an x-coordinate and the function and computes the second derivative at that coordinate by using the central difference method which gives a morte accurate
                           approximation.
  
-cminimum_finder(starting_guess, func, depth=0) :function whcih uses newton method of finding the next value by  subtracting fromt he current valeu the ration of the derivative at the current
                                                valeu and the secodn derivative of the current value (if you are not fmailiar with newton's method I woudl suggest watching balck pen-red pen video on 
                                                it whcih turned otu to be very usefull). Note that the fucntion will return the next value when  the chaneg between the current value adn the next valeu                                                 is less signficant then 10 decimal palces. Note also that the algorhtm mgiht get stuck in lcoal miniam or infleciton poitns as it might think tis alredy                                                 at a local minima and and mgith cause divion by 0 respectevly. The function has a dpeth whcih ensures that the recursive algorithm can call itself a                                                     maximum of 5 time before stopping.

3)
<img width="1000" height="997" alt="image" src="https://github.com/user-attachments/assets/eaabd279-e693-4bfb-a9c4-6e569ef599fa" /> (citetion for immage --> me on freeform)

- def genetic_findera(problem, sample, termination=None, seed=None, **kwargs): the function returns the x_coordinate sand the y_coordiantes of the otpimal points hwich are ofudn by calling run_evolution. The 
  Run evolution method is another methof within the function. The fucntion has aprametters problem and smapel were problem defines the boduenries and evalaution fucntion (see problem 1) and sampel defines the size of the popualtion that we are going to use.

- run evolution accepts 7 paramters: populate_func, fitness_func, new_population_size, selection_func, crossover_func, mutation_func, generation_limit. The mehtod starts by defining a stepp by deving the width (difference ebtween end point of domain and start point of domain) by 20. This will be sued in rder to mvoe across the funciton in a less random menner. The FUnction processed by calling populate_func and passing in the given size defined by smapel we create a new population (refer to other emhtods below). We then start a loop that goes from 0 up untilt he generation limit. We start each loop by soritng the funciton using the fitness fucniton. We then save for the enxt popualtion our two ebst reustls fromt eh curren population (the oes withthe lwoest vlaue). Then startin from 0 up iuntil to 1 less the lenght of the orignal population (as 1 pair was alredy preserved in the orignal popultion)  we user the selection_func to select a pair of parents. We then use the crossover function between them to generate two offrspring usign the crossover_func. Finally we apply to each of the children the mutation_func befor adding it to the next generaion. When the popualtion has returned to its orignal size we restart the loop until we hit generation_limit. Once we have repated this process generation_limit tiems (if youa re wodnering the why the naiming of this vairbel its becuase its becuase in otehr applcaition of the genetic algorhtm thsi is actually alimti but the algorthm could stop before this). We then sort the popualtion on last time and take the first elemnt, which is the x-cooridnate of the lowest y-variabel we have obtained. We then icnrease the accuracy of the last decimal palces by passing our x value in the minimum_finder (which as a standalone function woudl get stuck in local minimua or maxima or ifnelciton point) to refine the decimla places. We then return its x coordinte and then its assoicated y-coordinate 









There are two versions. The arithmetic version handles variation by shifting the current float by a random value, within a range the user can set. The second version first creats a normisled lsit of x coordinates and then uses bit oeprations to modify the decimal part in amroe controlled menner, allowign big shifts in valeus at the start of the loop promoting expelation whsil increaisng the change in "less" signficant btis as the progrma contineus allows for fine tuning. Also note that both of this algorithm have been equipped by newotn Newton-Raphson method as whislt th emehtod is evry inefficent for th etest cases alone that we are experiemnting with a it mgith get stuck in alcoal minima or maxima or inflection point, here the mehtod is used for fine tuining at the end to slgihtlu ocmrease accuracy of lower decimal palces hcih the genetic algoirthm might struggle to find.


--> I got to mention : ##This represent the udpated version of my other genetic algorhtm. Singificant chnaegs were made on errors however here we have vecotrised and normiseld the  project. Vecotrisaiton trough the numpy library allwos for the progrma to run faster (which is crucial cosndieirng it has to ru many tests on different populaitosn) and the normalisation prevents the error that we had in the previous ersion were the prigrma woudl end up out of boudns and owuld be resetted at the limit, whcih lead ot great inefficency. Note that this is comapred to pymoo NSGA-III whcih is however ment ot be a mono dimensional and a mono objective algorithm, and hsu appling to a context whcih is not the one it was ment for leads to it not beeigng a compeltely fair competition between the two 





  ###### here follow some test ######


function: .... domain: ...
grpah of function --> put to be inserted here if I did not put it yet (look at my other redme in my other rpeo if possible)
grpah of reuslt --> (if I did not put a file here put to be inserted)
