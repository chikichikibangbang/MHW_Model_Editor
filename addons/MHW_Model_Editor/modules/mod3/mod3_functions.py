import re
import bpy
import bmesh
import numpy as np
from mathutils import Vector, Matrix, Euler
from itertools import chain, repeat, islice
from math import radians, floor, sqrt
from .....common.i18n.i18n import i18n
from .file_mod3 import BoneInfo
from ..common.message_functions import addErrorToDict
from ..common.blender_functions import getCollection

rotateNeg90Matrix = Matrix.Rotation(radians(-90.0), 4, 'X')
rotate90Matrix = Matrix.Rotation(radians(90.0), 4, 'X')
scaleImportMatrix = Matrix.Scale(0.01, 4)
scaleExportMatrix = Matrix.Scale(100, 4)
mod3ImportMatrix = rotate90Matrix @ scaleImportMatrix
exportMatrix = scaleExportMatrix @ rotateNeg90Matrix

# 导入MHW MOD3部分
# --------------------------------
def importSkeleton(boneInfoList, armatureName, collection, armatureType, boneSize):
    """
    导入mod3骨架

    boneInfoList: 从mod3文件解析得到的骨骼信息列表
    armatureName: 骨架对象的名称
    collection: 骨架对象的父级集合
    armatureType: 骨架对象的显示类型，如棍形、八面锥等
    boneSize: 骨骼的显示尺寸

    return 导入完成的骨架对象
    """
    armatureData = bpy.data.armatures.new(armatureName)
    armatureObj = bpy.data.objects.new(armatureName, armatureData)
    collection.objects.link(armatureObj)

    armatureObj.hide_viewport = False
    armatureObj.show_in_front = True
    armatureObj.data.display_type = armatureType
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.mode_set(mode='EDIT')

    boneNameIndexDict = {index: bone.boneName for index, bone in enumerate(boneInfoList)}
    boneParentList = []

    for bone in boneInfoList:
        if bone.boneName == "":
            continue  # 跳过空结构的骨骼
        boneName = bone.boneName
        editBone = armatureData.edit_bones.new(boneName)
        editBone.head = (0.0, 0.0, 0.0)
        editBone.tail = editBone.head + Vector((0.0, 0.0, boneSize))

        if bone.boneParent != 255:
            boneParentList.append((editBone, boneNameIndexDict[bone.boneParent]))

        editBone.matrix = bone.worldMatrix
        editBone.inherit_scale = "NONE"

        editBone["Mod3_Bone_Unkn"] = bone.boneUnkn
        if bone.boneSymmetry != 255:
            editBone["Mod3_Bone_Symmetry"] = boneNameIndexDict[bone.boneSymmetry]

    for editBone, parentBoneName in boneParentList:
        # print(editBone.name, parentBoneName)
        editBone.parent = armatureData.edit_bones[parentBoneName]
    bpy.ops.object.mode_set(mode='OBJECT')

    prevSelection = bpy.context.selected_objects
    for obj in prevSelection:
        obj.select_set(False)

    armatureObj.matrix_world = armatureObj.matrix_world @ mod3ImportMatrix
    armatureObj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    armatureObj.select_set(False)

    for obj in prevSelection:
        obj.select_set(True)

    return armatureObj, boneNameIndexDict

def createMaterialDict(materialNameList):
    """
    创建材质名映射材质的字典

    return 结构如 {材质名: 材质} 的字典
    """
    materialDict = {}
    for materialName in materialNameList:
        material = bpy.data.materials.new(materialName)
        material.use_nodes = True
        materialDict[materialName] = material
    return materialDict

