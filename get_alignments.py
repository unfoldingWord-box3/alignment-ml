
# download all the en ult new testament alignments into data

import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = './data/alignmentData.sqlite'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'

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

# # get alignments for OT (not working yet)
# db.getAlignmentsForTestament(connection, 0, dataFolder, bibleType)

# get alignments for NT
db.getAlignmentsForTestament(connection, 1, dataFolder, bibleType)


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

lemma = 'θεός'
word = 'Θεοῦ'

# find all forms of word by lemma
lemmas = db.findOriginalLemma(connection, lemma)
print (f"{len(lemmas)} items found")

# find specific word by text
words = db.findOriginalWord(connection, word)
print (f"{len(words)} items in search")

first_word = words[0]

# item = db.findWordById(connection, 75, original_words_table)

alignment = db.getAlignmentForWord(connection, first_word, 1)

alignments = db.getAlignmentsForWord(connection, words, 1)

# load as dataframe
df = pd.DataFrame(alignments)

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

