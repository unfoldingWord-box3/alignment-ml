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
  occurrence INTEGER,
  occurrences INTEGER,
  strong TEXT,
  lemma TEXT,
  morph TEXT
);
"""

################################



