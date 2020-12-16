# search alignments

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
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'
targetLang = 'en'
tWordsTargetPath = f'/Users/blm/translationCore/resources/{targetLang}/translationHelps/translationWords/v16'
tWordsList = ['kt', 'names', 'others']
tWordsGreekPath = '/Users/blm/translationCore/resources/el-x-koine/translationHelps/translationWords/v0.14'

connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/AlignmentsFromProjects'
bookId = 'tit'

searchOriginal = True
searchTarget = False
searchLemma = True
caseInsensitive = True

###########################



###########################

# this command will update all the current entries in keyTermsPath
start = time.time()
db.refreshSavedAlignmentData(connection, keyTermsPath, minLen=3)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'refreshed saved alignments, Elapsed time: {elapsed}')
