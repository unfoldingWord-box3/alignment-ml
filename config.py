# shared configuration file

import utils.db_utils as db
import utils.file_utils as file
import time
from datetime import timedelta
from pathlib import Path
import configs.config_ru as config_ru

home = str(Path.home())

############################################
# configure these values for your system
############################################

def getConfig():
    return config_ru.getConfig() # look in the config referenced in import for specific configuration

def getTwordsPath(type_, bibleType, testamentStr=''):
    cfg = getConfig()
    tWordsDataFolder = cfg['tWordsDataFolder']
    if not testamentStr:
        testamentStr = cfg['testamentStr']
    quotesPath = f'{tWordsDataFolder}/{type_}_{bibleType}_{testamentStr}_quotes.json'
    lemmasPath = f'{tWordsDataFolder}/{type_}_{bibleType}_{testamentStr}_lemmas.json'
    return quotesPath, lemmasPath

