import pandas as pd
import os

#"Static" variables
BATCH_SIZE_LIMIT = 3

#Storing File Path
file_path1 = r'Z:\PROTOCASE USER FILES\Spencer Miske\PowderCoatTimes.csv'
file_path2 = r'Z:\PROTOCASE USER FILES\Spencer Miske\CookingTimes.csv'
file_path3 = r'Z:\PROTOCASE USER FILES\Spencer Miske\OvenJobs.csv'

# Loading files
curingTimes = pd.read_csv(file_path1, encoding='latin1')
cookingTimes = pd.read_csv(file_path2, encoding='latin1')
jobs = pd.read_csv(file_path3, encoding='latin1')

batchable = []

def addToBatch(jobID, paintID, thickness, metal):
    temp = []
    thicknessRow = cookingTimes[cookingTimes.iloc[:, 0] == thickness].index[0]
    temp.append(jobID)
    temp.append(paintID)
    temp.append(cookingTimes.loc[thicknessRow, metal])
    temp.append(temp[2] + 3)
    batchable.append(temp)

# Takes Jobs from queue
for index, row in jobs.iterrows():
    addToBatch(row.iloc[0], row.iloc[1], row.iloc[3], row.iloc[2])

#Lists all jobs
for item in batchable:
    print(item)

#Batching loop
while batchable:
    #Waits for user input
    input("Next Batch?")

    #initializing Variables
    nextUp = []
    jobUp = batchable.pop(0)
    nextUp.append(jobUp)
    maxHeatUpTime = jobUp[2] + 1.5

    #Checks if paint type exists
    paintRow = curingTimes[curingTimes.iloc[:, 0] == jobUp[1]].index
    if len(paintRow) == 0:
        print(f"No matching paint row found for job {jobUp[1]}.")
        continue
    
    paintRow = paintRow[0]

    #Checks for valid oven temp
    paintTime = -9999
    if curingTimes.loc[paintRow, 'min400'] != -9999:
        heat = "400"
        paintTime = curingTimes.loc[paintRow, 'min400']
        tolerence = (curingTimes.loc[paintRow, 'max400'] - paintTime)/2
    elif curingTimes.loc[paintRow, 'min375'] != -9999:
        heat = "375"
        paintTime = curingTimes.loc[paintRow, 'min375']
        tolerence = (curingTimes.loc[paintRow, 'max375'] - paintTime)/2
    elif curingTimes.loc[paintRow, 'min350'] != -9999:
        heat = "350"
        paintTime = curingTimes.loc[paintRow, 'min350']
        tolerence = (curingTimes.loc[paintRow, 'max350'] - paintTime)/2

    if paintTime == -9999:
        print("No valid paint time found for job.")
        continue

    #Checking if any jobs can fit with the first job in queue
    i = 0
    while i < len(batchable) and len(nextUp) < BATCH_SIZE_LIMIT:
        #If paint ID matches
        if jobUp[1] == batchable[i][1]:
            if (batchable[i][2] - jobUp[2]) > -tolerence and (batchable[i][2] - jobUp[2]) < tolerence:
                if batchable[i][2] > jobUp[2]:
                    maxHeatUpTime = batchable[i][2] + 1.5
                nextUp.append(batchable.pop(i))
                i -= 1
        i += 1

    for item in nextUp:
        print(str(item[0]) + " " + str(item[1]))

    print("Cook at " + heat + " for " + str(maxHeatUpTime + paintTime))

#ADD PREDICTED TIME

print("All done!")
