# Author: NSA Cloud
# V5
import os
import glob
from pathlib import Path
import platform

# ---General Functions---#
os.system("color")  # Enable console colors

# bitflag operations
def getBit(bitFlag, index):  # Index starting from rightmost bit
    return bool((bitFlag >> index) & 1)


def setBit(bitFlag, index):
    return bitFlag | (1 << index)


def unsetBit(bitFlag, index):
    return bitFlag & ~(1 << index)


def dictString(dictionary):  # Return string of dictionary contents
    outputString = ""
    for key, value in dictionary.items():
        outputString += str(key) + ": " + str(value) + "\n"
    return outputString





def getFolderSize(path='.'):
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += getFolderSize(entry.path)
    except:
        total = -1
    return total


def formatByteSize(num, suffix="B"):
    for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def wildCardFileSearch(wildCardFilePath):  # Returns first file found matching wildcard, none if not found
    search = glob.glob(wildCardFilePath)
    if search == []:
        search = [None]
    return search[0]


def wildCardFileSearchList(wildCardFilePath):  # Returns all files matching wildcard
    search = glob.glob(wildCardFilePath)
    return search


CHUNK_FOLDERS = {"nativepc", "chunk", "chunkg0", "chunkg1", "chunkg2",
                 "chunkg3", "chunkg4", "chunkg5", "chunkg6", "chunkg7",
                 "chunkg8", "chunkg9", "chunkg10", "chunkg60"}
'''这个函数可能要修改'''
def splitNativesPath(filePath):  # Splits file path of MHW Chunk or nativePC folder, returns none if there's no such folder
    path = Path(filePath)
    parts = path.parts

    target_index = [
        i for i, part in enumerate(parts)
        if part.lower() in CHUNK_FOLDERS
    ]
    if not target_index:
        return None

    target_index = target_index[-1]  # 取最后一个匹配的索引，避免嵌套目录误判（如...\chunk\chunkg0）
    rootPath = str(Path(*parts[:target_index + 1]))  # D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC
    subPath = str(Path(*parts[target_index + 1:]))  # pl\f_equip\pl045_0020\body\mod\f_body045_0020.mod3

    return rootPath, subPath



def getAdjacentFileVersion(rootPath, fileType):
    fileVersion = -1
    search = wildCardFileSearch(os.path.join(glob.escape(rootPath), "*" + fileType + "*"))
    if search != None:
        versionExtension = os.path.splitext(search)[1][1::]
        if versionExtension.isdigit():
            fileVersion = int(versionExtension)
    return fileVersion


def progressBar(iterable, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    total = len(iterable)

    # Progress Bar Printing Function
    def printProgressBar(iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()


IS_WINDOWS = platform.system() == 'Windows'


def resolvePath(pathString):
    if IS_WINDOWS:
        return pathString
    else:  # Fix issues related to case sensitive paths on linux, doesn't matter on windows
        newPath = pathString.replace("/", os.sep).replace("\\", os.sep)
        if not os.path.isfile(newPath):  # Lower case the path in case the pak list is lowercased
            newPath = newPath.lower()
            return newPath

def string_reformat(s):
    if s[0] in ["t", "b", "f", "i"]:
        s = s[1:]
    elif s.startswith("SS") or s.startswith("CB"):
        s = s[2:]
    return s.split("__")[0]