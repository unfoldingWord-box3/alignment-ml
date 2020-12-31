import time
from datetime import timedelta
from config import getConfig

############################################
# get configuration
cfg = getConfig() # configure values in config.js

start = time.time()

############################################

# download resources:
import download_resource_files

# get original language words for tWords
import fetch_translation_words

# generate ML training data
import fetch_alignment_training_data

# generate warnings reports
import create_alignment_warning_csv

############################################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Parse alignments, total elapsed time: {elapsed}')