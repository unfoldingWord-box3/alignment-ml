# Creating CSV of alignment warnings

import json
import csv
import time
from datetime import timedelta
import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import config

############################################
# get configuration
cfg = config.getConfig() # configure values in config.js
############################################

type_ = 'kt'
bibleType = cfg['targetBibleType']
trainingDataPath = cfg['trainingDataPath']
baseDataPath = cfg['baseDataPath']
testamentStr = cfg['testamentStr']

#############################

start = time.time()
minAlignments = 0
remove = ['ὁ']
alignmentsForWord, filteredAlignmentsForWord = db.fetchAlignmentDataForTWordCached(trainingDataPath, type_, bibleType, minAlignments, remove)

#############################

print(f"Testing tWords {type_} with minimum of {minAlignments} alignments")

alignmentOrigWordsThreshold = 3
alignmentTargetWordsThreshold = 5
origWordsBetweenThreshold = 1
targetWordsBetweenThreshold = 1
alignmentFrequencyMinThreshold = 5
warningPath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_warnings.json'
warningData = db.generateWarnings(warningPath, type_, bibleType, filteredAlignmentsForWord, alignmentOrigWordsThreshold,
                                  alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                  targetWordsBetweenThreshold, alignmentFrequencyMinThreshold,
                                  tag=f'{minAlignments}')
print(f"Found {len(warningData)} alignments to check - min threshold {minAlignments}")

#############################

basePath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_summary'
summary = db.getStatsForAlignments(filteredAlignmentsForWord)
df = pd.DataFrame(summary)
csvPath = basePath + '.csv'
summary_ = db.saveDictOfDictToCSV(csvPath, df)
print(f"saved summary of {len(summary)} original words to {csvPath}")

#############################

print(f"Testing all tWords {type_}")
type_ = 'all'
minAlignments = 0
types = ['kt', 'other', 'names']
alignmentsForWord, filteredAlignmentsForWord0 = db.fetchAlignmentDataForAllTWordsCached(trainingDataPath, bibleType, types, minAlignments, remove)
print(f"Original Language Alignments: {len(filteredAlignmentsForWord)}")

warningPath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_warnings.json'
warningData2 = db.generateWarnings(warningPath, type_, bibleType, filteredAlignmentsForWord0, alignmentOrigWordsThreshold,
                                   alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                   targetWordsBetweenThreshold, alignmentFrequencyMinThreshold,
                                   tag=f'{minAlignments}')
print(f"Found {len(warningData2)} alignments to check - min threshold {minAlignments}")

#############################

type_ = 'all'
basePath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_summary'
summary = db.getStatsForAlignments(filteredAlignmentsForWord0)
df = pd.DataFrame(summary)
csvPath = basePath + '.csv'
summary_ = db.saveDictOfDictToCSV(csvPath, df)
print(f"saved summary of {len(summary)} original words to {csvPath}")

#############################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'generated CSV with {len(warningData)} warnings, Elapsed time: {elapsed}')

# generated CSV with 1823 warnings, Elapsed time: 0:00:08


