import pandas as pd
import json
import sqlite3
from sqlite3 import Error
import utils.file_utils as file
import utils.bible_utils as bible

original_words_table = 'original_words'
target_words_table = 'target_words'
alignment_table = 'alignment_table'
origLangPathGreek = './data/OrigLangJson/ugnt/v0.14'
origLangPathHebrew = './data/OrigLangJson/uhb/v2.1.15'
targetLangPathEn = './data/TargetLangJson/ult/v14'

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        # print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query_dict(connection, query):
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        found = cursor.fetchall()
        result = []
        for r in found:
            row = dict(r)
            # print(row)
            result.append(row)
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

create_original_words_table = f"""
CREATE TABLE IF NOT EXISTS {original_words_table} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id TEXT NOT NULL,
  chapter TEXT NOT NULL,
  verse TEXT NOT NULL,
  word_num INTEGER,
  word TEXT NOT NULL,
  occurrence INTEGER,
  strong TEXT,
  lemma TEXT,
  morph TEXT
);
"""

create_target_words_table = f"""
CREATE TABLE IF NOT EXISTS {target_words_table} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id TEXT NOT NULL,
  chapter TEXT NOT NULL,
  verse TEXT NOT NULL,
  word_num INTEGER,
  word TEXT NOT NULL,
  occurrence INTEGER
);
"""

create_alignment_table = f"""
CREATE TABLE IF NOT EXISTS {alignment_table} (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  book_id TEXT NOT NULL,
  chapter TEXT NOT NULL,
  verse TEXT NOT NULL,
  alignment_num INTEGER,
  orig_lang_words TEXT NOT NULL,
  target_lang_words TEXT NOT NULL
);
"""

# will create and initialize the database if it does not exist or tables not created
# will return connection
def initAlignmentDB(dbPath):
    connection = create_connection(dbPath)
    execute_query(connection, create_original_words_table)
    execute_query(connection, create_target_words_table)
    execute_query(connection, create_alignment_table)
    return connection

def resetTable(connection, table):
    print(f"resetTable - dropping table: {table}")
    command = f"DROP TABLE {table};"
    execute_query(connection, create_alignment_table)

    print(f"resetTable - initializing table: {table}")
    if table == target_words_table:
        execute_query(connection, create_target_words_table)
    elif table == alignment_table:
        execute_query(connection, create_alignment_table)
    elif table == original_words_table:
        execute_query(connection, create_original_words_table)
    else:
        print(f"resetTable - unknown table: {table}")

def getWordsFromVerse(verseObjects):
    words = []
    for i in range(len(verseObjects)):
        vo = verseObjects[i]
        type_ = getKey(vo,'type')
        if (type_ == 'word'):
            # print(f'At {i} Found word: {vo}')
            words.append(vo)
        elif (type_ == 'milestone'):
            children = vo['children']
            # print(f"At {i} Found children: {len(children)}")
            child_words = getWordsFromVerse(children)
            words.extend(child_words)
            # print('finished processing children')
        elif (type_ == ''):
            print(f"getWordsFromVerse - missing type in: {vo}")

    return words

# TODO: finish algorithm to parse en_ult
def getAlignmentsFromVerse(verseObjects, wordNum = 0):
    words = []
    alignments = []
    wordNum = 0
    for i in range(len(verseObjects)):
        vo = verseObjects[i]
        type_ = getKey(vo,'type')
        if (type_ == 'word'):
            # print(f'At {i} Found word: {vo}')
            words.append(vo)
            wordNum = wordNum + 1
        elif (type_ == 'milestone'):
            children = vo['children']
            # print(f"At {i} Found children: {len(children)}")

            # TODO: finish
            # topWord = {
            #     'word': text,
            #     'occurrence': getOccurrences(text, db_words) + 1,
            #     'strong': getKey(word,'strong'),
            #     'lemma': getKey(word,'lemma'),
            #     'morph': getKey(word,'morph')
            # }

            (child_words, child_alignments, child_wordNum) = getAlignmentsFromVerse(vo, wordNum)
            words.extend(child_words)
            # print('finished processing children')
        elif (type_ == ''):
            print(f"getWordsFromVerse - missing type in: {vo}")

    return (words, alignments, wordNum)

def getVerseWordsFromChapter(chapter_dict, verse):
    words = getWordsFromVerse(chapter_dict[verse]['verseObjects'])
    return words

def getOccurrences(text, words):
    count = 0
    for word in words:
        if (word['word'] == text):
            count = count + 1
    return count

def getKey(dict, key, default=''):
    if key in dict:
        return dict[key]
    print(f"getKey({dict}, {key} - key not found")
    return default

