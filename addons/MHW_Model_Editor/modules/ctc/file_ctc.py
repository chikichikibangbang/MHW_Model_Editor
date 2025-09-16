from ..common.general_function import textColors,raiseWarning,raiseError,getPaddingAmount,read_uint,read_int,\
    read_uint64,read_int64,read_float,read_ushort,read_ubyte,read_unicode_string,read_byte,read_short,write_uint,\
    write_int,write_uint64,write_int64,write_float,write_ushort,write_ubyte,write_unicode_string,write_byte,write_short
import math
import ctypes

#CTC文件结构大小
class SIZE_DATA():
    def __init__(self):
        self.HEADER_SIZE = 80
        self.CTC_SETTING_SIZE = 80
        self.CTC_NODE_SIZE = 112

#CTC Header数据
class CTCHeaderData():
    def __init__(self):
        self.magic = 4412483
        self.Version = 28
        self.ID = 0
        self.Always1000 = 1000

        self.ChainGroupCount = 0
        self.ChainNodeTotalCount = 0

        self.AttributeFlags = 64
        self.StepTime = 1/60
        self.GravityScaling = 1.0
        self.GlobalDamping = 0.0
        self.GlobalTransForceCoef = 1.0
        self.SpringScaling = 1.0
        self.WindScale = 0.6
        self.WindScaleMin = 0.3
        self.WindScaleMax = 1.0
        self.WindScaleWeight0 = 0.2
        self.WindScaleWeight1 = 0.7
        self.WindScaleWeight2 = 0.1

        self.SolveStrNum = 1
        self.SolveAngNum = 1
        self.SolveMdlColNum = 1
        self.SolveSelColNum = 1
        self.SolveScrColNum = 1
        self.SolveChnColNum = 1




    def read(self, file):
        print("Reading CTC Header...")
        self.magic = read_uint(file)
        if self.magic != 4412483:
            raiseError("File is not a ctc file.")

        self.Version = read_int(file)
        self.ID = read_int(file)
        self.Always1000 = read_int(file)

        self.ChainGroupCount = read_int(file)
        self.ChainNodeTotalCount = read_int(file)

        self.AttributeFlags = read_int(file)
        self.StepTime = read_float(file)

        self.GravityScaling = read_float(file)
        self.GlobalDamping = read_float(file)
        self.GlobalTransForceCoef = read_float(file)
        self.SpringScaling = read_float(file)

        self.WindScale = read_float(file)
        self.WindScaleMin = read_float(file)
        self.WindScaleMax = read_float(file)

        self.WindScaleWeight0 = read_float(file)
        self.WindScaleWeight1 = read_float(file)
        self.WindScaleWeight2 = read_float(file)

        self.SolveStrNum = read_byte(file)
        self.SolveAngNum = read_byte(file)
        self.SolveMdlColNum = read_byte(file)
        self.SolveSelColNum = read_byte(file)
        self.SolveScrColNum = read_byte(file)
        self.SolveChnColNum = read_byte(file)
        file.seek(2, 1)
    def write(self,file):
        write_uint(file, self.magic)
        write_int(file, self.Version)
        write_int(file, self.ID)
        write_int(file, self.Always1000)

        write_int(file, self.ChainGroupCount)
        write_int(file, self.ChainNodeTotalCount)

        write_int(file, self.AttributeFlags)
        write_float(file, self.StepTime)
        write_float(file, self.GravityScaling)
        write_float(file, self.GlobalDamping)
        write_float(file, self.GlobalTransForceCoef)
        write_float(file, self.SpringScaling)
        write_float(file, self.WindScale)
        write_float(file, self.WindScaleMin)
        write_float(file, self.WindScaleMax)
        write_float(file, self.WindScaleWeight0)
        write_float(file, self.WindScaleWeight1)
        write_float(file, self.WindScaleWeight2)

        write_byte(file, self.SolveStrNum)
        write_byte(file, self.SolveAngNum)
        write_byte(file, self.SolveMdlColNum)
        write_byte(file, self.SolveSelColNum)
        write_byte(file, self.SolveScrColNum)
        write_byte(file, self.SolveChnColNum)
        write_short(file, 0)


    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Joint():
    def __init__(self):
        self.offset = 0
        self.jointName = "READ_ERROR"

    def read(self, file):
        self.offset = read_uint64(file)
        currentPos = file.tell()
        file.seek(self.offset)
        self.jointName = read_unicode_string(file)
        file.seek(currentPos)

    def write(self, file):
        pass  # TODO

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

