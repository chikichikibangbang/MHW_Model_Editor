import time

from ..common.general_function import getPaddedPos, raiseError,read_uint,read_int, \
    read_uint64,read_float, read_ushort,read_ubyte, read_byte,write_uint,write_int, write_uint64,write_float, \
    write_ushort,write_ubyte, write_byte, read_string, write_string
import numpy as np

from ..mrl3.mrl3_dicts import get_block_format_dict, clear_block_format_dict_cache

timeFormat = "%d"

# mod3_block_hash_dict = {
#     2807493369: "IANonSkin1UV",
#     2769308832: "IANonSkin2UV",
#     2173240540: "IANonSkin1UVColor",
#     252052287: "IANonSkin2UVColor",
#     4130816028: "IASkin4wt1UV",
#     4101111365: "IASkin4wt2UV",
#     1014171488: "IASkin4wt1UVColor",
#     3002859651: "IASkin4wt2UVColor",
#     2180350055: "IASkin8wt1UV",
#     2209562174: "IASkin8wt2UV",
#     912889255: "IASkin8wt1UVColor",
#     3102118468: "IASkin8wt2UVColor",
#     3592044045: "IASkin4wt1UVRcn",
#     1351503011: "IASkin4wt2UVRcn",
#     1165554616: "IASkin4wt1UVColorRcn",
#     3701118393: "IASkin4wt2UVColorRcn",
#     808373529: "IASkin8wt1UVRcn",
#     3065692087: "IASkin8wt2UVRcn",
#     1871536789: "IASkin8wt1UVColorRcn",
#     4134470804: "IASkin8wt2UVColorRcn",
#     3993480186: "IADevelopPrim2D",
#     1139705668: "IADevelopPrimImage2D",
#     4145846971: "IADevelopPrim3D",
#     2281592594: "IADevelopPos3UV1",
#     4289380069: "IASystemCopy",
#     3839359605: "IASystemClear",
#     2279177237: "IAFilter",
#     2777508887: "IAFilter2",
#     2767991478: "IADecal",
#     3933321995: "IADecal2",
#     55792455: "IASea",
#     3658059176: "IAWaterWave",
#     2337935659: "IAPosOnly",
#     3143073532: "IA_AmbientOccluder",
#     2633253930: "IA_SnowShoveler",
#     2744022753: "IA_SnowShovelerWithTex",
#     619199677: "IA_SnowShovelerWithNormal",
#     151265452: "IARibbon",
#     3853588429: "IARibbonBlade",
#     3478476201: "IAPrimDebug3D",
#     1866325959: "IAPrimDebugFont2D",
#     4069508834: "IAGUI",
#     1691341603: "IAPrecomputedStarrySky",
#     3282830241: "IANonSkin3UVColor",
#     3379104440: "IANonSkin4UVColor"
# }

class UV():
    def __init__(self):
        self.X = 0.0
        self.Y = 0.0
    def read(self, file):
        self.X = read_float(file)
        self.Y = read_float(file)
    def write(self,file):
        write_float(file, self.X)
        write_float(file, self.Y)


class Color():
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
        self.alpha = 0

    def read(self, file):
        self.red = read_ubyte(file)
        self.green = read_ubyte(file)
        self.blue = read_ubyte(file)
        self.alpha = read_ubyte(file)


class Normal_Tangent():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.w = 0

    def read(self, file):
        self.x = read_byte(file)
        self.y = read_byte(file)
        self.z = read_byte(file)
        self.w = read_byte(file)



class Vec3():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    def read(self,file):
        self.x = read_float(file)
        self.y = read_float(file)
        self.z = read_float(file)
    def write(self,file):
        write_float(file, self.x)
        write_float(file, self.y)
        write_float(file, self.z)

class Vec4():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.w = 0.0
    def read(self,file):
        self.x = read_float(file)
        self.y = read_float(file)
        self.z = read_float(file)
        self.w = read_float(file)
    def write(self,file):
        write_float(file, self.x)
        write_float(file, self.y)
        write_float(file, self.z)
        write_float(file, self.w)