def importMesh(meshName="newMesh", vertexDict={}, faceList=[], boneRemapDict={},
               material="Material", armature=None, collection=None):
    """
    导入mod3网格

    meshName: 网格对象的名称
    vertexDict: 从mod3文件解析得到的顶点信息字典
    faceList: 从mod3文件解析得到的面索引列表
    boneRemapDict: 从mod3文件解析得到的骨骼重映射字典
    material: 分配给网格对象的材质
    armature: 网格对象的绑定骨架
    collection: 网格对象的父级集合
    
    return 导入完成的mod3网格对象
    """
    meshData = bpy.data.meshes.new(meshName)

    # 导入顶点位置信息和面索引信息
    posList = vertexDict["Position"]
    if posList == []:
        # raise Exception("Invalid mesh, submesh has no vertices")
        return
    if faceList == []:
        # raise Exception("Invalid mesh, submesh has no faces")
        return
    meshData.from_pydata(posList, [], faceList)

    # 导入顶点法向信息
    normalList = vertexDict["NorTan"][0]
    if normalList != []:
        meshData.update(calc_edges=True)
        meshData.polygons.foreach_set("use_smooth", [True] * len(meshData.polygons))
        meshData.normals_split_custom_set_from_vertices([normalizeVec(v) for v in normalList])
        if bpy.app.version < (4, 0, 0):
            meshData.use_auto_smooth = True
            meshData.calc_normals_split()

    # 导入顶点UV信息
    UVLayerList = (vertexDict["UV1"], vertexDict["UV2"], vertexDict["UV3"], vertexDict["UV4"])
    for layerIndex, layer in enumerate(UVLayerList):
        if layer != []:
            newUVLayer = meshData.uv_layers.new(name="UVMap" + str(layerIndex))
            for face in meshData.polygons:
                for vertexIndex, loopIndex in zip(face.vertices, face.loop_indices):
                    newUVLayer.data[loopIndex].uv = layer[vertexIndex]

    # 导入顶点色信息
    colorList = vertexDict["Color"]
    if colorList != []:
        vcol_layer = meshData.vertex_colors.new(name="Color")
        for l, color in zip(meshData.loops, vcol_layer.data):
            color.color = colorList[l.vertex_index]

    meshObj = bpy.data.objects.new(meshName, meshData)

    # 导入顶点权重信息
    boneWeightList = vertexDict["Weight"]
    boneIndicesList = vertexDict["Bone"]
    if boneWeightList != []:
        # 将绑定骨骼按照骨骼层级排序，这样可以让网格的顶点组也按照骨骼层级顺序显示
        usedBoneIndices = sorted(list({x for vertex in boneIndicesList for x in vertex}))
        
        for boneIndex in usedBoneIndices:
            boneName = "MhBone_" + str(boneRemapDict[boneIndex]).zfill(3)
            meshObj.vertex_groups.new(name=boneName)

        for vertexIndex, boneIndexList in enumerate(boneIndicesList):
            for weightIndex, boneIndex in enumerate(boneIndexList):
                if boneWeightList[vertexIndex][weightIndex] > 0:
                    boneName = "MhBone_" + str(boneRemapDict[boneIndex]).zfill(3)
                    meshObj.vertex_groups[boneName].add([vertexIndex], boneWeightList[vertexIndex][weightIndex], 'ADD')
                    # if vertexIndex == 2312:
                    #     print(vertexGroupWeightList[vertexIndex])

    if armature != None:
        meshObj.parent = armature
        mod = meshObj.modifiers.new(name='Armature', type='ARMATURE')
        mod.object = armature
    # meshObj.data.transform(rotate90Matrix)
    meshObj.data.transform(mod3ImportMatrix)
    if material != None:
        meshObj.data.materials.append(material)
    if collection != None:
        collection.objects.link(meshObj)
    else:
        bpy.context.scene.collection.objects.link(meshObj)

    return meshObj

def importLODGroup(parsedMod3, mod3Collection, materialDict, armatureObj, hiddenColSet, importAllLODs=False):
    """
    导入lod层级

    parsedMod3: 解析得到的mod3结构
    mod3Collection: mod3集合
    materialDict: 材质名映射材质的字典
    armatureObj: mod3骨架对象
    hiddenColSet: 需要隐藏可见性的lod集合的列表
    importAllLODs: 是否导入全部的lod层级

    return 导入的各lod层级的网格对象数量信息
    """
    LODGroupDict = parsedMod3.meshDict

    boneRemapDict = {}
    if parsedMod3.skeleton and parsedMod3.skeleton.boneRemapDict:
        boneRemapDict = parsedMod3.skeleton.boneRemapDict

    countInfo = ""
    for lod_level, meshList in LODGroupDict.items():
        if meshList == []:
            continue

        # 若导入全部的lod层级，则创建各个lod层级的集合
        if importAllLODs:
            lodCollection = getCollection(f"LOD {lod_level} - {mod3Collection.name}", mod3Collection, makeNew=True)
            LODNum = f"LOD_{lod_level}_"
            countInfo += f"LOD{lod_level}: {len(meshList)} "
        else:
            lodCollection = mod3Collection
            LODNum = ""
            countInfo += f"{len(meshList)}"

        for mesh in meshList:
            meshInfo = mesh.meshInfo
            materialName = parsedMod3.materialNameList[meshInfo.materialID]

            # 导入mod3网格
            meshObj = importMesh(
                meshName=f"{LODNum}Group_{str(meshInfo.groupID)}_Sub_{str(mesh.submeshIndex)}__{materialName}",
                vertexDict=mesh.vertexDict,
                faceList = mesh.faceList,
                boneRemapDict=boneRemapDict,

                material=materialDict[materialName],
                armature=armatureObj,
                collection=lodCollection,
            )

            # 赋予自定义属性
            meshObj.data["Mod3_Mesh_ShadowFlag"] = meshInfo.shadowFlag
            meshObj.data["Mod3_Mesh_RenderMode"] = meshInfo.renderMode
            meshObj.data["Mod3_Mesh_Unkn"] = meshInfo.unkn3
            meshObj.data["Mod3_Mesh_Index"] = meshInfo.meshIndex

        # 隐藏非主要lod层级的集合
        if lod_level not in {"ALL", "0"}:
            # lodCollection.hide_viewport = True
            hiddenColSet.add(lodCollection.name)

    return countInfo

