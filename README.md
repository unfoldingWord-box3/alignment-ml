# alignment-ml

These are programs to generate Machine Learning training data as well as generate alignment warnings based on statistical data from translationCore resources.
Future exploration:
- explore how to tag poor alignments for use in training or testing ML models.

Tested using Python 3.9.1 & 3.8.5 for New Testament only.

## Setup:
- make sure node 15.5+ is installed.  Verify with: `node --version`
  - download installer from: `https://nodejs.org/`
- make sure python 3 is installed.  Verify with: `python3 --version`
- on Mac or Linux, can try running `./start.sh install.py`
  - if that does not say `Install Success` then do:
```
pip3 install pandas
pip3 install requests
cd node_stuff
npm i
cd ..
```

## Automatic Alignments Processing:
- select download source by changing config.py to point to appropriate config file.
- run: `python3 download_resources_and_process_alignments.py`

## Generated data files:
- differentiated in data folder by target language and target literal bible (e.g. `./data/en/ult`)
  - `alignments_NT.sqlite` sqlite database containing tables for target language words, original language words, and alignments.
  - `alignments_NT.ow_index.sqlite` sqlite database containing alignments ordered by original language word along with frequency of alignments
  - `all_twords_*_*_NT_warnings_0.csv` spreadsheet with warnings for alignments of tWords based on frequency, number of target words, discontiguous target words, number of original language words, discontiguous original language words in alignment
  - `all_alignments_*_*_NT_warnings_0.csv` spreadsheet with warnings for alignments of all words in NT based on frequency, number of target words, discontiguous target words, number of original language words, discontiguous original language words in alignment
  - `all_*_*_NT_summary.csv` spreadsheet with summary and statistical analysis for all alignments of original language words in NT

## Manual Operations:
**Coping resources from catalog:
- if you want to manually run scripts (not necessary if you run download_resources_and_process_alignments.py), then need to download specific resources from door43 catalog (change version numbers to match latest for resource):
```
cd node_stuff
node ./downloadResource.js https://cdn.door43.org ../resources el-x-koine ugnt 0.16 ugnt
node ./downloadResource.js https://cdn.door43.org ../resources en ult 18 ult
node ./downloadResource.js https://cdn.door43.org ../resources en tw 19 bible
cd ..
```
- or can download directly from repo: `node ./downloadResource.js --fullUrl https://git.door43.org/unfoldingWord/en_ult/archive/master.zip ~/resources en ult 18 bible`

**Create the DB from downloaded resources:**

- see: db_load_alignments_from_resources.py
- run: `python3 db_load_alignments_from_resources.py`  
- configure paths at top of file before running, and sqlite database is created at dbPath.
- tip: this can take over an hour to run, but seems to run much faster if you delete the .sqlite file before running python program.  A new database file will be created automatically.

**Get lemmas and original language words used for tWords:**

- see: fetch_translation_words.py
- run: `python3 fetch_translation_words.py`
- configure paths at top of file before running, and lemmas jsons stored in './data'

**Get ML training data:**

For example of how to get an alignment table for key terms see: fetch_alignment_training_data.py
- run: `python3 fetch_alignment_training_data.py`

**Visualizing alignment data:**

On Jupyter notebooks have these examples:
- plots of multiple alignments: plot_multi_alignments.ipynb or plot_multi_alignments_twords.pdf
  
**Creating a CSV file of the suspect warnings:**

- see: create_alignment_warning_csv.py
- run: `python3 create_alignment_warning_csv.py`
- outputs to: ./data/kt_en_ult_NT_warnings*.csv
