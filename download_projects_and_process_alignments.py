import time
from datetime import timedelta
from config import getConfig

############################################
# get configuration
cfg = getConfig() # configure values in config.js

import utils.system_utils as system
from config import getConfig

############################################
# get configuration
cfg = getConfig() # configure values in config.js
############################################

resourceBasePath = cfg['resourceBasePath'].replace('./', '../')
origLangResourceUrl = cfg['origLangResourceUrl']
origLangId = cfg['origLangId']
origLangBibleId = cfg['origLangBibleId']
origLangVersion = cfg['origLangVersion']
targetBibleLangResourceUrl = cfg['targetBibleLangResourceUrl']
targetLang = cfg['targetLang']
targetBibleId = cfg['targetBibleId']
targetLangBibleVersion = cfg['targetLangBibleVersion']
targetTWordsLangResourceUrl = cfg['targetTWordsLangResourceUrl']
tWordsId = cfg['tWordsId']
targetLangTWordsVersion = cfg['targetLangTWordsVersion']
tWordsResourceName = cfg['tWordsResourceName']

system.printSystemInfo()
start = time.time()

############################################
# download resources

# download original language bible and tW
print(f"Saving resources to {resourceBasePath}")
system.downloadAndProcessResource(cfg, origLangResourceUrl, resourceBasePath, origLangId, origLangBibleId, origLangVersion, origLangBibleId)
system.downloadAndProcessResource(cfg, targetTWordsLangResourceUrl, resourceBasePath, targetLang, tWordsId, targetLangTWordsVersion, tWordsResourceName)

############################################

print("extract alignments:")
import db_load_alignments_from_projects

print("get original language words for tWords:")
import fetch_translation_words

print("generate ML training data:")
import fetch_alignment_training_data

print("generate warnings reports:")
import create_alignment_warning_csv

############################################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Parse alignments, total elapsed time: {elapsed}')