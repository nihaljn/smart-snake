from nn import Brain
from game import Game
import math
import numpy as np
import pickle
from random import shuffle
from gamesim import GameSim

nn_config = [8, 16]
mutation_rate = 0.01
gene_mixing_rate = 0.005

class Population:
    
    def __init__(self, population_size, env='env1'):
        '''
        Creates a population of snakes
        Attributes:
            population_size: Size of the population
        '''
        self.population_size = population_size
        self.snakes = []
        self.globalBest = None
        self.env = env
        # Generate a random population
        for _ in range(population_size):
            self.snakes.append(Snake())
    
    def natural_selection(self):
        '''
        Peforms one iteration of natural selection to produce stable new generation.
        Uses Roulette Wheel selection and random elitism
        '''
        fitness = []
        # Total length of all snakes (for calculating average)
        totlen = 0
        for i, snake in enumerate(self.snakes):
            snake.train(self.env)
            fitness.append((snake.score, i))
            totlen += snake.len
        fitness.sort(reverse=True)
        best = self.snakes[fitness[0][1]].clone()
        self.best = best
        # Store the global best of all times
        if self.globalBest == None:
            self.globalBest = best
        if self.globalBest.score < best.score:
            self.globalBest = best
        print('Current best score: ', best.score)
        print('Best length: ', best.len)
        print('Average length: ', totlen / self.population_size)
        new_population = [self.globalBest.clone()]
        # Select best 'rand' individuals and keep them for next generation (random elitism)
        rand = np.random.randint(1, self.population_size)
        for i in range(1, rand):
            new_population.append(self.snakes[fitness[i][1]])
        # Shuffling for randomness
        shuffle(fitness)
        # Generate new snakes by crossover and mutation
        for i in range(rand, self.population_size):
            parent1 = self.select_snake(fitness)
            parent2 = self.select_snake(fitness)
            child = parent1.cross_over(parent2)
            child.mutate(mutation_rate)
            new_population.append(child)
        self.snakes = new_population

    def select_snake(self, scores):
        '''
        Selects snake for crossover using Roulette Wheel selection strategy
        '''
        tsum = 0
        for score, i in scores:
            tsum += score
        rand = np.random.randint(1, int(tsum))
        curr_sum = 0.
        for score, i in scores:
            curr_sum += score
            if curr_sum >= rand:
                return self.snakes[i]
        # Unreachable code
        assert(False)

    def save(self, name):
        '''
        Saves the entire population
        '''
        filename = 'saved/' + name + '.pickle'
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f)
    
    def load(self, name, env='env1'):
        '''
        Loads the population from saved file
        '''
        filename = 'saved/' + name + '.pickle'
        with open(filename, 'rb') as f:
            tmp_dict = pickle.load(f)
        self.__dict__.update(tmp_dict)
        self.env = env
    
    def mix(self, pop2):
        '''
        Perform gene pool mixing between the two populations
        '''
        if self.population_size != pop2.population_size:
            raise ValueError('Population size inconsistent for mixing')
        n = self.population_size
        k = np.random.randint(0, n / 2)
        for i in range(k):
            chance = float(np.random.random(1))
            if chance <= gene_mixing_rate:
                pop2.snakes[n-i-1] = self.snakes[i]
                self.snakes[n-i-1] = pop2.snakes[i]

class Snake:

    def __init__(self, brain=None):
        '''
        Creates a new snake
        Attributes:
            brain: for specifying brain (not randomly initialized)
        '''
        # Initialize the brain
        self.brain = brain if brain else Brain(nn_config)

    def play(self, env):
        '''
        Plays the game and return the score achieved
        '''
        fitness = self.fitness1
        if env == 'env2':
            fitness = self.fitness2
        g = Game()
        # Play the game and return the score
        score, time = g.play(self.brain)
        self.len = score
        return fitness(score, time)

    def train(self, env):
        '''
        Plays snake without pygame for superfast training time.
        Note: High CPU usage. Don't provide very large number of generations to train in one go.
        '''
        fitness = self.fitness1
        if env == 'env2':
            fitness = self.fitness2
        g = GameSim()
        # Play the game and return the score
        score, time = g.play(self.brain)
        self.len = score
        return fitness(score, time)
    
    def fitness1(self, score, time):
        if score < 10:
            self.score = math.pow(2, score) * time
        else:
            score -= 9
            self.score = math.pow(2, 10) * time * score * score
        return self.score

    def fitness2(self, score, time):
        if score < 10:
            self.score = math.pow(2, score) * time
        else:
            score -= 9
            self.score = math.pow(2, 10) * time * score * score
        return self.score

    def clone(self):
        '''
        Generates clone of the snake
        '''
        b = self.brain.clone()
        snake = Snake(b)
        snake.score = self.score
        snake.len = self.len
        return snake
    
    def mutate(self, prob):
        '''
        Mutates the chromosome of the snake
        Attributes:
            prob: mutation rate
        '''
        self.brain.mutate(prob)

    def cross_over(self, partner):
        '''
        Performs genetic crossover between 'this' snake and partner snake and returns a child snake.
        '''
        b = self.brain.cross_over(partner.brain)
        snake = Snake(b)
        return snake



if __name__ == '__main__':
    population1 = Population(100)
    population2 = Population(100)
    
    population1.load('poprp1.2')
    population2.load('poprp1.3', 'env2')

    # population1.globalBest.play()
    # exit()
    try:
        for i in range(2):
            print('Generation: ', i+1)
            population1.natural_selection()
            population2.natural_selection()
            population1.mix(population2)
    except BaseException as e:	# BaseException can catch even Keyboard interrupt (Ctrl + C)
        print(e)
        population1.save('tmp')
        population2.save('tmp2')
        exit()
    population1.save('m1')
    population2.save('m2')