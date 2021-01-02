# load all the alignments in project format (i.e. topWords, bottomWords) into data folder

import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta
from config import getConfig

############################################
# get configuration
cfg = getConfig() # configure values in config.js
############################################

targetBibleType = cfg['targetBibleType']
origLangPath =  cfg['origLangPath']
targetLanguagePath = cfg['targetLanguagePath']
dbPath = cfg['dbPath']
newTestament = cfg['newTestament']
testamentStr = cfg['testamentStr']
projectsUrl = cfg['projectsUrl']
projectsFolder = './data/AlignmentsFromProjects'

############################################

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
original_words_index_table = db.original_words_index_table

########################

# move old sqlite
file.moveFile(f"{dbPath}.save", f"{dbPath}.save2", ifExists=True, overWrite=True)
file.moveFile(dbPath, f"{dbPath}.save", ifExists=True, overWrite=True)
dbPathOwIdx = db.getOrigLangIndexSqlPath(dbPath)
file.moveFile(f"{dbPathOwIdx}.save", f"{dbPathOwIdx}.save2", ifExists=True, overWrite=True)
file.moveFile(dbPathOwIdx, f"{dbPathOwIdx}.save", ifExists=True, overWrite=True)

connections = db.initAlignmentDB(dbPath)
connection = db.getConnectionForTable(connections, 'default')
connection_owi = db.getConnectionForTable(connections, db.original_words_index_table)

########################

# download  testament alignments into data
bible.downloadTestamentAlignments(projectsUrl, targetBibleType, newTestament, projectsFolder)

#################

# db.saveAlignmentsForBook(connection, bookId, projectsFolder, bibleType, origLangPathGreek)

#################

# # get alignments for OT (not working yet)
# start = time.time()
# db.getAlignmentsForTestament(connection, 0, dataFolder, bibleType)
# delta = (time.time() - start)
# elapsed = str(timedelta(seconds=delta))
# print(f'Get OT alignments, Elapsed time: {elapsed}')

# get alignments for NT
start = time.time()
db.getAlignmentsForTestament(connections, newTestament, projectsFolder, origLangPath, projectsFolder, targetBibleType, nestedFormat=True)
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
