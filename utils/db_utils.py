import sqlite3
from sqlite3 import Error
import utils.file_utils as file
import utils.bible_utils as bible

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

def getWordsFromVerse(verseObjects):
    words = []
    for i in range(len(verseObjects)):
        vo = verseObjects[i]
        type_ = vo['type']
        if (type_ == 'word'):
            # print(f'At {i} Found word: {vo}')
            words.append(vo)
        elif (type_ == 'milestone'):
            children = vo['children']
            # print(f"At {i} Found children: {len(children)}")
            child_words = getWordsFromVerse(children)
            words.extend(child_words)
            # print('finished processing children')
    return words

def getVerseWordsFromChapter(chapter_dict, verse):
    words = getWordsFromVerse(chapter_dict[verse]['verseObjects'])
    return words

def getOccurrances(text, words):
    count = 0
    for word in words:
        if (word['word'] == text):
            count = count + 1
    return count

def getDbWordsForVerse(words, bookId, chapter, verse):
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
            'occurrance': getOccurrances(text, db_words) + 1,
            'strong': word['strong'],
            'lemma': word['lemma'],
            'morph': word['morph']
        }
        # print(f'At {i} new word entry: {db_word}')
        db_words.append(db_word)
    return db_words

def createCommandToAddToDatabase(table, data):
    header = ''
    for key, value in data[0].items():
        if (len(header) > 0) :
            header = header + ', '
        header = header + key

    dataStr = ''
    length = len(data)
    for i in range(length):
        db_word = data[i]
        line = ''
        for key, value in db_word.items():
            if (len(line) > 0) :
                line = line + ', '
            else:
                line = '  ('

            if isinstance(value, str):
                line = f"{line}'{value}'"
            else:
                line = f"{line}{value}"
        dataStr = dataStr + line
        if (i < length - 1):
            dataStr = dataStr + '),\n'
        else:
            dataStr = dataStr + ');\n'

    add_words = f"INSERT INTO\n  {table} ({header})\nVALUES\n{dataStr}"
    return add_words

def addMultipleItemsToDatabase(connection, table, db_words):
    add_words = createCommandToAddToDatabase(table, db_words)
    execute_query(connection, add_words)

def getRecords(connection, table, filter):
    select_items = f"SELECT * FROM {table}"
    if len(filter):
        select_items = select_items + f"\nWHERE {filter}"
    print(f"getRecords:\n{select_items}")
    items = execute_read_query(connection, select_items)
    return items

def deleteWordsForBook(connection, table, bookId):
    selection = f"book_id = '{bookId}'"
    deleteBook = f"DELETE FROM {table}\nWHERE {selection};\n"
    print(f"deleteWordsForBook:\n{deleteBook}")
    execute_query(connection, deleteBook)

def loadAllWordsFromBookIntoDB(connection, origLangPath, bookId, table):
    deleteWordsForBook(connection, table, bookId)

    foundNonNumericalVerse = 0
    chapters = bible.getChaptersForBook(bookId)
    for chapter in chapters:
        print(f"{bookId} - Reading chapter {chapter}")

        chapterPath = f"{origLangPath}/{bookId}/{chapter}.json"
        chapter_dict = file.readJsonFile(chapterPath)

        for verse, verseData in chapter_dict.items():
            try:
                verseNum = int(verse) # make sure its a number
                # print(f"Reading verse {verse}")
                words = getVerseWordsFromChapter(chapter_dict, verse)
                db_words = getDbWordsForVerse(words, bookId, chapter, verse)

                # print(f"For {chapter}:{verse} Saving {len(db_words)}")

                addMultipleItemsToDatabase(connection, table, db_words)
            except:
                # print(f"Skipping verse {verse}")
                foundNonNumericalVerse = 1

def loadAllWordsFromTestamentIntoDB(connection, origLangPath, newTestament, table):
    books = bible.getBookList(newTestament)
    for book in books:
        print (f"reading {book}")
        loadAllWordsFromBookIntoDB(connection, origLangPath, book, table)