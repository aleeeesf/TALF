import numpy as np

a = np.arange(2)
a[0] = 5
a[1] = 5
findError = np.where(a == 5)[0]
print(findError)
#print(findError)