def getDbOrigLangWordsForVerse(words, bookId, chapter, verse):
    db_words = []
    for i in range(len(words)):
        word = words[i]
        text = word['text']
        db_word = {
            'book_id': bookId,
            'chapter': chapter,
            'verse': verse,
            'word_num': i,
            'word': text,
            'occurrence': getOccurrences(text, db_words) + 1,
            'strong': getKey(word,'strong'),
            'lemma': getKey(word,'lemma'),
            'morph': getKey(word,'morph')
        }
        # print(f'At {i} new word entry: {db_word}')
        db_words.append(db_word)
    return db_words

def getDbTargetLangWordsForVerse(words, bookId, chapter, verse):
    db_words = []
    for i in range(len(words)):
        word = words[i]
        text = getWordText(word)
        db_word = {
            'book_id': bookId,
            'chapter': chapter,
            'verse': verse,
            'word_num': i,
            'word': text,
            'occurrence': getOccurrences(text, db_words) + 1
        }
        # print(f'At {i} new word entry: {db_word}')
        db_words.append(db_word)
    return db_words

def getWordText(word):
    key = 'text'
    if key in word:
        return word[key]
    key = 'word'
    if key in word:
        return word[key]
    return ''

def insert_row(connection, table, data):
    header = getHeader(data)
    row = getDataItems(data)
    sql = f''' INSERT INTO {table}({header})
              VALUES({row}) '''
    cur = connection.cursor()
    cur.execute(sql)
    connection.commit()
    return cur.lastrowid

def createCommandToAddToDatabase(table, data):
    header = getHeader(data[0])

    dataStr = ''
    length = len(data)
    for i in range(length):
        db_word = data[i]
        line_data = getDataItems(db_word)
        dataStr = dataStr + '  (' + line_data
        if (i < length - 1):
            dataStr = dataStr + '),\n'
        else:
            dataStr = dataStr + ');\n'

    add_words = f"INSERT INTO\n  {table} ({header})\nVALUES\n{dataStr}"
    return add_words


def getDataItems(db_word):
    line_data = ''
    for key, value in db_word.items():
        if (len(line_data) > 0):
            line_data = line_data + ', '

        if isinstance(value, str):
            line_data = f"{line_data}'{value}'"
        else:
            line_data = f"{line_data}{value}"
    return line_data


def getHeader(data):
    header = ''
    for key, value in data.items():
        if (len(header) > 0):
            header = header + ', '
        header = header + key
    return header


def addMultipleItemsToDatabase(connection, table, db_words):
    add_words = createCommandToAddToDatabase(table, db_words)
    # print(f"addMultipleItemsToDatabase:\n{add_words}")
    execute_query(connection, add_words)

def fetchRecords(connection, table, filter, caseInsensitive = False):
    select_items = f"SELECT * FROM {table}"
    if len(filter):
        select_items = select_items + f"\nWHERE {filter}"
    if caseInsensitive:
        select_items = select_items + ' COLLATE NOCASE'
    # print(f"getRecords:\n{select_items}")
    items = execute_read_query_dict(connection, select_items)
    return items

def fetchWordsForVerse(connection, table, bookId, chapter, verse):
    filter = f"(book_id = '{bookId}') AND (chapter = '{chapter}') AND (verse = '{verse}')"
    items = fetchRecords(connection, table, filter)
    # print(f"getRecords:\n{len(items)}")
    return items

def fetchForWordInVerse(connection, table, word, occurrence, bookId, chapter, verse):
    filter = f"(book_id = '{bookId}') AND (chapter = '{chapter}') AND (verse = '{verse}') AND (word = '{word}') AND (occurrence = '{occurrence}')"
    items = fetchRecords(connection, table, filter)
    # print(f"getRecords:\n{len(items)}")
    return items

def deleteWordsForBook(connection, table, bookId):
    selection = f"book_id = '{bookId}'"
    deleteBook = f"DELETE FROM {table}\nWHERE {selection};\n"
    # print(f"deleteWordsForBook:\n{deleteBook}")
    execute_query(connection, deleteBook)

def getVerses(chapter_dict):
    verses = []
    foundNonNumericalVerse = []
    for verse, verseData in chapter_dict.items():
        try:
            verseNum = int(verse) # make sure its a number
            verses.append(verse)
        except:
            foundNonNumericalVerse.append(verse)
    return verses

