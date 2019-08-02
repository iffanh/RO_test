import numpy as np


#importing data from folder
#folder name
folderName = '../data/'
#file name
fileName = 'WOPRH-BR-P-9_summary_brugge_prior.npy'

x = np.load(folderName + fileName)

print(x)