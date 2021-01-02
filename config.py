# shared configuration file

import utils.db_utils as db
import utils.file_utils as file
import time
from datetime import timedelta
from pathlib import Path

# uncomment the source you want to use:

import configs.config_ru as config_ # ru from ru_tw
# import configs.config_en_unfoldingword as config_ # en from unfoldingWord
# import configs.config_en_catalog as config_ # en from Door43 catalog: cdn.door43.org
# import configs.config_hi_str as config_ # hi STR

home = str(Path.home())

############################################
# configure these values for your system
############################################

def getConfig():
    return config_.getConfig() # look in the config referenced in import for specific configuration

def getTwordsPath(type_, bibleType, testamentStr=''):
    cfg = getConfig()
    tWordsDataFolder = cfg['tWordsDataFolder']
    if not testamentStr:
        testamentStr = cfg['testamentStr']
    quotesPath = f'{tWordsDataFolder}/{type_}_{bibleType}_{testamentStr}_quotes.json'
    lemmasPath = f'{tWordsDataFolder}/{type_}_{bibleType}_{testamentStr}_lemmas.json'
    return quotesPath, lemmasPath

