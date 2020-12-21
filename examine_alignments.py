# search alignments

import json
import pandas as pd
import utils.db_utils as db
import utils.file_utils as file
import utils.bible_utils as bible
import time
from datetime import timedelta

original_words_table = db.original_words_table
target_words_table = db.target_words_table
alignment_table = db.alignment_table
dbPath = './data/en_ult_alignments.sqlite'
keyTermsPath = './data/keyTerms.json'
alignmentTrainingDataPath = './data/alignmentTrainingData.json'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

connection = db.initAlignmentDB(dbPath)

bibleType = 'en_ult'
testament = 1
dataFolder = './data/AlignmentsFromProjects'
bookId = 'tit'

searchOriginal = True
searchTarget = False
searchLemma = True
caseInsensitive = True

########################

# find exact word in original language
godAlignments = db.findAlignmentsForWord(connection, 'Θεοῦ', searchOriginal)
frequency = godAlignments['alignmentTxt'].value_counts()

# find all forms of word in original language by lemma
godAlignments = db.findAlignmentsForWord(connection, 'θεός', searchOriginal, searchLemma)
frequency = godAlignments['alignmentTxt'].value_counts()

# find exact word in target language
godAlignments = db.findAlignmentsForWord(connection, 'God', searchTarget)
frequency = godAlignments['alignmentTxt'].value_counts()

# find word (ignore case) in target language
godAlignments = db.findAlignmentsForWord(connection, 'God', searchTarget, searchLemma, caseInsensitive)
frequency = godAlignments['alignmentTxt'].value_counts()

# frequency = godAlignments.sort_values(by=['alignmentTxt'])

# summary = {}
# for a in alignments:
#     target = a['targetWordsTxt']
#     original = a['origWordsTxt']
#     key = f"{original} = {target}"
#
#     if (key in summary):
#         summary[key]['count'] = summary[key]['count'] + 1
#     else:
#         newItem = {
#             'target': target,
#             'original': original,
#             'count': 1
#         }
#         summary[key] = newItem


godAlignments = db.findAlignmentsForWord(connection, 'θεός', True, True)

# import json
# origWordsJson = '[{"id": 799637, "book_id": "1jn", "chapter": "1", "verse": "5", "word_num": 12, "word": "\u1f45\u03c4\u03b9", "occurrence": 1, "strong": "G37540", "lemma": "\u1f45\u03c4\u03b9", "morph": "Gr,CS,,,,,,,,"}, {"id": 799638, "book_id": "1jn", "chapter": "1", "verse": "5", "word_num": 13, "word": "\u1f41", "occurrence": 1, "strong": "G35880", "lemma": "\u1f41", "morph": "Gr,EA,,,,NMS,"}, {"id": 799639, "book_id": "1jn", "chapter": "1", "verse": "5", "word_num": 11, "word": "\u0398\u03b5\u1f78\u03c2", "occurrence": 1, "strong": "G23160", "lemma": "\u03b8\u03b5\u03cc\u03c2", "morph": "Gr,N,,,,,NMS,"}]'
# origWords = json.loads(origWordsJson) # make sure json

###############

# reading dataFrame from json:
f = open('data/TrainingData/θεός.json')
dataStr = f.read()
data = json.loads(dataStr)
df = pd.DataFrame(data)
df.describe()

###############

# foundWords = db.findWord(connection, word, searchOriginal, searchLemma, caseInsensitive)

###################

# find all forms of word in original language by lemma
foundWords = db.findOriginalWordsForLemma(connection, 'θεός')
frequency = foundWords['word'].value_counts()
usage = dict(frequency)

word = 'God'
lemmas = db.findLemmasAlignedWithTarget(connection, word)
print(f"for word '{word}' found aligned lemmas {lemmas}")

wordList = 'saved save safe salvation'
unique = db.findUniqueLemmasAlignedWithTargetWords(connection, wordList, threshold = 2)
print(f"for words '{wordList}' found unique aligned lemmas {unique}")

#########################

wordList = 'saved save safe salvation'
unique = db.saveUniqueLemmasAlignedWithTargetWords(connection, keyTermsPath, wordList)
print (f"words '{wordList}' got list: {unique}")

wordList = 'sanctify sanctification'
unique = db.saveUniqueLemmasAlignedWithTargetWords(connection, keyTermsPath, wordList)
print (f"words '{wordList}' got list: {unique}")

