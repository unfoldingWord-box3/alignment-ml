import sqlite3
from sqlite3 import Error

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
        print("Query executed successfully")
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
    select_items = f"SELECT {filter} from {table}"
    items = execute_read_query(connection, select_items)
    return items

