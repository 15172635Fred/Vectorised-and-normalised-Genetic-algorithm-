# Genetic Algorithm Function Minimizer

## Setup

This project uses [uv](https://docs.astral.sh/uv/). With uv installed:

```bash
uv sync          # create the virtual environment and install dependencies
uv run runner.py # run the benchmark and generate error plots in figures/
```

## Overview

A genetic algorithm is a computer program that mimics biological evolution to solve complex problems. In this case, it finds the absolute minimum of a function within a given range. The implementation is meant to integrate seamlessly with the pymoo library, following the same idea of starting from the definition of a problem. The function returns both the x and y coordinate of the minimum point, and it can be extended to work on other problems.

There are two versions. The arithmetic version handles variation by shifting the current float by a random value, within a range the user can set. The second version converts the value into its bit representation and then flips a random bit, where the least significant bit is more likely to be changed.

The repository includes an application built for functions, as well as a general version that can be adapted with small changes to work on other problems. Genetic algorithms are often used for things like finding the best path in a video game, even on levels that are considered impossible.


The arithmetic version works directly on the floating-point value, nudging it up or down by a random amount within a range you set, so its changes are smooth and continuous. The bit version instead encodes the value into binary and flips a single random bit, which can cause either a tiny or a large jump depending on which bit changes. Since flipping a high-order bit shifts the value a lot while a low-order bit barely moves it, the bit method is biased toward the least significant bits to keep most mutations small. In short, the arithmetic method explores in smooth steps, while the bit method mostly takes small steps but can occasionally make big leaps across the search space.



Below are some graphs showing how the algorithm approximated the absolute minimum within a given domain.

**1)**

$$10 + x^2 - 10\cos(2\pi x), \quad -6 \le x \le 6$$

<img width="1421" height="921" alt="image" src="https://github.com/user-attachments/assets/d106a06f-1318-4ad0-9228-2e7ce1e912bd" />
<img width="769" height="578" alt="image" src="https://github.com/user-attachments/assets/572019df-ec32-40dc-a273-12fb98f0ebdd" />

**2)**

$$-20e^{-0.2}\sqrt{x^2} - e^{\cos(2\pi x)} + 20 + e, \quad -32.768 \le x \le 32.768$$

<img width="1423" height="924" alt="image" src="https://github.com/user-attachments/assets/98c5e1d4-bd01-4d14-8f26-43ca85d8028b" />
<img width="769" height="577" alt="image" src="https://github.com/user-attachments/assets/ad45073d-b9a7-4f82-ad6e-3823138b3c54" />

**3)**

$$1 + \frac{x^2}{4000} - \cos(x), \quad -300 \le x \le 300$$

<img width="1420" height="923" alt="image" src="https://github.com/user-attachments/assets/03705e1b-43c1-4427-9a25-97c2a955c6f6" />
<img width="770" height="578" alt="image" src="https://github.com/user-attachments/assets/338c7ea8-0685-42c6-9820-a431b996aadf" />

**4)**

$$418.9829 - x\sin\left(\sqrt{|x|}\right), \quad -500 \le x \le 500$$

<img width="1422" height="922" alt="image" src="https://github.com/user-attachments/assets/f16b31af-f1df-44bb-91a4-bd6a4a87b005" />
<img width="770" height="578" alt="image" src="https://github.com/user-attachments/assets/3c0467d5-bc36-4564-816e-2253baf7f8f5" />

**5)**

$$\sin(x^2) + 0.05x^2 - \cos(3x), \quad -10 \le x \le 10$$

<img width="1418" height="920" alt="image" src="https://github.com/user-attachments/assets/d4806b86-cbb6-4e01-849e-280dd67e1df0" />
<img width="768" height="577" alt="image" src="https://github.com/user-attachments/assets/ecfe1c0c-447f-4259-a8de-9a8adc6e15aa" />

**6)**

$$x^2\sin\left(\frac{1}{x^2 + 0.001}\right) + 0.3x^2 + \cos\left(\frac{x^2}{4}\right), \quad -3 \le x \le 3$$

<img width="1421" height="923" alt="image" src="https://github.com/user-attachments/assets/461549cb-5f87-4a93-afd8-8f350f2bc586" />
<img width="769" height="577" alt="image" src="https://github.com/user-attachments/assets/51750d1f-2a81-49f8-a17f-d33ca3df1d03" />