class Sphere():
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.r = 0.0
    def read(self,file):
        self.x = read_float(file)
        self.y = read_float(file)
        self.z = read_float(file)
        self.r = read_float(file)
    def write(self,file):
        write_float(file, self.x)
        write_float(file, self.y)
        write_float(file, self.z)
        write_float(file, self.r)


class SphereNew():
    def __init__(self):
        self.sphere = [0.0,0.0,0.0,0.0]
    def read(self,file):
        self.sphere = np.frombuffer(file.read(16),dtype="<4f").tolist()
    def write(self,file):
        for val in self.sphere:
                write_float(file, val)

class AABB():
    def __init__(self):
        self.min = Vec4()
        self.max = Vec4()
    def read(self,file):
        self.min.read(file)
        self.max.read(file)
    def write(self,file):
        self.min.write(file)
        self.max.write(file)


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
        '''对矩阵求逆'''
        np_mat = np.array(self.matrix, dtype=np.float32)
        self.matrix = np.linalg.inv(np_mat).tolist()

class FileHeader():
    def __init__(self):
        self.magic = 4476749
        self.version = 237

        self.boneCount = 0
        self.meshCount = 0
        self.materialCount = 0
        self.vertexCount = 0
        self.faceCount = 0
        self.unkn1 = 0  #未知
        self.vertexBufferSize = 0
        self.groupCount = 0

        self.timestamp = 0

        self.boneOffset = 0
        self.groupOffset = 0
        self.materialOffset = 0
        self.meshOffset = 0
        self.vertexOffset = 0
        self.faceOffset = 0
        self.vertexRemapOffset = 0
        self.unknOffset = 0

        self.sphere = Sphere()
        self.bbox = AABB()

        self.unkn2 = 15000
        self.unkn3 = 1
        self.lodCount = 0
        self.unkn4 = []
        self.unkn5 = []

    def read(self, file):
        self.magic = read_uint(file)
        if self.magic != 4476749:
            raise Exception("File is not an MHW Mod3 file.")
        self.version = read_ushort(file)

        self.boneCount = read_ushort(file)
        self.meshCount = read_ushort(file)
        self.materialCount = read_ushort(file)
        self.vertexCount = read_uint(file)
        self.faceCount = read_uint(file)
        self.unkn1 = read_uint(file)
        self.vertexBufferSize = read_uint64(file)
        self.groupCount = read_uint(file)
        file.seek(4, 1)

        self.timestamp = read_uint64(file)

        self.boneOffset = read_uint64(file)
        self.groupOffset = read_uint64(file)
        self.materialOffset = read_uint64(file)
        self.meshOffset = read_uint64(file)
        self.vertexOffset = read_uint64(file)
        self.faceOffset = read_uint64(file)
        self.vertexRemapOffset = read_uint64(file)
        self.unknOffset = read_uint64(file)

        self.sphere.read(file)
        self.bbox.read(file)

        self.unkn2 = read_float(file)
        self.unkn3 = read_ushort(file)
        self.lodCount = read_ushort(file)
        self.unkn4 = np.frombuffer(file.read(88), dtype="<f").tolist()
        self.unkn5 = np.frombuffer(file.read(64), dtype="<b").tolist()

    def write(self, file):
        write_uint(file, self.magic)
        write_ushort(file, self.version)

        write_ushort(file, self.boneCount)
        write_ushort(file, self.meshCount)
        write_ushort(file, self.materialCount)
        write_uint(file, self.vertexCount)
        write_uint(file, self.faceCount)
        write_uint(file, self.unkn1)
        write_uint64(file, self.vertexBufferSize)
        write_uint(file, self.groupCount)
        file.seek(4, 1)

        self.timestamp = int(time.time())
        write_uint64(file, self.timestamp)

        write_uint64(file, self.boneOffset)
        write_uint64(file, self.groupOffset)
        write_uint64(file, self.materialOffset)
        write_uint64(file, self.meshOffset)
        write_uint64(file, self.vertexOffset)
        write_uint64(file, self.faceOffset)
        write_uint64(file, self.vertexRemapOffset)
        write_uint64(file, self.unknOffset)


        # file.seek(48, 1)
        self.sphere.write(file)
        self.bbox.write(file)
        #
        write_float(file, self.unkn2)
        write_ushort(file, self.unkn3)
        write_ushort(file, self.lodCount)

        for val in self.unkn4:
            write_float(file, val)
        for val in self.unkn5:
            write_byte(file, val)


