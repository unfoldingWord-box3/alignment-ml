
import utils.bible_utils

userUrl = 'https://git.door43.org/lrsallee'
bibleType = 'en_ult'
testament = 1
outputFolder = './data'

utils.bible_utils.downloadTestamentAlignments(userUrl, bibleType, testament, outputFolder)