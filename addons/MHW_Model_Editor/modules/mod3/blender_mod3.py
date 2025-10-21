import zlib

import bpy
import os
import glob
import time
import datetime
import numpy as np
from math import floor

from ..common.general_function import splitNativesPath
from ..common.message_functions import raiseWarning, addErrorToDict
from ..common.blender_functions import clearScene, createCollection, getCollection, checkObjForUVDoubling, \
    solveRepeatedUVs, splitSharpEdges, triangulateMesh

from .file_mod3 import Mod3File, readMod3File, writeMod3File, Skeleton, Mesh, BoneBoundingBox
from .mod3_parser import ParsedMod3File, buildMod3File
from .mod3_functions import importSkeleton, createMaterialDict, importLODGroup, importOrientedBoundingBox, \
    importBoundingSphere, importAxisAlignedBoundingBox, importBoundingBoxes, exportMatrix, pad, sortLODCollections, \
    parseArmatureData, createCloneMesh, parseMeshGroupID, getUsedVertexGroup, parseMaterialName, initUVColorDict, \
    parseVertexDict, calulateBoundingBoxes, transVertexToBoneLocal, hideLODCollections
from .mod3_export_errors import printMod3ErrorDict, showMHWMod3ErrorWindow
from ..ctc.blender_ctc import importMHWCTCFile

from ..mrl3.file_mrl3 import readMrl3File
from ..mrl3.blender_mrl3 import importMHWMrl3File
from ..mrl3.blender_mod3_mrl3 import importMHWMrl3

timeFormat = "%d"

def loadMrl3(filePath, materialDict, parentCollection, options, warningList):
    # 确定mrl3文件路径
    mrl3Path = options["mrl3Path"] if options["mrl3Path"] else f"{glob.escape(filePath.split('.mod3')[0])}.mrl3"
    print("")

    if not os.path.isfile(mrl3Path):
        warning = f"An error occurred while reading {mrl3Path} - File is not found."
        raiseWarning(warning)
        warningList.append(warning)
        return

    try:
        # 提取根路径
        split = splitNativesPath(mrl3Path)
        chunkPath = split[0] if split else None

        # 读取mrl3文件
        try:
            # mrl3ReadStartTime = time.time()
            mrl3File = readMrl3File(mrl3Path)
            # mrl3ReadEndTime = time.time()
            # mrl3ReadTime = mrl3ReadEndTime - mrl3ReadStartTime
            # print(f"Mrl3 reading took {timeFormat % (mrl3ReadTime * 1000)} ms.")
        except Exception as err:
            warning = f"An error occurred while reading {mrl3Path} - {str(err)}"
            raiseWarning(warning)
            warningList.append(warning)
            return

        mod3MatHashDict = {zlib.crc32(key.encode()) ^ 0xffffffff: key for key in materialDict}
        print("Parsed mrl3.")

        # 导入mrl3数据
        if options["loadMrl3Data"]:
            print("Loading mrl3 data...")
            # importMHWMrl3File(mrl3File, mrl3Path, materialDict, parentCollection=parentCollection)
            dataOptions = {"mrl3File": mrl3File, "mod3MatHashDict": mod3MatHashDict, "parentCollection": parentCollection}
            importMHWMrl3File(mrl3Path, dataOptions, warningList, isNested=True)

        # 导入材质
        if options["loadMaterials"]:
            print("Loading mod3 materials from mrl3...")
            mrl3ImportStartTime = time.time()
            if chunkPath:
                importMHWMrl3(mrl3File, materialDict, options["loadUnusedTextures"], options["loadUnusedProps"],
                              options["useBackfaceCulling"], options["reloadCachedTextures"],
                              chunkPath, mrl3Path=mrl3Path, arrangeNodes=True)
                mrl3ImportEndTime = time.time()
                mrl3ImportTime = mrl3ImportEndTime - mrl3ImportStartTime
                print(f"Materials loading took {timeFormat % (mrl3ImportTime * 1000)} ms.")
            else:
                warning = f"An error occurred while loading materials from {mrl3Path} - File is not under the chunk or nativePC path."
                raiseWarning(warning)
                warningList.append(warning)

    except Exception as err:
        warning = f"An error occurred while importing {mrl3Path} - {str(err)}"
        raiseWarning(warning)
        warningList.append(warning)