class BoneInfo():
    def __init__(self):
        self.boneFunction = 0
        self.boneParent = 0
        self.boneSymmetric = 0
        self.boneUnkn = 0 #1.如果这根骨骼没有对应的绑定权重（顶点组），那么boneUnkn必定为0
        self.boneLength = 0
        self.bonePos = Vec3()

        # parse用
        self.boneIndex = 0
        self.boneName = ""
        # self.localMatrix = None
        self.worldMatrix = None

    def read(self,file):
        self.boneFunction = read_ushort(file)
        self.boneParent = read_ubyte(file)
        self.boneSymmetric = read_ubyte(file)
        self.boneUnkn = read_float(file)
        self.boneLength = read_float(file)

        entry = Vec3()
        entry.read(file)
        self.bonePos = entry

    def write(self,file):
        write_ushort(file, self.boneFunction)
        write_ubyte(file, self.boneParent)
        write_ubyte(file, self.boneSymmetric)
        write_float(file, self.boneUnkn)
        write_float(file, self.boneLength)
        self.bonePos.write(file)


class Skeleton():
    def __init__(self):
        self.boneCount = 0
        self.boneInfoList = []
        self.boneBuffer = bytearray()

        # parse用
        self.localMatList = []  # 骨骼的局部矩阵
        self.worldMatList = []  # 骨骼的世界矩阵的逆矩阵，需要取逆得到的才是真正的世界矩阵
        self.boneRemapDict = {}

    def read(self, file):
        self.boneInfoList = []
        for i in range(0, self.boneCount):
            entry = BoneInfo()
            entry.read(file)
            entry.boneIndex = i
            self.boneInfoList.append(entry)

        boneBufferSize = self.boneCount * 128 + 512
        self.boneBuffer.extend(file.read(boneBufferSize))

        file.seek(getPaddedPos(file.tell(), 16))

    def write(self, file):
        for entry in self.boneInfoList:
            entry.write(file)
        file.write(self.boneBuffer)

        file.seek(getPaddedPos(file.tell(), 16))


class MeshGroup():
    def __init__(self):
        self.groupID = 0

        # self.sphere = Sphere()
        self.sphere = []


    def read(self,file):
        self.groupID = read_uint(file)
        file.seek(12, 1)
        # self.sphere.read(file)

        # entry = Sphere()
        # entry.read(file)
        # self.sphere = entry
        self.sphere = []
        for i in range(0, 4):
            self.sphere.append(read_float(file))


    def write(self,file):
        write_uint(file, self.groupID)
        # write_int(file, -842150451)
        # write_int(file, -842150451)
        # write_int(file, -842150451)
        # self.sphere.write(file)
        file.write(b'\xCD' * 12)
        for val in self.sphere:
            write_float(file, val)


# VertexStride = {
#     2807493369: 24,
#     2769308832: 28,
#     3282830241: 36,
#     3379104440: 40,
#     2173240540: 28,
#     252052287:  32,
#     4130816028: 32,
#     4101111365: 36,
#     1014171488: 36,
#     3002859651: 40,
#     2180350055: 40,
#     2209562174: 44,
#     912889255:  44,
#     3102118468: 48,
#     }


