# save

import utils.db_utils as db
import utils.file_utils as file
import time
from datetime import timedelta
import config

############################################
# get configuration
cfg = config.getConfig() # configure values in config.js
############################################

minAlignments = 40
targetLang = cfg['targetLang']
bibleType = cfg['targetBibleType']
tWordsTypeList = cfg['tWordsTypeList']
dbPath = cfg['dbPath']
trainingDataPath = cfg['trainingDataPath']
testamentStr = cfg['testamentStr']

connections = db.initAlignmentDB(dbPath)
connection = db.getConnectionForTable(connections, 'default')
connection_owi = db.getConnectionForTable(connections, db.original_words_index_table)

################################

start = time.time()
for type_ in tWordsTypeList:
    db.saveAlignmentDataForLemmas(connection_owi, type_, cfg, config.getTwordsPath, minAlignments)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'fetch alignments for tW lemmas, Elapsed time: {elapsed}')

# fetch alignments for lemmas, Elapsed time: 0:00:22