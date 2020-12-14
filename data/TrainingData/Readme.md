## Training data folder

### loading alignments data into a dataframe in Python:

```
# example reading dataFrame from json which preserves types:
f = open('data/TrainingData/θεός.json')
dataStr = f.read()
data = json.loads(dataStr)
df = pd.DataFrame(data)
df.describe() # show key metric data
```

### description of keys used in json and csv files

**Current metric Columns:** origSpan, alignmentOrigWords, targetSpan, alignmentTargetWords, frequency

**Key Explanations for alignments columns:**
- 'id' - identifier for specific alignment
- 'book_id' - identifier for specific alignment
- 'chapter' - identifier for specific alignment
- 'verse' - identifier for specific alignment
- 'alignment_num' - identifier for specific alignment
- 'orig_lang_words' - internal field from alignment db - id number of original words in db
- 'target_lang_words' - internal field from alignment db - id number of target words in db
- 'origSpan' - determine how close the original words are (the highest word number minus the lowest word number)
- 'origWordsBetween' - original language extra unaligned word count between aligned original language words 
- 'origWords' - list of original language words used in alignment
- 'origWordsTxt' - text form of original language words used in alignment
- 'alignmentOrigWords' - count of original language words used in alignment
- 'targetSpan' - determine how close the original words are (the highest word number minus the lowest word number)
- 'targetWordsBetween' - target language extra unaligned word count between aligned original language words
- 'targetWords' - list of target language words used in alignment
- 'targetWordsTxt' - text form of target language words used in alignment
- 'alignmentTargetWords'  - count of target language words used in alignment
- 'alignmentTxt' - origWordsTxt combined with targetWordsTxt (easy visual of
- 'frequency' - normalized frequency that this specific alignment was made (alignment count/total alignments in table)
