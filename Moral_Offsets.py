#Script to analyze cost of morally offsetting the average American diet

############################# SETUP #############################
import squigglepy as sq
import numpy as np
import pickle
import os
import pandas as pd 
from FoodType import FoodType
from computeSummaryStats import computeSummaryStats
from sqDistWrapper import sqDistWrapper

############################# INPUTS #############################
    
#Read in diet input data
# Note: treating all fish as farmed right now. Need to figure out balance 
# between farmed/wild-caught and how to model. Current format doesn't allow 
# for uncertainty in consumption 
inputData = pd.read_csv('inputs.csv', index_col=0,header=0)
foodTypes = list(inputData.index);

#Read in welfare range distributions 
# Would like to re-save these in a format other than pickle dumps since other 
# users may be reluctant to load pickle files for security reasons
# NOTE: Currently using my own results from 500 runs (10000 is slow)
rpSpeciesList = ['pigs', 'chickens', 'carp', 'salmon', 'octopuses',\
                 'shrimp', 'crabs', 'crayfish', 'bees', 'bsf', 'silkworms']
welfareCapacity = dict.fromkeys(rpSpeciesList)
for species in rpSpeciesList:
     welfareCapacity[species] = pickle.load(open('{}_wr_Mixture Neuron Count_model.p'.format(os.path.join('welfare_range_estimates', species)), 'rb'))

#Verbose flag
verbose = False

################### COMPUTING HARMS OF MEAT EATING ###################

#Create object describing each food's impact and store in dict
#Assuming possible welfare range is -0.5 to 0.5
foodDict = dict.fromkeys(foodTypes) 
dayToYear = 1/365.25;
minWelfare = -0.5;
maxWelfare = 0.5;
for food in foodTypes:
    foodDict[food] = FoodType(inputData.loc[food]['Source Animal (Approx.)'],\
                     sq.norm(mean=inputData.loc[food]['Mean days of suffering per kg']*dayToYear, sd=inputData.loc[food]['SD days of suffering per kg']*dayToYear),\
                     sq.norm(mean=inputData.loc[food]['Welfare Level Mean'], sd=inputData.loc[food]['Welfare Level SD'],lclip=minWelfare,rclip=maxWelfare),\
                     inputData.loc[food]['Average Annual US Consumption (kg)'],\
                     sq.discrete(welfareCapacity[inputData.loc[food]['Source Animal (Approx.)']]),\
                     sqDistWrapper(inputData.loc[food]['CO2e Distribution Type'],inputData.loc[food]['CO2e 5th Percentile Per kg (kg)'],inputData.loc[food]['CO2e 95th Percentile Per kg (kg)']),\
                     sqDistWrapper(inputData.loc[food]['Fresh Water Distribution Type'],inputData.loc[food]['Fresh Water 5th Percentile Per kg (L)'],inputData.loc[food]['Fresh Water 95th Percentile Per kg (L)']),\
                     sqDistWrapper(inputData.loc[food]['Land Use Distribution Type'],inputData.loc[food]['Land Use 5th Percentile per kg (m^2)'],inputData.loc[food]['Land Use 95th Percentile per kg (m^2)']))

#Would like a second step here that involves augmenting distributions with additional 
#animals killed to feed the farmed animals 

#Sum impact distributions across all food types
welfareSumDist  = sq.norm(mean=0, sd=0)
climateSumDist  = sq.norm(mean=0, sd=0)
landUseSumDist  = sq.norm(mean=0, sd=0)
WaterUseSumDist = sq.norm(mean=0, sd=0)
welfareImpactStats = dict.fromkeys(foodTypes)
for food in foodTypes:
    welfareSumDist  = welfareSumDist + foodDict[food].welfareImpact
    climateSumDist  = climateSumDist + foodDict[food].climateImpact
    landUseSumDist  = landUseSumDist + foodDict[food].landUseImpact
    WaterUseSumDist = WaterUseSumDist + foodDict[food].waterUseImpact

#Modify climate effects distribution to account for climate impacts of 
#substitution
    

#Sample overall distributions
computeSummaryStats(welfareSumDist,printEn=True,name='Welfare Impacts Distribution (Human-Equivalent DALYs)')
computeSummaryStats(climateSumDist,printEn=True,name='Climate Impacts Distribution (kg CO2e)')

################### COMPUTING COSTS OF OFFSETTING ###################
#Need to think about how to reorg this section (e.g. make some classes)


#Climate 

#Need to figure out shape of distribution
catfCostPerKgCO2e = sq.norm(0.35/1000, 4.40/1000)
costOfClimateOffsetting = climateSumDist*catfCostPerKgCO2e
computeSummaryStats(costOfClimateOffsetting,printEn=True,name='Total Cost of Climate Offsets:')

#Welfare 

#Hand-fit to roughly match https://www.getguesstimate.com/models/13441 - could use discrete samples instead 
#chickYearsPerDollar = sq.beta(a=2,b=9)*270
#More conservative version - subjective guess
chickYearsPerDollar = sq.beta(a=2,b=9)*135

#Rough data from https://www.pain-track.org/hens
#Time spent in hurtful pain goes from 4052.50 ± 788.95 h
#to 1759.73 ± 754.55 h.
#Factor of 1.5 for conservatism
chickenNominalWelfareLevel =inputData.loc['Chicken']['Welfare Level Mean']
minDeltaWelfarelevel = (1759.73+(754.55*1.5)-(4052.50-(788.95*1.5)))/4052.50*chickenNominalWelfareLevel
maxDeltaWelfareLevel = (1759.73-(754.55*1.5)-(4052.50+(788.95*1.5)))/4052.50*chickenNominalWelfareLevel
welfareLevelImprovement = sq.norm(minDeltaWelfarelevel,maxDeltaWelfareLevel)


dalyEquivsPerDollar = chickYearsPerDollar*welfareLevelImprovement*sq.discrete(welfareCapacity['chickens'])
costOfWelfareOffsetting = -1*welfareSumDist/dalyEquivsPerDollar
computeSummaryStats(costOfWelfareOffsetting,printEn=True,name='Total Cost of Welfare Offsets:')

if verbose:
    print('CO2e \n')
    for food in foodTypes:
        print(food)
        computeSummaryStats(foodDict[food].co2eKgPerKg,True)
    print('Water \n')
    for food in foodTypes:
        print(food)
        computeSummaryStats(foodDict[food].waterLPerKg,True)        
    print('Land Use \n')
    for food in foodTypes:
        print(food)
        computeSummaryStats(foodDict[food].landM2PerKg,True)
