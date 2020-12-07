# parse greek words into table

import utils.db_utils as db
import utils.file_utils as file

origLangPath ='/Users/blm/translationCore/resources/el-x-koine/bibles/ugnt/v0.14'

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
chapterPath = f"{origLangPath}/{bookId}/{chapter}.json"

chapter_dict = file.readJsonFile(chapterPath)

verse = '4'

words = db.getVerseWordsFromChapter(chapter_dict, verse)

db_words = db.getDbWordsForVerse(words, bookId, chapter, verse)

table = 'original_words'

db.addMultipleItemsToDatabase(connection, table, db_words)

items = db.getRecords(connection, table, '*')

"""
INSERT INTO
  users (name, age, gender, nationality)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""
# isinstance(s, str)


# execute_query(connection, create_users)

# /Users/blm/translationCore/resources/el-x-koine/bibles/ugnt/v0.14
