# alignment-ml

These are programs to generate Machine Learning training data from translationCore resources.
Future exploration:
- explore how to tag poor alignments for use in training or testing ML models.

Tested using Python 3.9 for New Testament only.

**Create the DB from downloaded resources:**

- see: db_load_alignments_from_resources.py
- configure paths at top of file before running, and sqlite database is created at dbPath.
- tip: this can take over an hour to run, but seems to run much faster if you delete the .sqlite file before running python program.  A new databose file will be created automatically.

**Get lemmas used for tWords:**

- see: fetch_translation_words.py
- configure paths at top of file before running, and lemmas jsons stored in './data'

**Get ML training data:**

For example of how to get an alignment table for key terms see: fetch_alignment_training_data.py