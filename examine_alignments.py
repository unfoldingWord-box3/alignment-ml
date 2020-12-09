
# search alignments

import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = './data/alignmentsData.sqlite'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/Alignments'
bookId = 'tit'

searchOriginal = True
searchTarget = False
searchLemma = True
caseInsensitive = True

########################

# find exact word in original language
godAlignments = db.findAlignmentsForWord(connection, 'Θεοῦ', searchOriginal)
frequency = godAlignments['alignmentTxt'].value_counts()

# find all forms of word in original language by lemma
godAlignments = db.findAlignmentsForWord(connection, 'θεός', searchOriginal, searchLemma)
frequency = godAlignments['alignmentTxt'].value_counts()

# find exact word in target language
godAlignments = db.findAlignmentsForWord(connection, 'God', searchTarget)
frequency = godAlignments['alignmentTxt'].value_counts()

# find word (ignore case) in target language
godAlignments = db.findAlignmentsForWord(connection, 'God', searchTarget, searchLemma, caseInsensitive)
frequency = godAlignments['alignmentTxt'].value_counts()

# frequency = godAlignments.sort_values(by=['alignmentTxt'])

# summary = {}
# for a in alignments:
#     target = a['targetWordsTxt']
#     original = a['origWordsTxt']
#     key = f"{original} = {target}"
#
#     if (key in summary):
#         summary[key]['count'] = summary[key]['count'] + 1
#     else:
#         newItem = {
#             'target': target,
#             'original': original,
#             'count': 1
#         }
#         summary[key] = newItem

