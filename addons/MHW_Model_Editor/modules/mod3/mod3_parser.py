import struct
import numpy as np
from io import BytesIO
from itertools import chain

from ..common.rw_functions import getPaddedPos
from ..common.message_functions import raiseWarning

from .file_mod3 import SIZE_DATA, MeshGroup
from ..mrl3.mrl3_dicts import clear_block_format_dict_cache, get_block_format_dict


# 读取4x4矩阵数据
def ReadMatrixBuffer(matBuffer, invert=True):
    matCount = len(matBuffer) // 64
    matArray = np.frombuffer(matBuffer, dtype="<f4").reshape((matCount, 4, 4))
    if invert:
        try:
            invertArray = np.linalg.inv(matArray)
            matList = invertArray.tolist()
        except np.linalg.LinAlgError:
            matList = matArray.tolist()
    else:
        matList = matArray.tolist()
    return matList

# 读取骨骼缓冲区数据（局部矩阵，世界矩阵，重映射表）
def ReadBoneBuffer(boneBuffer, boneCount, invert=True):
    localMatBuffer = boneBuffer[0: boneCount * 64]
    worldMatBuffer = boneBuffer[boneCount * 64: boneCount * 128]
    remapBuffer = boneBuffer[boneCount * 128: boneCount * 128 + 512]

    localMatList = ReadMatrixBuffer(localMatBuffer, invert)
    worldMatList = ReadMatrixBuffer(worldMatBuffer, invert)

    remapArray = np.frombuffer(remapBuffer, dtype="<B")
    remapIndexArray = np.arange(512)
    valid_mask = remapArray != 255
    remapDict = dict(zip(remapArray[valid_mask], remapIndexArray[valid_mask]))

    return localMatList, worldMatList, remapDict

# 读取顶点位置数据
def ReadPosBuffer(vertexPosBuffer):
    posArray = np.frombuffer(vertexPosBuffer, dtype="<3f")
    # posArray = posArray / 100
    # posArray = np.divide(posArray, 100)
    posList = posArray.tolist()
    return posList

# 读取法线和切线数据
def ReadNorTanBuffer(norTanBuffer):
    norTanArray = np.frombuffer(norTanBuffer,dtype="<4b")
    norTanArray = np.delete(norTanArray, 3, axis=1)
    #print(norTanArray)
    norTanArray = np.divide(norTanArray,127)
    #norTanArray = np.add(norTanArray,0.5)
    norTanList = norTanArray.tolist()
    #Slice list by even and odd to get normals and tangents
    normalList = norTanList[::2]
    tangentList = norTanList[1::2]
    #print(normalList)
    return (normalList,tangentList)

# 读取UV数据
def ReadUVBuffer(uvBuffer):
    #uvArray = np.frombuffer(uvBuffer,dtype="<2e",)
    uvArray = np.frombuffer(bytearray(uvBuffer),dtype="<e",)#Convert bytes to bytearray to make numpy array mutable
    #Do (1-x) to v value
    uvArray[1::2] *= -1
    uvArray[1::2] += 1
    uvArray = uvArray.reshape((-1,2))
    return uvArray.tolist()

# 读取权重数据
def ReadWeightBuffer(weightBuffer,length,weightCount):
    dtype = "<I" if length == 4 else "<Q"
    oriArray = np.frombuffer(weightBuffer, dtype=dtype)

    # 一次性解包所有权重
    weightArray = np.zeros((len(oriArray), length), dtype="<f4")
    weightArray[:, 0] = (oriArray & 1023) / 1023
    weightArray[:, 1] = (oriArray >> 10 & 1023) / 1023
    weightArray[:, 2] = (oriArray >> 20 & 1023) / 1023
    if length == 4:
        sum_weights = np.sum(weightArray[:, :3], axis=1)
        weightArray[:, 3] = np.maximum(1 - sum_weights, 0)
        weightArray[weightArray[:, 3] < 1e-6, 3] = 0.0
    else:
        weightArray[:, 3] = (oriArray >> 32 & 255) / 1023
        weightArray[:, 4] = (oriArray >> 40 & 255) / 1023
        weightArray[:, 5] = (oriArray >> 48 & 255) / 1023
        weightArray[:, 6] = (oriArray >> 56 & 255) / 1023
        sum_weights = np.sum(weightArray[:, :7], axis=1)
        weightArray[:, 7] = np.maximum(1 - sum_weights, 0)
        weightArray[weightArray[:, 7] < 1e-6, 7] = 0.0

    # 按照weightCount进行分割
    weightArray = weightArray[:, :weightCount]
    boneWeightsList = weightArray.tolist()
    return boneWeightsList

