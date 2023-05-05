"""
Script to analyze cost of morally offsetting the average American diet
"""

############################# SETUP #############################
import squigglepy as sq
import numpy as np
import pickle
import os

############################# INPUTS #############################

#Need to consider whether to truncate distributions ]
dietSpeciesList = ['pigs', 'chickens','salmon', 'shrimp']

#American's diet, in kg 
#Treating cows, pigs, and "other" as equivalent to pigs
#Treating all fish as salmon
#Not accounting for milk/eggs yet 
americanDietKg = {'pigs': 37.3+30.2+0.8,\
                  'chickens': 57.8,\
                  'salmon': 6.35,\
                  'shrimp': 2.67}

#Need some estimate of many animals are hurt in the process of farming a given number of other 
#animals (e.g. fish used feed for pigs). Before doing computations, add extra animals harmed to 
#the directly-harmed ones 

#Need some estimate of the indirect animals saved by going vegan (e.g. by catalyzing demand
#for alt proteins). Add these animals that fail to be indirectly benefited to the sum

#Lifetimes in years
#Means from https://reducing-suffering.org/how-much-direct-suffering-is-caused-by-various-animal-foods/#Results_table
#Stds mad eup 
lifetimes = {'pigs': [183/365, 20/365],\
             'chickens': [42/365, 10/365],\
             'salmon': [639/365, 100/365],\
             'shrimp': [180/365, 60/365]} 

#Means from https://reducing-suffering.org/how-much-direct-suffering-is-caused-by-various-animal-foods/#Results_table
#Stds made up
kgsPerIndiv = {'pigs': [65, 10],\
               'chickens': [1.9, 0.5],\
               'salmon': [2.0, 0.5],\
               'shrimp': [0.028, 0.005]}
  
#Need to be careful here: modelling welfare fractional level as -0.5 to 0.5. May want to change this 
# Values made up 
welfareFractLevel = {'pigs': [-0.25, 0.1],\
                     'chickens': [-0.25, 0.1],\
                     'salmon': [-0.1, 0.1],\
                     'shrimp': [-0.1, 0.1]}


#Read in welfare range distributions 
# Would like to re-save these in a format other than pickle dumps since other users
# may be reluctant to load pickle files for security reasons
# NOTE: Currently using my own results from 500 runs (10000 is slow)
rpSpeciesList = ['pigs', 'chickens', 'carp', 'salmon', 'octopuses', 'shrimp', 'crabs', 'crayfish', 'bees', 'bsf', 'silkworms']
welfareCapacity = dict.fromkeys(rpSpeciesList)
for species in rpSpeciesList:
     welfareCapacity[species] = pickle.load(open('{}_wr_Mixture_model.p'.format(os.path.join('welfare_range_estimates', species)), 'rb'))


############################# COMPUTATION #############################


#For each species, compute distribution of expected animal welfare  
#harms from eating an average american's quantity of them
welfareImpactDists = dict.fromkeys(dietSpeciesList)
welfareImpactStats = dict.fromkeys(dietSpeciesList)
for species in dietSpeciesList:
    
    #Build distributions
    lifetimeDist = sq.norm(mean=lifetimes[species][0], sd=lifetimes[species][1])
    kgPerIndivDist = sq.norm(mean=kgsPerIndiv[species][0], sd=kgsPerIndiv[species][1])
    welfareFracDist = sq.norm(mean=welfareFractLevel[species][0], sd=welfareFractLevel[species][1])
    welfareCapacityDist = sq.discrete(welfareCapacity[species])
    
    #Multiply to get overall welfare impact of this species distribution 
    welfareImpactDists[species] = (americanDietKg[species]/kgPerIndivDist)*lifetimeDist*welfareFracDist*welfareCapacityDist
    
    #Sample distribution and record stats 
    samples = welfareImpactDists[species] @ 10000
    welfare_range_array = np.array(samples)
    welfareImpactStats[species] = np.percentile(welfare_range_array, [5, 50, 95])
    
print(welfareImpactStats)

#Sum across all animals
sumDist = sq.norm(mean=0, sd=0)
for species in dietSpeciesList:
    sumDist = sumDist + welfareImpactDists[species]

#Sample overall distribution
samples = sumDist @ 10000
sumArray = np.array(samples)
sumStats = np.percentile(sumArray, [5, 50, 95]) 
print("5th, 50th, 95th percentiles for Human-Year Equivalent Welfare Impacts of Diet: {}".format(sumStats))
#Need to compute impact of THL/SWP donation

#Need to add in climate effects 




