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

connections = db.initAlignmentDB(dbPath)
connection = db.getConnectionForTable(connections, 'default')
connection_owi = db.getConnectionForTable(connections, db.original_words_index_table)

########################

connection = db.getConnectionForTable(connections, 'default')
# items_target = db.fetchRecords(connection, target_words_table, '')
# print (f"{len(items_target)} items in target_words_table")

# items_orig = db.fetchRecords(connection, original_words_table, '')
# print (f"{len(items_orig)} items in original_words_table")

connection_owi = db.getConnectionForTable(connections, original_words_index_table)
items_orig_idx = db.fetchRecords(connection_owi, original_words_index_table, '')
print (f"{len(items_orig_idx)} items in original_words_index_table")

items_align = db.fetchRecords(connection, alignment_table, '')
print (f"{len(items_align)} items in alignment_table")

# query = 'SELECT * FROM alignment_table\nWHERE orig_lang_words LIKE \'%"lemma": "βίβλος"%\''
query = 'SELECT * FROM original_words_index_table\nWHERE (lemma = "βίβλος")'
results = db.execute_read_query_dict(connection_owi, query)

word = 'βίβλος'
lemmaAlignments = db.findAlignmentsFromIndexDbForOrigWord(connection_owi, word, searchLemma=True, maxRows=None)
print(lemmaAlignments)

# word = 'βίβλος'
# lemmaAlignments = db.getDataFrameForOriginalWords(connection, [word], searchLemma = True)
# lemmaAlignments

def findAlignmentsForWord(connection_owi, word, minAlignments, searchLemma=False, maxRows=None):
    alignmentsByWord = db.findAlignmentsFromIndexDbForOrigWord(connection_owi, word, searchLemma, maxRows)
    alignmentsList, rejectedAlignmentsList = db.filterAlignments(alignmentsByWord, minAlignments)
    return alignmentsList

word = 'θεός'
minAlignments = 0
lemmaAlignments = findAlignmentsForWord(connection_owi, word, minAlignments, searchLemma=True)
print(f"Found {len(lemmaAlignments)} alignments")