# 读取绑定骨骼数据
def ReadWeightBoneBuffer(weightBoneBuffer,length,weightCount):
    dtype = "<4B" if length == 4 else "<8B"
    boneArray = np.frombuffer(weightBoneBuffer, dtype=dtype)
    boneArray = boneArray[:, :weightCount]
    boneIndicesList = boneArray.tolist()
    return boneIndicesList

# 读取顶点色数据
def ReadColorBuffer(colorBuffer):
    colorArray = np.frombuffer(colorBuffer,dtype="<4B")
    colorArray = np.divide(colorArray,255)
    return colorArray.tolist()

# 读取面索引数据
def ReadFaceBuffer(faceBuffer, vertexSub, vertexCount):
    faceBuffer = np.frombuffer(faceBuffer,dtype="<3H")
    faceBuffer = faceBuffer - vertexSub
    isValid = np.all((faceBuffer >= 0) & (faceBuffer < vertexCount)) # 检查所有面索引是否在[0, vertexCount)范围内
    if not isValid:
        return None
    return faceBuffer.tolist()

BufferReadDict = {
    "Position":ReadPosBuffer,
    "NorTan":ReadNorTanBuffer,
    "UV1":ReadUVBuffer,
    "UV2":ReadUVBuffer,
    "UV3":ReadUVBuffer,
    "UV4":ReadUVBuffer,
    "Weight":ReadWeightBuffer,
    "Bone":ReadWeightBoneBuffer,
    "Color":ReadColorBuffer,
    }

def ReadVertexElementBuffers(vertexDict, vertexBuffer, vertexCount, weightCount, blockDict):
    blockSize = blockDict["size"]
    blockProp = blockDict["prop"]
    current_offset = 0

    # 将AOS结构转换为SOA结构，便于后续使用numpy处理数据
    new_vertexBuffer = convert_aos_to_soa_optimized(vertexBuffer, vertexCount, blockSize, blockProp)

    for name, length in blockProp.items():
        if name in {"Weight", "Bone"}:
            vertexDict[name] = BufferReadDict[name](
                new_vertexBuffer[current_offset:current_offset + vertexCount * length], length, weightCount)
        else:
            vertexDict[name] = BufferReadDict[name](
                new_vertexBuffer[current_offset:current_offset + vertexCount * length])
        current_offset = current_offset + vertexCount * length

    return vertexDict


def convert_aos_to_soa_optimized(vertexBuffer, vertexCount, blockSize, blockProp):
    soa_data = bytearray(len(vertexBuffer))
    soa_view = memoryview(soa_data)

    attr_offset = 0
    sum_length = 0

    for name, length in blockProp.items():
        for i in range(vertexCount):
            src_start = i * blockSize + sum_length
            dst_start = attr_offset + i * length
            soa_view[dst_start:dst_start + length] = vertexBuffer[src_start:src_start + length]

        sum_length += length
        attr_offset = vertexCount * sum_length

    # return soa_data
    return soa_view


