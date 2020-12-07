
# download all the en ult new testament alignments into data

import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = './data/alignments.sqlite'

connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data'
bookId = 'tit'
chapter = '1'
verse = '4'
word = 'καὶ'
occurrence = 2

# get reference for word
items = db.fetchWordsForVerse(connection, original_words_table, bookId, chapter, verse)
print (f"{len(items)} words found in verse")

# get reference for word
items = db.fetchForWordInVerse(connection, original_words_table, word, occurrence, bookId, chapter, verse)
print (f"{len(items)} matching words found")

#############

books = bible.getBookList(1)
for book in books:
    print (f"reading {book}")
    db.saveAlignmentsForBook(connection, book, dataFolder, bibleType)

items_orig = db.fetchRecords(connection, target_words_table, '')
print (f"{len(items_orig)} items in target_words_table")

items_align = db.fetchRecords(connection, alignment_table, '')
print (f"{len(items_align)} items in alignment_table")
