from ..common.general_function import textColors,raiseWarning,raiseError,getPaddingAmount,read_uint,read_int,\
    read_uint64,read_int64,read_float,read_ushort,read_ubyte,read_unicode_string,read_byte,read_short,write_uint,\
    write_int,write_uint64,write_int64,write_float,write_ushort,write_ubyte,write_unicode_string,write_byte,write_short
import math

class SIZE_DATA():
    def __init__(self):
        self.HEADER_SIZE = 16
        self.CCL_COLLISION_SIZE = 64

class CCLHeaderData():
    def __init__(self):
        self.magic = 4997955
        self.Version = 525848

        self.CCLCollisionCount = 0
        self.CCLCollisionTotalOffset = 0

    def read(self, file):
        print("Reading CCL Header...")
        self.magic = read_uint(file)
        if self.magic != 4997955:
            raiseError("File is not a ccl file.")

        self.Version = read_uint(file)

        self.CCLCollisionCount = read_int(file)
        self.CCLCollisionTotalOffset = read_int(file)

    def write(self,file):
        write_uint(file, self.magic)
        write_uint(file, self.Version)

        write_int(file, self.CCLCollisionCount)
        write_int(file, self.CCLCollisionTotalOffset)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)




class CCLCollisionData():
    def __init__(self):
        self.startboneID = 0
        self.endboneID = 0
        self.ColShape = 1
        self.startPosX = 0.0
        self.startPosY = 0.0
        self.startPosZ = 0.0
        self.endPosX = 0.0
        self.endPosY = 0.0
        self.endPosZ = 0.0
        self.ColRadius = 8.0

    def read(self, file):
        file.seek(4, 1)
        self.startboneID = read_short(file)
        self.endboneID = read_short(file)
        self.ColShape = read_byte(file)
        file.seek(7, 1)
        self.startPosX = read_float(file)
        self.startPosY = read_float(file)
        self.startPosZ = read_float(file)
        file.seek(4, 1)
        self.endPosX = read_float(file)
        self.endPosY = read_float(file)
        self.endPosZ = read_float(file)
        self.ColRadius = read_float(file)
        file.seek(16, 1)

    def write(self,file):
        write_uint(file, 0)
        write_short(file, self.startboneID)
        write_short(file, self.endboneID)
        write_byte(file, self.ColShape)
        write_byte(file, -51)
        write_short(file, -12851)
        write_int(file, -842150451)
        write_float(file, self.startPosX)
        write_float(file, self.startPosY)
        write_float(file, self.startPosZ)
        write_uint(file, 0)
        write_float(file, self.endPosX)
        write_float(file, self.endPosY)
        write_float(file, self.endPosZ)
        write_float(file, self.ColRadius)
        write_uint(file, 0)
        write_uint(file, 0)
        write_uint(file, 0)
        write_int(file, -842150451)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class CCLFile():
    def __init__(self):
        self.Header = CCLHeaderData()
        self.sizeData = SIZE_DATA()
        self.CCLCollisionList = []


    def read(self, file):
        self.Header.read(file)

        if self.Header.CCLCollisionCount > 0:
            print("Reading CCL Collisions...")

        for i in range(0, self.Header.CCLCollisionCount):
            newCCLCollision = CCLCollisionData()
            newCCLCollision.read(file)
            currentPos = file.tell()
            self.CCLCollisionList.append(newCCLCollision)

    def write(self, file):
        self.Header.write(file)

        for cclCollision in self.CCLCollisionList:
            cclCollision.write(file)


def readCCL(filepath):
    print(textColors.OKCYAN + "__________________________________\nCCL read started." + textColors.ENDC)
    print("Opening " + filepath)
    try:
        file = open(filepath, "rb")
    except:
        raiseError("Failed to open " + filepath)

    cclFile = CCLFile()
    cclFile.read(file)
    file.close()
    print(textColors.OKGREEN + "__________________________________\nCCL read finished." + textColors.ENDC)
    return cclFile

def writeCCL(cclFile, filepath):
    print(textColors.OKCYAN + "__________________________________\nCCL write started." + textColors.ENDC)
    print("Opening " + filepath)
    try:
        file = open(filepath, "wb")
    except:
        raiseError("Failed to open " + filepath)

    cclFile.write(file)
    file.close()
    print(textColors.OKGREEN + "__________________________________\nCCL write finished." + textColors.ENDC)
