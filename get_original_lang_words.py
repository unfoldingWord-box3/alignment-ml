# parse greek words into table

import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible

origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'

dbPath = './data/alignments.sqlite'

connection = db.initAlignmentDB(dbPath)

################################

bookId = 'tit'
chapter = '1'
chapterPath = f"{origLangPathGreek}/{bookId}/{chapter}.json"

chapter_dict = file.readJsonFile(chapterPath)

verse = '4'

# words = db.getVerseWordsFromChapter(chapter_dict, verse)
#
# db_words = db.getDbWordsForVerse(words, bookId, chapter, verse)

original_words_table = db.original_words_table
target_words_table = db.target_words_table

#db.addMultipleItemsToDatabase(connection, table, db_words)

items = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items)} items after add")

###

# read all greek words
db.loadAllWordsFromTestamentIntoDB(connection, origLangPathGreek, 1, original_words_table)

items = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items)} items after reading testament")

# read all Hebrew words
db.loadAllWordsFromTestamentIntoDB(connection, origLangPathHebrew, 0, original_words_table)

items = db.fetchRecords(connection, original_words_table, '')
print (f"{len(items)} items after reading testament")

items = db.fetchRecords(connection, original_words_table, "book_id = 'tit'")
print (f"{len(items)} items in book")

# in bible we found 421298 total original language words
