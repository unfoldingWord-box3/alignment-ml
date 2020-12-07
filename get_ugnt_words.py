# parse greek words into table

import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible

origLangPathGreek = '/Users/blm/translationCore/resources/el-x-koine/bibles/ugnt/v0.14'
origLangPathHebrew = '/Users/blm/translationCore/resources/hbo/bibles/uhb/v2.1.15'

connection = db.create_connection('./data/alignments.sqlite')

create_original_words_table = """
CREATE TABLE IF NOT EXISTS original_words (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id TEXT NOT NULL,
  chapter TEXT NOT NULL,
  verse TEXT NOT NULL,
  word_num INTEGER,
  word TEXT NOT NULL,
  occurrance INTEGER,
  strong TEXT,
  lemma TEXT,
  morph TEXT
);
"""

db.execute_query(connection, create_original_words_table)

################################

bookId = 'tit'
chapter = '1'
chapterPath = f"{origLangPathGreek}/{bookId}/{chapter}.json"

chapter_dict = file.readJsonFile(chapterPath)

verse = '4'

# words = db.getVerseWordsFromChapter(chapter_dict, verse)
#
# db_words = db.getDbWordsForVerse(words, bookId, chapter, verse)

table = 'original_words'

#db.addMultipleItemsToDatabase(connection, table, db_words)

items = db.getRecords(connection, table, '')
print (f"{len(items)} items after add")

###

items = db.getRecords(connection, table, '')
print (f"{len(items)} items after delete")

db.loadAllWordsFromBookIntoDB(connection, origLangPathGreek, bookId, table)

items = db.getRecords(connection, table, '')
print (f"{len(items)} items after reading {bookId}")

# books = bible.getBookList(1)
# for book in books:
#     print (f"reading {book}")
#     db.loadAllWordsFromBookIntoDB(connection, origLangPath, book, table)

# db.loadAllWordsFromTestamentIntoDB(connection, origLangPathGreek, 1, table)

items = db.getRecords(connection, table, '')
print (f"{len(items)} items after reading testament")

# db.loadAllWordsFromTestamentIntoDB(connection, origLangPathHebrew, 0, table)

items = db.getRecords(connection, table, '')
print (f"{len(items)} items after reading testament")

items = db.getRecords(connection, table, "book_id = 'phm'")
print (f"{len(items)} items in book")

# in bible we found 421298 total original language words

# isinstance(s, str)


# execute_query(connection, create_users)

# /Users/blm/translationCore/resources/el-x-koine/bibles/ugnt/v0.14
