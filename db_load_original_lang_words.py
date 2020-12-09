# parse greek words into table
# Note: this was for testing and loads all words.  For better performance run `db_load_alignments.py` which only loads books that are alignmed

import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
original_words_table = db.original_words_table
target_words_table = db.target_words_table
dbPath = './data/alignmentsData.sqlite'

connection = db.initAlignmentDB(dbPath)

################################

db.resetTable(connection, original_words_table)

# read all greek words
start = time.time()
db.loadAllWordsFromTestamentIntoDB(connection, origLangPathGreek, 1, original_words_table)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Get NT original words, Elapsed time: {elapsed}')

items = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items)} items after reading testament")

# read all Hebrew words
start = time.time()
db.loadAllWordsFromTestamentIntoDB(connection, origLangPathHebrew, 0, original_words_table)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Get OT original words, Elapsed time: {elapsed}')

items = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items)} items after reading testament")

items = db.fetchRecords(connection, original_words_table, "book_id = 'tit'")
print (f"{len(items)} items in book")

# in bible we found 443108 total original language words
# Times on 2015 MBP 15":
# Get NT original words, Elapsed time: 0:00:16.487568
# Get OT original words, Elapsed time: 0:00:47.726208
