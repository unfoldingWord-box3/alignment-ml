# alignment-ml

These are programs to generate Machine Learning training data from translationCore resources.
Future exploration:
- explore how to tag poor alignments for use in training or testing ML models.

Tested using Python 3.9.1 & 3.8.5 for New Testament only.

##Setup:
- make sure node 15.5+ is installed.  Verify with: `node --version`
  - download installer from: `https://nodejs.org/`
- make sure python 3 is installed.  Verify with: `python3 --version`
- setup python modules:
```
pip3 install pandas
pip3 install requests
```    
- copy resources from catalog:
  - the first time will have to do:
```
cd node_stuff
npm i
cd ..
```
- if you want to manually run scripts (not necessary if you run download_resources_and_process_alignments.py), then need to download specific resources from door43 catalog (change version numbers to match latest for resource):
```
cd node_stuff
node ./downloadResource.js https://cdn.door43.org ../resources el-x-koine ugnt 0.16 ugnt
node ./downloadResource.js https://cdn.door43.org ../resources en ult 18 ult
node ./downloadResource.js https://cdn.door43.org ../resources en tw 19 bible
cd ..
```
- or can download directly from repo: `node ./downloadResource.js --fullUrl https://git.door43.org/unfoldingWord/en_ult/archive/master.zip ~/resources en ult 18 bible`

##Automatic Alignments Processing:
- select download source by changing config.py to point to appropriate config file.
- run: `python3 download_resources_and_process_alignments.py`

##Manual Operations:
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
