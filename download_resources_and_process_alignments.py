import time
from datetime import timedelta
from config import getConfig

############################################
# get configuration
cfg = getConfig() # configure values in config.js

start = time.time()

############################################

print("\n\ndownload resources:")
import download_resource_files

print("\n\nextract alignments:")
import db_load_alignments_from_resources

print("\n\nget original language words for tWords:")
import fetch_translation_words

print("\n\ngenerate ML training data:")
import fetch_alignment_training_data

print("\n\ngenerate warnings reports:")
import create_alignment_warning_csv

############################################

delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'Parse alignments, total elapsed time: {elapsed}')

# Dell Windows: Parse alignments, total elapsed time: 0:02:13
# MBP M1 Rosetta (native node): Parse alignments, total elapsed time: 0:00:18
# MBP M1 Native: Parse alignments, total elapsed time: 0:00:16
