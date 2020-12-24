# alignment-ml

These are programs to generate Machine Learning training data from translationCore resources.
Future exploration:
- explore how to tag poor alignments for use in training or testing ML models.

Tested using Python 3.9 for New Testament only.

**Create the DB from downloaded resources:**

- see: db_load_alignments_from_resources.py
- configure paths at top of file before running, and sqlite database is created at dbPath.
- tip: this can take over an hour to run, but seems to run much faster if you delete the .sqlite file before running python program.  A new database file will be created automatically.

**Get lemmas used for tWords:**

- see: fetch_translation_words.py
- configure paths at top of file before running, and lemmas jsons stored in './data'

**Get ML training data:**

For example of how to get an alignment table for key terms see: fetch_alignment_training_data.py

**Visualizing alignment data:**

On Jupyter notebooks have these examples:
- plots of single alignments: plot_original_word_alignments.ipynb or look at plot_original_word_alignments.pdf
- plots of multiple alignments: plot_multi_alignments.ipynb or plot_multi_alignments.pdf
  
**Creating a CSV file of the suspect warnings:**

- see: create_alignment_warning_csv.py
- outputs to: kt_en_ult_NT_warnings.csv
