# search alignments

import os
import json
import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = './data/en_ult_alignments.sqlite'
keyTermsPath = 'data/keyTerms.json'
alignmentTrainingDataPath = './data/TrainingData'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'
targetLang = 'en'
tWordsTargetPath = f'/Users/blm/translationCore/resources/{targetLang}/translationHelps/translationWords/v16'
tWordsTypeList = ['kt', 'names', 'others']
tWordsGreekPath = '/Users/blm/translationCore/resources/el-x-koine/translationHelps/translationWords/v0.14'

connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/AlignmentsFromProjects'
bookId = 'tit'

################################

tWordsTypes = ['kt', 'names', 'other']
newTestament = True
outputFolder = './data'
start = time.time()
for type_ in tWordsTypes:
    bible.saveTwordsQuotes(outputFolder, tWordsGreekPath, tWordsTargetPath, type_, targetLang, newTestament)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Save tWords quotes from NT, Elapsed time: {elapsed}')

################################

quotesPath = './data/kt_en_NT_quotes.json'
lemmasPath = './data/kt_en_NT_lemmas.json'
start = time.time()
db.findLemmasForQuotes(connection, quotesPath, lemmasPath)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Found lemmas for tWords in NT, Elapsed time: {elapsed}')


