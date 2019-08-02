#This is to test the central limit theorem

import random
import numpy as np
import matplotlib.pyplot as plt 

#define a distribution
#uniform distribution of with set {0,1,2,3,4,5,6}

nSample = 800
nObservation = 20

ave = np.zeros(nSample)


for j in range(nSample):
	x = np.zeros(nObservation)
	
	for i in range(nObservation):
		x[i] = random.randint(0,7)

	ave[j] = sum(x)/len(x) 

#print(ave)

plt.hist(ave, bins=20)
plt.show()

print('The central average is', np.average(ave))
print('The standard deviation is', np.std(ave))