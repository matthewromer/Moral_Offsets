"""
Script to analyze cost of morally offsetting the average American diet
"""

############################# SETUP #############################
import squigglepy as sq
import numpy as np
import pickle
import os
import pandas as pd 
from foodType import foodType
from computeSummaryStats import computeSummaryStats

############################# INPUTS #############################
    
#Read in diet input data
# Note: treating all fish as farmed right now. Need to figure out balance between farmed/
# wild-caught and how to model. Current format doesn't allow for uncertainty
# in concumption 
inputData = pd.read_csv('inputs.csv', index_col=0,header=0)
foodTypes = list(inputData.index);

#Read in welfare range distributions 
# Would like to re-save these in a format other than pickle dumps since other users
# may be reluctant to load pickle files for security reasons
# NOTE: Currently using my own results from 500 runs (10000 is slow)
rpSpeciesList = ['pigs', 'chickens', 'carp', 'salmon', 'octopuses', 'shrimp', 'crabs', 'crayfish', 'bees', 'bsf', 'silkworms']
welfareCapacity = dict.fromkeys(rpSpeciesList)
for species in rpSpeciesList:
     welfareCapacity[species] = pickle.load(open('{}_wr_Mixture_model.p'.format(os.path.join('welfare_range_estimates', species)), 'rb'))


############################# COMPUTATION #############################

#Create object describing each food's impact and store in dict
#Assuming possible xwelfare range is -0.5 to 0.5
foodDict = dict.fromkeys(foodTypes) 
dayToYear = 1/365.25;
minWelfare = -0.5;
maxWelfare = 0.5;
for food in foodTypes:
    foodDict[food] = foodType(inputData.loc[food]['Source Animal (Approx.)'],\
                     sq.norm(mean=inputData.loc[food]['Mean days of suffering per kg']*dayToYear, sd=inputData.loc[food]['SD days of suffering per kg']*dayToYear),\
                     sq.norm(mean=inputData.loc[food]['Welfare Level Mean'], sd=inputData.loc[food]['Welfare Level SD'],lclip=minWelfare,rclip=maxWelfare),\
                     inputData.loc[food]['Average Annual US Consumption (kg)'],\
                     sq.discrete(welfareCapacity[inputData.loc[food]['Source Animal (Approx.)']]),\
                     sq.norm(mean=inputData.loc[food]['CO2e Mean per kg (kg)'], sd=inputData.loc[food]['CO2e SD per kg (kg)']))

#Would like a second step here that involves augmenting distributions with additional 
#animals killed to feed the farmed animals 

#Sum welfare and climate impact distributions across all food types
welfareSumDist = sq.norm(mean=0, sd=0)
climateSumDist = sq.norm(mean=0, sd=0)
welfareImpactStats = dict.fromkeys(foodTypes)
for food in foodTypes:
    welfareSumDist = welfareSumDist + foodDict[food].welfareImpact
    climateSumDist = climateSumDist + foodDict[food].climateImpact
    

#Sample overall distributions
computeSummaryStats(welfareSumDist,printEn=True,name='Welfare Impacts Distribution (Human-Equivalent WELLBYs)')
computeSummaryStats(climateSumDist,printEn=True,name='Climate Impacts Distribution (kg CO2e)')
