import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.dates as mdates

from numbers import Number

from collections import Counter

from heapq import nlargest #to find top n largest number


timeSeriesFileName = '../data/brugge_time_series.npy'
jsonFileName = '../data/brugge_prior_summary_data.json'

#summaryDict = get_summary_ensemble_dictionary(jsonFileName)

'''
TASK 1
'''

'''
   a)  Write a function that for each producing well of the brugge field, and for each simulation case calculate the time to the well 
       starts cutting water (defined as water cut > 0.05) and returns the values as a dictionary of list where element j of the list contains 
       the water breakthrough time for case j. Example of the expected output (number not real): {'BR-P-3': [1300, 2341, 3131, ...., 1000], 'BR-P-2': [1000, 2311, 3041,...,3123],....}
'''
def get_water_breakthrough_time(mode):

    #mode = 1 print all the details, this is not needed when only calling the data

    print 'calling function get_water_breakthrough_time ...'
    if mode == 1:
        print "Task 1 a) starts now:"

    #Printing the number of wells:
    nWells = 20
    if mode == 1:
        print 'The number of wells are:', nWells

    #Get the number of time step
    timeSeries = np.load(timeSeriesFileName)
    nTimeSteps = len(np.load(timeSeriesFileName))
    if mode == 1:
        print 'The number of time steps are:', nTimeSteps

    #Get initial date
    InitDate = timeSeries[0]

    #Get the number of case data(timeSteps, cases)
    sample = np.load('../data/WWCT-BR-P-10_summary_brugge_prior.npy')
    nCases = np.size(sample,1)
    if mode == 1:
        print 'The number of cases are:', nCases

    #Get the well name and store to variable 'name'
    name = []
    for i in range(0,nWells):
        newName = 'BR-P-' + str(i + 1).zfill(2)
        name.append(newName)

    #defining dictionary for water cut named WCDict
    WCDict = {}
    for i in range(0,nWells):
        WCDict[name[i]] = ''

    #Get all the required data from the files with WWCT, waterCutData[which wel][timeSteps, cases]
    waterCutData = []
    for wellNumber in range(0,nWells):
        newFile = np.load('../data/WWCT-BR-P-'+ str(wellNumber + 1) + '_summary_brugge_prior.npy')
        waterCutData.append(newFile)

    for well in range(0,nWells):
        BTtime = []
        for case in range(0,nCases):
            if mode == 1:
                print '----------------------------------------------------------------------'
                print 'this is well: BR-P-', well
                print 'this is case:', case
            t = 0
            while (waterCutData[well][t,case] < 0.05 and t < nTimeSteps - 1):
                t = t + 1

           
            if t == nTimeSteps - 1:
                if mode == 1:
                    print "\tmaximum time reached, no water breakthrough found"
                    print "\tat maximum time, the water cut is:", waterCutData[well][t,case]
                date = 'None'
                BTtime.append(date)
            else:   
                if mode == 1: 
                    print "\twater breakthrough found, at time", timeSeries[t+1]
                    print "\tthe water cut is", waterCutData[well][t,case]
                date = timeSeries[t+1]
                dt = date - InitDate
                BTtime.append(dt.days)

            WCDict[name[well]] = BTtime


    print 'function get_water_breakthrough_time called and returned'
    return WCDict

'''


   b)  Write a function that for each well, create and store a histogram of the water breakthrough times calculated in assignment a)

'''

def get_histogram():
    print 'Task 1 b) starts now:'
    #First define how many bins
    nBins = 3.0

    #Get the data from Task 1 a)
    wcTime = get_water_breakthrough_time(0)

    for BTtime in wcTime.values():
        #Deleting the 'None' part of the array, and the new array is stored in 'temp'
        temp = list(filter(lambda x: isinstance(x, Number), BTtime))
        print temp

        if len(temp) < 1: #if array is empty
            print 'this well has 0 or 1 case with water breakthrough'
        else:
            #delta = (max(temp) - min(temp)) / nBins
        
            #for i in range(nBins):
            #    bin[i]

            n, bins, patches = plt.hist(x=temp, bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)
            plt.grid(axis='y', alpha=0.75)
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            plt.title('My Very Own Histogram')
            maxfreq = n.max()

        # Set a clean upper y-axis limit.
            plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
            plt.show()

    #print len(well)

    return 0



'''


   c)  Write a function that list the five wells that have highest variability in the water breakthough time 
          (reporting the standard deviation and range for the water breakthrough time) 

'''

def nlargest_variability(n):

    print 'calling function nlargest_variability ...'
    print 'Task 1 c) starts now:'

    #Printing the number of wells:
    nWells = 20
    print 'The number of wells are:', nWells

    #Initializing standard deviation and maxmin dictionary 
    standDevDict = {}
    maxminDict = {}

    #Get the data from Task 1 a)
    wcTime = get_water_breakthrough_time(0)

    for BTtimeKey, BTtimeValues in wcTime.iteritems():
        #Deleting the 'None' part of the array, and the new array is stored in 'temp'
        temp = list(filter(lambda x: isinstance(x, Number), BTtimeValues))
        if len(temp) < 1:
            standDevDict[BTtimeKey] = 0
            maxminDict[BTtimeKey] = ['nan', 'nan']    
        else:
            standDev = np.std(temp)
            if np.isnan(standDev) == True: standDev = 0
            print 'Well:', BTtimeKey, "has standard deviation of", standDev 

            #saving the standard deviation into a dictionary called 'standDevDict'
            standDevDict[BTtimeKey] = standDev
            maxminDict[BTtimeKey] = [min(temp), max(temp)]

    #finding the five largest 
    five_largest = sorted(standDevDict, key=standDevDict.get, reverse=True)[:n]

    print 'The five largest well with highest variability are:'

    for N in five_largest:
        print 'Well', N, 'with the standard deviation of ', standDevDict[N], 'with the range of breakthrough time between', maxminDict[N][0], 'and', maxminDict[N][1], 'days'

    print 'function nlargest_variability called and returned'

    return 0

#print answer for Task 1 a)
print get_water_breakthrough_time(1)

#print answer for Task 1 c)
#nlargest_variability(5)