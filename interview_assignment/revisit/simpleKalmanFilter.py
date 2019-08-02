import numpy as np 
import matplotlib.pyplot as plt 
import random

#Define true value
trueValue = 1000

#number of samples
nSample = 500

#Measurement error
measurementError = np.zeros(nSample)
for i in range(nSample):
	measurementError[i] = random.uniform(-1,1)

#State system
data = np.zeros(nSample)
data[0] = trueValue + measurementError[0]

currentData = data[0]
x = np.zeros(1)
y = np.ones(1)*trueValue
for i in range(nSample):
	#Kalman gain
	Kn = 1.0/(i+1)
	data[i] = trueValue + measurementError[i]

	#Feedback equation
	prediction = currentData + Kn * (data[i] - currentData)

	#Plant - since the system is static, then there is no further calculation
	currentData = prediction


	x = np.append(x,prediction)
	y = np.append(y,trueValue)
	#print(x)
	plt.plot(x[1:] - 1000)
	plt.plot(y[1:] - 1000)
	plt.draw()
	plt.pause(0.01)
	if i == nSample - 1:
		plt.savefig('simpleKalmanFilter02.png')
	plt.clf() 


