import numpy as np
import math

class Brain:

	def __init__(self, nn_config, activation='sigmoid'):
		'''
		Initializes the brain of the snake
		3 output nodes: left, straight, right
		Attributes:
			nn_config: describes the neural network configuration of hidden nodes
				example: nn_config = [10, 3, 4] will create 2 hidden layers with 3 and 4 hidden nodes respectively and input layer has 10 input nodes.
			activation: Activation function used
				available: 'sigmoid', 'relu'
		'''
		hidden_layers = []
		l = len(nn_config)
		for i in range(1, l):
			layer = Layer(nn_config[i-1], nn_config[i], activation=activation)
			hidden_layers.append(layer)
		# 3 output nodes
		layer = Layer(nn_config[l-1], 3, True)
		hidden_layers.append(layer)
		self.hidden_layers = hidden_layers
	
	def move(self, percept):
		'''
		Function to provide output move given the input percept of the snake using feed-forward on the neural net.
		Attributes:
			percept: row vector of percept. dim: 1 * nx
		'''
		percept = np.array(percept).reshape(-1)
		# 1 for bias term
		percept = np.append(percept, 1)
		percept = percept.reshape(-1, 1).T
		feed = percept
		# Feed Forward
		for layer in self.hidden_layers:
			feed = layer.product(feed)
		feed = feed.reshape(-1)
		mx = np.max(feed)
		# Return which move to take relative to the snake
		moves = np.zeros(3)
		for i, f in enumerate(feed):
			if f == mx:
				moves[i] = 1
				break
		return moves
	
	def mutate(self, prob):
		'''
		Perfrom mutation on all layers
		Attributes:
			prob: mutation rate
		'''
		for layer in self.hidden_layers:
			layer.mutate(prob)


class Layer:

	def __init__(self, nx, ny, is_output=False, activation='sigmoid'):
		'''
		Initializes the matrix for the layer
		Attributes:
			nx: number of rows
			ny: number of columns
			is_output: determines output layer or not
		'''
		self.nx = nx
		self.ny = ny
		# plus 1 for bias
		mat = np.random.normal(size=(nx+1, ny))
		self.mat = mat
		self.is_output = is_output
		self.activation = self.sigmoid
		if activation == 'relu':
			self.activation = self.relu

	def product(self, vec):
		'''
		Matrix multiplication of input vector and current layer matrix
		Attributes:
			vec: input vector
		'''
		vec = vec.reshape(-1, 1).T
		output = np.dot(vec, self.mat)
		if self.is_output:
			output = self.softmax(output)
		else:
			output = self.activation(output)
			output = output.reshape(-1)
			# 1 for bias term
			output = np.append(output, 1)
		return output

	def mutate(self, prob):
		'''
		Perform mutation on weight matrix
		'''
		for i in range(self.nx+1):
			for j in range(self.ny):
				chance = float(np.random.random(1))
				if chance <= prob:
					self.mat[i][j] += float(np.random.randn(1) / 5)

	def sigmoid(self, x):
		'''
		Perform sigmoid activation
		'''
		return 1 / (1 + np.exp(-x))

	def softmax(self, x):
		'''
		Compute softmax
		'''
		e_x = np.exp(x - np.max(x))
		return e_x / np.sum(e_x)
	
	def relu(self, x):
		'''
		Perfom relu activation
		'''
		return np.maximum(x, 0, x)	

if __name__ == "__main__":
	b = Brain([2, 4])
	b.mutate(0.2)
	print(b.move([1, 1]))