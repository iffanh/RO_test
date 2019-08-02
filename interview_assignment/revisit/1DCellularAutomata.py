import numpy as np 
import matplotlib.pyplot as plt 

length = 100
timeStep = 100

matrix = np.zeros([timeStep,length])

#rules

def ruleCA(left,center,right):
	if left == 0 and center == 0 and right == 0: center = 0
	elif left == 0 and center == 0 and right == 1: center = 1
	elif left == 0 and center == 1 and right == 0: center = 0
	elif left == 0 and center == 1 and right == 1: center = 0		
	elif left == 1 and center == 0 and right == 0: center = 1
	elif left == 1 and center == 0 and right == 1: center = 0
	elif left == 1 and center == 1 and right == 0: center = 0
	elif left == 1 and center == 1 and right == 1: center = 0

	return center

#initialize something here
#f.ex. matrix[1,0] = 1

matrix[0,:] = np.random.randint(2, size=length)

# # matrix[0,5] = 1
# matrix[0,50] = 1
# # matrix[0,95] = 1

plt.imshow(matrix)
plt.pause(0.05)
plt.close()

for t in range(1,timeStep):
	for i in range(length-1):
		matrix[t,i] = ruleCA(matrix[t-1,i-1], matrix[t-1,i], matrix[t-1,i+1])

	plt.imshow(matrix)
	plt.draw()
	plt.pause(0.01)

	if t == timeStep-1:
		plt.savefig('1DCellularAutomata.png')
	plt.clf()
