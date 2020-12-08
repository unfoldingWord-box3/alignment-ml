
# download all the en ult new testament alignments into data

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

# # get alignments for OT
# db.getAlignmentsForTestament(connection, 0, dataFolder, bibleType)

# get alignments for NT
db.getAlignmentsForTestament(connection, 1, dataFolder, bibleType)

items_orig = db.fetchRecords(connection, target_words_table, '')
print (f"{len(items_orig)} items in target_words_table")

items_align = db.fetchRecords(connection, alignment_table, '')
print (f"{len(items_align)} items in alignment_table")

items_align = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items_align)} items in original_words_table")