class MeshInfo():
    def __init__(self):
        self.shadowFlag = 0
        self.vertexCount = 0
        self.groupID = 0
        self.materialID = 0
        self.lod = 0
        self.unkn1 = 0
        self.weightDynamics = 0
        self.blockSize = 0
        self.renderMode = 0
        self.vertexSub = 0
        self.vertexOffset = 0
        self.blockType = 0
        self.beforeFaceCount = 0
        self.faceCount = 0
        self.vertexBase = 0
        self.boundingBoxCount = 0
        self.meshIndex = 0
        self.vertMinIndex = 0
        self.vertMaxIndex = 0
        self.unkn3 = []
        self.beforeVertexCount = 0

        self.blockName = "" # parse用

    def read(self, file):
        self.shadowFlag = read_ushort(file)
        self.vertexCount = read_ushort(file)
        self.groupID = read_ushort(file)
        self.materialID = read_ushort(file)
        self.lod = read_ushort(file)
        self.unkn1 = read_ushort(file)
        self.weightDynamics = read_ushort(file)
        self.blockSize = read_ubyte(file)
        self.renderMode = read_ubyte(file)
        self.vertexSub = read_uint(file)
        self.vertexOffset = read_uint(file)
        self.blockType = read_uint(file)
        self.beforeFaceCount = read_uint(file)
        self.faceCount = read_uint(file)
        self.vertexBase = read_uint(file)
        file.seek(1, 1)
        self.boundingBoxCount = read_ubyte(file)
        self.meshIndex = read_ushort(file)
        self.vertMinIndex = read_ushort(file)
        self.vertMaxIndex = read_ushort(file)
        file.seek(8, 1)

        self.unkn3 = []
        for i in range(0, 4):
            self.unkn3.append(read_ubyte(file))
        self.beforeVertexCount = read_uint(file)

    def write(self, file):
        write_ushort(file, self.shadowFlag)
        write_ushort(file, self.vertexCount)
        write_ushort(file, self.groupID)
        write_ushort(file, self.materialID)
        write_ushort(file, self.lod)
        write_ushort(file, self.unkn1)
        write_ushort(file, self.weightDynamics)
        write_ubyte(file, self.blockSize)
        write_ubyte(file, self.renderMode)
        write_uint(file, self.vertexSub)
        write_uint(file, self.vertexOffset)
        write_uint(file, self.blockType)
        write_uint(file, self.beforeFaceCount)
        write_uint(file, self.faceCount)
        write_uint(file, self.vertexBase)
        file.seek(1, 1)
        write_ubyte(file, self.boundingBoxCount)
        write_ushort(file, self.meshIndex)
        write_ushort(file, self.vertMinIndex)
        write_ushort(file, self.vertMaxIndex)
        write_uint(file, 4294967295)
        file.seek(4, 1)
        for val in self.unkn3:
            write_ubyte(file, val)
            
        write_uint(file, self.beforeVertexCount)
        file.write(bytes(16))

class Mesh():
    def __init__(self):
        self.meshInfo = MeshInfo()
        # parse用
        self.submeshIndex = 0
        self.faceList = []
        self.vertexDict = {"Position": [], "NorTan": [],
                           "UV": [], "UV2": [], "UV3": [], "UV4": [],
                           "Weight": [], "Bone": [], "Color": []}

    def read(self, file):
        entry = MeshInfo()
        entry.read(file)
        self.meshInfo = entry

    def write(self, file):
        self.meshInfo.write(file)

class BoneBoundingBox():
    def __init__(self):
        # self.bbCount = 0
        # self.boneIndex = 0

        # self.bbProperty = []

        self.boneIndex = 0
        self.sphere = Sphere() #此处sphere结构的xyz是相对于对应骨骼坐标的偏移量，即骨骼头部坐标+此处坐标才是球体最终的位置
        self.aabb = AABB() #此处aabb结构的xyz是相对于对应骨骼坐标的偏移量，即骨骼头部坐标+此处坐标才是包围盒最终的位置
        self.obb_matrix = Matrix4x4()
        self.obb_halfsize = Vec4()

    def read(self,file):
        self.boneIndex = read_ushort(file)
        file.seek(14, 1)
        self.sphere.read(file)
        self.aabb.read(file)
        self.obb_matrix.read(file)
        self.obb_halfsize.read(file)

    def write(self, file):
        write_ushort(file, self.boneIndex)
        file.seek(2, 1)
        file.write(b'\xCD' * 12)
        self.sphere.write(file)
        self.aabb.write(file)
        self.obb_matrix.write(file)
        self.obb_halfsize.write(file)


