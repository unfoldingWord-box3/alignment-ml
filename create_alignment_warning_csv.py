# Creating CSV of alignment warnings

import json
import csv
import time
from datetime import timedelta
import pandas as pd
import utils.db_utils as db
import utils.file_utils as file

targetLang = 'en'
bibleType = 'en_ult'
dbPath = f'./data/{bibleType}_alignments.sqlite'

connection = db.initAlignmentDB(dbPath)

#############################

start = time.time()
minAlignments = 100
termsPath = f'./data/kt_{bibleType}_NT_lemmas.json'
remove = ['ὁ']
lemmasList = db.getFilteredLemmas(termsPath, minAlignments, remove)

# find all alignments for this lemma

alignmentsForWord = db.getAlignmentsForOriginalWords(connection, lemmasList, searchLemma = True)

remove = ['ὁ']
filteredAlignmentsForWord = db.getFilteredAlignmentsForWord(alignmentsForWord, minAlignments, remove)

#############################

alignmentOrigWordsThreshold = 3
alignmentTargetWordsThreshold = 5
origWordsBetweenThreshold = 1
targetWordsBetweenThreshold = 1
alignmentsToCheck = []

for origWord in alignmentsForWord.keys():
    alignments = alignmentsForWord[origWord]
    for alignment in alignments:
        warnings = []

        alignmentOrigWords = alignment['alignmentOrigWords']
        if alignmentOrigWords >= alignmentOrigWordsThreshold:
            warnings.append(f"Too many original language words in alignment: {alignmentOrigWords}, threshold {alignmentOrigWordsThreshold}")

        alignmentTargetWords = alignment['alignmentTargetWords']
        if alignmentTargetWords >= alignmentTargetWordsThreshold:
            warnings.append(f"Too many target language words in alignment: {alignmentTargetWords}, threshold {alignmentTargetWordsThreshold}")

        origWordsBetween = alignment['origWordsBetween']
        if origWordsBetween >= origWordsBetweenThreshold:
            warnings.append(f"Discontiguous original language alignment, extra words: {origWordsBetween}, threshold {origWordsBetweenThreshold}")

        targetWordsBetween = alignment['targetWordsBetween']
        if targetWordsBetween >= targetWordsBetweenThreshold:
            warnings.append(f"Discontiguous target language alignment, extra words: {targetWordsBetween}, threshold {targetWordsBetweenThreshold}")

        if len(warnings):
            alignment['warnings'] = json.dumps(warnings, ensure_ascii = False)
            alignmentsToCheck.append(alignment)

basePath = f'./data/kt_{bibleType}_NT_warnings'
jsonPath = basePath + '.json'
file.writeJsonFile(jsonPath, alignmentsToCheck)

df = pd.DataFrame(alignmentsToCheck)
csvPath = basePath + '.csv'
warningData = df.drop(columns=["id", "origSpan", "targetSpan"]).sort_values(by=["book_id", "chapter", "verse", "alignment_num"])
warningData.to_csv(path_or_buf=csvPath, index=False, header=True, quoting=csv.QUOTE_NONNUMERIC)

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'generated CSV with {len(alignmentsToCheck)} warnings, Elapsed time: {elapsed}')

# generated CSV with 1520 warnings, Elapsed time: 0:01:06
