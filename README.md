# smart-snake
An AI agent that plays the classic Snake game. The AI agent is trained using genetic algorithm. This project aims to test a different approach of training the agents using genetic algorithm.

## Usage

1. Ensure you have `python3` and `pygame` (library) installed.
2. Clone the repository locally.
3. Move to the root directory and run: `python3 population.py`

## Summary
This project aims to implement an AI based agent which learns to play the classic snake game using Neuro Evolution (Training a Neural Network using Genetic Algorithm). 
However, the major focus in the project is to use and test a variation of genetic algorithm using the concept of "gene pool mixing". Inspired from real life biological systems, in this kind of approach multiple populations are evolved over different environments and occasionally few individuals are migrated from one environment to another. 
Hence, inducing genetic variability. This occasionally produces hybrid individuals possesing the best qualities of multiple populations. Results are faster evolution rates and better individuals (solutions).

## Introduction
Genetic Algorithms (GA) are nothing but optimization algorithms. In this project we used Neuro Evolution to teach the snake to learn to play. What this means is that there is a neural network which takes certain inputs which is the percept for the snake and computes and output decision to move in any of the four directions. 

Now, since we cannot tell at any point of the game what is a good move, this learning task is not supervised. Hence, back-propogation is of no help here. 

Genetic Algorithm comes to rescue, in GA we let a population of snakes to play the gane and then define fitness of the snakes by how well they played (score and lifetime etc). Then we perform natural selection i.e. is choosing snake with higher fitness along with crossover and mutation to give new individuals for the next generation. By this process slowly good genes survive, by genes we mean parameters of the neural network which are the chromosomes in this case. Hence, the population slowly improves its performance dictated by the fitness function.

## Gene pool mixing
Along with the usual process of natural selection in genetic algorithm, in this project we used the concept of niche or environments to induce genetic variability.

Similar to biological evolution where certain part of the species often split up and migrate to new environments and evolve differently. Here environment refers to using different fitness functions for the different populations.

For example, one fitness function could be the score the snake achieves and the other could be the lifetime of the snake.
So by this the two populations evolve to adapt their own enviroments and hence, will have different genes.

However, we associate a probability of gene pool mixing which dictates the chances of mixing of the two populations. By mixing we refer to migration of certain individuals from one population to another. This type of strategy had a significant advantage in terms of faster evolution rates.

##### Schematic representation of algorithm used:
![Figure 1-1](plots/Genetic_Algorithm.png?raw=true)


## Results

##### Using Genetic Algorithm without Gene pool mixing:

![Figure 1-1](plots/gawgm.png?raw=true)

##### Using Genetic Algorithm with Gene pool mixing:

![Figure 2-2](plots/genemix.png?raw=true)

Here red and blue points correspond to individuals from the two different populations.
We can see the rate of improvement is faster for the latter case.

##### Finally, training plot for 1000 generations:

![Figure 3-3](plots/genplot.png?raw=true)