def loadPhysics(filePath, armatureObj, warningList):
    # 确定ctc文件路径
    ctcPath = f"{glob.escape(filePath.split('.mod3')[0])}.ctc"
    print("")

    if not os.path.isfile(ctcPath):
        warning = f"An error occurred while reading {ctcPath} - File is not found."
        raiseWarning(warning)
        warningList.append(warning)
        return

    options = {"targetArmature": armatureObj, "mergeCollection": None, "loadCCL": True}
    importMHWCTCFile(ctcPath, options, warningList=warningList, isNested=True)


def importMHWMod3File(filePath, options):
    warningList = []
    errorList = []

    if options["clearScene"]:
        clearScene()

    print("\033[96m__________________________________\nMHW Mod3 import started.\033[0m")
    mod3ImportStartTime = time.time()
    mod3FileName = os.path.split(filePath)[1]

    # 读取mod3文件
    try:
        mod3File = readMod3File(filePath, options)
    except Exception as err:
        warning = f"An error occurred while reading {filePath} - {str(err)}"
        raiseWarning(warning)
        warningList.append(warning)
        return False

    # 解析mod3文件
    mod3ParseStartTime = time.time()
    parsedMod3 = ParsedMod3File()
    parsedMod3.parse(mod3File, options)
    print("Parsed mod3.")
    mod3ParseEndTime = time.time()
    mod3ParseTime = mod3ParseEndTime - mod3ParseStartTime
    print(f"Mod3 parsing took {timeFormat % (mod3ParseTime * 1000)} ms.")

    armatureObj = None
    parentCollection = None
    countInfo = None

    # 创建集合
    if options["createCollections"]:
        # if options["loadMrl3Data"]:
        if options["addNestedCollections"]:
            parentCollection = getCollection(mod3FileName.split(".mod3")[0], makeNew=True)
        mod3Collection = createCollection(mod3FileName, "COLOR_01", "MHW_MOD3_COLLECTION", parentCollection)
        bpy.context.scene.mhw_mrl3_toolpanel.mod3Collection = mod3Collection
        bpy.context.scene.mhw_mod3_toolpanel.lastImportCollection = mod3Collection.name

        # 赋予自定义属性
        mod3Collection["Mod3_Header_Unkn1"] = parsedMod3.header.unkn1
        mod3Collection["Mod3_Header_Unkn2"] = parsedMod3.header.unkn2
        mod3Collection["Mod3_Header_Unkn3"] = parsedMod3.header.unkn3
        mod3Collection["Mod3_Header_Unkn4"] = parsedMod3.header.unkn4
        mod3Collection["Mod3_Header_Unkn5"] = parsedMod3.header.unkn5

        # 将meshGroup导入为自定义属性
        if parsedMod3.meshGroupList != []:
            for group in parsedMod3.meshGroupList:
                mod3Collection["Mod3_Group_" + str(group.groupID).zfill(3)] = group.sphere
    else:
        mod3Collection = bpy.context.scene.collection

    # 导入mod3骨架
    boneNameIndexDict = {}
    if parsedMod3.skeleton != None:
        armatureObj, boneNameIndexDict = importSkeleton(parsedMod3.skeleton.boneInfoList,
                                                        mod3FileName.split(".mod3")[0] + " Armature", mod3Collection,
                                                        options["ArmatureDisplayType"], options["BonesDisplaySize"])

    # 创建材质名映射材质的字典，防止在材质名重复时分配错误的材质
    materialDict = createMaterialDict(parsedMod3.materialNameList)

    # 导入mod3网格
    hiddenColSet = set()
    if not options["importArmatureOnly"]:
        countInfo = importLODGroup(parsedMod3, mod3Collection, materialDict, armatureObj,
                                   hiddenColSet, options["importAllLODs"])

        # 隐藏非lod all和lod 0层级的其他lod集合的可见性
        hideLODCollections(parentCollection, mod3Collection, hiddenColSet)

    '''因为旧mod3插件将boneBoundingBox作为自定义属性导入导出，所以其数量与序号不一定匹配，最终决定关闭导入导出原始boneBoundingBox的选项，仅作为debug用'''
    if options["importBoundingBoxes"]:
        if options["createCollections"]:
            bboxCollection = createCollection(f"{mod3FileName} Bounding Boxes", "NONE",
                                              "MHW_MOD3_BBOX_COLLECTION", mod3Collection)
        else:
            bboxCollection = mod3Collection

        # 导入总的BoundingBox
        importBoundingBoxes(parsedMod3.header.sphere, parsedMod3.header.aabb, bboxCollection)

        # 导入每个网格单独的BoneBoundingBox
        for index, bboxEntry in enumerate(parsedMod3.BoneBoundingBoxList):
            if armatureObj != None:
                # boneName = "MhBone_" + str(parsedMod3.skeleton.boneRemapDict[bboxEntry.boneIndex]).zfill(3)
                boneName = boneNameIndexDict[bboxEntry.boneIndex]
                sphereObj = importBoundingSphere(bboxEntry.sphere,
                                                 str(index) + "_Sphere" + "_" + boneName,
                                                 bboxCollection, armatureObj, boneName)
                aabbObj = importAxisAlignedBoundingBox(bboxEntry.aabb,
                                                       str(index) + "_AABB" + "_" + boneName,
                                                       bboxCollection, armatureObj, boneName)
                obbObj = importOrientedBoundingBox(bboxEntry.obb_matrix, bboxEntry.obb_halfsize,
                                                   str(index) + "_OBB" + "_" + boneName,
                                                   bboxCollection, armatureObj, boneName)
            else:
                sphereObj = importBoundingSphere(bboxEntry.sphere, str(index) + "_Sphere", bboxCollection)
                aabbObj = importAxisAlignedBoundingBox(bboxEntry.aabb, str(index) + "_AABB", bboxCollection)
                obbObj = importOrientedBoundingBox(bboxEntry.obb_matrix, bboxEntry.obb_halfsize,
                                                   str(index) + "_OBB", bboxCollection)

    mod3ImportEndTime = time.time()
    mod3ImportTime = mod3ImportEndTime - mod3ImportStartTime
    print(f"Mod3 imported in {timeFormat % (mod3ImportTime * 1000)} ms.")

    # 格式化时间戳
    dt_object = datetime.datetime.fromtimestamp(parsedMod3.header.timestamp)
    formatted_date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

    print("\nMod3 Info:")
    print(f"Mod3 TimeStamp: {formatted_date_time}")
    print(f"Mesh Count: {parsedMod3.header.meshCount}")
    print(f"Valid Mesh Count: {parsedMod3.validMeshCount} / {parsedMod3.header.meshCount}")
    print(f"Imported Mesh Count: {countInfo}")

    # 导入材质
    if options["loadMaterials"] or options["loadMrl3Data"]:
        loadMrl3(filePath, materialDict, parentCollection, options, warningList)

    # 导入物理链和碰撞
    if options["loadPhysics"] and armatureObj != None:
        loadPhysics(filePath, armatureObj, warningList)

    print("\033[92m__________________________________\nMHW Mod3 import finished.\033[0m")
    # return warningList, errorList
    return True



