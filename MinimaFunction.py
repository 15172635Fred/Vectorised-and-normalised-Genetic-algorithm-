#the idea is that we give the two fucniton the same renge, where if f(x) gets stuc

import numpy as np
import time
def d_fun(x, func):
    h = 1e-5
    return (func(x+h)-func(x-h))/(2*h)

def d2_fun(x, func):
    h = 1e-5
    return (d_fun(x+h,func)-d_fun(x-h,func))/(2*h)


def minimum_finder(starting_guess, func, depth=0):
    if depth > 2:
        return starting_guess
    derivative_at_current_guess = d_fun(starting_guess, func)
    second_derivative_at_current_guess =  d2_fun(starting_guess, func)

    if second_derivative_at_current_guess<(1e-10) and second_derivative_at_current_guess>-(1e-10):
       return starting_guess

    else:
        next_x = starting_guess- (derivative_at_current_guess/second_derivative_at_current_guess)
        if np.round(starting_guess,10) == np.round(next_x,10) :
           return next_x

        else:
            return minimum_finder(next_x, func, depth+1)