class ParsedMod3File:
    def __init__(self):
        self.header = None
        self.skeleton = None
        self.meshGroupList = []
        self.materialNameList = []
        self.meshDict = {}
        self.validMeshCount = 0
        self.bbCount = 0
        self.BoneBoundingBoxList = []

    def parse(self, mod3File, options):
        self.header = mod3File.fileHeader
        self.validMeshCount = mod3File.validMeshCount

        if mod3File.skeleton != None:
            self.skeleton = mod3File.skeleton
            _, self.skeleton.worldMatList, self.skeleton.boneRemapDict = \
                ReadBoneBuffer(self.skeleton.boneBuffer, self.skeleton.boneCount, invert=True)

            for boneInfo in self.skeleton.boneInfoList:
                boneIndex = boneInfo.boneIndex
                if boneIndex not in self.skeleton.boneRemapDict:
                    # boneInfo.boneName = ""
                    continue  # 跳过不存在的键

                # 修复因父级骨骼id不在重映射表中，导致导入模型时报错的问题
                # if boneInfo.boneParent != 255 and boneInfo.boneParent not in self.skeleton.boneRemapDict:
                #     boneInfo.boneParent = self.skeleton.boneInfoList[boneInfo.boneParent].boneParent
                # 循环向上查找boneParent，直到找到一个数值为255或在重映射表中的boneParent
                while boneInfo.boneParent != 255 and boneInfo.boneParent not in self.skeleton.boneRemapDict:
                    boneInfo.boneParent = self.skeleton.boneInfoList[boneInfo.boneParent].boneParent

                boneInfo.boneName = "MhBone_" + str(self.skeleton.boneRemapDict[boneIndex]).zfill(3)
                boneInfo.worldMatrix = self.skeleton.worldMatList[boneIndex]

        if mod3File.meshGroupList != []:
            self.meshGroupList = mod3File.meshGroupList

        if mod3File.materialNameList != []:
            self.materialNameList = mod3File.materialNameList

        try:
            if mod3File.meshDict != {}:
                vBufferView = memoryview(mod3File.vertexBuffer)
                fBufferView = memoryview(mod3File.faceBuffer)

                blockFormatDict = get_block_format_dict()

                if options["importAllLODs"]:
                    self.meshDict = mod3File.meshDict
                else:
                    mod3File.meshDict["ALL"].extend(mod3File.meshDict["0"])
                    self.meshDict = {"ALL": mod3File.meshDict["ALL"]}

                # 对每个lod层级中的mesh按照groupID进一步排序
                for lod_level, meshList in self.meshDict.items():
                    meshList.sort(key=lambda x: x.meshInfo.groupID)
                    removeMeshList = []

                    current_groupID = None
                    submesh_counter = 0
                    for mesh in meshList:
                        meshInfo = mesh.meshInfo
                        blockType = str(meshInfo.blockType)

                        # 解析vertexBuffer和faceBuffer
                        # 先解析faceBuffer，并同时检查面索引是否超限，若无超限再解析vertexBuffer，否则直接跳过当前循环
                        faceBufferOffset = 2 * meshInfo.beforeFaceCount
                        faceBuffer = fBufferView[faceBufferOffset:faceBufferOffset + 2 * meshInfo.faceCount]
                        mesh.faceList = ReadFaceBuffer(faceBuffer, meshInfo.vertexSub, meshInfo.vertexCount)
                        if mesh.faceList == None:
                            removeMeshList.append(mesh)
                            # self.validMeshCount -= 1
                            continue

                        blockDict = blockFormatDict[blockType]
                        weightCount = 8 if (meshInfo.weightDynamics >> 3) > 8 else meshInfo.weightDynamics >> 3
                        vertexBufferOffset = \
                            meshInfo.vertexOffset + meshInfo.blockSize * (meshInfo.vertexSub + meshInfo.vertexBase)
                        vertexBuffer = \
                            vBufferView[vertexBufferOffset:vertexBufferOffset + meshInfo.vertexCount * meshInfo.blockSize]
                        mesh.vertexDict = ReadVertexElementBuffers(mesh.vertexDict, vertexBuffer,
                                                                   meshInfo.vertexCount, weightCount, blockDict)

                        if meshInfo.groupID != current_groupID:
                            current_groupID = meshInfo.groupID
                            submesh_counter = 0
                        else:
                            submesh_counter += 1
                        mesh.submeshIndex = submesh_counter

                    for mesh in removeMeshList:
                        meshList.remove(mesh)
                    self.validMeshCount -= len(removeMeshList)

                if options["importBoundingBoxes"]:
                    self.bbCount = mod3File.bbCount
                    if mod3File.BoneBoundingBoxList != []:
                        self.BoneBoundingBoxList = mod3File.BoneBoundingBoxList

        finally:
            clear_block_format_dict_cache()


