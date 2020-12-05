
################################

import utils.bible_utils as bu

userUrl = 'https://git.door43.org/lrsallee'
bibleType = 'en_ult'
testament = 1
outputFolder = './data'

# download all the en ult new testament alignments into data
bu.downloadTestamentAlignments(userUrl, bibleType, testament, outputFolder)

################################

import utils.db_utils as db

connection = db.create_connection('./data/dummy.sqlite')

create_users_table = """
CREATE TABLE IF NOT EXISTS word (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id TEXT NOT NULL,
  chapter TEXT NOT NULL,
  verse TEXT NOT NULL,
  word_num INTEGER,
  word TEXT NOT NULL,
  occurrance INTEGER,
  occurrances INTEGER,
  strong TEXT,
  lemma TEXT,
  morph TEXT
);
"""