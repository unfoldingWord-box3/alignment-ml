# save

import utils.db_utils as db
import utils.file_utils as file
import time
from datetime import timedelta

############################################
# configure these values for your system
############################################

targetLang = 'en'
bibleType = 'en_ult'
tWordsTypeList = ['kt', 'names', 'other'] # categories of tWords
dbPath = f'./data/{bibleType}_NT_alignments.sqlite'

connection = db.initAlignmentDB(dbPath)

################################


def saveAlignmentDataForLemmas(type_):
    print(f"Saving Alignments for {type_}")

    # read alignment data for all the lemmas
    termsPath = f'./data/{type_}_{bibleType}_NT_lemmas.json'
    data = file.initJsonFile(termsPath)
    print (f"'{termsPath}' has {len(list(data.keys()))} words")
    lemmasList = list(data.keys())

    alignments = db.getAlignmentsForOriginalWords(connection, lemmasList)
    print(f"alignments size is {len(alignments)}")

    ################################
    # flatten the lemmas into an alignment list

    alignmentsList, rejectedAlignmentsList = db.filterAlignments(alignments)
    termsPath = f'./data/TrainingData/{type_}_{bibleType}_NT_alignments_all'
    print(f"Unfiltered training list size is {len(alignmentsList)}")
    file.writeJsonFile(termsPath + '.json', alignmentsList)
    db.saveListToCSV(termsPath + ".csv", alignmentsList)

    ################################
    # flatten the lemmas into a filtered alignment list

    minAlignments = 100
    alignmentsList, rejectedAlignmentsList = db.filterAlignments(alignments, minAlignments)
    termsPath = f'./data/TrainingData/{type_}_{bibleType}_NT_alignments_filtered_{minAlignments}'
    print(f"filtered {minAlignments} training list size is {len(alignmentsList)}")
    print(f"rejected size is {len(rejectedAlignmentsList)}")
    file.writeJsonFile(termsPath + '.json', alignmentsList)
    db.saveListToCSV(termsPath + ".csv", alignmentsList)

start = time.time()
for type_ in tWordsTypeList:
    saveAlignmentDataForLemmas(type_)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'fetch alignments for tW lemmas, Elapsed time: {elapsed}')

# fetch alignments for lemmas, Elapsed time: 0:01:07