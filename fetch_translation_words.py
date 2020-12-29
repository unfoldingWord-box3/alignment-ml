# search alignments

import utils.db_utils as db
import utils.bible_utils as bible
import time
from datetime import timedelta
from pathlib import Path

############################################
# configure these values for your system
############################################

targetLang = 'en'
bibleType = 'en_ult'
newTestament = True
home = str(Path.home())
tWordsTargetPath = f'{home}/translationCore/resources/{targetLang}/translationHelps/translationWords/v19'
tWordsTypeList = ['kt', 'names', 'other'] # categories of tWords
tWordsGreekPath = f'{home}/translationCore/resources/el-x-koine/translationHelps/translationWords/v0.16'
dbPath = f'./data/{bibleType}_NT_alignments.sqlite'

connections = db.initAlignmentDB(dbPath)
connection = db.getConnectionForTable(connections, 'default')
connection_owi = db.getConnectionForTable(connections, db.original_words_index_table)

start = time.time()

################################

outputFolder = './data/tWords'
for type_ in tWordsTypeList:
    bible.saveTwordsQuotes(outputFolder, tWordsGreekPath, tWordsTargetPath, type_, bibleType, newTestament)

################################

lexiconPath = f'{home}/translationCore/resources/en/lexicons/ugl/v0/content'
for type_ in tWordsTypeList:
    quotesPath = f'./data/tWords/{type_}_{bibleType}_NT_quotes.json'
    lemmasPath = f'./data/tWords/{type_}_{bibleType}_NT_lemmas'
    db.findLemmasForQuotes(connection, quotesPath, lemmasPath, lexiconPath)

################################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Getting tWords quotes from NT, Elapsed time: {elapsed}')

# Getting tWords quotes from NT, Elapsed time: 0:01:27

