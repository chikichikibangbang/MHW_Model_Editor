import os
import bpy
from .....common.i18n.i18n import i18n
from ..common.message_functions import textColors, raiseError, raiseWarning
from ..common.rw_functions import read_ubyte,read_byte,read_short,read_ushort,read_uint,read_int,read_uint64,\
    read_int64,read_float,read_double,read_string,read_unicode_string,write_ubyte,write_byte,write_short,write_ushort,\
    write_uint,write_int,write_uint64,write_int64,write_float,write_double,write_string,write_unicode_string,\
    getPaddingAmount,getPaddedPos

class SIZE_DATA():
    def __init__(self):
        self.HEADER_SIZE = 16
        self.COLLISION_SIZE = 64

class FileHeader():
    def __init__(self):
        self.Magic = 4997955
        self.Version = 525848

        self.ColCount = 0
        self.ColTotalOffset = 0

    def read(self, file):
        self.Magic = read_uint(file)
        if self.Magic != 4997955:
            raise Exception(i18n("File is not a MHW CCL file."))
        self.Version = read_uint(file)

        self.ColCount = read_uint(file)
        self.ColTotalOffset = read_uint(file)

    def write(self,file):
        write_uint(file, self.Magic)
        write_uint(file, self.Version)

        write_uint(file, self.ColCount)
        write_uint(file, self.ColTotalOffset)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Collision():
    def __init__(self):
        self.StartID = 0
        self.EndID = 0
        self.ColShape = 1
        self.StartPos = [0.0, 0.0, 0.0]
        self.EndPos = [0.0, 0.0, 0.0]
        self.ColRadius = 8.0

        # parse用
        self.StartName = ""
        self.EndName = ""

    def read(self, file):
        file.seek(4, 1)
        self.StartID = read_ushort(file)
        self.EndID = read_ushort(file)
        self.StartName = "MhBone_" + str(self.StartID).zfill(3)
        self.EndName = "MhBone_" + str(self.EndID).zfill(3)

        self.ColShape = read_ubyte(file)
        file.seek(7, 1)

        self.StartPos = []
        for i in range(3):
            self.StartPos.append(read_float(file))
        file.seek(4, 1)

        self.EndPos = []
        for i in range(3):
            self.EndPos.append(read_float(file))

        self.ColRadius = read_float(file)
        file.seek(16, 1)

    def write(self,file):
        write_uint(file, 0)
        write_ushort(file, self.StartID)
        write_ushort(file, self.EndID)
        write_ubyte(file, self.ColShape)
        file.write(b'\xCD' * 7)
        for val in self.StartPos:
            write_float(file, val)
        write_uint(file, 0)
        for val in self.EndPos:
            write_float(file, val)
        write_float(file, self.ColRadius)
        file.write(b'\x00' * 12)
        file.write(b'\xCD' * 4)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class CCLFile():
    def __init__(self):
        self.sd = SIZE_DATA()
        self.Header = FileHeader()
        self.CollisionList = []
        self.misBoneSet = set()
        self.totalCount = 0

    def read(self, file, fileSize, bones):
        # totalSize = self.sd.HEADER_SIZE + \
        #             self.sd.COLLISION_SIZE * self.Header.ColCount
        # if totalSize > fileSize:
        #     raise Exception("Total byte length exceeds file size.")

        self.Header.read(file)

        # if self.Header.ColCount:
        #     for i in range(0, self.Header.ColCount):

        # 经测试游戏读取ccl文件的碰撞体时，不和header里的count或offset挂钩，也就是说即使数量不匹配也不影响碰撞体生效，所以这里使用while遍历
        while file.tell() < fileSize:
            entry = Collision()
            entry.read(file)
            self.totalCount += 1

            # 检查头尾节点是否有对应骨骼
            if not bones.get(entry.StartName):
                self.misBoneSet.add(entry.StartName)
            elif entry.ColShape == 1 and not bones.get(entry.EndName):
                self.misBoneSet.add(entry.EndName)
            else:
                self.CollisionList.append(entry)

    def write(self, file):
        self.Header.write(file)
        for col in self.CollisionList:
            col.write(file)


#---MHW CCL IO FUNCTIONS---#
def readCCLFile(filepath, bones):
    lang = bpy.context.preferences.view.language
    print(i18n("Opening ") + filepath)
    try:
        fileSize = os.path.getsize(filepath)
        file = open(filepath, "rb", buffering=8192)
    except:
        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            raiseError(f"打开 {filepath} 失败")
        else:
            raiseError(f"Failed to open {filepath}")

    cclFile = CCLFile()
    cclFile.read(file, fileSize, bones)
    file.close()
    return cclFile

def writeCCLFile(cclFile, filepath):
    lang = bpy.context.preferences.view.language
    print(i18n("Writing to ") + filepath)
    try:
        file = open(filepath, "wb", buffering=8192)
    except:
        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            raiseError(f"打开 {filepath} 失败")
        else:
            raiseError(f"Failed to open {filepath}")

    cclFile.write(file)
    file.close()