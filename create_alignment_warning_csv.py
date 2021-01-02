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
targetLang = cfg['targetLang']
bibleType = cfg['targetBibleType']
trainingDataPath = cfg['trainingDataPath']
baseDataPath = cfg['baseDataPath']
testamentStr = cfg['testamentStr']
tWordsTypeList = cfg['tWordsTypeList']
dbPath = cfg.get('dbPath')
processAllAlignments = cfg.get('processAllAlignments', False)
processTWordsAlignments = cfg.get('processTWordsAlignments', True)
alignmentOrigWordsThreshold = cfg.get('alignmentOrigWordsThreshold', 3)
alignmentTargetWordsThreshold = cfg.get('alignmentTargetWordsThreshold', 5)
origWordsBetweenThreshold = cfg.get('origWordsBetweenThreshold', 1)
targetWordsBetweenThreshold = cfg.get('targetWordsBetweenThreshold', 1)
alignmentFrequencyMinThreshold = cfg.get('alignmentFrequencyMinThreshold', 8) # % of the max frequency of alignments for original word

#############################

start = time.time()

if processAllAlignments:

    ############################################

    print(f"\nTesting all alignments")

    minAlignments = 0
    remove = []

    connections = db.initAlignmentDB(dbPath)
    connection = db.getConnectionForTable(connections, 'default')
    connection_owi = db.getConnectionForTable(connections, db.original_words_index_table)

    #############################

    items_orig_idx = db.fetchRecords(connection_owi, db.original_words_index_table, '')
    print (f"{len(items_orig_idx)} items in original_words_index_table")

    alignmentsForWord = {}
    for origWordItem in items_orig_idx:
        orig_word = origWordItem['originalWord']
        if orig_word:
            if orig_word in alignmentsForWord:
                print(f"duplicate {orig_word} in database")
            else:
                alignmentsList, rejectedAlignmentsList = db.filterAlignments([origWordItem], minAlignments)
                alignmentsForWord[orig_word] = alignmentsList
        else:
            print(f"missing 'originalWord'' in alignment: {origWordItem}")

    # for orig_word in alignmentsForWord:
    #     length = len(alignmentsForWord[orig_word])
    #     if length > 1:
    #         print(f"Found {orig_word} length {length}")

    # filteredAlignmentsForWord = db.getFilteredAlignmentsForWord(alignmentsForWord, minAlignments, remove)

    #############################

    type = 'all_alignments'
    warningPath = f'{baseDataPath}/{type}_{bibleType}_{testamentStr}_warnings.json'
    warningData = db.generateWarnings(warningPath, type, bibleType, alignmentsForWord, alignmentOrigWordsThreshold,
                                      alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                      targetWordsBetweenThreshold, alignmentFrequencyMinThreshold,
                                      tag=f'{minAlignments}')
    print(f"Found {len(warningData)} alignments with warnings - min count threshold {minAlignments}")

    #############################

    basePath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_summary'
    summary = db.getStatsForAlignments(alignmentsForWord)
    df = pd.DataFrame(summary)
    csvPath = basePath + '.csv'
    summary_ = db.saveDictOfDictToCSV(csvPath, df)
    print(f"saved summary of {len(summary)} original words to {csvPath}")

    #############################

if processTWordsAlignments:

    #############################

    minAlignments = 0
    remove = ['ὁ']
    alignmentsForWord, filteredAlignmentsForWord = db.fetchAlignmentDataForTWordCached(trainingDataPath, type_, bibleType, minAlignments, remove)
    print(f"\nTesting tWords {type_} with minimum of {minAlignments} alignments")

    warningPath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_warnings.json'
    warningData = db.generateWarnings(warningPath, type_, bibleType, filteredAlignmentsForWord, alignmentOrigWordsThreshold,
                                      alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                      targetWordsBetweenThreshold, alignmentFrequencyMinThreshold,
                                      tag=f'{minAlignments}')
    print(f"Found {len(warningData)} alignments with warnings - min count threshold {minAlignments}")

    #############################

    basePath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_summary'
    summary = db.getStatsForAlignments(filteredAlignmentsForWord)
    df = pd.DataFrame(summary)
    csvPath = basePath + '.csv'
    summary_ = db.saveDictOfDictToCSV(csvPath, df)
    print(f"saved summary of {len(summary)} original words to {csvPath}")

    #############################

    print(f"\nTesting all tWords")
    type_ = 'all_twords'
    minAlignments = 0
    types = ['kt', 'other', 'names']
    alignmentsForWord, filteredAlignmentsForWord0 = db.fetchAlignmentDataForAllTWordsCached(trainingDataPath, bibleType, types, minAlignments, remove)
    print(f"Original Language Alignments: {len(filteredAlignmentsForWord)}")

    warningPath = f'{baseDataPath}/{type_}_{bibleType}_{testamentStr}_warnings.json'
    warningData2 = db.generateWarnings(warningPath, type_, bibleType, filteredAlignmentsForWord0, alignmentOrigWordsThreshold,
                                       alignmentTargetWordsThreshold, origWordsBetweenThreshold,
                                       targetWordsBetweenThreshold, alignmentFrequencyMinThreshold,
                                       tag=f'{minAlignments}')
    print(f"Found {len(warningData2)} alignments with warnings - min count threshold {minAlignments}")

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
print(f'Elapsed time: {elapsed}')

# generated CSV with 1823 warnings, Elapsed time: 0:00:08


