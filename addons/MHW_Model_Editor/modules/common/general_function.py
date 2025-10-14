# Author: NSA Cloud
# V5
import os
import glob
from pathlib import Path
import platform

# ---General Functions---#
os.system("color")  # Enable console colors
from ..common.rw_functions import read_ubyte,read_byte,read_short,read_ushort,read_uint,read_int,read_uint64,\
    read_int64,read_float,read_double,read_string,read_unicode_string,write_ubyte,write_byte,write_short,write_ushort,\
    write_uint,write_int,write_uint64,write_int64,write_float,write_double,write_string,write_unicode_string,\
    getPaddingAmount,getPaddedPos,unsignedToSigned,signedToUnsigned

#######################################################################################################################
#读取mrl3材质的property字典
def read_fields_data(file_object, data_type, endian='<'):
    if data_type == 'float':
        return read_float(file_object, endian)
    elif data_type == 'uint':
        return read_uint(file_object, endian)
    elif data_type == 'int':
        return read_int(file_object, endian)
    elif data_type == 'ubyte':
        return read_ubyte(file_object, endian)
    elif data_type == 'byte':
        return read_byte(file_object, endian)
    elif data_type == 'bbool':
        value = read_uint(file_object, endian)
        return bool(value)
    elif data_type.endswith(']'):
        # 处理数组类型，如 float[4], ubyte[8] 等
        base_type, size = data_type[:-1].split('[')
        size = int(size)
        return [read_fields_data(file_object, base_type, endian) for _ in range(size)]
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def read_fields_dict(file_object, fields_dict, endian='<'):
    for field_name, field_type in list(fields_dict.items()):  # 使用list()避免迭代时修改字典
        # if field_name.startswith('align'):
        #     # 对齐字段，读取但不存储
        #     read_fields_data(file_object, field_type, endian)
        #     del fields_dict[field_name]  # 删除对齐字段
        # else:

        # 读取数据并直接替换原来的类型字符串
        # fields_dict[field_name] = read_fields_data(file_object, field_type, endian)
        fields_dict[field_name] = [fields_dict[field_name]]
        fields_dict[field_name].append(read_fields_data(file_object, field_type, endian))
#######################################################################################################################

def write_fields_data(file_object, value, data_type, endian='<'):
    if data_type == 'float':
        write_float(file_object, value, endian)
    elif data_type == 'uint':
        write_uint(file_object, value, endian)
    elif data_type == 'int':
        write_int(file_object, value, endian)
    elif data_type == 'ubyte':
        write_ubyte(file_object, value, endian)
    elif data_type == 'byte':
        write_byte(file_object, value, endian)
    elif data_type == 'bbool':
        # 将布尔值转换为整数写入
        write_uint(file_object, int(value), endian)
    elif data_type.endswith(']'):
        # 处理数组类型，如 float[4], ubyte[8] 等
        base_type, size = data_type[:-1].split('[')
        size = int(size)
        for item in value:
            write_fields_data(file_object, item, base_type, endian)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def write_fields_dict(file_object, fields_dict, endian='<'):
    for field_name, field_info in fields_dict.items():
        # field_info 应该是 [data_type, value] 格式
        data_type, value = field_info
        write_fields_data(file_object, value, data_type, endian)
#######################################################################################################################



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