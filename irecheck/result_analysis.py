
#!/usr/bin/env python3

import sys
import random
import time
import os
import pandas as pd
# from irecheck_toolkit import *




# path =  '~/Documents/iReCHeCk_logs'

path = "/home/carnieto/Documents/iReCHeCk_logs/Feb_23/"


cond_index = 0

options = ['Meditation', 'Stretching']
condition =  options[cond_index]

path = os.path.join(path, condition)


file_list = os.listdir(path)

# print(file_list)


final = pd.DataFrame()

# exit()


for subject in file_list: 
# subject = file_list[0]
# subject = '13-02-2023_09-50-51_1000'
  
    if len(subject)< 25:
        continue
    
    # filename = path
    filename = os.path.join(path, subject) #+ ".csv"
    print(filename)
    df = pd.read_csv(filename)

    try:

        # take first and last lines correspondind to the first and second dynamilis HW analysis. Add the tag to the column "round" regardig the time the analysis was displayed
        first = df.iloc[0]
        first['round'] = 'first' 
        last = df.iloc[-1]
        last['round'] = 'last' 


    except:
        pass

    final = final.append(first)
    final = final.append(last)
    final['condition'] = condition


# Filtering the columns
final = final[['round', 'condition', 'totalScore', 'totalScoreLabel',
               'kinematicScore', 'kinematicScoreLabel',
               'pressureScore', 'pressureScoreLabel',
               'staticScore', 'staticScoreLabel', 
               'tiltScore', 'tiltScoreLabel', 
               'writingAnalysisExerciseId']]


print(final.columns)



final.to_csv(os.path.join(path, 'Total_HW_analysis.csv'), index=False)




print("Done!")
# print(final['round'])

