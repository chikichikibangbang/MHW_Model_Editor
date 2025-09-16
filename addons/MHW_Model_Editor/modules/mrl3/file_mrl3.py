import time
import zlib

from ..common.general_function import raiseError, read_uint, read_uint64, read_short, read_ushort, read_ubyte, \
    read_string, read_fields_dict, write_uint, write_uint64, write_short,write_ushort,write_ubyte,write_string, \
    getPaddingAmount
from .mrl3_dicts import get_property_dict, get_texture_dict, get_master_material_dict, \
    get_ibhash_to_material_dict, clear_ibhash_to_material_dict_cache
import copy
timeFormat = "%d"

DEBUG_MODE = False

class SIZEDATA():
    def __init__(self):
        self.HEADER_SIZE = 40
        self.MATERIAL_ENTRY_SIZE = 56
        self.TEXTURE_ENTRY_SIZE = 272
        self.RESOURCE_ENTRY_SIZE = 16

# c_int32 = ctypes.c_int32
# class Mrl3Flags_bits(ctypes.LittleEndianStructure):
#     _fields_ = [
#         ("BaseTwoSideEnable", c_int32, 1),
#         ("BaseAlphaTestEnable", c_int32, 1),
#         ("ShadowCastDisable", c_int32, 1),
#         ("VertexShaderUsed", c_int32, 1),
#         ("EmissiveUsed", c_int32, 1),
#         ("TessellationEnable", c_int32, 1),
#         ("EnableIgnoreDepth", c_int32, 1),
#         ("AlphaMaskUsed", c_int32, 1),
#         ("ForcedTwoSideEnable", c_int32, 1),
#         ("TwoSideEnable", c_int32, 1),
#         ("TessFactor", c_int32, 6),
#         ("PhongFactor", c_int32, 8),
#         ("RoughTransparentEnable", c_int32, 1),
#         ("ForcedAlphaTestEnable", c_int32, 1),
#         ("AlphaTestEnable", c_int32, 1),
#         ("SSSProfileUsed", c_int32, 1),
#         ("EnableStencilPriority", c_int32, 1),
#         ("RequireDualQuaternion", c_int32, 1),
#         ("PixelDepthOffsetUsed", c_int32, 1),
#         ("NoRayTracing", c_int32, 1),
#     ]

# class Mrl3Flags(ctypes.Union):
#     _anonymous_ = ("flagValues",)
#     _fields_ = [
#         ("flagValues", Mrl3Flags_bits),
#         ("asInt32", c_int32)
#     ]

def debugprint(string):
    if DEBUG_MODE:
        print(string)

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
            raise Exception("File is not an MHW Mrl3 file.")
        self.version = read_uint(file)

        self.timestamp = read_uint64(file)

        self.materialCount = read_uint(file)
        self.textureCount = read_uint(file)

        self.textureOffset = read_uint64(file)
        self.materialOffset = read_uint64(file)

    def read_fast(self,file):
        file.seek(16,1)

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


