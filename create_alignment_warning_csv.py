### Plotting alignment data

#%%

import json
import csv
import pandas as pd
import utils.db_utils as db
import utils.file_utils as file

targetLang = 'en'
bibleType = 'en_ult'
dbPath = f'./data/{bibleType}_alignments.sqlite'

connection = db.initAlignmentDB(dbPath)

#############################

minAlignments = 100
termsPath = './data/kt_en_NT_lemmas.json'
remove = ['ὁ']
lemmasList = db.getFilteredLemmas(termsPath, minAlignments, remove)
#%%

# find all alignments for this lemma

alignmentsForWord = db.getAlignmentsForOriginalWords(connection, lemmasList, searchLemma = True)
#%%
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

basePath = './data/kt_en_NT_warnings'
jsonPath = basePath + '.json'
file.writeJsonFile(jsonPath, alignmentsToCheck)

df = pd.DataFrame(alignmentsToCheck)
csvPath = basePath + '.csv'
warningData = df.drop(columns=["id", "origSpan", "targetSpan"]).sort_values(by=["book_id", "chapter", "verse", "alignment_num"])
warningData.to_csv(path_or_buf=csvPath, index=False, header=True, quoting=csv.QUOTE_NONNUMERIC)
