import bpy
import time
import struct
from io import BytesIO
import copy
from ..common.rw_functions import read_ubyte,read_byte,read_short,read_ushort,read_uint,read_int,read_uint64,\
    read_int64,read_float,read_double,read_string,read_unicode_string,write_ubyte,write_byte,write_short,write_ushort,\
    write_uint,write_int,write_uint64,write_int64,write_float,write_double,write_string,write_unicode_string,\
    getPaddingAmount,getPaddedPos
from ..common.general_function import read_fields_dict
from ..common.message_functions import raiseError
from .mrl3_dicts import get_property_dict, get_master_material_dict, \
    get_various_hash_dict, clear_various_hash_dict_cache, clear_master_material_dict_cache, clear_property_dict_cache, \
    clear_all_caches
from .....common.i18n.i18n import i18n
timeFormat = "%d"


class SIZEDATA():
    def __init__(self):
        self.HEADER_SIZE = 40
        self.TEXTURE_ENTRY_SIZE = 272
        self.MATERIAL_ENTRY_SIZE = 56
        self.RESOURCE_ENTRY_SIZE = 16


class Mrl3Header():
    def __init__(self):
        self.magic = 5001805
        self.version = 12

        self.timestamp = 0

        self.materialCount = 0
        self.textureCount = 0

        self.textureOffset = 40
        self.materialOffset = 0

    def read(self,file):
        self.magic = read_uint(file)
        if self.magic != 5001805:
            raise Exception(i18n("File is not a MHW MRL3 file."))
        self.version = read_uint(file)

        self.timestamp = read_uint64(file)

        self.materialCount = read_uint(file)
        self.textureCount = read_uint(file)

        self.textureOffset = read_uint64(file)
        self.materialOffset = read_uint64(file)

    def write(self,file):
        write_uint(file,self.magic)
        write_uint(file,self.version)

        self.timestamp = int(time.time())
        write_uint64(file, self.timestamp)

        write_uint(file,self.materialCount)
        write_uint(file, self.textureCount)
        write_uint64(file, self.textureOffset)
        write_uint64(file, self.materialOffset)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class MaterialInfo():
    def __init__(self):
        self.typeID = 1159129003  # 应该都是1159129003，对应的字符串是"nDraw::Material"
        self.materialNameHash = 0
        self.materialName = None  # parse用

        self.mmtrHash = 0
        self.mmtrName = ""  # parse用

        self.shaderHash = 0

        self.surfaceCoef = [0, 225]  # -1f00，1100这个字段
        self.alphaCoef = [150, 112, 4, 0]

        self.resourceCount = 0

        self.blockSize = 0  # 该材质的resource和resource value字段的size总和
        self.blockOffset = 0

    def read(self, file):
        self.typeID = read_uint(file)
        self.materialNameHash = read_uint(file)
        # print(f"materialNameHash: {self.materialNameHash}")

        self.mmtrHash = read_uint(file)
        self.shaderHash = read_uint(file)

        self.blockSize = read_uint(file)

        self.surfaceCoef = []
        for i in range(2):
            self.surfaceCoef.append(read_ubyte(file))

        self.resourceCount = read_ushort(file)  # 除2算

        self.alphaCoef = []
        for i in range(0, 4):
            self.alphaCoef.append(read_ubyte(file))

        file.seek(20, 1)
        self.blockOffset = read_uint64(file)

    def write(self, file):
        write_uint(file, self.typeID)
        write_uint(file, self.materialNameHash)
        write_uint(file, self.mmtrHash)
        write_uint(file, self.shaderHash)

        write_uint(file, self.blockSize)

        for val in self.surfaceCoef:
            write_ubyte(file, val)

        write_ushort(file, self.resourceCount)

        for val in self.alphaCoef:
            write_ubyte(file, val)

        file.seek(20, 1)
        write_uint64(file, self.blockOffset)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Material():
    def __init__(self):
        self.matInfo = MaterialInfo()
        self.resourceDict = {}

    def read(self, file):
        entry = MaterialInfo()
        entry.read(file)
        self.matInfo = entry

    def write(self, file):
        self.matInfo.write(file)

    def getPropertyDict(self):
        propertyDict = {}
        for resource in self.resourceDict.values():
            if not resource["name"].startswith("CB") or resource["name"] in {"CBMaterialCommon__disclosure",
                                                                             "CBSpeedTreeCollision__disclosure",
                                                                             "CBMhMaterialIvyFloorLocal__disclosure",
                                                                             "CBMhMaterialSlantFloorLocal__disclosure"}:
                continue

            propertyDict = resource["prop"]
        return propertyDict #{prop.propName: prop for prop in self.resourceDict}


