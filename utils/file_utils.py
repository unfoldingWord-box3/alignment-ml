import os
import time
import requests
import json
from pathlib import Path

def fetchFile(url):
    print('fetchFile ' + url)
    try:
        data = requests.get(url, allow_redirects=True)
        if data.status_code != 200:
            print(f"Error returned {data.status_code}")
            data = None
    except:
        print(f"Error loading {url}")
        data = None
    return data

def getRepoName(bibleType, bookId):
    fullPath = bibleType + '_' + bookId + '_book'
    # print ('getRepoName ' + fullPath)
    return fullPath

def getBibleUrl(userUrl, bibleType, bookId, chapter):
    fullPath = userUrl + '/' + getRepoName(bibleType, bookId) + '/raw/branch/master/.apps/translationCore/alignmentData/' + bookId + '/' + chapter + '.json'
    print ('getBibleUrl - ' + fullPath)
    return fullPath

def getBookUrl(userUrl, bibleType, bookId):
    repoName = getRepoName(bibleType, bookId)
    fullPath = userUrl + '/' + repoName + '/raw/branch/master/' + repoName + '.usfm'
    print ('getBookUrl - ' + fullPath)
    return fullPath

def fetchAlignments(userUrl, bibleType, bookId, chapter):
    url = getBibleUrl(userUrl, bibleType, bookId, chapter)
    data = fetchFile(url)
    return data

def downloadFile(url, outputPath):
    data = fetchFile(url)
    text = data.text
    print ('downloadAlignments ' + outputPath)
    writeFile(outputPath, text)


def writeFile(outputPath, text):
    f = open(outputPath, "w", encoding='utf-8')
    f.write(text)

def writeJsonFile(outputPath, data):
    text = json.dumps(data, indent=2, ensure_ascii = False)
    f = open(outputPath, "w", encoding='utf-8')
    f.write(text)

def downloadJsonFile(url, outputPath):
    data = fetchFile(url)
    if data:
        text = data.text
        try:
            dataJson = json.loads(text) # make sure json
            f = open(outputPath, "w")
            print ('downloadJsonFile ' + outputPath)
            f.write(text)
        except:
            print (f'downloadJsonFile - file invalid: {url} ')
    else:
        print (f'downloadJsonFile - no data found: {url} ')

def readFile(inputPath):
    f = open(inputPath, "r", encoding='utf-8')
    # print ('readFile ' + inputPath)
    data = f.read()
    return data

def getModifiedTime(filePath):
    modifiedTime = os.path.getmtime(filePath)
    return modifiedTime

def getFileSize(filePath):
    size = os.path.getsize(filePath)
    return size

def readJsonFile(inputPath):
    # print ('readJsonFile ' + inputPath)
    dataStr = readFile(inputPath)
    data = json.loads(dataStr)
    return data

def doesFileExist(path_):
    return os.path.isfile(path_)

def doesFolderExist(path_):
    return os.path.isdir(path_)

def moveFile(srcPath, destPath, ifExists=False, overWrite=False):
    if overWrite and os.path.isfile(destPath):
        print(f"moveFile - removing {destPath}")
        os.remove(destPath)

    if ifExists and not os.path.isfile(srcPath):
        print(f"moveFile - file not found {srcPath}")
        return

    os.rename(srcPath, destPath)

def makeFolder(outputFolder):
    if not os.path.isdir(outputFolder):
        print ('makeFolder - creating folder ' + outputFolder)
        os.mkdir(outputFolder)
    return True

def ensureFolderExists(outputFolder):
    if os.path.isdir(outputFolder):
        return True

    parts = outputFolder.split('/')
    if len(parts) > 1:
        parent = '/'.join(parts[0:len(parts)-1])
        if not os.path.isdir(parent):
            ensureFolderExists(parent)
        makeFolder(outputFolder)
    return True

def removeFolder(outputFolder):
    if os.path.isdir(outputFolder):
        try:
            os.rmdir(outputFolder)
            print ('removeFolder - removed folder ' + outputFolder)
            return 1
        except OSError as e:
            print (f"removeFolder - removing '{outputFolder}' failed, error {e.strerror}")
    else:
        print ('removeFolder - folder not found' + outputFolder)
    return 0

def removeEmptyFolder(folderPath):
    files = listFolder(folderPath)

    if files is not None: # files not None
        if (len(files) == 0): # if empty
            print(f"removeEmptyFolder - removing {folderPath}")
            removeFolder(folderPath)

def listFolder(outputFolder):
    if os.path.isdir(outputFolder):
        # print ('listFolder - ' + outputFolder)
        files = os.listdir(outputFolder)
        return files
    print ('listFolder - folder not found: ' + outputFolder)
    return None

def initJsonFile(keyTermsPath):
    try:
        data = readJsonFile(keyTermsPath)
    except FileNotFoundError:
        data = {} # initialize data if not found
    return data