def hideLODCollections(parentCollection, mod3Collection, hiddenColSet):
    """
    隐藏非主要lod集合的可见性

    parentCollection: 嵌套集合结构的总父级集合
    mod3Collection: mod3集合
    hiddenColSet: 需要隐藏可见性的lod集合的列表
    """
    collections = bpy.context.view_layer.layer_collection.children
    targetColName = parentCollection.name if parentCollection != None else mod3Collection.name

    for collection in collections:
        if collection.name == targetColName:

            targetCollection = collection.children[0] if parentCollection != None else collection

            for childCollection in targetCollection.children:
                if childCollection.name in hiddenColSet:
                    childCollection.hide_viewport = True
            break



def importAxisAlignedBoundingBox(bbox, bboxName, mod3Collection, armatureObj=None, boneParent=None):
    bboxVertList = [
        (bbox.min.x/100, bbox.min.y/100, bbox.min.z/100),
        (bbox.max.x/100, bbox.max.y/100, bbox.max.z/100),

    ]
    bboxData = bpy.data.meshes.new(bboxName)
    bboxData.from_pydata(bboxVertList, [], [])
    bboxData.update()

    bboxObj = bpy.data.objects.new(bboxName, bboxData)
    mod3Collection.objects.link(bboxObj)

    if armatureObj != None and boneParent != None:
        boneName = boneParent
        constraint = bboxObj.constraints.new(type="CHILD_OF")
        constraint.target = armatureObj
        constraint.subtarget = boneName
        constraint.name = "BoneName"
        constraint.inverse_matrix = Matrix()
        bboxObj["~TYPE"] = "MHW_MOD3_BONE_AABB"

    else:
        bboxObj["~TYPE"] = "MHW_MOD3_AABB"
        bboxObj.matrix_world = bboxObj.matrix_world @ rotate90Matrix

    bboxObj["Mod3ExportExclude"] = 1

    bboxObj.show_bounds = True
    return bboxObj

def importOrientedBoundingBox(mat, halfsize, obbName, mod3Collection, armatureObj=None, boneParent=None):
    obbMat = Matrix(mat.matrix)
    obbMat.transpose()

    obbData = bpy.data.lattices.new(obbName)
    obbObj = bpy.data.objects.new(obbName, obbData)
    obbObj["Mod3ExportExclude"] = 1
    obbObj.display_type = "BOUNDS"

    obbObj.matrix_world = scaleImportMatrix @ obbMat
    # obbObj.scale = (2 * halfsize.x / 100, 2 * halfsize.y / 100, 2 * halfsize.z / 100)

    # Add the object into the scene.
    mod3Collection.objects.link(obbObj)

    if armatureObj != None and boneParent != None:
        boneName = boneParent
        constraint = obbObj.constraints.new(type="CHILD_OF")
        constraint.target = armatureObj
        constraint.subtarget = boneName
        constraint.name = "BoneName"
        constraint.inverse_matrix = Matrix()
        obbObj["~TYPE"] = "MHW_MOD3_BONE_OBB"

    else:
        obbObj["~TYPE"] = "MHW_MOD3_OBB"
        obbObj.matrix_world = rotate90Matrix @ obbObj.matrix_world

    obbObj.scale = (2 * halfsize.x / 100, 2 * halfsize.y / 100, 2 * halfsize.z / 100)
    return obbObj

