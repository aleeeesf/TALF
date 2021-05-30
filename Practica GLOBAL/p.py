import numpy as np

a = np.arange(3)
a[0] = 5
a[1] = 5
a[2] = 5
findError = np.where(a == 5)[0]
print(findError[0])
#print(findError)