wordList = 'holy holiness unholy sacred'
unique = db.saveUniqueLemmasAlignedWithTargetWords(connection, keyTermsPath, wordList)
print (f"words '{wordList}' got list: {unique}")

data = file.initJsonFile(keyTermsPath)
print (f"'{keyTermsPath}' has words: {data}")

#########################

wordList = 'holy holiness unholy sacred'
unique = db.saveUniqueLemmasAlignedWithTargetWords(connection, keyTermsPath, wordList)
words = unique.keys()
# firstWord = list(words)[0]
# alignments = db.findAlignmentsForWord(connection, firstWord, searchOriginal = True, searchLemma = True, caseInsensitive = True)

wordList = list(words)
alignments = db.findAlignmentsForWords(connection, wordList, searchOriginal = True, searchLemma = True, caseInsensitive = True)

############################

# firstItem = list(data[firstKey].keys())

####################

# keyTermsList = list(data.keys())
# firstKey = keyTermsList[0]
# firstItem = list(data[firstKey].keys())
# db.saveAlignmentDataForWords(connection, firstKey, firstItem, searchOriginal = True, searchLemma = True, caseInsensitive = True)
#

wordList = 'kingdom'
unique = db.saveUniqueLemmasAlignedWithTargetWords(connection, keyTermsPath, wordList)
words = list(unique.keys())
alignments = db.saveAlignmentDataForWords(connection, wordList, words, searchOriginal = True, searchLemma = True, caseInsensitive = True)

wordList = 'ancestor father fathered forefather grandfather'
unique = db.saveUniqueLemmasAlignedWithTargetWords(connection, keyTermsPath, wordList)
words = list(unique.keys())
alignments = db.saveAlignmentDataForWords(connection, wordList, words, searchOriginal = True, searchLemma = True, caseInsensitive = True)

################

wordList = 'saved save safe salvation'
unique = db.findUniqueLemmasAlignedWithTargetWords(connection, wordList, threshold = 2)
print(f"for words '{wordList}' found unique aligned lemmas {unique}")

words = unique.keys()
wordList = list(words)
alignments = db.findAlignmentsForWords(connection, wordList, searchOriginal = True, searchLemma = True, caseInsensitive = True)

###############

db.saveAlignmentDataForLemmas(connection, keyTermsPath)

################

wordList = 'saved save safe salvation'
unique = db.findUniqueLemmasAlignedWithTargetWords(connection, wordList, threshold = 2)
print(f"for words '{wordList}' found unique aligned lemmas {unique}")

words = list(unique.keys())

alignments_df = db.saveAlignmentDataForWords(connection, wordList, words, searchOriginal = True, searchLemma = True, caseInsensitive = True)

#################

# get all greek words
items_orig_greek = db.fetchRecords(connection, original_words_table, "morph LIKE 'Gr%'")
print (f"{len(items_orig_greek)} greek words in original_words_table")
original_df = pd.DataFrame(items_orig_greek)
morphs = original_df['morph']

# get count of times each used
frequency = morphs.value_counts()
print("Frequency of morph usage:")
print(frequency)

# get alphabetized list of morphs
morphs_list = list(dict(frequency).keys())
morphs_list.sort()
print("Alphabetized morph list:")
print(morphs_list)

# get all Hebrew words
items_orig_hebrew = db.fetchRecords(connection, original_words_table, "morph LIKE 'He%'")
print (f"{len(items_orig_hebrew)} hebrew words in original_words_table")
original_df = pd.DataFrame(items_orig_hebrew)
morphs = original_df['morph']

# get count of times each used
frequency = morphs.value_counts()
print("Frequency of morph usage:")
print(frequency)

# get alphabetized list of morphs
morphs_list = list(dict(frequency).keys())
morphs_list.sort()
print("Alphabetized morph list:")
print(morphs_list)

# get all Aramaic words
items_orig_aramaic = db.fetchRecords(connection, original_words_table, "morph LIKE 'Ar%'")
print (f"{len(items_orig_aramaic)} aramaic words in original_words_table")
original_df = pd.DataFrame(items_orig_aramaic)
morphs = original_df['morph']

# get count of times each used
frequency = morphs.value_counts()
print("Frequency of morph usage:")
print(frequency)

# get alphabetized list of morphs
morphs_list = list(dict(frequency).keys())
morphs_list.sort()
print("Alphabetized morph list:")
print(morphs_list)