def importBoundingSphere(sphere, sphereName, mod3Collection, armatureObj=None, boneParent=None):
    # Create an empty mesh and the object.
    sphereData = bpy.data.meshes.new(sphereName)
    sphereObj = bpy.data.objects.new(sphereName, sphereData)
    sphereObj.location = (sphere.x/100, sphere.y/100, sphere.z/100)
    sphereObj.display_type = "BOUNDS"
    sphereObj.display_bounds_type = "SPHERE"
    # sphereObj["~TYPE"] = "MHW_MOD3_BOUNDING_SPHERE"
    sphereObj["Mod3ExportExclude"] = 1

    # Add the object into the scene.
    mod3Collection.objects.link(sphereObj)

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=8, v_segments=8, radius=sphere.r/100)
    bm.to_mesh(sphereData)
    bm.free()
    bpy.context.view_layer.update()

    if armatureObj != None and boneParent != None:
        boneName = boneParent
        constraint = sphereObj.constraints.new(type="CHILD_OF")
        constraint.target = armatureObj
        constraint.subtarget = boneName
        constraint.name = "BoneName"
        constraint.inverse_matrix = Matrix()
        sphereObj["~TYPE"] = "MHW_MOD3_BONE_BOUNDING_SPHERE"
    else:
        sphereObj["~TYPE"] = "MHW_MOD3_BOUNDING_SPHERE"
        sphereObj.matrix_world = rotate90Matrix @ sphereObj.matrix_world

    # sphereObj.matrix_world = rotate90Matrix @ sphereObj.matrix_world
    return sphereObj

def importBoundingBoxes(mod3BoundingSphere, mod3BoundingBox, mod3Collection):
    mod3Sphere = importBoundingSphere(mod3BoundingSphere, "Mod3_BoundingSphere", mod3Collection)
    mod3BBox = importAxisAlignedBoundingBox(mod3BoundingBox,"Mod3_BoundingBox",mod3Collection)
# --------------------------------


# 导出MHW MOD3部分
# --------------------------------
def pad_infinite(iterable, padding=None):
    return chain(iterable, repeat(padding))
def pad(iterable, size, padding=None):
    return islice(pad_infinite(iterable, padding), size)
def normalize(lst):
    s = sum(lst)
    if s != 0.0:
        return list(map(lambda x: float(x)/s, lst))
    else:
        return lst
def normalizeVec(vec):
    return Vector(vec).normalized()

def vertexPosToGlobal(local_coords, world_matrix):
    # Reshape coords to Nx3 matrix
    local_coords.shape = (-1, 3)

    # Add an extra 1.0s column (for matrix dot product)
    local_coords = np.c_[local_coords, np.ones(local_coords.shape[0])]

    # Then:
    # Dot product matrix with the coords transpose
    # Keep the first 3 rows (x,y,z)
    # Transpose result to Nx3
    # Flatten
    global_coords = np.dot(world_matrix, local_coords.T)[0:3].T.reshape((-1))
    return np.reshape(global_coords, (-1, 3))

def joinObjects(objList):
    if bpy.app.version < (3, 2, 0):
        ctx = bpy.context.copy()

        # one of the objects to join
        ctx['active_object'] = objList[0]
        ctx['selected_editable_objects'] = objList
        bpy.ops.object.join(ctx)
    else:
        with bpy.context.temp_override(active_object=objList[0], selected_editable_objects=objList):
            bpy.ops.object.join()

def sortLODCollections(targetCollection, errorDict):
    """
    将lod集合按层级分类存为字典

    targetCollection: 导出时选择的mod3集合
    errorDict: 报错信息字典

    return lod集合字典，最大lod值
    """
    maxLOD = 0
    lodColDict = {}

    # 先按照子集合名称排序整个子集合列表，以保证lod集合按从小到大的数字排列
    childColList = sorted(targetCollection.children, key=lambda col: col.name)

    pattern = re.compile(r'^LOD (ALL|\d+) -')  # 匹配 "LOD ALL -" 或 "LOD 数字 -"
    for childCol in childColList:
        match = pattern.match(childCol.name)
        if not match:
            continue

        # 如果存在多个相同lod层级的lod集合，则添加报错
        if match.group(1) in lodColDict:
            addErrorToDict(errorDict, "MultipleSameLodCollections")

        if match.group(1) == "ALL":
            # 合并lod all层级和其他层级的键值对，强制让lod all层级在第一位
            lodColDict = {"ALL": (65535, childCol), **lodColDict}
        else:
            maxLOD = int(match.group(1))
            lodColDict[match.group(1)] = (2 ** maxLOD, childCol)

    # 重新计算最大lod层级的lod值，比如最大lod层级为5的话，lod值应为65536 - 2^5 = 65504
    if str(maxLOD) in lodColDict:
        lodColDict[str(maxLOD)] = (65536 - 2 ** maxLOD, lodColDict[str(maxLOD)][1])

    if lodColDict == {}:  # 如果lodColDict仍然为空，说明当前mod3集合中没有lod层级的集合，那么直接将当前mod3集合赋予lod all层级
        lodColDict = {"ALL": (65535, targetCollection)}

    return lodColDict, maxLOD

