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
dbPath = f'./data/{bibleType}_alignments.sqlite'

connection = db.initAlignmentDB(dbPath)

################################

outputFolder = './data'
start = time.time()
for type_ in tWordsTypeList:
    bible.saveTwordsQuotes(outputFolder, tWordsGreekPath, tWordsTargetPath, type_, targetLang, newTestament)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Save tWords quotes from NT, Elapsed time: {elapsed}')

################################

for type_ in tWordsTypeList:
    quotesPath = f'./data/{type_}_en_NT_quotes.json'
    lemmasPath = f'./data/{type_}_en_NT_lemmas.json'
    start = time.time()
    db.findLemmasForQuotes(connection, quotesPath, lemmasPath)
    delta = (time.time() - start)
    elapsed = str(timedelta(seconds=delta))
    print(f'Found lemmas for tWords "{type_}" in NT, Elapsed time: {elapsed}')


