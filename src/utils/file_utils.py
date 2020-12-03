import requests

# %load_ext autoreload
# %autoreload 2

# https://git.door43.org/lrsallee/en_ust_2ti_book/raw/branch/master/.apps/translationCore/alignmentData/2ti/1.json

# userUrl = 'https://git.door43.org/lrsallee'
# bibleType = 'en_ult'
# bookId = '1ti'
# chapter = '1'


def fetchFile(url):
    print ('fetchFile ' + url)
    data = requests.get(url, allow_redirects=True)
    return data

def getBibleUrl(userUrl, bibleType, bookId, chapter):
    fullPath = userUrl + '/' + bibleType + '_' + bookId + '_book/raw/branch/master/.apps/translationCore/alignmentData/' + bookId + '/' + chapter + '.json'
    print ('getBibleUrl ' + fullPath)
    return fullPath

def fetchAlignments(userUrl, bibleType, bookId, chapter):
    url = getBibleUrl(userUrl, bibleType, bookId, chapter)
    data = fetchFile(url)
    return data

def downloadAlignments(userUrl, bibleType, bookId, chapter, outputPath):
    url = fetchAlignments(userUrl, bibleType, bookId, chapter)
    data = fetchFile(url)
    return data