def parseArmatureData(skeleton, armatureObj, errorDict):
    """
    导出时解析骨架数据

    skeleton: mod3File的Skeleton结构
    armatureObj: 骨架对象
    errorDict: 报错信息字典

    return 应用导出变换的骨架数据，骨骼索引字典
    """
    cloneData = armatureObj.data.copy()  # 复制一份数据用于解析
    skeleton.boneCount = len(cloneData.bones)

    # 若骨架中的骨骼数量超过了最大限制255，则添加报错
    # if skeleton.boneCount > MAX_BONES_TOTAL:
    if skeleton.boneCount > 255:
        # print(f"\nMaximum Bones Exceeded! {mod3File.skeleton.boneCount} / {MAX_BONES_TOTAL}")
        addErrorToDict(errorDict, "MaxBonesExceeded")

    # 应用导出变换
    transform = exportMatrix @ armatureObj.matrix_world
    cloneData.transform(transform)

    indexDict = {}  # 骨骼名称映射骨骼索引的字典
    posDict = {}  # 骨骼坐标映射骨骼索引的字典

    # 首次遍历构建两个字典，用于二次遍历时获取信息
    for index, bone in enumerate(armatureObj.data.bones):
        indexDict[bone.name] = index
        posDict[bone.name] = {"pos": bone.head_local,
                              "sym": bone.get("Mod3_Bone_Symmetry", "")}  # 用于处理镜像骨骼

    pattern = re.compile(r'^MhBone_\d{3}$')  # 严格匹配 "MhBone__xxx"
    for index, bone in enumerate(cloneData.bones):
        boneInfo = BoneInfo()
        boneInfo.boneUnkn = bone.get("Mod3_Bone_Unkn", 0.0)

        if pattern.match(bone.name):
            boneInfo.boneFunction = int(bone.name.split("MhBone_")[1])

            # 若骨骼的boneFunction超过了最大限制511，则添加报错
            # if boneInfo.boneFunction > MAX_BONE_FUNCTION:
            if boneInfo.boneFunction > 511:
                addErrorToDict(errorDict, "IncorrectBoneNameFormat", boneName=bone.name)
        else:
            # 若骨骼名称不符合MhBone_xxx的格式，则添加报错
            addErrorToDict(errorDict, "IncorrectBoneNameFormat", boneName=bone.name)

        '''没有比较好的判定对称骨骼的方法，暂时还是靠自定义属性来辅助判定'''
        boneHeadPos = posDict[bone.name]["pos"]  # 当前骨骼的头部坐标
        symName = posDict[bone.name]["sym"]  # 当前骨骼的Symmetry属性指向的骨骼名

        # 若当前骨骼坐标的x分量接近0，则其对称骨骼即为自身
        # if abs(boneHeadPos[0]) <= 1e-6:
        if abs(boneHeadPos[0]) <= 5e-4:
            boneInfo.boneSymmetry = index
        # 否则用当前骨骼的Symmetry属性在字典中获取指向骨骼，若二者的Symmetry属性指向闭合，再进一步判断骨骼坐标是否对称
        elif symName in posDict and posDict[symName]["sym"] == bone.name:
            symHeadPos = posDict[symName]["pos"]
            # if abs(boneHeadPos[0] + symHeadPos[0]) <= 1e-6 \
            #         and abs(boneHeadPos[1] - symHeadPos[1]) <= 1e-6 \
            #         and abs(boneHeadPos[2] - symHeadPos[2]) <= 1e-6:
            if abs(boneHeadPos[0] + symHeadPos[0]) <= 5e-4 \
                    and abs(boneHeadPos[1] - symHeadPos[1]) <= 5e-4 \
                    and abs(boneHeadPos[2] - symHeadPos[2]) <= 5e-4:
                # 若满足以上条件，则确定指向骨骼为当前骨骼的对称骨骼
                boneInfo.boneSymmetry = indexDict[symName]

        # 获取父级骨骼索引，并计算局部矩阵
        if bone.parent != None:
            boneInfo.boneParent = indexDict[bone.parent.name]
            localMatrix = (bone.matrix_local.to_4x4().transposed()) @ (
                bone.parent.matrix_local.to_4x4().transposed().inverted())
        else:
            # boneInfo.boneParent = 255
            localMatrix = bone.matrix_local.transposed()

        # 计算世界矩阵
        worldMatrix = bone.matrix_local.to_4x4().transposed().inverted()

        boneVector = np.array(localMatrix[3][:3])  # 取最后一列的前3个元素
        boneInfo.boneLength = np.linalg.norm(boneVector)  # 直接计算模长
        boneInfo.bonePos.x, boneInfo.bonePos.y, boneInfo.bonePos.z = boneVector

        skeleton.boneInfoList.append(boneInfo)
        skeleton.localMatList.append([list(row) for row in localMatrix])
        skeleton.worldMatList.append([list(row) for row in worldMatrix])
        skeleton.boneRemapDict[index] = boneInfo.boneFunction

    return cloneData, indexDict

