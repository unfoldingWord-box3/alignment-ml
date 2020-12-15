# load all the alignments in resource format (i.e. zaln) into data folder

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
keyTermsPath = './data/keyTerms.json'
alignmentTrainingDataPath = './data/alignmentTrainingData.json'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/TargetLangJson/en/ult/v14'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

searchOriginal = True
searchTarget = False
searchLemma = True
caseInsensitive = True

########################

# filePath = dataFolder + '/luk/1.json'
# luke_1 = file.readJsonFile(filePath)
# luk_1_5_align = luke_1['5']

# target_words, alignments = db.getAlignmentsFromVerse(luk_1_5_align['verseObjects'])

# target_words = db.saveAlignmentsForBook(connection, 'mat', dataFolder, 'ult', origLangPathGreek, nestedFormat=True)

#################

# completely clear old data
db.resetTable(connection, target_words_table)
db.resetTable(connection, original_words_table)
db.resetTable(connection, alignment_table)

########################

# get alignments for NT
start = time.time()
db.getAlignmentsForTestament(connection, 1, dataFolder, bibleType, nestedFormat=True)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Get NT alignments, Elapsed time: {elapsed}')

########################

items_target = db.fetchRecords(connection, target_words_table, '')
print (f"{len(items_target)} items in target_words_table")

items_align = db.fetchRecords(connection, alignment_table, '')
print (f"{len(items_align)} items in alignment_table")

items_orig = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items_orig)} items in original_words_table")

# see:
# 45996 items in target_words_table
# 31219 items in alignment_table
# 357007 items in original_words_table

# now see with updated db:
# 184166 items in target_words_table
# 130137 items in alignment_table
# 443108 items in original_words_table

# Times on 2015 MBP 15":
# Get NT alignments, Elapsed time: 0:38:44.645573