def exportMHWMod3File(filePath, options):
    # 可能需要警告的情况
    # 某个网格对象不符合网格命名格式 #TODO
    # 某个顶点组有权重但没有对应的绑定骨骼 #TODO
    # 如果同时存在对应的mrl3空物体对象，检查网格对象的材质名是否和mrl3材质名匹配 #TODO

    # 需要报错的情况
    # 导出时未选择目标集合
    # 目标集合内没有网格对象，或没有选中的网格对象，或没有可见的网格对象
    # 目标集合内存在多个相同层级的lod集合
    # 目标集合内有1个以上的骨架
    # 骨架中的骨骼数量超过最大限制255
    # 骨骼名称不符合MhBone_xxx格式，或骨骼后缀数字超过了最大限制511
    # 目标集合内有骨架，但某个网格对象没有任何有效绑定顶点组
    # 某个网格对象没有点
    # 某个网格对象没有面片
    # 某个网格对象无法成功解析材质名
    # 某个网格对象的顶点数超过了最大限制65535
    # 某个网格对象的三角面数乘3超过了最大限制4294967295
    # 某个网格没有UV通道
    # 某个网格对象有重叠UV
    # 某个顶点的有效绑定顶点组数量超过了最大限制8
    # 某个网格对象中有松散元素
    # 所有网格对象的顶点数超过了最大限制4294967295
    # 所有网格对象的三角面数乘3超过了最大限制4294967295
    # 所有网格对象的数量超过了最大限制65535
    # 所有网格对象的材质数量超过了最大限制65535

    # 部分限制值
    MAX_WEIGHTS_PER_VERT = 8
    MAX_BONE_FUNCTION = 511
    MAX_BONES_TOTAL = 255
    MAX_MESHS_TOTAL = 65535
    MAX_MATERIALS_TOTAL = 65535
    MAX_VERTICES_PER = 65535
    MAX_FACES_PER = 4294967295  # 乘3算
    MAX_VERTICES_TOTAL = 4294967295
    MAX_FACES_TOTAL = 4294967295  # 乘3算

    errorDict = dict()
    # 用于累积数量
    vertexCount = 0
    faceCount = 0
    subMeshCount = 0

    print("\033[96m__________________________________\nMHW Mod3 export started.\033[0m")
    mod3ExportStartTime = time.time()

    # previousSelection = bpy.context.selected_objects
    # 切换物体模式
    if bpy.context and bpy.context.active_object != None:
        bpy.ops.object.mode_set(mode='OBJECT')

    # 获取要导出的mod3集合
    targetCollection = options["targetCollection"]
    if targetCollection != None:
        print(f"Target Collection: {targetCollection.name}")
        bpy.context.scene.mhw_mod3_toolpanel.lastExportCollection = targetCollection.name
    else:
        # 若导出时未选择mod3集合，则添加报错，并直接返回False
        addErrorToDict(errorDict, "NoTargetMod3Collection")
        printMod3ErrorDict(errorDict)
        showMHWMod3ErrorWindow(errorDict, "None", "None")
        return False

    dg = bpy.context.evaluated_depsgraph_get()  # 获取依赖图
    deleteCopiedMeshList = []  # 用于存放最后要删除的克隆网格对象
    addedMaterialsSet = set()  # 用于存放所有网格对象的材质

    mod3File = Mod3File()

    # 添加一个不被使用的材质作为第一个材质，以避免隐藏衣装mod关闭第一个材质的发光
    if options["invisibleMantlesModFix"]:
        addedMaterialsSet.add("InvisibleMantlesModEmiFix")
        mod3File.materialNameList.append("InvisibleMantlesModEmiFix")

    # 将lod集合分类，并获取lod集合字典和最大lod值
    lodColDict, maxLOD = sortLODCollections(targetCollection, errorDict)
    mod3File.fileHeader.lodCount = maxLOD

    # 获取骨架
    armatureObj = None
    for obj in targetCollection.objects:
        if obj.type == "ARMATURE":
            if armatureObj == None:
                armatureObj = obj
            else:  # 如果找到一个以上的骨架，则添加报错
                addErrorToDict(errorDict, "MoreThanOneArmature")

    # 解析骨架数据
    exportArmatureData = None
    boneIndexDict = dict()  # 骨骼名称映射骨骼索引的字典
    if armatureObj != None:
        armatureName = armatureObj.name
        print(f"Target Armature: {armatureName}")
        mod3File.skeleton = Skeleton()
        exportArmatureData, boneIndexDict = parseArmatureData(mod3File.skeleton, armatureObj, errorDict)
    else:
        armatureName = "None"
        print(f"Target Armature: None")

    # 开始解析网格数据
    mod3DataStartTime = time.time()

    groupIDList = set()  # 用于存放所有网格对象的groupID
    vertArrayList = []  # 用于存放所有顶点的坐标向量，后续用于计算总的包围盒和包围球

    # 遍历每个lod集合
    for lodIndex, lodTuple in lodColDict.items():
        lodVal, lodCol = lodTuple
        mod3File.meshDict[lodIndex] = []

        # 根据导出选项筛选网格对象
        exportObjs = [
            obj for obj in lodCol.objects
            if (not options["selectedOnly"] or obj in bpy.context.selected_objects)
               and (not options["visibleOnly"] or obj.visible_get())
               and obj.type == "MESH"]

        if exportObjs != []:
            print(f"LOD {lodIndex} Collection: {lodCol.name}")

        for obj in exportObjs:
            subMeshCount += 1
            # 创建克隆网格对象
            cloneObj = createCloneMesh(obj, dg, deleteCopiedMeshList)

            # 获取groupID
            groupID = parseMeshGroupID(obj, groupIDList)

            # 获取有效绑定顶点组（即顶点组有对应的绑定骨骼，且顶点组有权重）
            boneVertDict, vgIndexToNameDict = getUsedVertexGroup(obj, cloneObj, boneIndexDict)
            vertexGroupCount = len(obj.vertex_groups)  # 防止后续解析权重数据时，遍历顶点组索引越界

            # 若mod3集合中有骨架，且boneVertDict仍然为空（说明当前网格对象没有有效绑定顶点组），则添加报错
            if armatureObj != None and boneVertDict == {}:
                addErrorToDict(errorDict, "NoWeightsOnMesh", objectName=obj.name)

            # 处理重叠UV和分离锐边
            if options["autoSolveRepeatedUVs"]:
                hasUVDoubling = checkObjForUVDoubling(cloneObj)
                if hasUVDoubling:
                    try:
                        solveRepeatedUVs(cloneObj)
                    except Exception as err:
                        raiseWarning(f"Failed to solve repeated UVs. {str(err)}")
            if options["preserveSharpEdges"]:
                try:
                    splitSharpEdges(cloneObj)
                except Exception as err:
                    raiseWarning(f"Failed to split sharp edges. {str(err)}")

            evaluatedData = cloneObj.data


            # 正式解析网格数据
            meshEntry = Mesh()
            meshInfo = meshEntry.meshInfo
            meshInfo.lod = lodVal
            meshInfo.groupID = groupID

            # 如果当前网格对象含有非三角面，则强制三角化
            if any(len(face.vertices) != 3 for face in evaluatedData.polygons):
                print(f"Triangulated {obj.name}")
                triangulateMesh(evaluatedData)

            transform = exportMatrix @ obj.matrix_world
            evaluatedData.transform(transform)  # 应用导出变换

            if bpy.app.version < (4, 0, 0):
                evaluatedData.use_auto_smooth = True
                evaluatedData.calc_normals_split()
            try:
                evaluatedData.calc_tangents()
            except:
                pass

            # 如果当前网格对象无顶点或无面片，则添加报错
            verticeCount = len(evaluatedData.vertices)
            polygonCount = len(evaluatedData.polygons)

            if verticeCount == 0:
                addErrorToDict(errorDict, "NoVerticesOnSubMesh", objectName=obj.name)
            elif polygonCount == 0:
                addErrorToDict(errorDict, "NoFacesOnSubMesh", objectName=obj.name)

            if polygonCount * 3 > MAX_FACES_PER:
                addErrorToDict(errorDict, "MaxFacesExceeded", objectName=obj.name)
            elif verticeCount > MAX_VERTICES_PER:
                addErrorToDict(errorDict, "MaxVerticesExceeded", objectName=obj.name)

            meshInfo.vertexCount = verticeCount
            meshInfo.faceCount = polygonCount * 3
            vertexCount += verticeCount
            faceCount += polygonCount

            # 解析材质名
            materialName = parseMaterialName(obj, evaluatedData, errorDict, options["useBlenderMaterialName"])
            if materialName not in addedMaterialsSet:
                addedMaterialsSet.add(materialName)
                mod3File.materialNameList.append(materialName)
                meshInfo.materialID = len(mod3File.materialNameList) - 1
            else:
                meshInfo.materialID = mod3File.materialNameList.index(materialName)

            # 获取面索引列表
            meshEntry.faceList = [tuple(f.vertices) for f in evaluatedData.polygons]

            # 按照顶点索引序号排序克隆网格数据的循环属性
            sortedLoops = sorted(evaluatedData.loops, key=lambda loop: loop.vertex_index)
            previousIndex = -1

            meshInfo.blockName = "PosNorTan"  # 初始化blockName
            blockNameExtend, meshHasUV, meshHasColor, UVDict = \
                initUVColorDict(obj, evaluatedData, meshEntry.vertexDict, armatureObj, errorDict)
            meshInfo.blockName += blockNameExtend

            # 初始化6个列表
            vertexPosList, vertexNorList, vertexTanList, \
                vertexWeightList, vertexIndicesList, vertexColorList = (list() for _ in range(6))
            for loop in sortedLoops:
                currentVertIndex = loop.vertex_index

                # 解析顶点UV数据
                for i in range(4):
                    if not meshHasUV[i]:
                        continue
                    uvKey = f"UV{i+1}"
                    uv = evaluatedData.uv_layers[i].data[loop.index].uv
                    meshEntry.vertexDict[uvKey][currentVertIndex] = uv

                    # 如果当前顶点已经在集合中，说明有重叠UV，则添加报错
                    if currentVertIndex in UVDict[uvKey] and UVDict[uvKey][currentVertIndex] != uv:
                        addErrorToDict(errorDict, "MultipleUVsAssignedToVertex", objectName=obj.name)
                    else:
                        UVDict[uvKey][currentVertIndex] = uv

                if currentVertIndex == previousIndex:
                    continue  # 跳过已经读取过的顶点循环
                previousIndex = currentVertIndex

                # 解析顶点坐标数据
                vertex = evaluatedData.vertices[currentVertIndex]
                vertexPosList.append(vertex.co)

                # 解析顶点法向和切向数据
                loopTangent = loop.tangent * 1.001 * 127
                tx = int(floor(loopTangent[0])) & 0xFF
                ty = int(floor(loopTangent[1])) & 0xFF
                tz = int(floor(loopTangent[2])) & 0xFF
                sign = int(floor(loop.bitangent_sign * 127.0)) & 0xFF
                vertexNorList.append(loop.normal)
                vertexTanList.append((tx, ty, tz, sign))

                # 解析顶点色数据
                if meshHasColor:
                    vertexColorList.append(evaluatedData.vertex_colors[0].data[loop.index].color)

                # 解析顶点权重和绑定骨骼数据
                # MIN_WEIGHT = 0.002
                MIN_WEIGHT = 0.001  # 最小权重是1/1023，约等于0.001
                boneWeightList = []
                boneIndicesList = []

                if armatureObj != None:
                    sortedGroups = sorted(vertex.groups, key=lambda g: g.weight, reverse=True)
                    for g in sortedGroups:
                        # 若当前遍历的顶点组的权重值大于等于最小权重，且顶点组索引没有超界，同时顶点组索引在vgIndexToNameDict中
                        if g.weight >= MIN_WEIGHT and g.group < vertexGroupCount and g.group in vgIndexToNameDict:
                            boneWeightList.append(g.weight)
                            boneIndicesList.append(boneIndexDict[vgIndexToNameDict[g.group]])
                            # 将顶点坐标添加到boneVertDict的对应列表中
                            boneVertDict[vgIndexToNameDict[g.group]].append(vertex.co)

                    # 若某个顶点的有效绑定顶点组数量大于最大限制值8，则添加报错
                    if len(boneWeightList) > MAX_WEIGHTS_PER_VERT:
                        addErrorToDict(errorDict, "MaxWeightsPerVertexExceeded", objectName=obj.name)
                    # 按照8的长度来填充权重列表和绑定骨骼列表，不足部分用0补全
                    vertexWeightList.append(list(pad(boneWeightList, size=8, padding=0.0)))
                    vertexIndicesList.append(list(pad(boneIndicesList, size=8, padding=0)))

            # 将解析的各个顶点元素列表赋予vertexDict
            parseVertexDict(meshEntry.vertexDict, meshInfo, vertArrayList, vertexPosList, vertexNorList,
                            vertexTanList, vertexColorList, vertexWeightList, vertexIndicesList)

            # 获取网格对象的自定义属性
            meshInfo.shadowFlag = obj.data.get("Mod3_Mesh_ShadowFlag", 19)
            meshInfo.renderMode = obj.data.get("Mod3_Mesh_RenderMode", 195)
            meshInfo.unkn3 = obj.data.get("Mod3_Mesh_Unkn", [0, 0, 0, 48])
            meshInfo.meshIndex = obj.data.get("Mod3_Mesh_Index", 1)

            mod3File.meshDict[lodIndex].append(meshEntry)

            # 若网格对象中存在松散顶点，则添加报错
            if any([vertIndex not in UVDict["UV1"] for vertIndex in range(verticeCount)]):
                addErrorToDict(errorDict, "LooseVerticesOnSubMesh", objectName=obj.name)

            # 计算每个网格对象的包围球，AABB包围盒和OBB包围盒
            if armatureObj != None:
                bboxCount = len(boneVertDict)
                for boneName, vecList in boneVertDict.items():
                    if vecList == []:  # 保险起见，这里加一步判定
                        bboxCount -= 1
                        continue

                    bboxEntry = BoneBoundingBox()
                    bboxEntry.boneIndex = boneIndexDict[boneName]

                    # 将顶点坐标变换到骨骼局部空间
                    vecArray_local = transVertexToBoneLocal(exportArmatureData, boneName, vecList)

                    calulateBoundingBoxes(vecArray_local, bboxEntry, hasOBB=True)
                    mod3File.BoneBoundingBoxList.append(bboxEntry)

                meshInfo.boundingBoxCount = bboxCount
            else:
                vertArray = np.vstack(meshEntry.vertexDict["Position"])
                meshInfo.boundingBoxCount = 1
                bboxEntry = BoneBoundingBox()
                bboxEntry.boneIndex = 255
                calulateBoundingBoxes(vertArray, bboxEntry, hasOBB=True)
                mod3File.BoneBoundingBoxList.append(bboxEntry)

    # 计算总的包围球和AABB包围盒
    if vertArrayList != []:
        fullVertArray = np.vstack(vertArrayList)
        calulateBoundingBoxes(fullVertArray, mod3File.fileHeader)

    # 判定总数量是否合法
    if vertexCount > MAX_VERTICES_TOTAL:
        addErrorToDict(errorDict, "TotalVerticesExceeded")
    if faceCount * 3 > MAX_FACES_TOTAL:
        addErrorToDict(errorDict, "TotalFacesExceeded")
    if subMeshCount > MAX_MESHS_TOTAL:
        addErrorToDict(errorDict, "TotalMeshesExceeded")
    if len(mod3File.materialNameList) > MAX_MATERIALS_TOTAL:
        addErrorToDict(errorDict, "TotalMaterialsExceeded")
    mod3File.fileHeader.vertexCount = vertexCount
    mod3File.fileHeader.faceCount = faceCount * 3
    mod3File.fileHeader.meshCount = subMeshCount

    mod3DataEndTime = time.time()
    mod3DataExportTime = mod3DataEndTime - mod3DataStartTime
    print(f"Gathering mod3 data took {timeFormat % (mod3DataExportTime * 1000)} ms.")

    # 清理引用数据，参数，对象等
    evaluatedData = None
    if exportArmatureData != None:
        bpy.data.armatures.remove(exportArmatureData)
    for mesh in deleteCopiedMeshList:
        bpy.data.objects.remove(mesh, do_unlink=True)
        # bpy.data.meshes.remove(mesh)
    if "clonedMod3Meshes" in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections["clonedMod3Meshes"])
    deleteCopiedMeshList.clear()

    # 若目标集合中子网格数量为0，则添加报错
    if subMeshCount == 0:
        addErrorToDict(errorDict, "NoMeshesInCollection")

    if errorDict != {}:  # 若errorDict不为空，则打印报错信息到控制台，同时弹出报错信息窗口，然后直接退出函数，返回False
        printMod3ErrorDict(errorDict)
        showMHWMod3ErrorWindow(errorDict, targetCollection.name, armatureName)
        return False

    mod3WriteStartTime = time.time()

    mod3File = buildMod3File(mod3File, targetCollection, groupIDList)
    writeMod3File(mod3File, filePath)

    mod3WriteEndTime = time.time()
    mod3WriteExportTime = mod3WriteEndTime - mod3WriteStartTime
    print(f"Converting to mod3 file took {timeFormat % (mod3WriteExportTime * 1000)} ms.")

    mod3ExportEndTime = time.time()
    mod3ExportTime = mod3ExportEndTime - mod3ExportStartTime
    print(f"Mod3 exported in {timeFormat % (mod3ExportTime * 1000)} ms.")

    print("\nMod3 Info:")
    print(f"Mesh Count: {subMeshCount}")
    print(f"Vertex Count: {vertexCount}")
    print(f"Face Count: {faceCount}")
    if mod3File.skeleton != None:
        print(f"Armature Bone Count: {mod3File.skeleton.boneCount}")

    print(f"Materials ({len(mod3File.materialNameList)}):")
    for materialName in mod3File.materialNameList:
        print(materialName)

    print("\033[92m__________________________________\nMHW Mod3 export finished.\033[0m")
    return True