def createCloneMesh(obj, dg, deleteCopiedMeshList, languageCode=""):
    """
    创建克隆网格对象

    obj: 需要克隆的网格对象
    dg: 当前场景的依赖图
    deleteCopiedMeshList: 待删除的克隆网格对象的列表

    return 克隆网格对象
    """
    cloneObj = obj.copy()  # 克隆一份网格对象，用于处理重叠UV和分离锐边，同时不影响原网格对象
    cloneObj.name = "CLN_" + obj.name
    # 获取评估后的网格对象数据（相当于应用了所有修改器）
    cloneObj.data = bpy.data.meshes.new_from_object(obj.evaluated_get(dg))
    clonedMeshCollection = getCollection("clonedMod3Meshes")
    clonedMeshCollection.objects.link(cloneObj)

    if languageCode in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
        print(f"已创建 {obj.name} 的临时克隆对象: {cloneObj.name}")
    else:
        print(f"Created temporary clone of {obj.name}: {cloneObj.name}")
    deleteCopiedMeshList.append(cloneObj)  # 将克隆网格对象添加到待删除列表

    return cloneObj

def parseMeshGroupID(obj, groupIDList, languageCode=""):
    """
    解析网格对象的groupID

    obj: 网格对象
    groupIDList: 存放groupID的列表（此处实际是集合，可以直接去重）

    return groupID
    """
    match = re.search(r"Group_(\d+)", obj.name)  # 匹配第一个符合的"Group_数字"
    if match:
        groupID = int(match.group(1))
    else:
        if languageCode in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            print(f"无法解析 {obj.name} 的网格组ID, 设置为0.")
        else:
            print(f"Could not parse group ID of {obj.name}, setting to 0.")
        groupID = 0
    groupIDList.add(groupID)  # 添加groupID到列表中

    return groupID

def getUsedVertexGroup(obj, cloneObj, boneIndexDict):
    """
    获取有效绑定顶点组（即顶点组有对应的绑定骨骼，且顶点组有权重）

    obj: 原网格对象
    cloneObj: 克隆网格对象
    boneIndexDict: 骨骼索引字典

    return 骨骼名称映射绑定顶点坐标列表的字典，顶点组索引映射顶点组名称的字典
    """
    # 创建克隆网格对象的所有已使用的顶点组索引集合（即权重不为零的顶点组）
    used_vg_indices = {g.group
                       for v in cloneObj.data.vertices
                       for g in v.groups
                       if g.weight > 0}
    boneVertDict = dict()  # 骨骼名称映射绑定顶点坐标列表的字典
    vgIndexToNameDict = dict()  # 顶点组索引映射顶点组名称的字典

    for vg in obj.vertex_groups:  # 遍历原网格对象的顶点组
        # 如果当前顶点组索引在索引集合中（即该顶点组有权重），且顶点组名称在骨骼索引字典中（即顶点组有对应的骨骼），那么该顶点组为有效绑定顶点组
        if vg.index in used_vg_indices and vg.name in boneIndexDict:
            boneVertDict[vg.name] = []
            vgIndexToNameDict[vg.index] = vg.name

    return boneVertDict, vgIndexToNameDict

