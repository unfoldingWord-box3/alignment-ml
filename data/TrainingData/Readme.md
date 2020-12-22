## Training data folder

### loading alignments data into a dataframe in Python:

```
# example reading dataFrame from json which preserves types:
import json
import pandas as pd

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
- 'origSpan' - span of original words to determine how close the words are (highest word number minus lowest word number).  This includes aligned words, so is not normalized.  So better to use 'origWordsBetween' for training.
- 'origWordsBetween' - count of extra words (not part of current alignment) between aligned original language words (indicator that alignments are discontiguous)
- 'origWords' - list of original language words used in alignment
- 'origWordsTxt' - text form of original language words used in alignment
- 'alignmentOrigWords' - count of original language words used in alignment
- 'targetSpan' - span of target words to determine how close the words are (highest word number minus lowest word number).  This includes aligned words, so is not normalized.  So better to use 'targetWordsBetween' for training.
- 'targetWordsBetween' - count of extra words (not part of current alignment) between aligned target language words (indicator that alignments are discontiguous)
- 'targetWords' - list of target language words used in alignment
- 'targetWordsTxt' - text form of target language words used in alignment
- 'alignmentTargetWords'  - count of target language words used in alignment
- 'alignmentTxt' - origWordsTxt combined with targetWordsTxt (easy visual of
- 'frequency' - normalized frequency that this specific alignment was made (alignment count/total alignments in table)
- 'matchCount' - number of times this specific alignment was made (alignment count)

Note: to get the total alignments counts for a specific original language word do: matchCount / frequency
