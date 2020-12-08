# download all the en ult new testament alignments into data

import utils.bible_utils as bible

userUrl = 'https://git.door43.org/lrsallee'
bibleType = 'en_ult'
outputFolder = './data/Alignments'

# download new testament alignments into data
bible.downloadTestamentAlignments(userUrl, bibleType, 1, outputFolder)

# download old testament alignments into data
bible.downloadTestamentAlignments(userUrl, bibleType, 0, outputFolder)