def parseMaterialName(obj, evaluatedData, errorDict, useBLMaterialName=False, languageCode=""):
    """
    解析网格对象的材质名

    obj: 网格对象
    evaluatedData: 克隆网格对象的评估后的数据
    errorDict: 报错信息字典
    useBLMaterialName: 是否使用blender的材质名称来获取材质名

    return 材质名
    """
    materialName = "NO_ASSIGNED_MATERIAL"
    if useBLMaterialName:  # 如果勾选使用材质名称，则尝试从网格对象的材质获取材质名
        # 如果网格对象有材质槽，且第一个材质槽分配了材质，则从第一个材质获取材质名，否则转而尝试从网格对象的名称获取材质名
        if evaluatedData.materials and evaluatedData.materials[0]:
            materialName = evaluatedData.materials[0].name.split(".")[0]
        else:
            try:
                materialName = obj.name.split("__", 1)[1].split(".")[0]
            except:  # 如果仍然未获取到材质名，在添加报错
                addErrorToDict(errorDict, "NoMaterialOnSubMesh", objectName=obj.name)
    else:  # 如果未勾选使用材质名称，则尝试从网格对象的名称获取材质名
        try:
            materialName = obj.name.split("__", 1)[1].split(".")[0]
        except:  # 如果获取材质名失败，则尝试从网格对象的材质获取材质名
            if languageCode in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                print(f"无法拆分 {obj.name} 的材质名称, 改用blender的材质名称")
            else:
                print(f"Couldn't split material name on {obj.name}, using blender material name instead")
            if evaluatedData.materials and evaluatedData.materials[0]:
                materialName = evaluatedData.materials[0].name.split(".")[0]
            else:  # 如果仍然未获取到材质名，在添加报错
                addErrorToDict(errorDict, "NoMaterialOnSubMesh", objectName=obj.name)

    return materialName

def initUVColorDict(obj, evaluatedData, vertexDict, armatureObj, errorDict):
    """
    初始化顶点UV字典和顶点色字典

    obj: 原网格对象
    evaluatedData: 克隆网格对象的评估后的数据
    vertexDict: MeshInfo结构的顶点元素字典
    armatureObj: 骨架对象
    errorDict: 报错信息字典

    return 区块类型的扩展名称，UV通道是否存在的布尔值列表，顶点色是否存在的布尔值，UV通道字典
    """
    blockNameExtend = ""
    meshHasUV = [False] * 4
    meshHasColor = False
    UVDict = {f"UV{i + 1}": {} for i in range(4)}  # 用于检查顶点是否有重叠UV

    # if any([len(face) != 3 for face in meshEntry.faceList]):
    #     addErrorToDict(errorDict, "NonTriangulatedFace", objectName=obj.name)
    if len(evaluatedData.uv_layers) > 0:
        meshHasUV[0] = True
        vertexDict["UV1"] = np.zeros((len(evaluatedData.vertices), 2))
        blockNameExtend += "UV1"
    else:
        addErrorToDict(errorDict, "NoUVMapOnSubMesh", objectName=obj.name)
    if len(evaluatedData.uv_layers) > 1:
        meshHasUV[1] = True
        vertexDict["UV2"] = np.zeros((len(evaluatedData.vertices), 2))
        blockNameExtend += "UV2"
    if len(evaluatedData.vertex_colors) > 0:
        meshHasColor = True
        vertexDict["Color"] = np.zeros((len(evaluatedData.vertices), 4))
        if armatureObj == None:  # 仅在网格对象有顶点色，且没有骨架时尝试获取UV3和UV4
            if len(evaluatedData.uv_layers) > 2:
                meshHasUV[2] = True
                vertexDict["UV3"] = np.zeros((len(evaluatedData.vertices), 2))
                blockNameExtend += "UV3"
            if len(evaluatedData.uv_layers) > 3:
                meshHasUV[3] = True
                vertexDict["UV4"] = np.zeros((len(evaluatedData.vertices), 2))
                blockNameExtend += "UV4"
        blockNameExtend += "Color"

    return blockNameExtend, meshHasUV, meshHasColor, UVDict

def parseVertexDict(vertexDict, meshInfo, vertArrayList, vertexPosList, vertexNorList,
                    vertexTanList, vertexColorList, vertexWeightList, vertexIndicesList):

    vertexDict["Position"] = np.array(vertexPosList)
    vertArrayList.extend(vertexDict["Position"])  # 将当前网格对象的所有顶点坐标向量添加进vertArrayList
    vertexDict["NorTan"] = [np.array(vertexNorList), np.array(vertexTanList)]
    if vertexColorList:
        vertexDict["Color"] = np.array(vertexColorList)

    maxLength = 0  # 记录当前网格对象的所有顶点的有效绑定顶点组的最大数量，后续用于赋值weightDynamics
    if vertexWeightList:
        vertexWeightArray = np.array(vertexWeightList)
        vertexIndicesArray = np.array(vertexIndicesList)
        weightString = "Weight8Bone8"
        maxLength = np.max(np.sum(vertexWeightArray != 0.0, axis=1))  # 计算每行权重中非零权重的最大长度
        if maxLength <= 4:  # 如果maxLength小于等于4，则按照4列进行切片，否则默认8列
            vertexWeightArray = vertexWeightArray[:, :4]
            vertexIndicesArray = vertexIndicesArray[:, :4]
            weightString = "Weight4Bone4"

        vertexDict["Weight"] = vertexWeightArray
        vertexDict["Bone"] = vertexIndicesArray
        meshInfo.blockName += weightString
    # print(meshEntry.vertexDict)

    meshInfo.weightDynamics = 8 * maxLength + 1  # TODO 研究weightDynamics为5的情况
    # print("weightDynamics: ", meshInfo.weightDynamics)

