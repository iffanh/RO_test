import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.dates as mdates

from answers_task2 import calculate_standard_deviation

#from answers_task2 import  
timeSeriesFileName = '../data/brugge_time_series.npy'

'''
TASK 3: 
   a) Write a function that given a list of wells, automatically checks if the ensemble of simulated data is capturing the measured data for at 
           least 95 % of the timesteps for all available data measurement for this well
'''

'''
   b) Write a function that loops through all wells and checks the quality of the ensemble forecast. For all wells that have coverage less than 95 %, 
       determine the level of severity in the mismatch (through the intervalScore)
'''


def get_coverage(task, wellList, mode):
    
    if task == 'a':
        print "Task 3 a) starts here:"
    elif task == 'b':
        print "Task 3 b) starts here:"
    elif task == 'c':
        print "Task 3 c) starts here:"

    nWells = len(wellList)
    name = []
    for i in wellList:
        newName = 'BR-'+ i
        name.append(newName)

    data = []
    obsData = []

    #Loading the files
    for i in wellList:
        for j in mode:
            newFile1 = np.load('../data/W'+ j +'-BR-'+ i + '_summary_brugge_prior.npy')
            newFile2 = np.load('../data/W'+ j +'H-BR-'+ i + '_summary_brugge_prior.npy')
            data.append(newFile1)
            obsData.append(newFile2)

    #Get the number of case data(timeSteps, cases)
    sample = np.load('../data/W'+ mode[0] +'-BR-'+ wellList[0] + '_summary_brugge_prior.npy')
    nCases = np.size(sample,1)

    #Get the number of time step
    timeSeries = np.load(timeSeriesFileName)
    nTimeSteps = len(np.load(timeSeriesFileName))
    #print 'The number of time steps are:', nTimeSteps

    tol = 0.001 * np.ones((nTimeSteps,nCases))
    coverage = 0.95

    err = np.zeros((nTimeSteps,nCases))
    ind = np.zeros((nTimeSteps,nCases))
    perf = np.zeros(nCases)

    for well in range(nWells):
        for j in range(nCases):
            err[:,j] = abs(data[well][:,j] - obsData[well][:,j])/nTimeSteps
            ind[:,j] = np.where(err[:,j] < tol[:,j], 1, 0)
    
            perf[j] = np.sum(ind[:,j])/nTimeSteps

            if perf[j] > coverage: 
                print 'ensemble simulated W' + mode[0] + ' data captured the observed data for well:' + name[well]
                break

            if perf[j] < coverage and j == nCases -1:
                print 'warning: ensemble simulated W' + mode[0] + ' data did NOT capture the observed data for well:' + name[well]
                
                if task == 'b':
                    print '\tprinting the intervalScore for each case in this well...'
                
                    someDict = {}
                    someDict = calculate_standard_deviation('c', mode[0], name[well][3])
                    print someDict[name[well]]

                if task == 'c':
                    if mode == ['OPR']:
                        print 'the simulated oil production rate fails to match the history, '
                        print '\t - Consider revising horizontal permeability around well', name[well]
                        print '\t - Check BHP, if not captured, consider revising the bottomhole pressure of well', name[well]
                        print '\t - Consider revising the relative permeability curve'    

                    if mode == ['WPR']:
                        print 'the simulated water production rate fails to match the history, '
                        print '\t - Consider revising horizontal permeability around well', name[well]
                        print '\t - Check BHP, if not captured, consider revising the bottomhole pressure of well', name[well]
                        print '\t - Consider revising the relative permeability curve'

                    if mode == ['BHP']:
                        print 'the simulated water production rate fails to match the history, '
                        print '\t - Check other wells, if most of the BHP match fails, consider checking the pressure support in the reservoir'
                        print '\t - Check BHP, if not captured, consider revising the horizontal permeability around well', name[well]
                        
        print '----------------------------------------------------------------------'
    return 0
'''  
   c) For wells what have less than 95 % coverage write a function the returns a list of recommendations that the user should potentially consider to improve the 
       quality of the ensemble. One example could be:

        - "Ensemble is failing to match the water cut of well BR-P10 (breakthough is too late and slope is not correct): suggested fixes: 
            1. "Consider revising horizontal permeability around well BR-P-10"
            2. "..." 
 
'''

#This is task 3 a) and b), specify in the first input
#Specify input here
listOfWells = ['P-1', 'P-2', 'P-10', 'I-1', 'I-2', 'I-10']
var = ['BHP']

get_coverage('c', listOfWells, var)