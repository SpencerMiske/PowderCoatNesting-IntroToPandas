import pandas as pd
import os

file_path1 = r'Z:\PROTOCASE USER FILES\Spencer Miske\PowderCoatTimes.csv'
file_path2 = r'Z:\PROTOCASE USER FILES\Spencer Miske\CookingTimes.csv'

#loading files
curingTimes = pd.read_csv(file_path1, encoding='latin1')
cookingTimes = pd.read_csv(file_path2, encoding='latin1')
jobs = pd.read_csv(r'Z:\PROTOCASE USER FILES\Spencer Miske\OvenJobs.csv', 
encoding='latin1')

batchable = []

def addToBatch(jobID, paintID, thickness, metal):
    temp = []
    for i in range(len(cookingTimes)):
        if cookingTimes.iloc[i, 0] == thickness:
            thicknessRow = i

    temp.append(jobID)
    temp.append(paintID)
    temp.append(cookingTimes.loc[thicknessRow, metal])
    temp.append(temp[2]+3)
    batchable.append(temp)


for y in range(len(jobs)):
    addToBatch(jobs.iloc[y,0], jobs.iloc[y,1], jobs.iloc[y,3], jobs.iloc[y,2])


for i in range(len(batchable)):
    print(batchable[i])