from nn import Brain
from game import Game
import math

nn_config = [24, 16, 8]
mutation_rate = 0.1

class Population:

	def __init__(self, population_size):
		'''
		Creates a population of snakes
		Attributes:
			population_size: Size of the population
		'''
		self.population_size = population_size
		self.snakes = []
		# Generate a random population
		for _ in range(population_size):
			self.snakes.append(Snake())
	
	def natural_selection(self):
		'''
		Peforms one iteration of natural selection
		'''
		fitness = []
		for i, snake in enumerate(self.snakes):
			snake.play()
			fitness.append((snake.score, i))
		fitness.sort(reverse=True)
		best = self.snakes[fitness[0][1]].clone()
		self.best = best
		print(best.score)
		new_population = []
		for i in range(self.population_size // 2):
			new_population.append(self.snakes[fitness[i][1]])
		for i in range(self.population_size // 2):
			child = best.cross_over(self.snakes[fitness[i][1]])
			child.mutate(mutation_rate)
			new_population.append(child)
		self.snakes = new_population


class Snake:

	def __init__(self, brain=None):
		'''
		Creates a new snake
		Attributes:
			brain: for specifying brain (not randomly initialized)
		'''
		# Initialize the brain
		self.brain = brain if brain else Brain(nn_config)

	def play(self):
		'''
		Plays the game and return the score achieved
		'''
		g = Game()
		# Play the game and return the score
		score, time = g.play(self.brain)
		self.score = score * score + math.sqrt(time)
		return score

	def clone(self):
		'''
		Generates clone of the snake
		'''
		b = self.brain.clone()
		snake = Snake(b)
		snake.score = self.score
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
	population = Population(50)
	for i in range(10):
		print('Generation: ', i+1)
		population.natural_selection()