def WriteToMatrixBuffer(bufferStream, matList):
    matArray = np.array(matList, dtype=np.float32).reshape((-1, 4, 4))
    matArray[np.abs(matArray) < 1e-6] = 0.0
    flattened = matArray.ravel()
    data = struct.pack(f'<{len(flattened)}f', *flattened)
    bufferStream.write(data)

def WriteToBoneBuffer(bufferStream, matList, remapDict):
    WriteToMatrixBuffer(bufferStream, matList)
    remapArray = np.full(512, 255, dtype="<B")
    for oriIndex, newIndex in remapDict.items():
        if newIndex < 512:  # 确保索引不越界
            remapArray[newIndex] = oriIndex
    bufferStream.write(remapArray.tobytes())

def WriteToPosBuffer(vertexPosList,vertexCount):
    return struct.pack(f'{vertexCount*3}f', *chain.from_iterable(vertexPosList))

def WriteToNorTanBuffer(norTanList,vertexCount):
    normalArray = np.floor(np.multiply(norTanList[0], 127))
    normalArray = np.insert(normalArray, 3, np.zeros(vertexCount, np.dtype("<b")), axis=1)
    norTanArray = np.empty((vertexCount * 2, 4), dtype=np.dtype("<b"))
    norTanArray[::2] = normalArray
    norTanArray[1::2] = norTanList[1]
    return norTanArray.tobytes()

def WriteToUVBuffer(uvList,vertexCount):
    uvArray = np.array(uvList, dtype=np.dtype("<e"))
    uvArray = uvArray.flatten()
    uvArray[1::2] *= -1
    uvArray[1::2] += 1
    return uvArray.tobytes()

def WriteToWeightBoneBuffer(boneIndicesList,vertexCount):
    boneIndicesArray = boneIndicesList.astype("<B")
    return boneIndicesArray.tobytes()

def WriteToWeightBuffer(boneWeightsList,vertexCount):
    boneWeightsArray = np.array(boneWeightsList)
    length = boneWeightsArray.shape[1]
    weightSums = np.sum(boneWeightsArray, axis=1, dtype=np.float32)

    # 规格化权重
    with np.errstate(divide='ignore', invalid='ignore'):
        boneWeightsArray = boneWeightsArray / weightSums[:, None]
        boneWeightsArray[weightSums == 0] = 0
    boneWeightsArray = np.multiply(boneWeightsArray, 1023)
    boneWeightsArray = np.round(boneWeightsArray)
    diffSums = 1023.0 - np.sum(boneWeightsArray, axis=1, dtype=np.float32)

    # 将权重差值加到每一行的最大权重值上
    boneWeightsArray[np.arange(boneWeightsArray.shape[0]), np.argmax(boneWeightsArray, axis=1)] += diffSums
    if (1023 - np.sum(boneWeightsArray, axis=1) != 0).any():
        raiseWarning("Non normalized weights detected on sub mesh! Weights may not behave as expected in game!")

    dtype = "<I" if length == 4 else "<Q"
    boneWeightsArray = boneWeightsArray.astype(dtype)

    packArray = np.zeros(vertexCount, dtype=dtype)
    packArray |= boneWeightsArray[:, 0]
    packArray |= boneWeightsArray[:, 1] << 10
    packArray |= boneWeightsArray[:, 2] << 20
    if length == 4:
        return packArray.tobytes()
    else:
        packArray |= boneWeightsArray[:, 3] << 32
        packArray |= boneWeightsArray[:, 4] << 40
        packArray |= boneWeightsArray[:, 5] << 48
        packArray |= boneWeightsArray[:, 6] << 56
        return packArray.tobytes()

def WriteToColorBuffer(colorList,vertexCount):
    colorArray = np.array(colorList,dtype = np.float32)
    colorArray = np.multiply(colorArray,255)
    colorArray = colorArray.astype(dtype=">B")
    return colorArray.tobytes()

def WriteToFaceBuffer(bufferStream,faceList,vertexSub,faceCount):
    face_array = np.array(faceList) + vertexSub
    data = struct.pack(f'{faceCount}H', *face_array.flatten())
    bufferStream.write(data)

