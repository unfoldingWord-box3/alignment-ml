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
dbPath = './data/alignmentsData.sqlite'
keyTermsPath = 'data/keyTerms.json'
alignmentTrainingDataPath = './data/TrainingData'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'
targetLang = 'en'
tWordsTargetPath = f'/Users/blm/translationCore/resources/{targetLang}/translationHelps/translationWords/v16'
tWordsTypeList = ['kt', 'names', 'others']
tWordsGreekPath = '/Users/blm/translationCore/resources/el-x-koine/translationHelps/translationWords/v0.14'

# connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/AlignmentsFromProjects'
bookId = 'tit'

###########################

# tWordsType = 'kt'
# bible.getTwordsQuotes(tWordsGreekPath, tWordsTargetPath, tWordsType)
#
#
# word = 'apostle'
# tWordsPath = f"{tWordsGreekPath}/{tWordsType}/groups/{bookId}"
# tWordPath = f"{tWordsPath}/{word}.json"

# fileList_ = file.listFolder(tWordsPath)
# fileList = list(filter(lambda word: (word.find('.json') >= 0), fileList_))
# fileList.sort()


tWordsTypes = ['kt', 'names', 'other']
newTestament = True
outputFolder = './data'
for type_ in tWordsTypes:
    bible.saveTwordsQuotes(outputFolder, tWordsGreekPath, tWordsTargetPath, type_, targetLang, newTestament)

