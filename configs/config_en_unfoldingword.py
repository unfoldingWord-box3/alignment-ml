# shared configuration file

import utils.db_utils as db
import utils.file_utils as file
import time
from datetime import timedelta
from pathlib import Path

home = str(Path.home())

############################################
# configure these values for your system
############################################

def getConfig():
    newTestament = True
    testamentStr = "NT" if newTestament else "OT"
    targetLang = "en"
    targetBibleId = "ult"
    tWordsId = "tw"
    tWordsResourceName = 'bible'
    origLangVersionGreek = '0.16'
    origLangVersionHebrew = '2.1.16'
    targetLangBibleVersion = '18'
    targetLangTWordsVersion = '19'
    origLangIdGreek = 'el-x-koine'
    origLangIdHebrew = "hbo"
    origLangId = origLangIdGreek if newTestament else origLangIdHebrew
    origLangBibleIdGreek = 'ugnt'
    origLangBibleIdHebrew = "uhb"
    origLangBibleId = origLangBibleIdGreek if newTestament else origLangBibleIdHebrew
    origLangVersion = origLangVersionGreek if newTestament else origLangVersionHebrew
    targetBibleType = f'{targetLang}_{targetBibleId}'
    tWordsTypeList = ['kt', 'names', 'other'] # categories of tWords
    processTWordsAlignments = True
    processAllAlignments = True

    origLangResourceUrl = 'https://git.door43.org/unfoldingWord/el-x-koine_ugnt/archive/master.zip'
    targetBibleLangResourceUrl = 'https://git.door43.org/unfoldingWord/en_ult/archive/master.zip'
    targetTWordsLangResourceUrl = 'https://git.door43.org/unfoldingWord/en_tw/archive/master.zip'
    projectsUrl = 'https://git.door43.org/lrsallee'

    resourceBasePath = './resources'
    baseDataPath = f'./data/{targetLang}/{targetBibleId}'
    tWordsDataFolder = f'./data/{targetLang}/{targetBibleId}/tWords'
    trainingDataPath = f'./data/{targetLang}/{targetBibleId}/TrainingData'
    dbPath = f'{baseDataPath}/alignments_{testamentStr}.sqlite'

    origLangPathGreek =  f'{resourceBasePath}/{origLangIdGreek}/bibles/{origLangBibleIdGreek}/v{origLangVersionGreek}'
    origLangPathHebrew = f'{resourceBasePath}/{origLangIdHebrew}/bibles/{origLangBibleIdHebrew}/v{origLangVersionHebrew}'
    tWordsGreekPath = f'{resourceBasePath}/{origLangIdGreek}/translationHelps/translationWords/v{origLangVersionGreek}'
    targetLanguagePath = f'{resourceBasePath}/{targetLang}/bibles/{targetBibleId}/v{targetLangBibleVersion}'
    tWordsTargetPath = f'{resourceBasePath}/{targetLang}/translationHelps/translationWords/v{targetLangTWordsVersion}'
    greekLexiconPath = f'{home}/translationCore/resources/{targetLang}/lexicons/ugl/v0/content'
    origLangPath = origLangPathGreek if newTestament else origLangPathHebrew

    baseLangResourceUrl = 'https://cdn.door43.org'

    file.ensureFolderExists(resourceBasePath)
    file.ensureFolderExists(baseDataPath)
    file.ensureFolderExists(tWordsDataFolder)
    file.ensureFolderExists(trainingDataPath)

    cfg = {
        'newTestament': newTestament,
        'testamentStr': testamentStr,
        'targetBibleType': targetBibleType,
        'resourceBasePath': resourceBasePath,
        'baseDataPath': baseDataPath,
        'origLangPathGreek': origLangPathGreek,
        'origLangPathHebrew': origLangPathHebrew,
        'targetLanguagePath': targetLanguagePath,
        'dbPath': dbPath,
        'targetLang': targetLang,
        'targetBibleId': targetBibleId,
        'tWordsTargetPath': tWordsTargetPath,
        'tWordsTypeList': tWordsTypeList,
        'tWordsGreekPath': tWordsGreekPath,
        'tWordsDataFolder': tWordsDataFolder,
        'greekLexiconPath': greekLexiconPath,
        'trainingDataPath': trainingDataPath,
        'origLangResourceUrl': origLangResourceUrl,
        'targetBibleLangResourceUrl': targetBibleLangResourceUrl,
        'targetTWordsLangResourceUrl': targetTWordsLangResourceUrl,
        'baseLangResourceUrl': baseLangResourceUrl,
        'origLangId': origLangId,
        'origLangBibleId': origLangBibleId,
        'origLangVersionGreek': origLangVersionGreek,
        'origLangVersionHebrew': origLangVersionHebrew,
        'origLangVersion': origLangVersion,
        'targetLangBibleVersion': targetLangBibleVersion,
        'targetLangTWordsVersion': targetLangTWordsVersion,
        'tWordsId': tWordsId,
        'tWordsResourceName': tWordsResourceName,
        'projectsUrl': projectsUrl,
        'origLangPath': origLangPath,
        'processAllAlignments': processAllAlignments,
        'processTWordsAlignments': processTWordsAlignments
    }
    return cfg

def getTwordsPath(type_, bibleType, testamentStr=''):
    cfg = getConfig()
    tWordsDataFolder = cfg['tWordsDataFolder']
    if not testamentStr:
        testamentStr = cfg['testamentStr']
    quotesPath = f'{tWordsDataFolder}/{type_}_{bibleType}_{testamentStr}_quotes.json'
    lemmasPath = f'{tWordsDataFolder}/{type_}_{bibleType}_{testamentStr}_lemmas.json'
    return quotesPath, lemmasPath

