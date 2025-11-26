import math
import ctypes
import os
import bpy
import numpy as np
from .....common.i18n.i18n import i18n
from ..common.rw_functions import read_ubyte,read_byte,read_short,read_ushort,read_uint,read_int,read_uint64,\
    read_int64,read_float,read_double,read_string,read_unicode_string,write_ubyte,write_byte,write_short,write_ushort,\
    write_uint,write_int,write_uint64,write_int64,write_float,write_double,write_string,write_unicode_string,\
    getPaddingAmount,getPaddedPos
from ..common.message_functions import raiseWarning, raiseError, textColors

class Matrix4x4():
    def __init__(self):
        self.matrix = [[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0],[0.0,0.0,0.0,0.0]]
    def read(self,file):
        self.matrix = np.frombuffer(file.read(64),dtype="<4f").tolist()
    def write(self,file):
        for row in self.matrix:
            for val in row:
                write_float(file,val)
    def invert(self):
        """对矩阵求逆"""
        np_mat = np.array(self.matrix, dtype=np.float32)
        self.matrix = np.linalg.inv(np_mat).tolist()

class SIZE_DATA():
    def __init__(self):
        self.HEADER_SIZE = 80
        self.CHAIN_SIZE = 80
        self.NODE_SIZE = 112

class FileHeader():
    def __init__(self):
        self.Magic = 4412483
        self.Version = 28

        self.Unkn1 = 0
        self.Unkn2 = 1000

        self.ChainCount = 0
        self.NodeCount = 0

        self.AttributeFlags = 64
        self.StepTime = 1/60

        self.GravityScaling = 1.0
        self.GlobalDamping = 0.0
        self.GlobalTransForceCoef = 1.0
        self.SpringScaling = 1.0

        self.WindScale = 0.6
        self.WindScaleMin = 0.3
        self.WindScaleMax = 1.0

        self.WindScaleWeight = [0.2, 0.7, 0.1]

        self.SolveStrNum = 1
        self.SolveAngNum = 1
        self.SolveMdlColNum = 1
        self.SolveSelColNum = 1
        self.SolveScrColNum = 1
        self.SolveChnColNum = 1

    def read(self, file):
        self.Magic = read_uint(file)
        if self.Magic != 4412483:
            raise Exception(i18n("File is not a MHW CTC file."))
        self.Version = read_uint(file)
        file.seek(8, 1)

        self.ChainCount = read_uint(file)
        self.NodeCount = read_uint(file)

        self.AttributeFlags = read_uint(file)
        self.StepTime = read_float(file)

        self.GravityScaling = read_float(file)
        self.GlobalDamping = read_float(file)
        self.GlobalTransForceCoef = read_float(file)
        self.SpringScaling = read_float(file)

        self.WindScale = read_float(file)
        self.WindScaleMin = read_float(file)
        self.WindScaleMax = read_float(file)

        self.WindScaleWeight = []
        for i in range(3):
            self.WindScaleWeight.append(read_float(file))

        file.seek(8, 1)

    def write(self,file):
        write_uint(file, self.Magic)
        write_uint(file, self.Version)

        write_uint(file, self.Unkn1)
        write_uint(file, self.Unkn2)

        write_uint(file, self.ChainCount)
        write_uint(file, self.NodeCount)

        write_uint(file, self.AttributeFlags)
        write_float(file, self.StepTime)

        write_float(file, self.GravityScaling)
        write_float(file, self.GlobalDamping)
        write_float(file, self.GlobalTransForceCoef)
        write_float(file, self.SpringScaling)

        write_float(file, self.WindScale)
        write_float(file, self.WindScaleMin)
        write_float(file, self.WindScaleMax)

        for val in self.WindScaleWeight:
            write_float(file, val)

        file.write(b'\x01' * 6)
        file.write(b'\x00' * 2)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


c_int32 = ctypes.c_int32
class CollisionAttrFlag_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("CollisionFlags_None", c_int32, 1),
        ("CollisionSelfEnable", c_int32, 1),
        ("CollisionModelEnable", c_int32, 1),
        ("CollisionVGroundEnable", c_int32, 1),
    ]
class ColAttrFlag(ctypes.Union):
    _anonymous_ = ("flagValues",)
    _fields_ = [
        ("flagValues", CollisionAttrFlag_bits),
        ("asInt32", c_int32)
    ]