class CTCSettingsData():
    def __init__(self):
        self.NodeNum = 0
        self.CollisionAttrFlag = ColAttrFlag()
        self.CollisionAttrFlag.asInt32 = 4
        self.ChainAttrFlag = ChaAttrFlag()
        self.ChainAttrFlag.asInt32 = 39
        self.unknAttrFlag1 = 0
        self.unknAttrFlag2 = 0

        self.ColAttribute = -1
        self.ColGroup = 1
        self.ColType = 1

        self.xGravity = 0.0
        self.yGravity = -980.0
        self.zGravity = 0.0

        self.Damping = 0.0
        self.TransForceCoef = 0.2
        self.SpringCoef = 0.01

        self.LimitForce = 100.0
        self.FrictionCoef = 0.0
        self.ReflectCoef = 0.1

        self.WindRate = 0.1
        self.WindLimit = -1

    def read(self,file):
        self.NodeNum = read_int(file)
        self.CollisionAttrFlag.asInt32 = read_byte(file)
        self.ChainAttrFlag.asInt32 = read_byte(file)
        self.unknAttrFlag1 = read_byte(file)
        self.unknAttrFlag2 = read_byte(file)

        self.ColAttribute = read_int(file)
        self.ColGroup = read_uint(file)
        self.ColType = read_uint(file)
        file.seek(12, 1)
        self.xGravity = read_float(file)
        self.yGravity = read_float(file)
        self.zGravity = read_float(file)
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
            write_int(file, self.NodeNum)

            write_byte(file, self.CollisionAttrFlag.asInt32)
            write_byte(file, self.ChainAttrFlag.asInt32)

            write_byte(file, self.unknAttrFlag1)
            write_byte(file, self.unknAttrFlag2)

            write_int(file, self.ColAttribute)
            write_uint(file, self.ColGroup)
            write_uint(file, self.ColType)
            write_int(file, -842150451)
            write_int(file, -842150451)
            write_int(file, -842150451)
            write_float(file, self.xGravity)
            write_float(file, self.yGravity)
            write_float(file, self.zGravity)
            write_uint(file, 0)
            write_float(file, self.Damping)
            write_float(file, self.TransForceCoef)
            write_float(file, self.SpringCoef)

            write_float(file, self.LimitForce)
            write_float(file, self.FrictionCoef)
            write_float(file, self.ReflectCoef)

            write_float(file, self.WindRate)
            write_short(file, self.WindLimit)
            write_short(file, -12851)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class CTCNodeData():
    def __init__(self):
        self.row1_0 = 0.0
        self.row1_1 = 0.0
        self.row1_2 = 0.0
        self.row1_3 = 0.0
        self.row2_0 = 0.0
        self.row2_1 = 0.0
        self.row2_2 = 0.0
        self.row2_3 = 0.0
        self.row3_0 = 0.0
        self.row3_1 = 0.0
        self.row3_2 = 0.0
        self.row3_3 = 0.0
        self.row4_0 = 0.0
        self.row4_1 = 0.0
        self.row4_2 = 0.0
        self.row4_3 = 0.0

        self.unknByte1 = 0
        self.isParent = 0
        self.unknByte2 = 0
        self.AngleMode = 1
        self.CollisionShape = 1
        self.unknownEnum = 1

        self.boneFunctionID = 150
        self.unknownIntZero = 0

        self.boneColRadius = 2.0
        self.AngleLimitRadius = math.pi/4
        self.WidthRate = 1.0
        self.Mass = 1.0
        self.ElasticCoef = 1.0

    def read(self, file):
        self.row1_0 = read_float(file)
        self.row2_0 = read_float(file)
        self.row3_0 = read_float(file)
        self.row4_0 = read_float(file)
        self.row1_1 = read_float(file)
        self.row2_1 = read_float(file)
        self.row3_1 = read_float(file)
        self.row4_1 = read_float(file)
        self.row1_2 = read_float(file)
        self.row2_2 = read_float(file)
        self.row3_2 = read_float(file)
        self.row4_2 = read_float(file)
        self.row1_3 = read_float(file)
        self.row2_3 = read_float(file)
        self.row3_3 = read_float(file)
        self.row4_3 = read_float(file)
        file.seek(1, 1)
        self.unknByte1 = read_byte(file)
        self.isParent = read_byte(file)
        self.unknByte2 = read_byte(file)
        self.AngleMode = read_byte(file)
        file.seek(1, 1)
        self.CollisionShape = read_byte(file)
        self.unknownEnum = read_byte(file)

        self.boneFunctionID = read_int(file)
        self.unknownIntZero = read_int(file)

        self.boneColRadius = read_float(file)
        self.AngleLimitRadius = read_float(file)
        self.WidthRate = read_float(file)
        self.Mass = read_float(file)
        self.ElasticCoef = read_float(file)
        file.seek(12, 1)

    def write(self, file):
        write_float(file, self.row1_0)
        write_float(file, self.row2_0)
        write_float(file, self.row3_0)
        write_float(file, self.row4_0)
        write_float(file, self.row1_1)
        write_float(file, self.row2_1)
        write_float(file, self.row3_1)
        write_float(file, self.row4_1)
        write_float(file, self.row1_2)
        write_float(file, self.row2_2)
        write_float(file, self.row3_2)
        write_float(file, self.row4_2)
        write_float(file, self.row1_3)
        write_float(file, self.row2_3)
        write_float(file, self.row3_3)
        write_float(file, self.row4_3)

        write_byte(file, 0)
        write_byte(file, self.unknByte1)
        write_byte(file, self.isParent)
        write_byte(file, self.unknByte2)

        write_byte(file, self.AngleMode)
        write_byte(file, 0)
        write_byte(file, self.CollisionShape)
        write_byte(file, self.unknownEnum)

        write_int(file, self.boneFunctionID)
        write_int(file, self.unknownIntZero)

        write_float(file, self.boneColRadius)
        write_float(file, self.AngleLimitRadius)
        write_float(file, self.WidthRate)
        write_float(file, self.Mass)
        write_float(file, self.ElasticCoef)
        write_int(file, -842150451)
        write_int(file, -842150451)
        write_int(file, -842150451)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)



