import os
import requests
import json

def fetchFile(url):
    print('fetchFile ' + url)
    try:
        data = requests.get(url, allow_redirects=True)
    except:
        print(f"Error loading {url}")
        data = ''
    return data

def getRepoName(bibleType, bookId):
    fullPath = bibleType + '_' + bookId + '_book'
    # print ('getRepoName ' + fullPath)
    return fullPath

def getBibleUrl(userUrl, bibleType, bookId, chapter):
    fullPath = userUrl + '/' + getRepoName(bibleType, bookId) + '/raw/branch/master/.apps/translationCore/alignmentData/' + bookId + '/' + chapter + '.json'
    print ('getBibleUrl ' + fullPath)
    return fullPath

def fetchAlignments(userUrl, bibleType, bookId, chapter):
    url = getBibleUrl(userUrl, bibleType, bookId, chapter)
    data = fetchFile(url)
    return data

def downloadFile(url, outputPath):
    data = fetchFile(url)
    text = data.text
    f = open(outputPath, "w")
    print ('downloadAlignments ' + outputPath)
    f.write(text)

def downloadJsonFile(url, outputPath):
    data = fetchFile(url)
    text = data.text
    try:
        dataJson = json.loads(text) # make sure json
        f = open(outputPath, "w")
        print ('downloadJsonFile ' + outputPath)
        f.write(text)
    except:
        print (f'downloadJsonFile - file invalid: {url} ')

def readFile(inputPath):
    f = open(inputPath, "r")
    # print ('readFile ' + inputPath)
    data = f.read()
    return data

def makeFolder(outputFolder):
    if not os.path.isdir(outputFolder):
        print ('makeFolder - creating folder ' + outputFolder)
        os.mkdir(outputFolder)

def readJsonFile(inputPath):
    # print ('readJsonFile ' + inputPath)
    data = readFile(inputPath)
    dict = json.loads(data)
    return dict
