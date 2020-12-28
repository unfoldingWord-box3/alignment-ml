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

alignmentOrigWordsThreshold = 3
alignmentTargetWordsThreshold = 5
origWordsBetweenThreshold = 1
targetWordsBetweenThreshold = 1
alignmentFrequencyMinThreshold = 0.05
warningData = db.generateWarnings(type_, bibleType, filteredAlignmentsForWord, alignmentOrigWordsThreshold,
                                  alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                  targetWordsBetweenThreshold, alignmentFrequencyMinThreshold)
print(f"Found {len(warningData)} alignments to check")

#############################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'generated CSV with {len(warningData)} warnings, Elapsed time: {elapsed}')

# generated CSV with 1520 warnings, Elapsed time: 0:01:06