def loadAllWordsFromBookIntoDB(connection, origLangPath, bookId, table):
    deleteWordsForBook(connection, table, bookId)

    if table == original_words_table:
        getWordsForVerse = getDbOrigLangWordsForVerse
    else:
        getWordsForVerse = getDbTargetLangWordsForVerse

    chapters = bible.getChaptersForBook(bookId)
    for chapter in chapters:
        print(f"{bookId} - Reading chapter {chapter}")

        chapterPath = f"{origLangPath}/{bookId}/{chapter}.json"
        chapter_dict = file.readJsonFile(chapterPath)
        verses = getVerses(chapter_dict)

        for verse in verses:
            # print(f"Reading verse {verse}")
            words = getVerseWordsFromChapter(chapter_dict, verse)
            db_words = getWordsForVerse(words, bookId, chapter, verse)

            # print(f"For {chapter}:{verse} Saving {len(db_words)}")
            addMultipleItemsToDatabase(connection, table, db_words)

def loadAllWordsFromTestamentIntoDB(connection, origLangPath, newTestament, table):
    books = bible.getBookList(newTestament)
    for book in books:
        print (f"loadAllWordsFromTestamentIntoDB - reading {book}")
        loadAllWordsFromBookIntoDB(connection, origLangPath, book, table)

def saveTargetWordsForAlignment(connection, bookId, chapter, verse, alignment, alignmentNum):
    topwords = alignment['topWords']
    bottomWords = alignment['bottomWords']
    origLangWords = topwords
    targetLangWords = bottomWords

    targetIndices = ''
    missingWord = False
    for wordTL in targetLangWords:
        word = getWordText(wordTL)
        occurrence = wordTL['occurrence']
        items = fetchForWordInVerse(connection, target_words_table, word, occurrence, bookId, chapter, verse)
        if len(items) > 0:
            if len(targetIndices) > 0:
                targetIndices = targetIndices + ','
            pos = str(items[0]['id'])
        else:
            pos = '-1'
            missingWord = True
            print(f"saveTargetWordsForAlignment - missing {word}-{occurrence} in {bookId}-{chapter}:{verse}")
        targetIndices = targetIndices + pos
    targetIndices = f",{targetIndices}," # wrap to make searching easier

    originalIndices = ''
    for wordOL in origLangWords:
        word = getWordText(wordOL)
        occurrence = wordOL['occurrence']
        items = fetchForWordInVerse(connection, original_words_table, word, occurrence, bookId, chapter, verse)
        if len(items) > 0:
            if len(originalIndices) > 0:
                originalIndices = originalIndices + ','
            pos = str(items[0]['id'])
        else:
            pos = '-1'
            missingWord = True
            print(f"saveTargetWordsForAlignment - missing {word}-{occurrence} in {bookId}-{chapter}:{verse}")
        originalIndices = originalIndices + pos
    originalIndices = f",{originalIndices}," # wrap to make searching easier

    if missingWord:
        print(f"saveTargetWordsForAlignment - ignoring broken alignment in {bookId}-{chapter}:{verse}")
        return None

    alignment = {
        'book_id': bookId,
        'chapter': chapter,
        'verse': verse,
        'alignment_num':alignmentNum,
        'orig_lang_words':originalIndices,
        'target_lang_words': targetIndices
    }
    return alignment

def saveAlignmentsForVerse(connection, bookId, chapter, verse, verseAlignments):
    alignments = []
    for i in range(len(verseAlignments)):
        verseAlignment = verseAlignments[i]
        alignment = saveTargetWordsForAlignment(connection, bookId, chapter, verse, verseAlignment, i)
        if alignment:
            alignments.append(alignment)
    addMultipleItemsToDatabase(connection, alignment_table, alignments)

def saveAlignmentsForChapter(connection, bookId, chapter, dataFolder, bibleType):
    data = bible.loadChapterAlignments(dataFolder, bibleType, bookId, chapter)
    verses = getVerses(data)
    for verseAl in verses:
        verseAlignments = data[verseAl]['alignments']
        print(f"reading alignments for {chapter}:{verseAl}")
        saveAlignmentsForVerse(connection, bookId, chapter, verseAl, verseAlignments)

def saveAlignmentsForBook(connection, bookId, aligmentsFolder, bibleType, origLangPath):
    deleteWordsForBook(connection, alignment_table, bookId)
    deleteWordsForBook(connection, target_words_table, bookId)
    deleteWordsForBook(connection, original_words_table, bookId)

    bookFolder = aligmentsFolder + '/' + file.getRepoName(bibleType, bookId)
    files = file.listFolder(bookFolder)
    if files: # make sure folder has files
        print("reading original language words")
        loadAllWordsFromBookIntoDB(connection, origLangPath, bookId, original_words_table)
        print("reading target language words")
        loadAllWordsFromBookIntoDB(connection, targetLangPathEn, bookId, target_words_table)

        chapters = bible.getChaptersForBook(bookId)
        for chapterAL in chapters:
            print(f"reading alignments for {bookId} - {chapterAL}")
            saveAlignmentsForChapter(connection, bookId, chapterAL, aligmentsFolder, bibleType)
    else:
        print(f"No alignments for {bookId} at {bookFolder}")

