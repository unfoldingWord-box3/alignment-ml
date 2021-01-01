# search alignments

import utils.db_utils as db
import utils.bible_utils as bible
import utils.file_utils as file
import time
from datetime import timedelta
import config

############################################
# get configuration
cfg = config.getConfig() # configure values in config.js
############################################

targetLang = cfg['targetLang']
bibleType = cfg['targetBibleType']
newTestament = cfg['newTestament']

tWordsTargetPath = cfg['tWordsTargetPath']
tWordsTypeList = cfg['tWordsTypeList']
tWordsGreekPath = cfg['tWordsGreekPath']
dbPath = cfg['dbPath']
tWordsDataFolder = cfg['tWordsDataFolder']
testamentStr = cfg['testamentStr']
tWordsUseEnUlt = cfg['tWordsUseEnUlt'] if 'tWordsUseEnUlt' in cfg else False

connections = db.initAlignmentDB(dbPath)
connection = db.getConnectionForTable(connections, 'default')
connection_owi = db.getConnectionForTable(connections, db.original_words_index_table)

start = time.time()

################################

if tWordsUseEnUlt:
    print(f"Using tword quotes from en_ult")
    enUltPath = './data/en/ult/tWords'
    for type_ in tWordsTypeList:
        for ext in ['lemmas.csv', 'lemmas.json', 'quotes.json']:
            source = f'{enUltPath}/{type_}_en_ult_NT_{ext}'
            dest = f'{tWordsDataFolder}/{type_}_ru_rlob_NT_{ext}'
            file.copyFile(source, dest, ifExists=False, overWrite=True)

else:

    ################################

    for type_ in tWordsTypeList:
        bible.saveTwordsQuotes(tWordsDataFolder, tWordsGreekPath, tWordsTargetPath, type_, bibleType, newTestament)

    ################################

    lexiconPath = cfg['greekLexiconPath']
    for type_ in tWordsTypeList:
        quotesPath, lemmasPath = config.getTwordsPath(type_, bibleType)
        db.findLemmasForQuotes(connection, quotesPath, lemmasPath, lexiconPath)

    ################################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Getting tWords quotes from {testamentStr}, Elapsed time: {elapsed}')

# Getting tWords quotes from NT, Elapsed time: 0:01:27

