import numpy as np 
import matplotlib.pyplot as plt 
import random

steps = 300

#real position and velocity

trueVel = 10

realx = np.zeros(steps)
realVel = np.ones(steps)*trueVel
measuredx = np.zeros(steps)
measuredVel = np.ones(steps)*trueVel

deltaT = 5.

realx[0] = 0
realVel[0] = trueVel
measuredx[0] = 0
measuredVel[0] = trueVel
for i in range(steps - 1):
	realxError = random.uniform(-1,1)*5
	realVelError = random.uniform(-1,1)

	#Computing all the real value
	realVel[i+1] = trueVel
	realx[i+1] = (realx[i]) + realVel[i+1] * deltaT
	
	measuredVel[i+1] = trueVel + realVelError
	measuredx[i+1] = (realx[i] + realxError) + realVel[i+1] * deltaT

#predicted position and velocity

predictedx = np.zeros(steps)
predictedVel = np.zeros(steps)

#Initialization

predictedx[0] = measuredx[0]
predictedVel[0] = measuredVel[0]

alpha = 1
beta = 1

x = np.ones(1)
y = np.ones(1)
for j in range(steps - 1):

	#estimate
	predictedx[j + 1] = predictedx[j] + alpha*(measuredx[j] - predictedx[j])
	predictedVel[j + 1] = predictedVel[j] + beta*(measuredVel[j] - predictedVel[j])

	#state dynamics
	predictedx[j + 1] = predictedx[j + 1] + predictedVel[j + 1]*deltaT

	x = np.append(x,predictedx[j] - realx[j]) 
	y = np.append(y,measuredx[j] - realx[j]) 
	plt.plot(x[2:], label='true error') #true error
	plt.plot(y[1:], label ='measurement error') #measurement error
	plt.legend(loc='lower left')
	# plt.plot(predictedVel[1:] - realVel[1:])
	plt.draw()
	plt.pause(0.01)
	if j == steps - 2:
		plt.savefig('velocityKalmanFilter.png')
	plt.clf() 