#CTC文件
class CTCFile():
    def __init__(self):
        self.Header = CTCHeaderData()
        self.sizeData = SIZE_DATA()
        self.CTCSettingsList = []
        self.CTCNodesList = []


    def read(self, file):
        self.Header.read(file)

        if self.Header.ChainGroupCount > 0:
            print("Reading CTC Chains...")

        for i in range(0, self.Header.ChainGroupCount):
            newChainSettings = CTCSettingsData()
            newChainSettings.read(file)
            currentPos = file.tell()
            #file.seek(currentPos)
            self.CTCSettingsList.append(newChainSettings)

        if self.Header.ChainNodeTotalCount > 0:
            print("Reading CTC Nodes...")

        for i in range(0, self.Header.ChainNodeTotalCount):
            newCTCNodes = CTCNodeData()
            newCTCNodes.read(file)
            self.CTCNodesList.append(newCTCNodes)

    def write(self, file):
        self.Header.write(file)
        # file.seek(self.Header.ctcSettingsOffset)
        for ctcSettings in self.CTCSettingsList:
            ctcSettings.write(file)
        for ctcNodes in self.CTCNodesList:
            ctcNodes.write(file)


#读取ctc文件
def readCTC(filepath):
    print(textColors.OKCYAN + "__________________________________\nCTC read started." + textColors.ENDC)
    print("Opening " + filepath)
    try:
        file = open(filepath, "rb")
    except:
        raiseError("Failed to open " + filepath)

    ctcFile = CTCFile()
    ctcFile.read(file)
    file.close()
    print(textColors.OKGREEN + "__________________________________\nCTC read finished." + textColors.ENDC)
    return ctcFile

#写入ctc文件
def writeCTC(ctcFile, filepath):
    print(textColors.OKCYAN + "__________________________________\nCTC write started." + textColors.ENDC)
    print("Opening " + filepath)
    try:
        file = open(filepath, "wb")
    except:
        raiseError("Failed to open " + filepath)

    ctcFile.write(file)
    file.close()
    print(textColors.OKGREEN + "__________________________________\nCTC write finished." + textColors.ENDC)































