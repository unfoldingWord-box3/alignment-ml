# parse en ult words into table

import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

targetLangPathEn = './data/TargetLangJson/ult/v14'
target_words_table = db.target_words_table
dbPath = './data/alignmentsData.sqlite'

connection = db.initAlignmentDB(dbPath)

#############################

# completely clear old data
db.resetTable(connection, target_words_table)

# read all words
start = time.time()
db.loadAllWordsFromTestamentIntoDB(connection, targetLangPathEn, 1, target_words_table)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Get NT target words, Elapsed time: {elapsed}')

items = db.fetchRecords(connection, target_words_table, '')
print (f"{len(items)} items after reading testament")

# read all Hebrew words
# start = time.time()
# db.loadAllWordsFromTestamentIntoDB(connection, targetLangPathEn, 0, target_words_table)
# delta = (time.time() - start)
# elapsed = str(timedelta(seconds=delta))
# print(f'Get OT target words, Elapsed time: {elapsed}')
#
# items = db.fetchRecords(connection, target_words_table, '')
# print (f"{len(items)} items after reading testament")

items = db.fetchRecords(connection, target_words_table, "book_id = 'tit'")
print (f"{len(items)} items in book")

# 184166 items after reading testament
# Times on 2015 MBP 15":
# Get NT target words, Elapsed time: 0:00:19.498876
# Get OT target words, Elapsed time:
