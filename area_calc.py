
def f(x):
    return 3*x +1

import matplotlib.pyplot as plt
import numpy as np
import random

plt.xlim(0, 0.75)
plt.ylim(1, 3)

for i in range(100000):
   x = random.uniform(0, 0.75)
   y = random.uniform(0, 3)
   if y < f(x):
       plt.scatter(x, y, color="green")
   else:
       plt.scatter(x, y, color="red")

plt.show()