def dist(a, b) -> float:
    return  ((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5
def dist_squared(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return dx * dx + dy * dy + dz * dz
def caculateBoundingSphere(points, center):
    max_radius_squared = 0.0
    for p in points:
        d_sq = dist_squared(p, center)
        if d_sq > max_radius_squared:
            max_radius_squared = d_sq
    radius = sqrt(max_radius_squared)
    return radius

def caculateOBB(points):
    # 计算协方差矩阵
    cov = np.cov(points.T)
    # 特征值分解，得到主轴方向
    eigvals, eigvecs = np.linalg.eigh(cov)
    # 按特征值大小排序，获取主方向
    order = np.argsort(eigvals)[::-1]
    eigvecs = eigvecs[:, order]
    # 确保右手坐标系
    if np.linalg.det(eigvecs) < 0:
        eigvecs[:, 2] = -eigvecs[:, 2]  # 修正第三个轴
    # 将点转换到OBB局部坐标系
    localVec = np.dot(points, eigvecs)
    # 计算局部坐标系下的半长和中心点
    minVec = np.min(localVec, axis=0)
    maxVec = np.max(localVec, axis=0)
    halfSize = (maxVec - minVec) / 2
    centerLocal = (maxVec + minVec) / 2
    # 将局部中心转换回世界坐标系
    centerWorld = np.dot(eigvecs, centerLocal)
    # 构建OBB矩阵
    obbMat = np.eye(4)
    obbMat[:3, :3] = eigvecs
    obbMat[:3, 3] = centerWorld
    obbMat = obbMat.T
    return obbMat, halfSize

def transVertexToBoneLocal(exportArmatureData, boneName, vecList):
    # 获取骨骼的局部变换矩阵（4x4）
    boneMatrix = exportArmatureData.bones[boneName].matrix_local
    # 计算骨骼矩阵的逆矩阵
    boneMatrixInv = np.array(boneMatrix.inverted())
    # 将顶点坐标转换为齐次坐标 (N,4)
    vecArray = np.array(vecList)
    ones = np.ones((vecArray.shape[0], 1))
    vecArray_h = np.hstack([vecArray, ones])  # (N,4)
    # 变换到骨骼局部空间
    vecArray_local_h = (boneMatrixInv @ vecArray_h.T).T  # (N,4)
    # 取前三个分量作为局部坐标
    vecArray_local = vecArray_local_h[:, :3]

    return vecArray_local
def calulateBoundingBoxes(vertAarry, bboxEntry, hasOBB=False):
    minVec = np.min(vertAarry, axis=0)
    maxVec = np.max(vertAarry, axis=0)

    bboxEntry.aabb.min.x = minVec[0]
    bboxEntry.aabb.min.y = minVec[1]
    bboxEntry.aabb.min.z = minVec[2]
    bboxEntry.aabb.max.x = maxVec[0]
    bboxEntry.aabb.max.y = maxVec[1]
    bboxEntry.aabb.max.z = maxVec[2]

    # 包围球的球心固定在包围盒的中心点
    center = (maxVec + minVec) / 2
    radius = caculateBoundingSphere(vertAarry, center)
    bboxEntry.sphere.x = center[0]
    bboxEntry.sphere.y = center[1]
    bboxEntry.sphere.z = center[2]
    bboxEntry.sphere.r = radius

    '''暂时不清楚为什么有时游戏解包的mod3模型的某些网格的OBB会和AABB完全一致，即使顶点分布具有明显的方向性'''
    '''另外注意，导出时计算得到的OBB与原文件的OBB不一致是正常现象'''
    if hasOBB:
        if vertAarry.shape[0] >= 2:
            obbMat, halfSize = caculateOBB(vertAarry)
        else:
            obbMat = np.eye(4)
            obbMat[:3, 3] = center
            obbMat = obbMat.T
            halfSize = [0, 0, 0]
        bboxEntry.obb_halfsize.x = halfSize[0]
        bboxEntry.obb_halfsize.y = halfSize[1]
        bboxEntry.obb_halfsize.z = halfSize[2]

        bboxEntry.obb_matrix.matrix = [list(row) for row in obbMat]
# --------------------------------













