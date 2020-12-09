
# download all the en ult new testament alignments into data, and search

import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = './data/alignmentData.sqlite'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/Alignments'
bookId = 'tit'

# chapter = '1'
# verse = '4'
# word = 'καὶ'
# occurrence = 2

# # get reference for word
# items = db.fetchWordsForVerse(connection, original_words_table, bookId, chapter, verse)
# print (f"{len(items)} words found in verse")
#
# # get reference for word
# items = db.fetchForWordInVerse(connection, original_words_table, word, occurrence, bookId, chapter, verse)
# print (f"{len(items)} matching words found")

#############

# completely clear old data
db.resetTable(connection, target_words_table)

# # get alignments for OT (not working yet)
# start = time.time()
# db.getAlignmentsForTestament(connection, 0, dataFolder, bibleType)
# delta = (time.time() - start)
# elapsed = str(timedelta(seconds=delta))
# print(f'Get OT alignments, Elapsed time: {elapsed}')

# get alignments for NT
start = time.time()
db.getAlignmentsForTestament(connection, 1, dataFolder, bibleType)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Get NT alignments, Elapsed time: {elapsed}')

########################

items_target = db.fetchRecords(connection, target_words_table, '')
print (f"{len(items_target)} items in target_words_table")

items_align = db.fetchRecords(connection, alignment_table, '')
print (f"{len(items_align)} items in alignment_table")

items_orig = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items_orig)} items in original_words_table")

# 69050 items in target_words_table
# 48892 items in alignment_table
# 52996 items in original_words_table

searchOriginal = True
searchTarget = False
searchLemma = True
caseInsensitive = True

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

