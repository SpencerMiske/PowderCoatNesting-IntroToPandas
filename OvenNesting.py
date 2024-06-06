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

for item in batchable:
    print(item)

while batchable:
    input("Next Batch?")
    nextUp = []
    jobUp = batchable.pop(0)
    nextUp.append(jobUp)
    minTime = jobUp[2]
    maxTime = jobUp[3]
    
    i = 0
    while i < len(batchable) and len(nextUp) < BATCH_SIZE_LIMIT:
        if jobUp[1] == batchable[i][1]:
            if int(batchable[i][3]) > minTime and int(batchable[i][2]) < maxTime:
                if int(batchable[i][3]) < maxTime: maxTime = int(batchable[i][3])
                if int(batchable[i][2]) > minTime: minTime = int(batchable[i][2])
                nextUp.append(batchable.pop(i))
                i -= 1
        i += 1

    paintRow = curingTimes[curingTimes.iloc[:, 0] == jobUp[1]].index
    if len(paintRow) == 0:
        print(f"No matching paint row found for job {jobUp[1]}.")
        continue
    
    paintRow = paintRow[0]
    
    paintTime = -9999
    if curingTimes.loc[paintRow, 'min400'] != -9999: paintTime = curingTimes.loc[paintRow, 'min400']
    elif curingTimes.loc[paintRow, 'min375'] != -9999: paintTime = curingTimes.loc[paintRow, 'min375']
    elif curingTimes.loc[paintRow, 'min350'] != -9999: paintTime = curingTimes.loc[paintRow, 'min350']

    if paintTime == -9999:
        print("No valid paint time found for job.")
        continue

    for item in nextUp:
        print(str(item[0]) + " " + str(item[1]))

    print("Predicted batch time: " + str((((maxTime + minTime) / 2) + paintTime)))

print("All done!")