BufferWriteDict = {
    "Position":WriteToPosBuffer,
    "NorTan":WriteToNorTanBuffer,
    "UV1":WriteToUVBuffer,
    "UV2":WriteToUVBuffer,
    "UV3":WriteToUVBuffer,
    "UV4":WriteToUVBuffer,
    "Weight":WriteToWeightBuffer,
    "Bone":WriteToWeightBoneBuffer,
    "Color":WriteToColorBuffer,
    }
def WriteVertexElementBuffers(bufferStream, vertexDict, vertexCount, blockDict):
    blockSize = blockDict["size"]
    blockProp = blockDict["prop"]
    tempBuffer = bytearray()

    for name, length in blockProp.items():
        tempBuffer.extend(BufferWriteDict[name](vertexDict[name], vertexCount))

    # 将SOA结构转回AOS结构
    tempBuffer = convert_soa_to_aos_optimized(tempBuffer, vertexCount, blockSize, blockProp)
    bufferStream.write(tempBuffer)

def convert_soa_to_aos_optimized(tempBuffer, vertexCount, blockSize, blockProp):
    # 预分配空间
    aos_data = bytearray(len(tempBuffer))

    # 使用内存视图提高性能
    view = memoryview(tempBuffer)
    aos_view = memoryview(aos_data)

    attr_offset = 0
    sum_length = 0

    for name, length in blockProp.items():
        for i in range(vertexCount):
            src_start = attr_offset + i * length
            dst_start = i * blockSize + sum_length
            aos_view[dst_start:dst_start + length] = view[src_start:src_start + length]

        sum_length += length
        attr_offset = vertexCount * sum_length

    return aos_data

# mesh区块处理
def caculateBlock(state, blockSize, vertexCount, faceCount):
    # 首次赋值
    if state["currentBlockSize"] == None:
        state["currentBlockSize"] = blockSize

    elif blockSize != state["currentBlockSize"]:
        # 块大小变化，更新vertexOffset并重置计数器
        state["vertexOffset"] += (state["vertexBase"] + state["vertexSub"]) * state["currentBlockSize"]
        state["vertexBase"] = 0
        state["vertexSub"] = 0
        state["currentBlockSize"] = blockSize

    # 检查当前区块内的顶点数是否溢出上限
    if state["vertexSub"] + vertexCount > 65536:
        state["vertexBase"] += state["vertexSub"]
        state["vertexSub"] = 0

    # 累加顶点数和面数
    state["beforeFaceCount"] += faceCount
    state["beforeVertexCount"] += vertexCount


