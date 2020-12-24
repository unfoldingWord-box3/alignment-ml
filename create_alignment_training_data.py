
# search alignments

import json
import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

bibleType = 'en_ult'
original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = f'./data/{bibleType}_NT_alignments.sqlite'
keyTermsPath = 'data/keyTerms.json'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

connection = db.initAlignmentDB(dbPath)

testament = 1
dataFolder = './data/AlignmentsFromProjects'
bookId = 'tit'

searchOriginal = True
searchTarget = False
searchLemma = True
caseInsensitive = True

################################

# this command will update all the current entries in keyTermsPath
start = time.time()
termsPath = f'./data/kt_{bibleType}_ult_NT_quotes.json'
# db.saveAlignmentDataForLemmas(connection, termsPath)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'refreshed saved alignments, Elapsed time: {elapsed}')

# on m1 in rosetta: refreshed saved alignments, Elapsed time: 0:26:09.985418

################################

# wordList = 'angel angels archangel'
# unique = db.saveUniqueLemmasAlignedWithTargetWords(connection, keyTermsPath, wordList)
# unique

################################

# words = list(unique.keys())
# db.saveAlignmentDataForWords(connection, wordList, words, searchOriginal = True, searchLemma = True, caseInsensitive = True)