def getAlignmentsForTestament(connection, newTestament, dataFolder, bibleType):
    books = bible.getBookList(newTestament)
    for book in books:
        print (f"reading {book}")
        if newTestament:
            origLangPath = origLangPathGreek
        else:
            origLangPath = origLangPathHebrew
        saveAlignmentsForBook(connection, book, dataFolder, bibleType, origLangPath)

def findAlignmentForWord(connection, word, searchOriginal):
    match = str(word['id'])
    return findAlignmentFor(connection, match, searchOriginal)

def findAlignmentFor(connection, matchStr, searchOriginal):
    if searchOriginal:
        field = 'orig_lang_words'
    else:
        field = 'target_lang_words'

    search = f"{field} LIKE '%,{matchStr},%'"
    # print(f"search: {search}")
    alignments = fetchRecords(connection, alignment_table, search)
    if len(alignments) > 0:
        # print(f"found match: {alignments[0]}")
        return alignments[0]
    else:
        # print(f"match not found for: {matchStr}")
        return None

def lookupWords(connection, alignment, getOriginalWords):
    if getOriginalWords:
        alignedWords = alignment['orig_lang_words']
        table = original_words_table
    else:
        alignedWords = alignment['target_lang_words']
        table = target_words_table
    words = []
    # print(f"found ID = {foundId}")
    ids = alignedWords.split(",")
    for id in ids:
        if id:
            found = findWordById(connection, id, table)
            if found:
                words.append(found)
    return words

def combineWordList(words):
    words_ = []
    for word in words:
        words_.append(word['word'])
    return ' '.join(words_)

def getSpan(origWords):
    span = 0
    if len(origWords) > 1:
        wordNums = []
        for word in origWords:
            wordNum = int(word['word_num'])
            wordNums.append(wordNum)
        span = max(wordNums) - min(wordNums)
    return span

def getAlignmentForWord(connection, origWord, searchOriginal):
    alignment = findAlignmentForWord(connection, origWord, searchOriginal)

    if alignment:
        # get original language words
        origWords = lookupWords(connection, alignment, 1)
        alignment['origSpan'] = getSpan(origWords)
        alignment['origWords'] = origWords
        origWordsTxt = combineWordList(origWords)
        alignment['origWordsTxt'] = origWordsTxt
        alignment['alignmentOrigWords'] = len(origWords)

        # get target language words
        targetWords = lookupWords(connection, alignment, 0)
        alignment['targetSpan'] = getSpan(targetWords)
        alignment['targetWords'] = targetWords
        targetWordsTxt = combineWordList(targetWords)
        alignment['targetWordsTxt'] = targetWordsTxt
        alignment['alignmentTargetWords'] = len(targetWords)

        alignment['alignmentTxt'] = f"{origWordsTxt} = {targetWordsTxt}"

    return alignment

def findWordById(connection, id, table):
    search = f"id = {str(id)}"
    items = fetchRecords(connection, table, search)
    if items:
        return items[0]
    print(f"findWordById - {id} not found")
    return None

def findWord(connection, word, searchOriginal = True, searchLemma = False, caseInsensitive = False):
    if searchLemma:
        search = f"lemma = '{word}'"
    else:
        search = f"word = '{word}'"

    if searchOriginal:
        table = original_words_table
    else:
        table = target_words_table

    words = fetchRecords(connection, table, search, caseInsensitive)
    # print (f"{len(words)} items in search: {search}")
    return words

def getAlignmentsForWords(connection, words, searchOriginal):
    alignments = []
    for word in words:
        alignment = getAlignmentForWord(connection, word, searchOriginal)
        if alignment:
            alignments.append(alignment)
    return alignments

def findAlignmentsForWord(connection, word, searchOriginal = True, searchLemma = False, caseInsensitive = False):
    foundWords = findWord(connection, word, searchOriginal, searchLemma, caseInsensitive)
    print (f"{len(foundWords)} items in search")

    alignments = getAlignmentsForWords(connection, foundWords, searchOriginal)
    totalCount = len(alignments)
    counts = pd.DataFrame(alignments)['alignmentTxt'].value_counts() # get counts for each match type

    # insert frequency of alignment into table
    for alignment in alignments:
        alignmentText = alignment['alignmentTxt']
        if (alignmentText in counts):
            count = counts[alignmentText]
            ratio = count / totalCount
            alignment['frequency'] = ratio

    df = pd.DataFrame(alignments) # load as dataframe so we can to cool stuff
    return df