def buildMod3File(mod3File, targetCollection, groupIDList):
    # TODO 比对groupIDList和mod3集合自定义属性中的groupID
    sd = SIZE_DATA()

    mod3File.fileHeader.unkn1 = targetCollection.get("Mod3_Header_Unkn1", 4294967295)
    mod3File.fileHeader.unkn2 = targetCollection.get("Mod3_Header_Unkn2", 15000.0)
    mod3File.fileHeader.unkn3 = targetCollection.get("Mod3_Header_Unkn3", 1)
    mod3File.fileHeader.unkn4 = targetCollection.get("Mod3_Header_Unkn4",
                                                     [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1,
                                                      1.401298e-45, 100, 30, 20, 10, 10])
    mod3File.fileHeader.unkn5 = targetCollection.get("Mod3_Header_Unkn5",
                                                     [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1,
                                                      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                                      0, 2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15, 15, 15, 15, 15,
                                                      16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 27, 27, 27, 27])

    for key, value in targetCollection.items():
        if key.startswith("Mod3_Group_"):
            entry = MeshGroup()
            entry.groupID = int(key.split("_")[-1])
            entry.sphere = value
            mod3File.meshGroupList.append(entry)

    currentOffset = sd.HEADER_SIZE
    if mod3File.skeleton != None:
        boneBuffer = BytesIO()
        skeleton = mod3File.skeleton
        mod3File.fileHeader.boneCount = skeleton.boneCount
        mod3File.fileHeader.boneOffset = currentOffset

        WriteToBoneBuffer(boneBuffer, skeleton.localMatList + skeleton.worldMatList, skeleton.boneRemapDict)
        skeleton.boneBuffer = boneBuffer.getvalue()
        boneBuffer.close()

        currentOffset += getPaddedPos((sd.BONE_INFO_ENTRY_SIZE + 128) * mod3File.fileHeader.boneCount + 512, 16)

    if mod3File.meshGroupList != []:
        mod3File.fileHeader.groupCount = len(mod3File.meshGroupList)
        mod3File.fileHeader.groupOffset = currentOffset
        currentOffset += sd.GROUP_ENTRY_SIZE * mod3File.fileHeader.groupCount

    if mod3File.materialNameList != []:
        mod3File.fileHeader.materialCount = len(mod3File.materialNameList)
        mod3File.fileHeader.materialOffset = currentOffset
        currentOffset += sd.MATERIAL_ENTRY_SIZE * mod3File.fileHeader.materialCount

    if mod3File.fileHeader.meshCount:
        vertexBuffer = BytesIO()
        faceBuffer = BytesIO()
        mod3File.fileHeader.meshOffset = currentOffset
        try:
            blockFormatDict = get_block_format_dict()

            # 初始化顶点区块字典
            # currentBlockSize，当前块大小（初始为None，表示未设置）
            # vertexBase，基础顶点计数（累积值）
            # vertexSub，当前区块内的顶点计数
            # vertexOffset，偏移量
            # beforeFaceCount: 面的累计值
            # beforeVertexCount：点的累计值
            blockState = {
                "currentBlockSize": None,
                "vertexBase": 0,
                "vertexSub": 0,
                "vertexOffset": 0,
                "beforeFaceCount": 0,
                "beforeVertexCount": 0
            }

            for lod_level, meshList in mod3File.meshDict.items():
                # meshList.sort(key=lambda x: x.meshInfo.groupID)
                for mesh in meshList:
                    meshInfo = mesh.meshInfo
                    blockDict = blockFormatDict[meshInfo.blockName]
                    meshInfo.blockType = blockDict["type"]
                    meshInfo.blockSize = blockDict["size"]

                    # mesh区块处理
                    # --------------------------------
                    meshInfo.beforeFaceCount = blockState["beforeFaceCount"]
                    meshInfo.beforeVertexCount = blockState["beforeVertexCount"]
                    caculateBlock(blockState, meshInfo.blockSize, meshInfo.vertexCount, meshInfo.faceCount)

                    meshInfo.vertexBase = blockState["vertexBase"]
                    meshInfo.vertexSub = blockState["vertexSub"]
                    meshInfo.vertexOffset = blockState["vertexOffset"]
                    meshInfo.vertMinIndex = blockState["vertexSub"]
                    meshInfo.vertMaxIndex = meshInfo.vertMinIndex + meshInfo.vertexCount - 1
                    # 添加当前网格的顶点数到VertexSub
                    blockState["vertexSub"] += meshInfo.vertexCount
                    # --------------------------------

                    WriteVertexElementBuffers(vertexBuffer, mesh.vertexDict, meshInfo.vertexCount, blockDict)
                    WriteToFaceBuffer(faceBuffer, mesh.faceList, meshInfo.vertexSub, meshInfo.faceCount)

            mod3File.vertexBuffer = vertexBuffer.getvalue()
            # 填充faceBuffer到能被4整除
            padding = (4 - faceBuffer.tell() % 4) % 4
            if padding > 0:
                faceBuffer.write(b'\x00' * padding)
            mod3File.faceBuffer = faceBuffer.getvalue()
            vertexBuffer.close()
            faceBuffer.close()

        finally:
            clear_block_format_dict_cache()

        currentOffset += sd.MESH_INFO_ENTRY_SIZE * mod3File.fileHeader.meshCount

        mod3File.bbCount = len(mod3File.BoneBoundingBoxList)
        currentOffset += 4 + mod3File.bbCount * sd.BONE_BBOX_ENTRY_SIZE

        mod3File.fileHeader.vertexBufferSize = len(mod3File.vertexBuffer)
        mod3File.fileHeader.vertexOffset = currentOffset
        currentOffset += len(mod3File.vertexBuffer)
        mod3File.fileHeader.faceOffset = currentOffset
        currentOffset += len(mod3File.faceBuffer)

        mod3File.fileHeader.vertexRemapOffset = currentOffset

    return mod3File
