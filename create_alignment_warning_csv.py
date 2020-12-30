# Creating CSV of alignment warnings

import json
import csv
import time
from datetime import timedelta
import pandas as pd
import utils.db_utils as db
import utils.file_utils as file

type_ = 'kt'
bibleType = 'en_ult'

#############################

start = time.time()
minAlignments = 40
remove = ['ὁ']
alignmentsForWord, filteredAlignmentsForWord = db.fetchAlignmentDataForTWordCached(type_, bibleType, minAlignments, remove)

#############################

print(f"Testing tWords {type_} with minimum of {minAlignments} alignments")

alignmentOrigWordsThreshold = 3
alignmentTargetWordsThreshold = 5
origWordsBetweenThreshold = 1
targetWordsBetweenThreshold = 1
alignmentFrequencyMinThreshold = 5
warningData = db.generateWarnings(type_, bibleType, filteredAlignmentsForWord, alignmentOrigWordsThreshold,
                                  alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                  targetWordsBetweenThreshold, alignmentFrequencyMinThreshold,
                                  tag=f'{minAlignments}')
print(f"Found {len(warningData)} alignments to check - min threshold {minAlignments}")

#############################

print(f"Testing all tWords {type_}")
minAlignments = 0
types = ['kt', 'other', 'names']
alignmentsForWord, filteredAlignmentsForWord0 = db.fetchAlignmentDataForAllTWordsCached(bibleType, types, minAlignments, remove)
print(f"Original Language Alignments: {len(filteredAlignmentsForWord)}")

warningData2 = db.generateWarnings(type_, bibleType, filteredAlignmentsForWord0, alignmentOrigWordsThreshold,
                                   alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                   targetWordsBetweenThreshold, alignmentFrequencyMinThreshold,
                                   tag=f'{minAlignments}')
print(f"Found {len(warningData2)} alignments to check - min threshold {minAlignments}")

#############################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'generated CSV with {len(warningData)} warnings, Elapsed time: {elapsed}')

# generated CSV with 1520 warnings, Elapsed time: 0:01:06



#%%


#%%

basePath = f'./data/{type_}_{bibleType}_NT_summary'
summary = db.getStatsForAlignments(filteredAlignmentsForWord0)
df = pd.DataFrame(summary)
csvPath = basePath + '.csv'
summary_ = db.saveDictOfDictToCSV(csvPath, df)
print(f"saved summary of {len(summary)} original words to {csvPath}")
summary_

