# load all the alignments in project format (i.e. topWords, bottomWords) into data folder

import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = './data/en_ult_NT_alignments.sqlite'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

connections = db.initAlignmentDB(dbPath)
connection = db.getConnectionForTable(connections, 'default')
connection_owi = db.getConnectionForTable(connections, db.original_words_index_table)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/AlignmentsFromProjects'
bookId = 'tit'

# chapter = '1'
# verse = '4'
# word = 'καὶ'
# occurrence = 2

# # get reference for word
# items = db.fetchWordsForVerse(connection, original_words_table, bookId, chapter, verse)
# print (f"{len(items)} words found in verse")
#
# # get reference for word
# items = db.fetchForWordInVerse(connection, original_words_table, word, occurrence, bookId, chapter, verse)
# print (f"{len(items)} matching words found")

#################

db.saveAlignmentsForBook(connection, bookId, dataFolder, bibleType, origLangPathGreek)

#################

# completely clear old data
db.resetTable(connection, target_words_table)
db.resetTable(connection, original_words_table)
db.resetTable(connection, alignment_table)

# # get alignments for OT (not working yet)
# start = time.time()
# db.getAlignmentsForTestament(connection, 0, dataFolder, bibleType)
# delta = (time.time() - start)
# elapsed = str(timedelta(seconds=delta))
# print(f'Get OT alignments, Elapsed time: {elapsed}')

# get alignments for NT
start = time.time()
db.getAlignmentsForTestament(connection, 1, dataFolder, bibleType)
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

# 69050 items in target_words_table
# 48892 items in alignment_table
# 52996 items in original_words_table

# Times on 2015 MBP 15":
# Get NT alignments, Elapsed time: 0:38:44.645573