class MHWMod3():
    def __init__(self):
        self.fileHeader = FileHeader()
        # self.Mod3BoundingBox = []
        # self.Unkns = UnknAfterHeader()

        self.skeleton = None
        self.meshGroupList = []
        # self.meshGroup = None
        # self.meshGroupBuffer = bytearray()
        self.materialNameList = []

        # self.meshList = []
        self.meshDict = {}
        self.validMeshCount = 0
        self.bbCount = 0
        self.BoneBoundingBoxList = []

        self.vertexBuffer = bytearray()
        self.faceBuffer = bytearray()
        # self.vertexBuffer = bytearray()
        # self.vertexBufferSize = 0

        # self.faceBuffer = bytearray()

    def read(self, file, options):
        self.fileHeader.read(file)

        # self.Unkns.read(file)
        self.meshDict = {"ALL": []} | {str(i): [] for i in range(self.fileHeader.lodCount + 1)}

        if self.fileHeader.boneCount and self.fileHeader.boneOffset:
            file.seek(self.fileHeader.boneOffset)
            self.skeleton = Skeleton()
            self.skeleton.boneCount = self.fileHeader.boneCount
            self.skeleton.read(file)

        if self.fileHeader.groupCount and self.fileHeader.groupOffset:
            file.seek(self.fileHeader.groupOffset)
            # self.meshGroup = np.frombuffer(file.read(self.fileHeader.groupCount * 32), dtype="<8f").tolist()
            # self.meshGroupBuffer.extend(file.read(self.fileHeader.groupCount * 32))

            for i in range(0, self.fileHeader.groupCount):
                # file.seek(self.fileHeader.groupOffset + i * 32)
                entry = MeshGroup()
                entry.read(file)
                self.meshGroupList.append(entry)

        if not options["importArmatureOnly"]:
            if self.fileHeader.materialCount and self.fileHeader.materialOffset:
            # if self.fileHeader.materialCount and self.fileHeader.materialOffset and self.lodHeader != None:
                file.seek(self.fileHeader.materialOffset)
                for i in range(0, self.fileHeader.materialCount):
                    file.seek(self.fileHeader.materialOffset + i * 128)
                    self.materialNameList.append(read_string(file))


            if self.fileHeader.meshCount and self.fileHeader.meshOffset:
                try:
                    blockDict = get_block_format_dict()
                    # vertexBufferOffset = self.fileHeader.vertexOffset
                    # faceBufferOffset = self.fileHeader.faceOffset

                    file.seek(self.fileHeader.meshOffset)
                    for i in range(0, self.fileHeader.meshCount):
                        file.seek(self.fileHeader.meshOffset + i * 80)
                        mesh = Mesh()
                        mesh.read(file)
                        meshInfo = mesh.meshInfo
                        blockType = str(meshInfo.blockType)

                        # 非法mesh的情况
                        # 1.lod值为0
                        # 2.blockType的值不在blockDict中
                        # 3,在blockDict中获取的valid值为0
                        # 4.blockSize与在blockDict中获取的size不一致
                        # 5.faceCount不能被3整除
                        # 6.vertexCount大于faceCount
                        # 7.materialID超限
                        # 8.faceBuffer中面索引超限（这个检查过程在mod3_parser中执行）
                        if meshInfo.lod == 0 or not blockDict.get(blockType) \
                                or not blockDict.get(blockType, {})["valid"] \
                                or meshInfo.blockSize != blockDict.get(blockType, {})["size"] \
                                or meshInfo.faceCount % 3 != 0 or meshInfo.vertexCount > meshInfo.faceCount \
                                or meshInfo.materialID >= self.fileHeader.materialCount: # 跳过非法mesh
                            continue

                        # 将mesh按照LOD层进行分类放置
                        if meshInfo.lod != 65535:
                            lod_level = (meshInfo.lod & - meshInfo.lod).bit_length() - 1 #若lod值不为65535，则计算其lod_level
                            if str(lod_level) in self.meshDict: # 若lod_level存在于键值中，则存入字典中；否则直接跳过
                                self.meshDict[str(lod_level)].append(mesh)
                        else:
                            self.meshDict["ALL"].append(mesh)

                        self.validMeshCount += 1

                    # 一次性读入整个vertexBuffer和faceBuffer
                    file.seek(self.fileHeader.vertexOffset)
                    self.vertexBuffer.extend(file.read(self.fileHeader.vertexBufferSize))
                    file.seek(self.fileHeader.faceOffset)
                    self.faceBuffer.extend(file.read(2 * self.fileHeader.faceCount))

                finally:
                    clear_block_format_dict_cache()

                if options["importBoundingBoxes"]:
                    # file.seek(20, 1)
                    file.seek(self.fileHeader.meshOffset + self.fileHeader.meshCount * 80)
                    self.bbCount = read_uint(file)
                    if self.bbCount:
                        for i in range(0, self.bbCount):
                            boneBoundingBox = BoneBoundingBox()
                            boneBoundingBox.read(file)
                            self.BoneBoundingBoxList.append(boneBoundingBox)

    def write(self, file):
        self.fileHeader.write(file)

        if self.fileHeader.boneCount and self.fileHeader.boneOffset:
            if self.fileHeader.boneOffset != file.tell():
                print(
                    f"ERROR IN OFFSET CALCULATION - boneOffset - "
                    f"expected {self.fileHeader.boneOffset}, actual {file.tell()}")
            self.skeleton.write(file)

        if self.fileHeader.groupCount and self.fileHeader.groupOffset:
            if self.fileHeader.groupOffset != file.tell():
                print(
                    f"ERROR IN OFFSET CALCULATION - groupOffset - expected {self.fileHeader.groupOffset}, actual {file.tell()}")
            # file.write(self.meshGroupBuffer)
        # file.seek(32, 1)
            for group in self.meshGroupList:
                group.write(file)

        if self.fileHeader.materialCount and self.fileHeader.materialOffset:
            if self.fileHeader.materialOffset != file.tell():
                print(
                    f"ERROR IN OFFSET CALCULATION - materialOffset - "
                    f"expected {self.fileHeader.materialOffset}, actual {file.tell()}")
            for index, entry in enumerate(self.materialNameList):
                write_string(file, entry)
                file.seek(self.fileHeader.materialOffset + (index + 1) * 128)

        if self.fileHeader.meshCount and self.fileHeader.meshOffset:
            if self.fileHeader.meshOffset != file.tell():
                print(
                    f"ERROR IN OFFSET CALCULATION - meshOffset - "
                    f"expected {self.fileHeader.meshOffset}, actual {file.tell()}")
            for lodIndex, meshList in self.meshDict.items():
                for meshEntry in meshList:
                    meshEntry.write(file)

            # file.seek(4, 1) # boneBBox，暂时将count置0
            write_uint(file, self.bbCount)
            if self.bbCount:
                for bboxEntry in self.BoneBoundingBoxList:
                    bboxEntry.write(file)

            if self.fileHeader.vertexOffset != file.tell():
                print(
                    f"ERROR IN OFFSET CALCULATION - vertexOffset - "
                    f"expected {self.fileHeader.vertexOffset}, actual {file.tell()}")
            file.write(self.vertexBuffer)

            if self.fileHeader.faceOffset != file.tell():
                print(
                    f"ERROR IN OFFSET CALCULATION - vertexOffset - "
                    f"expected {self.fileHeader.faceOffset}, actual {file.tell()}")
            file.write(self.faceBuffer)

            if self.fileHeader.vertexRemapOffset != file.tell():
                print(
                    f"ERROR IN OFFSET CALCULATION - vertexRemapOffset - "
                    f"expected {self.fileHeader.vertexRemapOffset}, actual {file.tell()}")
            write_uint(file, 4)
            file.write(bytes(20))


class SIZE_DATA():
    def __init__(self):
        self.HEADER_SIZE = 320

        self.BONE_INFO_ENTRY_SIZE = 24
        self.MATRIX_SIZE = 64

        self.GROUP_ENTRY_SIZE = 32
        self.MATERIAL_ENTRY_SIZE = 128

        self.MESH_INFO_ENTRY_SIZE = 80
        self.BONE_BBOX_ENTRY_SIZE = 144



#---MHW MOD3 IO FUNCTIONS---#

def readMHWMod3(filepath, options):
    print("Opening " + filepath)
    try:
        file = open(filepath,"rb",buffering=8192)
    except:
        raiseError("Failed to open " + filepath)

    Mod3File = MHWMod3()
    Mod3File.read(file, options)
    file.close()
    return Mod3File

def writeMHWMod3(Mod3File,filepath):
    print("Writing to " + filepath)
    try:
        file = open(filepath,"wb",buffering=8192)
    except:
        raiseError("Failed to open " + filepath)

    Mod3File.write(file)
    file.close()