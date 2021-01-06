# load all the alignments in resource format (i.e. zaln) into data folder

import utils.db_utils as db
import utils.file_utils as file
import time
from datetime import timedelta
from pathlib import Path
from config import getConfig

############################################
# get configuration
cfg = getConfig() # configure values in config.js
############################################

targetBibleType = cfg['targetBibleType']
home = str(Path.home())

origLangPathGreek =  cfg['origLangPathGreek']
origLangPathHebrew = cfg['origLangPathHebrew']
targetLanguagePath = cfg['targetLanguagePath']
dbPath = cfg['dbPath']
testamentStr = cfg['testamentStr']
baseDataPath = cfg['baseDataPath']


############################################

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
original_words_index_table = db.original_words_index_table

# items = db.fetchRecords(connection, original_words_index_table, '')
# print (f"{len(items)} items after reading testament")

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

# get alignments for testament
start = time.time()
origWordAlignmentsPath = f'{baseDataPath}/originalWordAlignments.json'
alignmentsIndex = db.getAlignmentsForTestament(connections, 1, targetLanguagePath, origLangPathGreek, targetLanguagePath, targetBibleType, nestedFormat=True)
file.writeJsonFile(origWordAlignmentsPath, alignmentsIndex)
print(f"Saved original words alignments to {origWordAlignmentsPath}")
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Get {testamentStr} alignments, Elapsed time: {elapsed}')
print(f"Size of alignments database {dbPath} is {file.getFileSize(dbPath)/1000/1000:.3f} MB")
print(f"Size of original words index database {dbPathOwIdx} is {file.getFileSize(dbPathOwIdx)/1000/1000:.3f} MB")

########################

connection = db.getConnectionForTable(connections, 'default')
items_target = db.fetchRecords(connection, target_words_table, '')
print (f"{len(items_target)} items in target_words_table")

items_orig = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items_orig)} items in original_words_table")

connection_owi = db.getConnectionForTable(connections, original_words_index_table)
items_orig_idx = db.fetchRecords(connection_owi, original_words_index_table, '')
print (f"{len(items_orig_idx)} items in original_words_index_table")

items_align = db.fetchRecords(connection, alignment_table, '')
print (f"{len(items_align)} items in alignment_table")

# now see with updated db:
# 183353 items in target_words_table
# 130177 items in alignment_table
# 137962 items in original_words_table

# Get NT alignments - deleting sqlite DB first
# Get NT alignments, Elapsed time: 0:22:41
# on Dell Laptop: Elapsed time: 0:46:33
# on 2015 13" MBP: Elapsed time: 0:44:34.438381


