import matplotlib.pyplot as plt
import numpy as np

x = np.arange(1, 1001)
y = []
with open('plotdata.txt') as f:
    for i in range(1000):
        f.readline()
        f.readline()
        line = f.readline()
        line = line.split(' ')
        snake_len = int(line[3][:-1])
        y.append(snake_len)

plt.scatter(x, y)
plt.xlabel('Number of generations')
plt.ylabel('Length of best snake')
plt.show()