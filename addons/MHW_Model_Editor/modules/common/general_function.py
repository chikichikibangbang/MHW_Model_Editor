# Author: NSA Cloud
# V5
import os
import struct
import glob
from pathlib import Path
import platform

# ---General Functions---#
os.system("color")  # Enable console colors


class textColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# read unsigned byte from file
def read_ubyte(file_object, endian='<'):
    data = struct.unpack(endian + 'B', file_object.read(1))[0]
    return data


# read signed byte from file
def read_byte(file_object, endian='<'):
    data = struct.unpack(endian + 'b', file_object.read(1))[0]
    return data


# read signed short from file
def read_short(file_object, endian='<'):
    data = struct.unpack(endian + 'h', file_object.read(2))[0]
    return data


# read unsigned short from file
def read_ushort(file_object, endian='<'):
    data = struct.unpack(endian + 'H', file_object.read(2))[0]
    return data


# read unsigned integer from filel
def read_uint(file_object, endian='<'):
    data = struct.unpack(endian + 'I', file_object.read(4))[0]
    return data


# read signed integer from file
def read_int(file_object, endian='<'):
    data = struct.unpack(endian + 'i', file_object.read(4))[0]
    return data


# read unsigned long integer from file
def read_uint64(file_object, endian='<'):
    data = struct.unpack(endian + 'Q', file_object.read(8))[0]
    return data


# read signed long integer from file
def read_int64(file_object, endian='<'):
    data = struct.unpack(endian + 'q', file_object.read(8))[0]
    return data


# read floating point number from file
def read_float(file_object, endian='<'):
    data = struct.unpack(endian + 'f', file_object.read(4))[0]
    return data


# read double from file
def read_double(file_object, endian='<'):
    data = struct.unpack(endian + 'd', file_object.read(8))[0]
    return data


# read null terminated string from file
def read_string(file_object):
    data = ''.join(iter(lambda: file_object.read(1).decode('ascii'), '\x00'))
    return data


def read_unicode_string(file_object):  # Reads unicode string from file into utf-8 string
    wchar = file_object.read(2)
    byteString = wchar
    while wchar != b'\x00\x00':
        wchar = file_object.read(2)
        byteString += wchar
    unicodeString = byteString.decode("utf-16le").replace('\x00', '')
    return unicodeString

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

# write unsigned byte to file
def write_ubyte(file_object, input, endian='<'):
    data = struct.pack(endian + 'B', input)
    file_object.write(data)


# write signed byte to file
def write_byte(file_object, input, endian='<'):
    data = struct.pack(endian + 'b', input)
    file_object.write(data)


# write signed short to file
def write_short(file_object, input, endian='<'):
    data = struct.pack(endian + 'h', input)
    file_object.write(data)


# write unsigned short to file
def write_ushort(file_object, input, endian='<'):
    data = struct.pack(endian + 'H', input)
    file_object.write(data)


# write unsigned integer to file
def write_uint(file_object, input, endian='<'):
    data = struct.pack(endian + 'I', input)
    file_object.write(data)


# write signed integer to file
def write_int(file_object, input, endian='<'):
    data = struct.pack(endian + 'i', input)
    file_object.write(data)


# write unsigned long integer to file
def write_uint64(file_object, input, endian='<'):
    data = struct.pack(endian + 'Q', input)
    file_object.write(data)


# write unsigned long integer to file
def write_int64(file_object, input, endian='<'):
    data = struct.pack(endian + 'q', input)
    file_object.write(data)


# write floating point number to file
def write_float(file_object, input, endian='<'):
    data = struct.pack(endian + 'f', input)
    file_object.write(data)


# write double to file
def write_double(file_object, input, endian='<'):
    data = struct.pack(endian + 'd', input)
    file_object.write(data)


# write null terminated string to file
def write_string(file_object, input):
    input += '\x00'
    data = bytes(input, 'utf-8')
    file_object.write(data)


def write_unicode_string(file_object, input):  # Writes utf-8 string as utf-16
    data = input.encode('UTF-16LE') + b'\x00\x00'  # Little endian utf16
    file_object.write(data)


def getPaddingAmount(currentPos, alignment):
    padding = (currentPos * -1) % alignment
    return padding


# bitflag operations
def getBit(bitFlag, index):  # Index starting from rightmost bit
    return bool((bitFlag >> index) & 1)


def setBit(bitFlag, index):
    return bitFlag | (1 << index)


def unsetBit(bitFlag, index):
    return bitFlag & ~(1 << index)


def raiseError(error, errorCode=999):
    try:
        raise Exception()
    except Exception:
        print(textColors.FAIL + "ERROR: " + error + textColors.ENDC)


def raiseTexError(error, errorCode=999):
    print(textColors.FAIL + "ERROR: " + error + textColors.ENDC)
    raise Exception(error)


def raiseWarning(warning):
    print(textColors.WARNING + "WARNING: " + warning + textColors.ENDC)


def getByteSection(byteArray, offset, size):
    data = byteArray[offset:(offset + size)]
    return data


def removeByteSection(byteArray, offset, size):  # removes specified amount of bytes from byte array at offset
    del byteArray[offset:(offset + size)]  # Deletes directly from the array passed to it


def insertByteSection(byteArray, offset, input):  # inserts bytes into bytearray at offset
    byteArray[offset:offset] = input


def dictString(dictionary):  # Return string of dictionary contents
    outputString = ""
    for key, value in dictionary.items():
        outputString += str(key) + ": " + str(value) + "\n"
    return outputString


def unsignedToSigned(uintValue):
    intValue = uintValue & ((1 << 32) - 1)
    intValue = (intValue & ((1 << 31) - 1)) - (intValue & (1 << 31))
    return intValue


def signedToUnsigned(intValue):
    return intValue & 0xffffffff


def getPaddedPos(currentPos, alignment):
    paddedPos = ((currentPos * -1) % alignment) + currentPos
    return paddedPos


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


CHUNK_FOLDERS = ("nativepc", "chunk", "chunkg0", "chunkg1", "chunkg2", "chunkg3", "chunkg04", "chunkg05", "chunkg06", "chunkg7", "chunkg8", "chunkg09", "chunkg10", "chunkg60")
'''这个函数可能要修改'''
def splitNativesPath(filePath):  # Splits file path of MHW Chunk or nativePC folder, returns none if there's no such folder
    path = Path(filePath)
    parts = path.parts

    # target_index = next(
    #     i for i, part in enumerate(parts)
    #     if part.lower() in CHUNK_FOLDERS
    # )
    target_index = [
        i for i, part in enumerate(parts)
        if part.lower() in CHUNK_FOLDERS
    ]
    if not target_index:
        return None
    target_index = target_index[-1]  # 取最后一个匹配的索引，避免嵌套目录误判（如...\chunk\chunkg0）
    rootPath = str(Path(*parts[:target_index + 1])) # D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC
    subPath = str(Path(*parts[target_index + 1:])) # pl\f_equip\pl045_0020\body\mod\f_body045_0020.mod3
    return (rootPath, subPath)



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