PropertyFmtDict = {
    "float": {"size": 4, "fmt": "f"},
    "uint": {"size": 4, "fmt": "I"},
    "int": {"size": 4, "fmt": "i"},
    "ubyte": {"size": 1, "fmt": "B"},
    "byte": {"size": 1, "fmt": "b"},
    "bbool": {"size": 4, "fmt": "I"},
}


def ReadPropertyBuffers(resBuffer, offset, propertyDict):
    for propName, propInfo in propertyDict.items():
        propType = propInfo[1]

        if propType in PropertyFmtDict:
            propSize = PropertyFmtDict[propType]["size"]
            propFmt = PropertyFmtDict[propType]["fmt"]
            propInfo[0] = struct.unpack_from(f"<{propFmt}", resBuffer, offset)[0]

        elif propType.endswith(']'):
            baseType, baseSize = propType[:-1].split('[')
            propSize = PropertyFmtDict[baseType]["size"] * int(baseSize)
            propFmt = PropertyFmtDict[baseType]["fmt"]
            propInfo[0] = list(struct.unpack_from(f"<{baseSize}{propFmt}", resBuffer, offset))

        else:
            raise Exception(f"{i18n('Unknown property type:')} {propType}.")

        offset += propSize  # 累加偏移量


def ReadResourceBuffers(resBuffer, resCount, resDict, texList):
    offset = 0
    propDict = get_property_dict()

    for _ in range(resCount):
        resCode, resHash, resValue, unkn = struct.unpack_from("<4I", resBuffer, offset)
        offset += 16

        resource = resDict.get(str(resHash >> 12), None)
        if resource:
            resource["value"] = resValue
            if resource["name"].startswith("CB"):
                resource["match"] = True

    for code, resource in resDict.items():
        if resource["name"].startswith("t"):  # 将贴图索引转换为贴图路径
            if 0 <= (resource["value"] - 1) < len(texList):
                resource["value"] = texList[resource["value"] - 1]
            else:
                resource["value"] = ""

        elif resource["name"].startswith("CB") and resource["match"]:  # 解析常量缓冲区
            offset = resource["value"]
            tempDict = copy.deepcopy(propDict[code]["fields"])

            ReadPropertyBuffers(resBuffer, offset, tempDict)
            resource["prop"] = tempDict
            # print(tempDict)

    return resDict


def WritePropertyBuffers(bufferStream, propertyDict):
    for propName, propInfo in propertyDict.items():
        propValue = propInfo[0]
        propType = propInfo[1]

        if propType in PropertyFmtDict:
            fmt = PropertyFmtDict[propType]["fmt"]
            bufferStream.write(struct.pack(f"<{fmt}", propValue))

        elif propType.endswith(']'):
            baseType, baseSize = propType[:-1].split('[')
            fmt = PropertyFmtDict[baseType]["fmt"]
            if propName.startswith("align"):
                bufferStream.write(struct.pack(f"<{baseSize}{fmt}", *[0]*int(baseSize)))
            else:
                if propName.endswith("__uiColor") and propType == "float[3]":
                    del propValue[-1]
                    bufferStream.write(struct.pack(f"<{baseSize}{fmt}", *propValue))
                else:
                    bufferStream.write(struct.pack(f"<{baseSize}{fmt}", *propValue))

        else:
            raise Exception(f"{i18n('Unknown property type:')} {propType}.")


