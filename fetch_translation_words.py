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

targetLang = cfg['targetLang']
targetBibleId = cfg['targetBibleId']
tWordsTargetPath = cfg['tWordsTargetPath']
tWordsTypeList = cfg['tWordsTypeList']
tWordsGreekPath = cfg['tWordsGreekPath']
dbPath = cfg['dbPath']
tWordsDataFolder = cfg['tWordsDataFolder']
testamentStr = cfg['testamentStr']
tWordsUseEnUlt = cfg.get('tWordsUseEnUlt', False)

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
            source = f'{enUltPath}/{type_}_en_ult_{testamentStr}_{ext}'
            dest = f'{tWordsDataFolder}/{type_}_{targetLang}_{targetBibleId}_{testamentStr}_{ext}'
            file.copyFile(source, dest, ifExists=False, overWrite=True)

else:

    ################################

    for type_ in tWordsTypeList:
        bible.saveTwordsQuotes(tWordsDataFolder, tWordsGreekPath, tWordsTargetPath, type_, bibleType, newTestament)

    ################################

    lexiconPath = cfg['greekLexiconPath']
    lemmas = []
    for type_ in tWordsTypeList:
        quotesPath, lemmasPath = config.getTwordsPath(type_, bibleType)
        lemmas_ = db.findLemmasForQuotes(connection, quotesPath, lemmasPath, lexiconPath)
        lemmas.append(lemmas_)

    type_ = 'all'
    quotesPath, lemmasPath = config.getTwordsPath(type_, bibleType)
    # merge all lemmas into element 0
    lemmaRoot = lemmas[0]
    for i in range(1,len(tWordsTypeList)):
        lemmas_ = lemmas[i]
        for lemma in lemmas_.keys():
            if lemma in lemmaRoot:
                lemmaRoot[lemma]['count'] += lemmas_[lemma]['count']
            else:
                lemmaRoot[lemma] = lemmas_[lemma]

    lemmas_ = db.sortDictByKey(lemmaRoot)
    file.writeJsonFile(lemmasPath, lemmas_)
    db.saveDictOfDictToCSV(lemmasPath.replace(".json", ".csv"), lemmas_, keyName ='lemma')

################################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Getting tWords quotes from {testamentStr}, Elapsed time: {elapsed}')

# Getting tWords quotes from NT, Elapsed time: 0:01:27

