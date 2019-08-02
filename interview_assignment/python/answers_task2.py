import matplotlib

import numpy as np
import matplotlib.pyplot as plt
import json
import matplotlib.dates as mdates
import operator

from matplotlib import pyplot as mp #to save figure


summaryKeys = ['OPT','OPR','WPT','WPR','GPT','GPR','WIT','WIR','BHP','WCT','GOR','LPR','LPT']
timeSeriesFileName = '../data/brugge_time_series.npy'
jsonFileName = '../data/brugge_prior_summary_data.json'

#summaryDict = get_summary_ensemble_dictionary(jsonFileName)

#Loads the json file containing the summary data as a python dictionary
def get_summary_ensemble_dictionary(jsonFileName):
    with open(jsonFileName) as json_file:
        priorDict = json.load(json_file)

    return priorDict

'''TASK 2

   a) Write a function that for each well assesses the quality of the ensemble forecast using the following critera:
   
 
     
     the interval score is then given as

     intervalScore = \sum_{t=1}^{nT} ( (u_t - l_t) +  2.0 / 0.025 * (l_t - obs_t) * Ind(obs_t < l_t) + 2.0 / 0.025 * (obs_t - u_t) * Ind(obs_t > u_t) )

     
     Here: 
          u_t, is the 97.5 percentile of the ensemble of measurements, 
          l_t, is the 2.5 percentile of the ensemble of measurements at timestep t
          \sum is the sum operator
          nT  is the number of simulation time steps
          obs_t is the observed data at timestep t
          Ind(*) is the indicator function (returns 1 if the criterion is satisfied, zero otherwise)

      The interval score for each well and summary property (where you have observed data) should be returned as a python dictionary
'''

'''
   b) The interval score is sensitive to the scale of the specified summary property. Repeat task 2 a) where you re-scale all data by dividing by 
        max(1.0, 0.1 * obs_t) for each timestep before calculating the intervalScore
'''

def calculate_standard_deviation(task, mode1, mode2):
    #task -- either 'a' or 'b', as given in the problem statement
    #mode1 -- the variable we are interested in, e.g. 'OPR', 'WPR', WCT', that have historical data
    #mode2 -- either 'P' or 'I', production or injection well. However for now only 'P' works since it has historical data

    print 'calling function calculate_standard_deviation ...'

    if task == 'b':
        print "Task 2 b) starts here:"
    elif task == 'a':
        print "Task 2 a) starts here:"

    #Printing the number of wells:
    nWells = 20
    if task == 'a' or task == 'b': 
        print 'The number of wells are:', nWells

    #Get the number of time step
    timeSeries = np.load(timeSeriesFileName)
    nTimeSteps = len(np.load(timeSeriesFileName))
    if task == 'a' or task == 'b':
        print 'The number of time steps are:', nTimeSteps

    #Get initial date
    InitDate = timeSeries[0]

    #Get the number of case data(timeSteps, cases)
    sample = np.load('../data/WWCT-BR-P-10_summary_brugge_prior.npy')
    nCases = np.size(sample,1)
    if task == 'a' or task == 'b':
        print 'The number of cases are:', nCases


    data = []
    #Loading the file according to the modes
    if task == 'a' or task == 'b':
        print "...assessing the variable:", mode1
        print "well type:", mode2
    for wellNumber in range(0,nWells):
        newFile = np.load('../data/W'+ mode1 +'-BR-'+ mode2 + '-'+ str(wellNumber + 1) + '_summary_brugge_prior.npy')
        data.append(newFile)

    #Get the well name and store to variable 'name'
    name = []
    for i in range(0,nWells):
        newName = 'BR-'+ mode2 + '-' + str(i + 1)
        name.append(newName)

    obsData = []
    #Get the observed data
    for wellNumber in range(0,nWells):
        newFile = np.load('../data/W'+ mode1 +'H-BR-'+ mode2 + '-'+ str(wellNumber + 1) + '_summary_brugge_prior.npy')
        obsData.append(newFile)

    #print obsData


    #defining dictionary for sim data and observed data named myDict and my myObsDict
    myDict = {}
    myObsDict = {}
    for i in range(0,nWells):
        myDict[name[i]] = ''
        myObsDict[name[i]] = ''

    for well in range(0,nWells):
        sum = np.zeros(nCases)
        x = np.zeros(nCases)
        y = np.zeros(nCases)
        for t in range(0,nTimeSteps):
        #for case in range(0,nCases):
            dummyVec = data[well][t,:]
            dummyObsVec = obsData[well][t,:]

            if task == 'b':
                #print '...rescaling the observed data...'
                for case in range(nCases): 
                    #This rescaling does not seem right since the values are too different,
                    #..., perhaps this was the point
                    dummyVec[case] = dummyVec[case]/max(1.0, 0.1* dummyVec[case])
            
            u_t = np.percentile(dummyVec, 97.5)
            l_t = np.percentile(dummyVec, 2.5)

            x = [1 if i < l_t else 0 for i in dummyObsVec]
            y = [1 if i > u_t else 0 for i in dummyObsVec]

            #the interval score doesn't seem to have an intuitive range, hence computed as is
            sum = sum + ( (u_t - l_t) +  2.0 / 0.025 * (l_t - dummyObsVec) * x + 2.0 / 0.025 * (dummyObsVec - u_t) * y )
            
        myDict[name[well]] = sum

        
    print 'function calculate_standard_deviation called and returned'
    
    return myDict


'''
   c) Write a function that creates a bar chart of the 10 biggest interval scores obtained in Task 2 b) and store it as a .png file (ranked by the largest to smallest value)
'''

def create_bar_chart(mode, nbar):

    #mode -- the variable we are interested in, e.g. 'OPR', 'WPR', WCT', that have historical data
    #nbar -- the number of largest interval score desired

    print 'calling create_bar_chart ...'
    print "Task 2 c) starts here:"

    #storing the interval score data from previous task in variable 'myDict'
    myDict = calculate_standard_deviation('a', mode, 'P')

    #Calculating the average interval score
    newDict = {}
    for myDictKey,myDictValue in myDict.iteritems():
        
        ave = np.average(myDictValue)
        print 'Average interval score by case for well ', myDictKey, 'is', ave

        newDict[myDictKey] = ave
    
    #sorting the dictionary in decreasing fashion
    sortedDict = sorted(newDict.items(), key=operator.itemgetter(1), reverse=True)

    #Getting the x- and y- axis
    x = []
    y = []
    for i in range(nbar):
        x.append(sortedDict[i][0])
        y.append(sortedDict[i][1])

    y_pos = np.arange(len(x))
    plt.figure(str(nbar) + ' largest interval score for mode ' + mode, figsize=(10,5))
    plt.bar(y_pos, y, align='center', alpha=0.5)
    plt.xticks(y_pos, x)
    plt.ylabel('Interval score')
    plt.title( str(nbar) + ' largest interval score for mode ' + mode)
    mp.savefig(str(nbar) + '_largest_interval_score_for_mode_' + mode)
    print 'bar chart for mode', mode, 'is saved as .png file'
    plt.show()

    print 'function create_bar_chart called and returned'

    return 0



#print answer for Task 2 a) or b)
print calculate_standard_deviation('a', 'WPR', 'P')

#print answer for Task 2 c)
#create_bar_chart('OPR', 10)