class Mrl3File():
    def __init__(self):
        self.sd = SIZEDATA()
        self.fileHeader = Mrl3Header()
        self.textureList = []
        self.textureDict = {}
        self.materialList = []
        self.resourceBuffer = bytearray()
        self.resourceBufferOffset = 0
        self.validMatCount = 0
        self.misMatHashList = []

    def read(self, file):
        self.fileHeader.read(file)

        if self.fileHeader.textureCount and self.fileHeader.textureOffset:
            # file.seek(self.fileHeader.textureOffset)
            for i in range(0, self.fileHeader.textureCount):
                file.seek(self.fileHeader.textureOffset + i * self.sd.TEXTURE_ENTRY_SIZE + 16)
                self.textureList.append(read_string(file))

        if self.fileHeader.materialCount and self.fileHeader.materialOffset:
            mmtrDict = get_master_material_dict()
            file.seek(self.fileHeader.materialOffset)
            for i in range(0, self.fileHeader.materialCount):
                entry = Material()
                entry.read(file)
                matInfo = entry.matInfo

                # 非法material的情况
                # 1.mmtrType的值不在mmtrDict中
                # 2.resourceCount不能被2整除
                # TODO 测试更多的非法情况
                if not mmtrDict.get(str(matInfo.mmtrHash)) or matInfo.resourceCount % 2 != 0:
                    continue

                self.materialList.append(entry)
                self.validMatCount += 1

            if self.materialList != []:
                self.resourceBufferOffset = self.materialList[0].matInfo.blockOffset
                file.seek(self.resourceBufferOffset)
                self.resourceBuffer.extend(file.read())

    def parser(self, mod3MatHashDict={}):
        try:
            mmtrDict = get_master_material_dict()
            propDict = get_property_dict()

            if self.materialList != []:
                OutOfBound = False
                resBufferSize = len(self.resourceBuffer)
                resBufferView = memoryview(self.resourceBuffer)

                for material in self.materialList:
                    matInfo = material.matInfo
                    mmtrData = mmtrDict[str(matInfo.mmtrHash)]

                    matInfo.mmtrName = mmtrData["mmtrName"]

                    # 解析材质名
                    matInfo.materialName = mod3MatHashDict.get(matInfo.materialNameHash, None)
                    if not matInfo.materialName:
                        various_hash_dict = get_various_hash_dict()
                        matInfo.materialName = various_hash_dict.get(str(matInfo.materialNameHash), None)
                    if not matInfo.materialName:  # TODO 考虑如果仍然未获取到匹配材质名，则在当前场景的所有材质中寻找匹配的材质
                        self.misMatHashList.append(matInfo.materialNameHash)
                        matInfo.materialName = f"{i18n('Unknown Hash')} {matInfo.materialNameHash}"

                    resBufferOffset = matInfo.blockOffset - self.resourceBufferOffset
                    if resBufferOffset + matInfo.blockSize <= resBufferSize:  # 防止超界
                        resBuffer = resBufferView[resBufferOffset:resBufferOffset + matInfo.blockSize]

                        # 解析resource
                        material.resourceDict = ReadResourceBuffers(resBuffer, matInfo.resourceCount//2, copy.deepcopy(mmtrData["resourceDict"]), self.textureList)
                        # print(material.resourceDict)
                    else:
                        OutOfBound = True

                if OutOfBound:
                    del self.materialList[-1]
        finally:
            # clear_master_material_dict_cache()
            # clear_various_hash_dict_cache()
            clear_all_caches()


    def getMaterialDict(self):
        return {material.matInfo.materialName: material for material in self.materialList}

    def writeResourceBuffers(self):
        resBuffer = BytesIO()
        for entry in self.materialList:
            propList = []
            for code, resource in entry.resourceDict.items():
                resBuffer.write(struct.pack("<4I", resource["type"], resource["hash"], resource["value"], 0))
                if resource["name"].startswith("CB"):
                    propList.append(resource["props"])

            for propertyDict in propList:
                WritePropertyBuffers(resBuffer, propertyDict)
                resBuffer.write(bytes(getPaddingAmount(resBuffer.tell(), 16)))

        self.resourceBuffer = resBuffer.getvalue()
        resBuffer.close()

    def write(self, file):
        self.fileHeader.materialCount = len(self.materialList)
        self.fileHeader.textureCount = len(self.textureDict)
        self.fileHeader.materialOffset = self.fileHeader.textureOffset + len(self.textureDict) * self.sd.TEXTURE_ENTRY_SIZE
        self.fileHeader.write(file)

        # file.seek(self.fileHeader.textureOffset)
        for path, index in self.textureDict.items():
            file.seek(self.fileHeader.textureOffset + self.sd.TEXTURE_ENTRY_SIZE * index)
            write_uint(file, 606035435)
            file.seek(12, 1)
            write_string(file, path)

        self.resourceBufferOffset = self.fileHeader.materialOffset + len(self.materialList) * self.sd.MATERIAL_ENTRY_SIZE
        self.resourceBufferOffset = getPaddedPos(self.resourceBufferOffset, 16)

        file.seek(self.fileHeader.materialOffset)
        for entry in self.materialList:
            if entry.matInfo.blockSize == 0:
                entry.matInfo.blockOffset = 0
            else:
                entry.matInfo.blockOffset = self.resourceBufferOffset
            self.resourceBufferOffset += entry.matInfo.blockSize
            entry.write(file)

        file.write(bytes(getPaddingAmount(file.tell(), 16)))
        file.write(self.resourceBuffer)


def readMrl3File(filepath):
    lang = bpy.context.preferences.view.language
    print(i18n("Opening ") + filepath)
    try:
        file = open(filepath, "rb", buffering=8192)
    except:
        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            raiseError(f"打开 {filepath} 失败")
        else:
            raiseError(f"Failed to open {filepath}")

    mrl3File = Mrl3File()
    mrl3File.read(file)
    file.close()
    return mrl3File

def writeMrl3File(mrl3File, filepath):
    lang = bpy.context.preferences.view.language
    print(i18n("Writing to ") + filepath)
    try:
        file = open(filepath, "wb", buffering=8192)
    except:
        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            raiseError(f"打开 {filepath} 失败")
        else:
            raiseError(f"Failed to open {filepath}")

    mrl3File.write(file)
    file.close()