class Texture():
    def __init__(self):
        self.textureTypeCode = 606035435 #应该都是606035435
        self.unkn1 = 0
        self.unkn2 = 0
        self.unkn3 = 0
        self.texturePath = ""

    def read(self, file):
        self.textureTypeCode = read_uint(file)
        self.unkn1 = read_uint(file)
        self.unkn2 = read_uint(file)
        self.unkn3 = read_uint(file)
        self.texturePath = read_string(file)

    def read_fast(self, file):
        self.textureTypeCode = read_uint(file)
        file.seek(12, 1)
        self.texturePath = read_string(file)

    def write(self, file):
        write_uint(file, self.textureTypeCode)
        file.seek(12, 1)
        write_string(file, self.texturePath)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Resource():
    def __init__(self):
        # self.resouceIndex = 0 #记录顺序用
        self.resourceType = 0

        # self.unkn_bytes = [] # 3个字节

        self.resourceHash = 0
        self.resourceName = ""
        self.resourceValueIndex = 0 # texture的话，index是对应的贴图序号；cbuffer的话，index是该cbuffer字段在materialblock中的偏移值；sampler的话，index可能是指不同的采样方式
        self.unkn = 0

        self.resourcePath = ""
        self.propertyDict = {}

        # self.propertyBuffer = bytearray()

    def read(self, file):
        self.resourceType = read_uint(file)
        self.resourceHash = read_uint(file)
        self.resourceValueIndex = read_uint(file)
        self.unkn = read_uint(file)

    def write(self, file):
        write_uint(file, self.resourceType)
        write_uint(file, self.resourceHash)
        write_uint(file, self.resourceValueIndex)
        write_uint(file, self.unkn)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Material():
    def __init__(self):
        self.headID = 1159129003 #若为1159129003，对应的字符串是"nDraw::Material"
        self.materialNameHash = 0
        self.materialName = ""
        self.shaderHash1 = 0
        self.shaderHash2 = 0
        self.mastermaterialType = ""

        self.materialBlockSize = 0 #该材质的resource和resource value字段的size总和

        self.surfaceDirection = 0 #-1f00，1100这个字段

        # self.resourceBlockSize = 0 #乘以8才是最终的resource blocksize
        self.resourceCount = 0

        self.alpha_bytes = []

        self.null_0 = []
        # self.unkn1 = 0
        # self.unkn2 = 0

        self.materialBlockOffset = 0

        # self.resourceList = []
        self.resourceDict = {}

    def read(self, file, textureDict, texture_dict, property_dict, master_material_dict):
        self.headID = read_uint(file)
        self.materialNameHash = read_uint(file)
        debugprint("materialNameHash:" + str(self.materialNameHash))
        self.shaderHash1 = read_uint(file)
        self.shaderHash2 = read_uint(file)

        if str(self.shaderHash1) in master_material_dict:
            self.mastermaterialType = master_material_dict[str(self.shaderHash1)]["mmtrName"]
        else:
            print(f"Unknown Master Material Type Hash: {self.shaderHash1}")

        self.materialBlockSize = read_uint(file)

        self.surfaceDirection = read_short(file)

        # self.resourceBlockSize = 8 * read_ubyte(file)
        self.resourceCount = read_ushort(file) // 2 #整数除法

        self.alpha_bytes = []
        for i in range(0, 4):
            self.alpha_bytes.append(read_ubyte(file))

        self.null_0 = []
        for i in range(0, 20):
            self.null_0.append(read_ubyte(file))

        # self.unkn1 = read_uint64(file)
        # self.unkn2 = read_uint64(file)

        self.materialBlockOffset = read_uint64(file)
        debugprint("materialBlockOffset:" + str(self.materialBlockOffset))

        # currentPos = file.tell()

        if self.resourceCount and self.materialBlockOffset:
            self.resourceDict = {}
            # file.seek(self.materialBlockOffset)
            for i in range(0, self.resourceCount):
                file.seek(self.materialBlockOffset + i * 16)
                resourceEntry = Resource()
                resourceEntry.read(file)

                if resourceEntry.resourceType & 0xF == 2:
                    resourceEntry.resourceName = texture_dict[str(resourceEntry.resourceHash >> 12)]
                    if resourceEntry.resourceValueIndex > 0:
                        resourceEntry.resourcePath = textureDict[resourceEntry.resourceValueIndex]
                elif resourceEntry.resourceType & 0xF == 1:
                    resourceEntry.resourceName = texture_dict[str(resourceEntry.resourceHash >> 12)]
                elif resourceEntry.resourceType & 0xF == 0:
                    file.seek(self.materialBlockOffset + resourceEntry.resourceValueIndex)
                    resourceEntry.resourceName = property_dict[str(resourceEntry.resourceHash >> 12)]["name"]
                    resourceEntry.propertyDict = copy.deepcopy(property_dict[str(resourceEntry.resourceHash >> 12)]["fields"])
                    read_fields_dict(file, resourceEntry.propertyDict)

                    # propertySize = property_dict[str(resourceEntry.resourceHash >> 12)]["size"]
                    # resourceEntry.propertyBuffer.extend(file.read(propertySize))

                debugprint(resourceEntry)
                if resourceEntry.resourceType & 0xF not in self.resourceDict:
                    self.resourceDict[resourceEntry.resourceType & 0xF] = [resourceEntry]
                else:
                    self.resourceDict[resourceEntry.resourceType & 0xF].append(resourceEntry)
                # self.resourceList.append(resourceEntry)

        # file.seek(currentPos)

    def getPropertyDict(self):
        if 0 not in self.resourceDict:
            return None
        propertyDict = {}
        for resourceEntry in self.resourceDict[0]:
            if resourceEntry.resourceName in {"CBMaterialCommon__disclosure", "CBSpeedTreeCollision__disclosure", "CBMhMaterialIvyFloorLocal__disclosure", "CBMhMaterialSlantFloorLocal__disclosure"}:
                continue
            propertyDict = resourceEntry.propertyDict
        return propertyDict #{prop.propName: prop for prop in self.resourceDict}

    def write(self, file):
        write_uint(file, self.headID)
        write_uint(file, self.materialNameHash)
        write_uint(file, self.shaderHash1)
        write_uint(file, self.shaderHash2)
        write_uint(file, self.materialBlockSize)
        write_short(file, self.surfaceDirection)
        write_ushort(file, self.resourceCount * 2)
        for i in range(4):
            write_ubyte(file, self.alpha_bytes[i])
        file.seek(20, 1)
        write_uint64(file, self.materialBlockOffset)

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class MHWMrl3():
    def __init__(self):
        self.sizeData = None
        self.Header = Mrl3Header()
        # self.textureList = []
        self.textureDict = {}
        self.materialList = []

        # self.stringList = []#Used during writing

    def read(self, file,  materialHashDict={}):
        try:
            # 加载小字典
            property_dict = get_property_dict()
            # shader_dict = get_shader_dict()
            texture_dict = get_texture_dict()
            master_material_dict = get_master_material_dict()
            # ibhash_to_material_dict = get_ibhash_to_material_dict()

            # 延迟加载大字典
            # ibhash_to_material_dict = None

            self.Header.read(file)
            debugprint(self.Header)

            if self.Header.textureCount and self.Header.textureOffset:
                # file.seek(self.Header.textureOffset)
                for i in range(0, self.Header.textureCount):
                    file.seek(self.Header.textureOffset + i * 272)
                    textureEntry = Texture()
                    textureEntry.read(file)
                    self.textureDict[i + 1] = textureEntry.texturePath
                    # self.textureList.append(textureEntry)

                # debugprint(self.textureList)

            if self.Header.materialCount and self.Header.materialOffset:
                # file.seek(self.Header.materialOffset)
                for i in range(0, self.Header.materialCount):
                    file.seek(self.Header.materialOffset + i * 56)
                    materialEntry = Material()
                    materialEntry.read(file, self.textureDict, texture_dict, property_dict, master_material_dict)

                    # debugprint(materialEntry)
                    #如果当前材质名哈希值不在对应mod3文件的材质名哈希字典中，则直接跳过当前材质区块，这意味着插件只会导入匹配mod3文件材质名的材质区块
                    if materialEntry.materialNameHash in materialHashDict:
                        materialEntry.materialName = materialHashDict[materialEntry.materialNameHash]
                        self.materialList.append(materialEntry)
                    else:
                        ibhash_to_material_dict = get_ibhash_to_material_dict()
                        if str(materialEntry.materialNameHash) in ibhash_to_material_dict:
                            materialEntry.materialName = ibhash_to_material_dict[str(materialEntry.materialNameHash)]
                            self.materialList.append(materialEntry)
                        else:
                            print(f"mismatched hash: {materialEntry.materialNameHash}")
                            materialEntry.materialName = "666"
                            self.materialList.append(materialEntry)

        finally:
            clear_ibhash_to_material_dict_cache() # 仅清理大字典

    def read_fast(self, file):
        self.Header.read_fast(file)
        debugprint(self.Header)
    #     for i in range(0, self.Header.materialCount):
    #         materialEntry = Material()
    #         materialEntry.read_fast(file, version)
    #         debugprint(materialEntry)
    #         self.materialList.append(materialEntry)

    def getMaterialDict(self):
        return {material.materialName: material for material in self.materialList}

    def recalculateHashesAndOffsets(self):
        self.Header.materialCount = len(self.materialList)
        self.Header.textureCount = len(self.textureDict)
        self.sizeData = SIZEDATA()

        textureEntriesSize = self.sizeData.TEXTURE_ENTRY_SIZE * self.Header.textureCount
        materialEntriesSize = self.sizeData.MATERIAL_ENTRY_SIZE * self.Header.materialCount

        self.Header.materialOffset = self.Header.textureOffset + textureEntriesSize

        currentOffset = self.Header.materialOffset + materialEntriesSize
        currentOffset = currentOffset + getPaddingAmount(currentOffset, 16)

        for material in self.materialList:
            material.materialBlockOffset = currentOffset
            currentOffset += material.materialBlockSize

    def write(self, file):
        self.recalculateHashesAndOffsets()
        self.Header.write(file)
        # It would be more faster and more efficient to write everything to buffers instead of looping again for each entry type but this is fast enough so ¯\_(ツ)_/¯
        # Loop to write texture entries
        print("Writing Texture Entries...")
        for texturePath, index in self.textureDict.items():
            file.seek(self.Header.textureOffset + self.sizeData.TEXTURE_ENTRY_SIZE * index)
            textureEntry = Texture()
            textureEntry.texturePath = texturePath
            textureEntry.write(file)

        # Loop to write material entries
        print("Writing Material Entries...")
        file.seek(self.Header.materialOffset)
        for material in self.materialList:
            material.write(file)
        file.write(b"\x00" * getPaddingAmount(file.tell(), 16))

        # Loop to write resource entries
        print("Writing Resource Entries...")
        for material in self.materialList:
            file.seek(material.materialBlockOffset)
            for resource in material.resourceDict.values():
                resourceEntry = Resource()
                resourceEntry.resourceType = resource["type"]
                resourceEntry.resourceHash = resource["hash"]
                resourceEntry.resourceValueIndex = resource["value"]
                resourceEntry.write(file)

        # print("Writing Texture Headers")
        # for material in self.materialList:
        #     file.seek(material.texHeadersOffset)
        #     for texture in material.textureList:
        #         texture.write(file, version)
        # # Loop to write property headers
        # print("Writing Property Headers")
        # for material in self.materialList:
        #     file.seek(material.propHeadersOffset)
        #     for prop in material.propertyList:
        #         prop.write(file, version)
        # # Write string table
        # print("Writing Strings")
        # """
        # for string in sorted(list(stringOffsetDict.items()),key = lambda item: item[1]):
        #     write_unicode_string(file, string[0])
        # """
        # for string in self.stringList:
        #     write_unicode_string(file, string)
        # # Clear string list after writing
        # self.stringList = []
        # # Loop over materials one last time to write property values
        #
        # print("Writing Property Values")
        # for material in self.materialList:
        #     for prop in material.propertyList:
        #         file.seek(material.propDataOffset + prop.propDataOffset)
        #         for value in list(prop.propValue):
        #             write_float(file, value)



def readMHWMrl3(filepath,  materialDict={}):
    print("Opening " + filepath)
    try:
        file = open(filepath,"rb")
    except:
        raiseError("Failed to open " + filepath)

    materialHashDict = {zlib.crc32(key.encode()) ^ 0xffffffff: key for key in materialDict}

    Mrl3File = MHWMrl3()
    Mrl3File.read(file,  materialHashDict)
    file.close()
    return Mrl3File

def readMHWMrl3Fast(filepath):
    print("Opening " + filepath)
    try:
        file = open(filepath,"rb")
    except:
        raiseError("Failed to open " + filepath)

    Mrl3File = MHWMrl3()
    Mrl3File.read_fast(file)
    file.close()
    return Mrl3File

def writeMHWMrl3(Mrl3File, filepath):
    print("Opening " + filepath)
    try:
        file = open(filepath,"wb")
    except:
        raiseError("Failed to open " + filepath)

    Mrl3File.write(file)
    file.close()