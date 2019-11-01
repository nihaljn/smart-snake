import numpy as np
import math

class Brain:

	def __init__(self, nn_config, activation='sigmoid', hidden_layers=None):
		'''
		Initializes the brain of the snake
		4 output nodes: left, right, down, up
		Attributes:
			nn_config: describes the neural network configuration of hidden nodes
				example: nn_config = [10, 3, 4] will create 2 hidden layers with 3 and 4 hidden nodes respectively and input layer has 10 input nodes.
			hidden_layers: optional. used to specify determined params instead of random initializations
			activation: Activation function used
				available: 'sigmoid', 'relu'
		'''
		self.nn_config = nn_config
		if hidden_layers:
			self.hidden_layers = hidden_layers
			return
		hidden_layers = []
		l = len(nn_config)
		for i in range(1, l):
			layer = Layer(nn_config[i-1], nn_config[i], activation=activation)
			hidden_layers.append(layer)
		# 4 output nodes
		layer = Layer(nn_config[l-1], 4, True)
		hidden_layers.append(layer)
		self.hidden_layers = hidden_layers
	
	def move(self, percept):
		'''
		Function to provide output move given the input percept of the snake using feed-forward on the neural net.
		Attributes:
			percept: row vector of percept. dim: 1 * nx
		'''
		percept = np.array(percept).reshape(-1)
		l = percept.shape[0]
		if l != self.nn_config[0]:
			raise ValueError('Invalid percept length')
		# 1 for bias term
		percept = np.append(percept, 1)
		percept = percept.reshape(1, -1)
		feed = percept
		# Feed Forward
		for layer in self.hidden_layers:
			feed = layer.product(feed)
		feed = feed.reshape(-1)
		mx = np.max(feed)
		# Return which move to take relative to the snake
		moves = np.zeros(4)
		for i, f in enumerate(feed):
			if f == mx:
				moves[i] = 1
				break
		return moves
	
	def clone(self):
		'''
		Returns a clone of the brain.
		'''
		new_layers = []
		for layer in self.hidden_layers:
			new_layer = layer.clone()
			new_layers.append(new_layer)
		b = Brain(self.nn_config, hidden_layers=new_layers)
		return b

	def mutate(self, prob):
		'''
		Perfrom mutation on all layers
		Attributes:
			prob: mutation rate
		'''
		for layer in self.hidden_layers:
			layer.mutate(prob)

	def cross_over(self, partner):
		'''
		Performs genetic crossover operation on this chromosome with partner chromosome.
		Attributes:
			partner: Brain of the partner snake
		Note: nn_config of partner must be same as 'this' brain
		'''
		if self.nn_config != partner.nn_config:
			raise ValueError('Brains incompatible for crossover. nn_config must be same')
		
		new_hidden_layers = []
		for i, layer in enumerate(self.hidden_layers):
			new_layer = layer.cross_over(partner.hidden_layers[i])
			new_hidden_layers.append(new_layer)
		# Child brain after crossover
		b = Brain(self.nn_config, hidden_layers=new_hidden_layers)
		return b

class Layer:

	def __init__(self, nx, ny, is_output=False, activation='sigmoid'):
		'''
		Initializes the matrix for the layer
		Attributes:
			nx: number of rows
			ny: number of columns
			is_output: determines output layer or not
		'''
		# plus 1 for bias
		nx += 1
		self.nx = nx
		self.ny = ny
		# Random values between [-1, 1]
		mat = np.random.random(size=(nx, ny)) * 2 - 1
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
		vec = vec.reshape(1, -1)
		output = np.dot(vec, self.mat)
		if self.is_output:
			output = self.softmax(output)
		else:
			output = self.activation(output)
			output = output.reshape(-1)
			# 1 for bias term
			output = np.append(output, 1)
		return output

	def clone(self):
		'''
		Returns a clone of the current layer
		'''
		layer = Layer(self.nx-1, self.ny, self.is_output, self.activation)
		for i in range(self.nx):
			for j in range(self.ny):
				layer.mat[i][j] = self.mat[i][j]
		return layer

	def mutate(self, prob):
		'''
		Perform mutation on weight matrix
		'''
		for i in range(self.nx):
			for j in range(self.ny):
				chance = float(np.random.random(1))
				if chance <= prob:
					change = float(np.random.random(1) * 2 - 1)
					self.mat[i][j] += change
				# Bounding weights in [-1, 1]
				self.mat[i][j] = min(1, self.mat[i][j])
				self.mat[i][j] = max(-1, self.mat[i][j])

	def cross_over(self, layer):
		'''
		Performs crossover on the 'this' layer with layer
		Attributes:
			layer: partner layer
		'''
		new_layer = self.clone()
		x = np.random.randint(0, self.nx)
		y = np.random.randint(0, self.ny)
		for i in range(self.nx):
			for j in range(self.ny):
				if i * self.ny + j > x * self.ny + y:
					new_layer.mat[i][j] = layer.mat[i][j]
		return new_layer

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