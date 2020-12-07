# download all the en ult new testament alignments into data

import utils.bible_utils as bu

userUrl = 'https://git.door43.org/lrsallee'
bibleType = 'en_ult'
testament = 1
outputFolder = './data'

# download testament alignments into data
bu.downloadTestamentAlignments(userUrl, bibleType, testament, outputFolder)
