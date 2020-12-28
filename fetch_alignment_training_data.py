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
minAlignments = 40
tWordsTypeList = ['kt', 'names', 'other'] # categories of tWords
dbPath = f'./data/{bibleType}_NT_alignments.sqlite'

connection = db.initAlignmentDB(dbPath)

################################

def saveAlignmentDataForLemmas(type_, minAlignments = 100):
    print(f"Saving Alignments for {type_}")

    # read alignment data for all the lemmas
    termsPath = f'./data/{type_}_{bibleType}_NT_lemmas.json'
    data = file.initJsonFile(termsPath)
    print (f"'{termsPath}' has {len(list(data.keys()))} words")
    lemmasList = list(data.keys())
    alignments = {}

    for word in lemmasList:
        alignments_ = db.findAlignmentsFromIndexDbForOrigWord(connection, word, searchLemma=True, maxRows=None)
        alignments[word] = alignments_

    # alignments = db.getAlignmentsForOriginalWords(connection, lemmasList)
    print(f"alignments size is {len(alignments)}")

    ################################
    # flatten the lemmas into a filtered alignment list

    alignmentsList, rejectedAlignmentsList = db.filterAlignments(alignments, minAlignments)
    termsPath = f'./data/TrainingData/{type_}_{bibleType}_NT_alignments_filtered_{minAlignments}'
    print(f"filtered {minAlignments} training list count is {len(alignmentsList)}")
    print(f"rejected count is {len(rejectedAlignmentsList)}")
    jsonPath = termsPath + '.json'
    file.writeJsonFile(jsonPath, alignmentsList)
    print(f"Size of filtered alignments {jsonPath} is {file.getFileSize(jsonPath)/1024/1024:.3f} MB")
    csvPath = termsPath + ".csv"
    db.saveListToCSV(csvPath, alignmentsList)
    print(f"Size of filtered alignments {csvPath} is {file.getFileSize(csvPath)/1024/1024:.3f} MB")

    ################################
    # merge to make a complete list

    alignmentsList.extend(rejectedAlignmentsList)
    termsPath = f'./data/TrainingData/{type_}_{bibleType}_NT_alignments_all'
    print(f"Unfiltered training list size is {len(alignmentsList)}")
    jsonPath = termsPath + '.json'
    file.writeJsonFile(jsonPath, alignmentsList)
    print(f"Size of filtered alignments {jsonPath} is {file.getFileSize(jsonPath)/1024/1024:.3f} MB")
    csvPath = termsPath + ".csv"
    db.saveListToCSV(csvPath, alignmentsList)
    print(f"Size of filtered alignments {csvPath} is {file.getFileSize(csvPath)/1024/1024:.3f} MB")


start = time.time()
for type_ in tWordsTypeList:
    saveAlignmentDataForLemmas(type_, minAlignments)
delta = (time.time() - start)
elapsed = str(timedelta(seconds=delta))
print(f'fetch alignments for tW lemmas, Elapsed time: {elapsed}')

# fetch alignments for lemmas, Elapsed time: 0:00:22