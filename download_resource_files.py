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

############################################
# download resources

# download original language bible and tW
print(f"Saving resources to {resourceBasePath}")
system.downloadAndProcessResource(origLangResourceUrl, resourceBasePath, origLangId, origLangBibleId, origLangVersion, origLangBibleId)
system.downloadAndProcessResource(targetBibleLangResourceUrl, resourceBasePath, targetLang, targetBibleId, targetLangBibleVersion, targetBibleId)
# https://cdn.door43.org ../resources en tw 19 bible
system.downloadAndProcessResource(targetTWordsLangResourceUrl, resourceBasePath, targetLang, tWordsId, targetLangTWordsVersion, tWordsResourceName)