class ChaAttrFlag_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("AngleLimitEnable", c_int32, 1),
        ("AngleLimitRestitutionEnable", c_int32, 1),
        ("EndRotConstraintEnable", c_int32, 1),
        ("TransAnimationEnable", c_int32, 1),
        ("AngleFreeEnable", c_int32, 1),
        ("StretchBothEnable", c_int32, 1),
        ("PartBlendEnable", c_int32, 1),
    ]
class ChaAttrFlag(ctypes.Union):
    _anonymous_ = ("flagValues",)
    _fields_ = [
        ("flagValues", ChaAttrFlag_bits),
        ("asInt32", c_int32)
    ]

class Chain():
    def __init__(self):
        self.NodeCount = 0

        self.CollisionAttrFlag = ColAttrFlag()
        self.CollisionAttrFlag.asInt32 = 4
        self.ChainAttrFlag = ChaAttrFlag()
        self.ChainAttrFlag.asInt32 = 39
        self.UnknAttrFlag1 = 0
        self.UnknAttrFlag2 = 0

        self.ColAttribute = -1
        self.ColGroup = 1
        self.ColType = 1

        self.Gravity = [0.0, -980.0, 0.0]

        self.Damping = 0.0
        self.TransForceCoef = 0.2
        self.SpringCoef = 0.01

        self.LimitForce = 100.0
        self.FrictionCoef = 0.0
        self.ReflectCoef = 0.1

        self.WindRate = 0.1
        self.WindLimit = -1

        self.NodeList = []

    def read(self,file):
        self.NodeCount = read_uint(file)

        self.CollisionAttrFlag.asInt32 = read_ubyte(file)
        self.ChainAttrFlag.asInt32 = read_ubyte(file)
        self.UnknAttrFlag1 = read_ubyte(file)
        self.UnknAttrFlag2 = read_ubyte(file)

        self.ColAttribute = read_int(file)
        self.ColGroup = read_int(file)
        self.ColType = read_int(file)
        file.seek(12, 1)

        self.Gravity = []
        for i in range(3):
            self.Gravity.append(read_float(file))
        file.seek(4, 1)

        self.Damping = read_float(file)
        self.TransForceCoef = read_float(file)
        self.SpringCoef = read_float(file)

        self.LimitForce = read_float(file)
        self.FrictionCoef = read_float(file)
        self.ReflectCoef = read_float(file)

        self.WindRate = read_float(file)
        self.WindLimit = read_short(file)
        file.seek(2, 1)

    def write(self,file):
        write_uint(file, self.NodeCount)

        write_ubyte(file, self.CollisionAttrFlag.asInt32)
        write_ubyte(file, self.ChainAttrFlag.asInt32)

        write_ubyte(file, self.UnknAttrFlag1)
        write_ubyte(file, self.UnknAttrFlag2)

        write_int(file, self.ColAttribute)
        write_int(file, self.ColGroup)
        write_int(file, self.ColType)
        file.write(b'\xCD' * 12)

        for val in self.Gravity:
            write_float(file, val)
        file.seek(4, 1)

        write_float(file, self.Damping)
        write_float(file, self.TransForceCoef)
        write_float(file, self.SpringCoef)

        write_float(file, self.LimitForce)
        write_float(file, self.FrictionCoef)
        write_float(file, self.ReflectCoef)

        write_float(file, self.WindRate)
        write_short(file, self.WindLimit)
        file.write(b'\xCD' * 2)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Node():
    def __init__(self):
        self.NodeMatrix = Matrix4x4()

        self.UnknByte1 = 0
        self.IsParent = 0
        self.UnknByte2 = 0

        self.AngleMode = 1
        self.CollisionShape = 1
        self.UnknEnum = 1

        self.BoneFunctionID = 150
        self.BoneName = ""  # parse用

        self.BoneColRadius = 3.0
        self.AngleLimitRadius = math.pi / 4
        self.WidthRate = 1.0
        self.Mass = 1.0
        self.ElasticCoef = 1.0

    def read(self, file):
        self.NodeMatrix.read(file)
        file.seek(1, 1)

        self.UnknByte1 = read_ubyte(file)
        self.IsParent = read_ubyte(file)
        self.UnknByte2 = read_ubyte(file)

        self.AngleMode = read_ubyte(file)
        file.seek(1, 1)
        self.CollisionShape = read_ubyte(file)
        self.UnknEnum = read_ubyte(file)

        self.BoneFunctionID = read_ushort(file)
        self.BoneName = "MhBone_" + str(self.BoneFunctionID).zfill(3)
        file.seek(6, 1)

        self.BoneColRadius = read_float(file)
        self.AngleLimitRadius = read_float(file)
        self.WidthRate = read_float(file)
        self.Mass = read_float(file)
        self.ElasticCoef = read_float(file)
        file.seek(12, 1)

    def write(self, file):
        self.NodeMatrix.write(file)
        file.seek(1, 1)

        write_ubyte(file, self.UnknByte1)
        write_ubyte(file, self.IsParent)
        write_ubyte(file, self.UnknByte2)

        write_ubyte(file, self.AngleMode)
        file.seek(1, 1)
        write_ubyte(file, self.CollisionShape)
        write_ubyte(file, self.UnknEnum)

        write_ushort(file, self.BoneFunctionID)
        file.seek(6, 1)

        write_float(file, self.BoneColRadius)
        write_float(file, self.AngleLimitRadius)
        write_float(file, self.WidthRate)
        write_float(file, self.Mass)
        write_float(file, self.ElasticCoef)
        file.write(b'\xCD' * 12)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class CTCFile():
    def __init__(self):
        self.sd = SIZE_DATA()
        self.Header = FileHeader()
        self.ChainList = []
        self.NodeList = []
        self.misBoneSet = set()

    def read(self, file, fileSize, bones):
        # totalSize = self.sd.HEADER_SIZE + \
        #             self.sd.CHAIN_SIZE * self.Header.ChainCount + self.sd.NODE_SIZE * self.Header.NodeCount
        # if totalSize > fileSize:
        #     raise Exception("Total byte length exceeds file size.")

        self.Header.read(file)
        '''待做，考虑检查所有node是否有重复的BoneFunctionID，不过不影响导入就是了'''

        if self.Header.ChainCount and self.Header.NodeCount:
            # node偏移的累计值
            nodeStartOffset = self.sd.HEADER_SIZE + self.sd.CHAIN_SIZE * self.Header.ChainCount

            for i in range(0, self.Header.ChainCount):
                chainEntry = Chain()
                chainEntry.read(file)

                # 若chain的链长为0或1，则累加node偏移，然后跳过当前循环
                if chainEntry.NodeCount in {0, 1}:
                    nodeStartOffset += self.sd.NODE_SIZE * chainEntry.NodeCount
                    continue

                currentPos = file.tell()
                file.seek(nodeStartOffset)  # 跳转到当前链的起始node偏移位置
                for j in range(0, chainEntry.NodeCount):
                    nodeEntry = Node()
                    nodeEntry.read(file)

                    # 若当前node找不到对应的骨骼，则跳过该node
                    if not bones.get(nodeEntry.BoneName):
                        self.misBoneSet.add(nodeEntry.BoneName)
                        continue

                    chainEntry.NodeList.append(nodeEntry)

                # 累加偏移值
                nodeStartOffset += self.sd.NODE_SIZE * chainEntry.NodeCount
                file.seek(currentPos)

                if len(chainEntry.NodeList) not in {0, 1}:
                    self.ChainList.append(chainEntry)

    def write(self, file):
        self.Header.write(file)

        for chain in self.ChainList:
            chain.write(file)
        for node in self.NodeList:
            node.write(file)


#---MHW CTC IO FUNCTIONS---#
def readCTCFile(filepath, bones):
    lang = bpy.context.preferences.view.language
    print(i18n("Opening ") + filepath)
    try:
        fileSize = os.path.getsize(filepath)
        file = open(filepath, "rb", buffering=8192)
    except:
        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            raiseError(f"打开 {filepath} 失败")
        else:
            raiseError("Failed to open " + filepath)

    ctcFile = CTCFile()
    ctcFile.read(file, fileSize, bones)
    file.close()
    return ctcFile

def writeCTCFile(ctcFile, filepath):
    lang = bpy.context.preferences.view.language
    print(i18n("Writing to ") + filepath)
    try:
        file = open(filepath, "wb", buffering=8192)
    except:
        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            raiseError(f"打开 {filepath} 失败")
        else:
            raiseError("Failed to open " + filepath)

    ctcFile.write(file)
    file.close()































