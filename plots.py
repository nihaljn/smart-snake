import matplotlib.pyplot as plt
import numpy as np


x = np.arange(1, 201)
y = []
with open('progress.txt') as f:
    for i in range(200):
        f.readline()
        f.readline()
        line = f.readline()
        line = line.split(' ')
        snake_len = int(line[3][:-1])
        y.append(snake_len)

plt.scatter(x, y)
plt.title('Genetic Algorithm without Gene mixing')
plt.xlabel('Number of generations')
plt.ylabel('Length of best snake')
plt.legend()
plt.show()


'''
x = np.arange(1, 101)
y1 = []
y2 = []
with open('genemix.txt') as f:
    for i in range(100):
        f.readline()
        f.readline()
        line = f.readline()
        line = line.split(' ')
        snake_len = int(line[3][:-1])
        y1.append(snake_len)
        f.readline()
        f.readline()
        line = f.readline()
        line = line.split(' ')
        snake_len = int(line[3][:-1])
        y2.append(snake_len)
        f.readline()

plt.scatter(x, y1, color='blue', label='Env1')
plt.scatter(x, y2, color='red', label='Env2')
plt.xlabel('Number of generations')
plt.ylabel('Length of best snake')
plt.legend()
plt.show()
'''