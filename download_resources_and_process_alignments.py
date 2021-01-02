import time
from datetime import timedelta
from config import getConfig

############################################
# get configuration
cfg = getConfig() # configure values in config.js

start = time.time()

############################################

print("download resources:")
import download_resource_files

print("extract alignments:")
import db_load_alignments_from_resources

print("get original language words for tWords:")
import fetch_translation_words

print("generate ML training data:")
import fetch_alignment_training_data

print("generate warnings reports:")
import create_alignment_warning_csv

############################################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Parse alignments, total elapsed time: {elapsed}')