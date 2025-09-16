import glob
import math
import re
import numpy as np
from ..mrl3.blender_mrl3 import importMHWMrl3File
from .file_mod3 import MHWMod3, readMHWMod3, writeMHWMod3, Vec3, Matrix4x4, \
    Sphere, BoneInfo, Skeleton, Mesh, BoneBoundingBox
from .mod3_parser import ParsedMHWMod3, buildMod3File
import bpy
from math import radians, floor, sqrt
from mathutils import Vector, Matrix, Euler
from itertools import chain, repeat, islice
import time
import os
import bmesh
from ..common.general_function import splitNativesPath, raiseWarning
from .mod3_export_errors import addErrorToDict, printErrorDict, showMHWMod3ErrorWindow
from ..mrl3.blender_mod3_mrl3 import importMHWMrl3
from ..mrl3.file_mrl3 import readMHWMrl3

timeFormat = "%d"
rotateNeg90Matrix = Matrix.Rotation(radians(-90.0), 4, 'X')
rotate90Matrix = Matrix.Rotation(radians(90.0), 4, 'X')
scaleImportMatrix = Matrix.Scale(0.01, 4)
scaleExportMatrix = Matrix.Scale(100, 4)


def triangulateMesh(mesh):
    # BMesh triangulation screws up normals, so save them and reset them after triangulation
    # custom_normals = None
    # if mesh.has_custom_normals:
    #    custom_normals = [0.0]*len(mesh.vertices)
    #    for vertex in mesh.vertices:
    #        custom_normals[vertex.index] = vertex.normal.copy()

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bm.to_mesh(mesh)
    bm.free()
    # if custom_normals:
    # mesh.normals_split_custom_set_from_vertices(custom_normals)
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
def createMaterialDict(materialNameList):
    materialDict = {}
    for materialName in materialNameList:
        material = bpy.data.materials.new(materialName)
        material.use_nodes = True;
        materialDict[materialName] = material
    return materialDict

#创建新的Mod3集合
#参数：collectionName（表示新集合的名称），parentCollection（表示新集合的父集合，默认为None，即没有父集合）
def createmod3Collection(collectionName,parentCollection = None):
    #创建一个新集合，集合名称为collectionName
    collection = bpy.data.collections.new(collectionName)
    #给新集合设置一个颜色标签
    collection.color_tag = "COLOR_01"
    #给新集合添加一个自定义属性 ~TYPE，并将其值设置为 "MOD3_COLLECTION"
    collection["~TYPE"] = "MHW_MOD3_COLLECTION"
    #如果有父集合，则将新集合作为子集合；如果没有父集合，则将新集合添加到当前场景的主集合中
    if parentCollection != None:
        parentCollection.children.link(collection)
    else:
        bpy.context.scene.collection.children.link(collection)
    #返回新创建的集合对象
    return collection

#根据提供的集合名称（collectionName）获取对应的集合
#参数：collectionName（要获取或创建的集合的名称），parentCollection（表示新集合的父集合，默认为None，即没有父集合），makeNew（布尔值，指定当集合不存在时是否创建新集合，默认为False）
def getCollection(collectionName,parentCollection = None,makeNew = False):
    if makeNew or not bpy.data.collections.get(collectionName):
        collection = bpy.data.collections.new(collectionName)
        collectionName = collection.name
        if parentCollection != None:
            parentCollection.children.link(collection)
        else:
            bpy.context.scene.collection.children.link(collection)
    return bpy.data.collections[collectionName]

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
    eigvals, eigvecs = np.linalg.eig(cov)
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


# def importSkeleton(parsedSkeleton, armatureName, collection, ArmatureDisplayType, BonesDisplaySize):
#     armatureData = bpy.data.armatures.new(armatureName)
#     armatureObj = bpy.data.objects.new(armatureName, armatureData)
#     armatureObj.show_in_front = True
#     armatureObj.data.display_type = ArmatureDisplayType
#     #骨架X轴旋转90度，三维缩小0.01倍
#     armatureObj.rotation_mode = "XYZ"
#     armatureObj.rotation_euler.rotate(Euler([math.radians(90), 0, 0]))
#     armatureObj.scale *= Vector([0.01, 0.01, 0.01])
#
#     collection.objects.link(armatureObj)
#     armatureObj.hide_viewport = False
#     bpy.context.view_layer.objects.active = armatureObj
#     bpy.ops.object.mode_set(mode='EDIT')
#     rootbone = armatureData.edit_bones.new("Root")
#     rootbone.head = (0.0, 0.0, 0.0)
#     rootbone.tail = (0.0, BonesDisplaySize, 0.0)
#     boneNameIndexDict = {index: bone.boneName for index, bone in enumerate(parsedSkeleton.boneList)}
#     boneParentList = []
#
#     for bone in parsedSkeleton.boneList:
#         if bone.boneName == '':
#             continue #跳过空结构的骨骼
#         boneName = bone.boneName
#         editBone = armatureData.edit_bones.new(boneName)
#         editBone.head = (0.0, 0.0, 0.0)
#         editBone.tail = (bone.boneposition.x, bone.boneposition.y, bone.boneposition.z)
#         editBone.tail = (0.0, BonesDisplaySize, 0.0)
#
#         if bone.parentIndex != 255:
#             boneParentList.append((editBone, bone.localMatrix, boneNameIndexDict[bone.parentIndex]))
#         else:
#             editBone.parent = rootbone
#             localmat = Matrix(bone.localMatrix.matrix)
#             localmat.transpose()
#             editBone.matrix = editBone.matrix @ localmat
#
#         editBone.inherit_scale = "NONE"
#
#         '''考虑去掉这两个自定义属性，unknfloat似乎并没有实际读到内存中（或者说没有起到作用），summetry考虑导出时自动按镜像匹配'''
#         editBone["mod3_unknfloat"] = bone.unknfloat
#         # if bone.symmetryBoneIndex != 255:
#         #     editBone["symmetry"] = parsedSkeleton.boneRemapDict[bone.symmetryBoneIndex]
#
#
#     for editBone, mat, parentBoneName in boneParentList:
#         editBone.parent = armatureData.edit_bones[parentBoneName]
#         localmat = Matrix(mat.matrix)
#         localmat.transpose()
#         editBone.matrix = editBone.parent.matrix @ localmat
#
#
#     bpy.ops.armature.select_all(action='DESELECT')
#     bpy.ops.object.mode_set(mode='OBJECT')
#
#     #应用全部变换
#     armatureObj.select_set(True)
#     bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
#     armatureObj.select_set(False)
#
#     return armatureObj


def importSkeleton(boneInfoList, armatureName, collection, ArmatureDisplayType, BonesDisplaySize):
    armatureData = bpy.data.armatures.new(armatureName)
    armatureObj = bpy.data.objects.new(armatureName, armatureData)
    collection.objects.link(armatureObj)

    armatureObj.hide_viewport = False
    armatureObj.show_in_front = True
    armatureObj.data.display_type = ArmatureDisplayType
    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.mode_set(mode='EDIT')

    # rootbone = armatureData.edit_bones.new("Root")
    # rootbone.head = (0.0, 0.0, 0.0)
    # rootbone.tail = (0.0, BonesDisplaySize, 0.0)
    boneNameIndexDict = {index: bone.boneName for index, bone in enumerate(boneInfoList)}
    boneParentList = []

    for bone in boneInfoList:
        if bone.boneName == "":
            continue #跳过空结构的骨骼
        boneName = bone.boneName
        editBone = armatureData.edit_bones.new(boneName)
        editBone.head = (0.0, 0.0, 0.0)
        editBone.tail = editBone.head + Vector((0.0, 0.0, BonesDisplaySize))

        if bone.boneParent != 255:
            boneParentList.append((editBone, boneNameIndexDict[bone.boneParent]))
        # else:
        #     editBone.parent = rootbone

        editBone.matrix = bone.worldMatrix
        editBone.inherit_scale = "NONE"

        '''考虑去掉这两个自定义属性，unknfloat似乎并没有实际读到内存中（或者说没有起到作用），summetry考虑导出时自动按镜像匹配'''
        editBone["mod3_unknfloat"] = bone.boneUnkn
        # if bone.symmetryBoneIndex != 255:
        #     editBone["symmetry"] = parsedSkeleton.boneRemapDict[bone.symmetryBoneIndex]

    for editBone, parentBoneName in boneParentList:
        editBone.parent = armatureData.edit_bones[parentBoneName]
    bpy.ops.object.mode_set(mode='OBJECT')

    prevSelection = bpy.context.selected_objects
    for obj in prevSelection:
        obj.select_set(False)

    armatureObj.matrix_world = armatureObj.matrix_world @ rotate90Matrix @ scaleImportMatrix
    armatureObj.select_set(True)
    # I would prefer not to use bpy.ops but the data.transform on armatures does not function correctly.
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    armatureObj.select_set(False)

    for obj in prevSelection:
        obj.select_set(True)

    return armatureObj


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

    # bboxObj["~TYPE"] = "MHW_MOD3_BOUNDING_BOX"
    # bboxObj.matrix_world = bboxObj.matrix_world @ rotate90Matrix

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
    obbObj.scale = (2 * halfsize.x / 100, 2 * halfsize.y / 100, 2 * halfsize.z / 100)

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

# def importBoundingBoxes(mod3BoundingBox,mod3BoundingSphere,mod3Collection,armatureObj,parsedSkeleton = None):
def importBoundingBoxes(mod3BoundingSphere, mod3BoundingBox, mod3Collection, armatureObj, parsedSkeleton=None):
    mod3Sphere = importBoundingSphere(mod3BoundingSphere, "Mod3_BoundingSphere", mod3Collection)
    mod3BBox = importAxisAlignedBoundingBox(mod3BoundingBox,"Mod3_BoundingBox",mod3Collection)

    # if parsedSkeleton != None:
    #     for bone in parsedSkeleton.boneList:
    #         if bone.boundingBox != None:
    #             importBoundingBox(bone.boundingBox,f"Bone Bounding Box ({bone.boneName})",mod3Collection,armatureObj,bone.boneName)


def importLODGroup(parsedMod3,mod3Collection,materialDict,armatureObj,hiddenCollectionSet,importAllLODs = False,createCollections = True):

    LODGroupDict = parsedMod3.meshDict

    boneRemapDict = {}
    if parsedMod3.skeleton and parsedMod3.skeleton.boneRemapDict:
        boneRemapDict = parsedMod3.skeleton.boneRemapDict

    # #若不导入全部的LOD层，则只将LOD All和LOD 0重新赋值给LODGroupDict
    # if not importAllLODs and LODGroupDict != {}:
    #     # LODGroupList = [LODGroupList[0]]
    #     LODGroupDict = {"All": LODGroupDict["All"], "0": LODGroupDict["0"]}

    for lod_level, meshList in LODGroupDict.items():
        if meshList != []:
            #若导入全部的LOD层，则创建各个LOD层的集合
            if createCollections and importAllLODs:
                lodCollection = getCollection(f"LOD {lod_level} - {mod3Collection.name}", mod3Collection, makeNew=True)
                LODNum = f"LOD_{lod_level}_"
            else:
                lodCollection = mod3Collection
                LODNum = ""
            #如果当前循环的LOD层不是LOD 0，则将LOD集合添加到hiddenCollectionSet中，以便后续隐藏可视性
            # if not firstLOD and createCollections:
            #     hiddenCollectionSet.add(lodCollection.name)
            if lod_level not in ["ALL", "0"] and createCollections:
                hiddenCollectionSet.add(lodCollection.name)

            for mesh in meshList:
                vertexDict = mesh.vertexDict
                faceList = mesh.faceList
                #判断当前mesh属于4wt还是8wt，或者是没有权重
                # weight_key = "4Weight" if vertexDict.get("4Weight") else "8Weight"
                # if vertexDict.get(weight_key):
                #     vertexGroupWeightList = vertexDict[weight_key][0]
                #     vertexGroupBoneIndicesList = vertexDict[weight_key][1]
                # else:
                #     vertexGroupWeightList = []
                #     vertexGroupBoneIndicesList = []

                materialName = parsedMod3.materialNameList[mesh.meshInfo.materialID]

                #导入模型
                meshObj = importMod3Mesh(
                    # meshName=f"{LODNum}Group_{str(mesh.meshInfo.groupID)}_Sub_{str(mesh.meshInfo.meshIndex)}",
                    meshName=f"{LODNum}Group_{str(mesh.meshInfo.groupID)}_Sub_{str(mesh.submeshIndex)}__{materialName}",
                    vertexList=vertexDict["Position"],
                    faceList=faceList,
                    vertexNormalList=vertexDict["NorTan"][0],
                    vertexColorList=vertexDict["Color"],
                    UVList=vertexDict["UV"],
                    UV2List=vertexDict["UV2"],
                    UV3List=vertexDict["UV3"],
                    UV4List=vertexDict["UV4"],
                    boneRemapDict=boneRemapDict,
                    boneWeightList=vertexDict["Weight"],
                    boneIndicesList=vertexDict["Bone"],

                    material=materialDict[materialName],
                    armature=armatureObj,
                    collection=lodCollection,
                )

                meshObj.data["Mod3_Mesh_ShadowFlag"] = mesh.meshInfo.shadowFlag
                meshObj.data["Mod3_Mesh_RenderMode"] = mesh.meshInfo.renderMode
                meshObj.data["Mod3_Mesh_Unkn"] = mesh.meshInfo.unkn3
                meshObj.data["Mod3_Mesh_Index"] = mesh.meshInfo.meshIndex



def importMod3Mesh(meshName = "newMesh",vertexList = [],faceList = [],vertexNormalList = [],vertexColorList = [],UVList = [],UV2List = [],UV3List = [],UV4List = [],boneRemapDict = {},boneWeightList = [],boneIndicesList = [],material="Material",armature = None,collection = None):
    meshData = bpy.data.meshes.new(meshName)

    # Import vertices and faces
    if vertexList == []:
        # print(meshName)
        # raise Exception("Invalid mesh, submesh has no vertices")
        return
    if faceList == []:
        # raise Exception("Invalid mesh, submesh has no faces")
        return
    meshData.from_pydata(vertexList, [], faceList)

    # Import vertex normals
    if vertexNormalList != []:
        meshData.update(calc_edges=True)
        meshData.polygons.foreach_set("use_smooth", [True] * len(meshData.polygons))
        meshData.normals_split_custom_set_from_vertices([normalizeVec(v) for v in vertexNormalList])
        if bpy.app.version < (4, 0, 0):
            meshData.use_auto_smooth = True
            meshData.calc_normals_split()

    # Import UV Layers
    UVLayerList = (UVList, UV2List, UV3List, UV4List)
    for layerIndex, layer in enumerate(UVLayerList):
        if layer != []:
            newUVLayer = meshData.uv_layers.new(name="UVMap" + str(layerIndex))
            for face in meshData.polygons:
                for vertexIndex, loopIndex in zip(face.vertices, face.loop_indices):
                    newUVLayer.data[loopIndex].uv = layer[vertexIndex]

    # Import vertex color layer
    if vertexColorList != []:
        vcol_layer = meshData.vertex_colors.new(name="Color")
        for l, color in zip(meshData.loops, vcol_layer.data):
            color.color = vertexColorList[l.vertex_index]

    meshObj = bpy.data.objects.new(meshName, meshData)

    # Import Weights
    if boneWeightList != []:
        # 将绑定骨骼按照骨架层级排序
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
    meshObj.data.transform(rotate90Matrix)

    if material != None:
        meshObj.data.materials.append(material)

    if collection != None:
        collection.objects.link(meshObj)
    else:
        bpy.context.scene.collection.objects.link(meshObj)

    return meshObj


def loadMrl3(options, filePath, materialDict, parentCollection, warningList):
    #确定mrl3文件路径
    mrl3Path = options["mrl3Path"] if options["mrl3Path"] else f"{glob.escape(filePath.split('.mod3')[0])}.mrl3"
    if not os.path.isfile(mrl3Path):
        warning = f"An error occurred while reading {mrl3Path} - File is not found."
        raiseWarning(warning)
        warningList.append(warning)
        return

    try:
        #提取根路径
        split = splitNativesPath(mrl3Path)
        chunkPath = split[0] if split else None

        #读取mrl3文件
        mrl3ImportStartTime = time.time()
        try:
            mrl3ReadStartTime = time.time()
            mrl3File = readMHWMrl3(mrl3Path, materialDict)
            mrl3ReadEndTime = time.time()
            mrl3ReadTime = mrl3ReadEndTime - mrl3ReadStartTime
            print(f"Mrl3 reading took {timeFormat % (mrl3ReadTime * 1000)} ms.")
        except Exception as err:
            warning = f"An error occurred while reading {mrl3Path} - {str(err)}"
            raiseWarning(warning)
            warningList.append(warning)
            return

        # 导入mrl3数据
        if options["loadMrl3Data"]:
            print("Loading mrl3 data...")
            importMHWMrl3File(mrl3File, mrl3Path, materialDict, parentCollection=parentCollection)

        # 导入材质
        if options["loadMaterials"] and not options["importArmatureOnly"]:
            print("Loading mod3 materials from mrl3...")
            if chunkPath:
                importMHWMrl3(mrl3File, materialDict, options["loadUnusedTextures"],
                              options["loadUnusedProps"], options["useBackfaceCulling"],
                              options["reloadCachedTextures"], chunkPath, mrl3Path=mrl3Path,
                              arrangeNodes=True)
                mrl3ImportEndTime = time.time()
                mrl3ImportTime = mrl3ImportEndTime - mrl3ImportStartTime
                print(f"Materials loading took {timeFormat % (mrl3ImportTime * 1000)} ms.")
            else:
                warning = f"An error occurred while loading materials from {mrl3Path} - File is not under the chunk or nativePC path."
                raiseWarning(warning)
                warningList.append(warning)

    except Exception as err:
        warningList.append(f"An error occurred while importing {mrl3Path} - {str(err)}")


def importMHWMod3File(filePath, options):
    mod3ImportStartTime = time.time()
    fileName = os.path.split(filePath)[1].split(".mod3")[0]

    warningList = []
    errorList = []

    if options["clearScene"]:
        for collection in bpy.data.collections:
            for obj in collection.objects:
                collection.objects.unlink(obj)
            bpy.data.collections.remove(collection)
        for bpy_data_iter in (bpy.data.objects, bpy.data.meshes, bpy.data.lights, bpy.data.cameras):
            for id_data in bpy_data_iter:
                bpy_data_iter.remove(id_data)
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
        for amt in bpy.data.armatures:
            bpy.data.armatures.remove(amt)
        for obj in bpy.data.objects:
            bpy.data.objects.remove(obj)
            obj.user_clear()
        for nodeGroup in bpy.data.node_groups:
            bpy.data.node_groups.remove(nodeGroup)
        for img in bpy.data.images:
            if not img.users:
                bpy.data.images.remove(img)

    print("\033[96m__________________________________\nMHW Mod3 import started.\033[0m")

    # mod3ReadStartTime = time.time()
    #读取Mod3文件结构
    Mod3 = readMHWMod3(filePath, options)
    mod3FileName = os.path.split(filePath)[1]
    # mod3ReadEndTime = time.time()
    # mod3ReadTime = mod3ReadEndTime - mod3ReadStartTime
    # print(f"Mod3 reading took {timeFormat % (mod3ReadTime * 1000)} ms.")

    # #使用datetime.fromtimestamp()函数将时间戳转换为datetime对象
    # dt_object = datetime.datetime.fromtimestamp(Mod3.fileHeader.timestamp)
    # #格式化输出日期和时间
    # formatted_date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    # print("Mod3 timestamp: " + formatted_date_time)

    mod3ParseStartTime = time.time()
    parsedMod3 = ParsedMHWMod3()
    parsedMod3.ParseMHWMod3(Mod3, options)
    print("Parsed mod3.")
    mod3ParseEndTime = time.time()
    mod3ParseTime = mod3ParseEndTime - mod3ParseStartTime
    print(f"Mod3 parsing took {timeFormat % (mod3ParseTime * 1000)} ms.")

    armatureObj = None
    parentCollection = None  # Collection for grouping mod3 and mrl3

    if options["createCollections"]:
        if options["loadMrl3Data"]:
            parentCollection = getCollection(mod3FileName.split(".mod3")[0], makeNew=True)
        mod3Collection = getCollection(mod3FileName, parentCollection, makeNew=True)
        mod3Collection.color_tag = "COLOR_01"
        mod3Collection["~TYPE"] = "MHW_MOD3_COLLECTION"

        bpy.context.scene.mhw_mrl3_toolpanel.mod3Collection = mod3Collection

        mod3Collection["Mod3_Header_Unkn1"] = parsedMod3.header.unkn1
        mod3Collection["Mod3_Header_Unkn2"] = parsedMod3.header.unkn2
        mod3Collection["Mod3_Header_Unkn3"] = parsedMod3.header.unkn3
        mod3Collection["Mod3_Header_Unkn4"] = parsedMod3.header.unkn4
        mod3Collection["Mod3_Header_Unkn5"] = parsedMod3.header.unkn5


        # for i in range(len(parsedMod3.meshGroupList)):
        #     meshGroup = parsedMod3.meshGroupList[i]
        #     # mod3Collection["meshgroup_" + str(meshGroup.groupID)] = [meshGroup.sphere.x, meshGroup.sphere.y, meshGroup.sphere.z, meshGroup.sphere.r]
        #     mod3Collection["meshgroup_" + str(meshGroup.groupID)] = meshGroup.sphere.sphere

        if parsedMod3.meshGroupList != []:
            # mod3Collection["Mod3_Group"] = parsedMod3.meshGroupList
            for group in parsedMod3.meshGroupList:
                # mod3Collection["Mod3_Group_" + str(group.groupID).zfill(3)] = [group.sphere.x, group.sphere.y,
                #                                                                group.sphere.z, group.sphere.r]
                mod3Collection["Mod3_Group_" + str(group.groupID).zfill(3)] = group.sphere


        # #将BoneBoundingBox写入自定义属性
        # for i in range(len(parsedMod3.BoneBoundingBoxList)):
        #     # boneboundingbox = parsedMod3.BoneBoundingBoxList[i]
        #     width = len(str(parsedMod3.bbCount))
        #     mod3Collection["boneboundingbox_" + str(i).zfill(width)] = parsedMod3.BoneBoundingBoxList[i].bbProperty

        # bpy.context.scene.mhw_mdf_toolpanel.meshCollection = mod3Collection.name
    else:
        mod3Collection = bpy.context.scene.collection

    hiddenCollectionSet = set()

    if parsedMod3.skeleton != None:
        armatureObj = importSkeleton(parsedMod3.skeleton.boneInfoList, mod3FileName.split(".mod3")[0] + " Armature", mod3Collection, options["ArmatureDisplayType"], options["BonesDisplaySize"])

    # Create dictionary of material names mapping to material data to avoid assigning the wrong material in case of name duplication
    materialDict = createMaterialDict(parsedMod3.materialNameList)

    if not options["importArmatureOnly"]:
        importLODGroup(parsedMod3, mod3Collection, materialDict, armatureObj, hiddenCollectionSet, options["importAllLODs"], options["createCollections"])



    # Hide other lods in viewport
    collections = bpy.context.view_layer.layer_collection.children
    for collection in collections:
        if collection.name == mod3Collection.name:
            for childCollection in collection.children:
                if childCollection.name in hiddenCollectionSet:
                    childCollection.hide_viewport = True
            break

    '''导入材质，待做'''
    if options["loadMaterials"] or options["loadMrl3Data"]:
        loadMrl3(options, filePath, materialDict, parentCollection, warningList)

    if options["createCollections"]:
        bpy.context.scene["MHWMod3LastImportedCollection"] = mod3Collection.name

    '''因为旧mod3插件仅将boneboundingbox作为自定义属性导入导出，所以boneboundingbox序号不一定与meshInfo的boneboundingbox数量匹配，考虑最终关闭importBoundingBoxes选项，仅作为debug用'''
    if options["importBoundingBoxes"]:
        if options["createCollections"]:
            boundingBoxCollection = getCollection(f"{mod3FileName} Bounding Boxes", mod3Collection, makeNew=True)
            boundingBoxCollection["~TYPE"] = "MHW_MOD3_BOUNDING_BOX_COLLECTION"
        else:
            boundingBoxCollection = mod3Collection

        #总的BoundingBox
        # importBoundingBoxes(parsedMod3.header.sphere, parsedMod3.header.bbox, boundingBoxCollection, armatureObj, parsedMod3.skeleton)

        # importBoundingBoxes(parsedMod3.boundingBox, parsedMod3.boundingSphere, boundingBoxCollection, armatureObj, parsedMod3.skeleton)

        # BoneBoundingBox的BoundingBox
        for index, BoneBoundingBox in enumerate(parsedMod3.BoneBoundingBoxList):
            # bonefunctionID = parsedMod3.skeleton.boneRemapDict[BoneBoundingBox.boneIndex]
            sphere = BoneBoundingBox.sphere
            if armatureObj != None:
                target_bone_name = "MhBone_" + str(parsedMod3.skeleton.boneRemapDict[BoneBoundingBox.boneIndex]).zfill(3)
                # sphereObj = importBoundingSphere(sphere, str(index) + "_BoundingSphere" + "_" + target_bone_name, boundingBoxCollection, armatureObj, target_bone_name)

                # aabbObj = importAxisAlignedBoundingBox(BoneBoundingBox.aabb, str(index) + "_BoundingBox" + "_" + target_bone_name, boundingBoxCollection, armatureObj, target_bone_name)

                obbObj = importOrientedBoundingBox(BoneBoundingBox.obb_matrix, BoneBoundingBox.obb_halfsize, str(index) + "_OBB" + "_" + target_bone_name, boundingBoxCollection, armatureObj, target_bone_name)
            else:
                sphereObj = importBoundingSphere(sphere, str(index) + "_BoundingSphere",
                                                 boundingBoxCollection)
                aabbObj = importAxisAlignedBoundingBox(BoneBoundingBox.aabb, str(index) + "_BoundingBox", boundingBoxCollection)
                obbObj = importOrientedBoundingBox(BoneBoundingBox.obb_matrix, BoneBoundingBox.obb_halfsize,
                                                   str(index) + "_OBB", boundingBoxCollection)


    mod3ImportEndTime = time.time()
    mod3ImportTime = mod3ImportEndTime - mod3ImportStartTime
    print(f"Mod3 imported in {timeFormat % (mod3ImportTime * 1000)} ms.")
    print(f"Valid Mesh Count: {parsedMod3.validMeshCount} / {parsedMod3.header.meshCount}")
    print("\033[92m__________________________________\nMHW Mod3 import finished.\033[0m")
    return (warningList, errorList)


def checkObjForUVDoubling(obj):
    hasUVDoubling = False
    UVPoints = dict()
    if len(obj.data.uv_layers) > 0:
        for loop in obj.data.loops:
            currentVertIndex = loop.vertex_index
            # Vertex UV
            uv = obj.data.uv_layers[0].data[loop.index].uv

            if currentVertIndex in UVPoints and UVPoints[currentVertIndex] != uv:
                hasUVDoubling = True
                break
            # raise Exception
            else:
                UVPoints[currentVertIndex] = uv
    return hasUVDoubling

def cloneMesh(mesh):
    new_obj = mesh.copy()
    new_obj.data = mesh.data.copy()
    bpy.context.scene.collection.objects.link(new_obj)
    return new_obj

def bad_iter(blenderCrap):
    #This might look stupid but it's actually necessary, blender will throw errors if you loop directly over the uv layers
    i = 0
    while (True):
        try:
            yield(blenderCrap[i])
            i+=1
        except:
            return
def selectRepeated(bm):
    bm.verts.index_update()
    bm.verts.ensure_lookup_table()
    targetVert = set()
    for uv_layer in bad_iter(bm.loops.layers.uv):
        uvMap = {}
        for face in bm.faces:
            for loop in face.loops:
                uvPoint = tuple(loop[uv_layer].uv)
                if loop.vert.index in uvMap and uvMap[loop.vert.index] != uvPoint:
                    targetVert.add(bm.verts[loop.vert.index])
                else:
                    uvMap[loop.vert.index] = uvPoint
    return targetVert
def solveRepeatedVertex(op, mesh):
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(mesh.data)
    oldmode = bm.select_mode
    bm.select_mode = {'VERT'}
    targets = selectRepeated(bm)
    for target in targets:
        bmesh.utils.vert_separate(target, target.link_edges)
        bm.verts.ensure_lookup_table()
    bpy.ops.mesh.select_all(action='DESELECT')
    bm.select_mode = oldmode
    bm.verts.ensure_lookup_table()
    bm.verts.index_update()
    bmesh.update_edit_mesh(mesh.data)
    mesh.data.update()
    return


def transferNormals(clone, mesh):
    m = mesh.modifiers.new("Normals Transfer", "DATA_TRANSFER")
    m.use_loop_data = True
    m.loop_mapping = "TOPOLOGY"  # "POLYINTERP_NEAREST"#
    m.data_types_loops = {'CUSTOM_NORMAL'}
    m.object = clone
    bpy.ops.object.modifier_move_to_index(modifier=m.name, index=0)
    bpy.ops.object.modifier_apply(modifier=m.name)


def deleteClone(clone):
    objs = bpy.data.objects
    objs.remove(objs[clone.name], do_unlink=True)

def solveRepeatedUVs(obj):
    context = bpy.context
    context.view_layer.objects.active = obj
    if bpy.app.version < (4, 0, 0):
        if obj.data.use_auto_smooth == False:
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = .785  # 45 degrees, try to preserve normals if auto smooth was disabled
    obj.data.polygons.foreach_set("use_smooth", [True] * len(obj.data.polygons))
    clone = cloneMesh(obj)
    bpy.ops.object.mode_set(mode='EDIT')
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    # old seams
    old_seams = [e for e in bm.edges if e.seam]
    # unmark
    for e in old_seams:
        e.seam = False
    # mark seams from uv islands
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.seams_from_islands()
    seams = [e for e in bm.edges if e.seam]
    bmesh.ops.split_edges(bm, edges=seams)
    for e in old_seams:
        e.seam = True
    bmesh.update_edit_mesh(me)
    solveRepeatedVertex(None, obj)
    bpy.ops.object.mode_set(mode='OBJECT')
    transferNormals(clone, obj)
    if bpy.app.version < (4, 0, 0):
        obj.data.calc_normals_split()
    deleteClone(clone)

    print(f"Solved Repeated UVs on {obj.name}")


def splitSharpEdges(obj):
    context = bpy.context
    isHidden = obj.hide_viewport
    if isHidden:
        obj.hide_viewport = False
    context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    # old seams
    sharp = [e for e in bm.edges if not e.smooth]
    if sharp != []:
        print(f"Split Sharp Edges on {obj.name}")
    bmesh.ops.split_edges(bm, edges=sharp)
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.hide_viewport = isHidden





def exportMHWMod3File(filePath, options):
    # TODO Warning Conditions
    # Invalid mesh naming scheme - notify when using blender material name and setting viscon id to 0
    # Vertex groups weighted to bones that aren't on the armature
    # If an mrl3 for the mod3 imported, check if the mod3 materials are mismatched with mrl3

    # Error Conditions
    # No meshes in collection or selection x
    # More than one armature in collection x
    # No material on submesh x
    # Loose vertices on submesh x
    # No uv on submesh x
    # Max weighted bones exceeded x
    # Max weights per vertex exceeded x
    # Multiple uvs assigned to single vertex x
    # No vertices on submesh x
    # No faces on submesh x
    # Non triangulated face x
    # Max vertices exceeded x
    # Max faces exceeded x
    # No bones on armature x

    # TODO Error Conditions
    # More than one material on submesh


    errorDict = dict()
    # TODO Fix having all bones as weighted bones breaks export
    mod3ExportStartTime = time.time()
    vertexCount = 0
    faceCount = 0
    fileName = os.path.split(filePath)[1].split(".mod3")[0]

    print("\033[96m__________________________________\nMHW Mod3 export started.\033[0m")

    if bpy.context and bpy.context.active_object != None:
        bpy.ops.object.mode_set(mode='OBJECT')

    previousSelection = bpy.context.selected_objects
    maxWeightsPerVertex = 8
    maxBones = 255
    maxMeshs = 65535
    MAX_VERTICES_PER = 65535
    MAX_FACES_PER = 4294967295 # 乘3算
    MAX_VERTICES_TOTAL = 4294967295
    MAX_FACES_TOTAL = 4294967295 # 乘3算

    subMeshCount = 0
    targetCollection = options["targetCollection"]
    if targetCollection == None:
        addErrorToDict(errorDict, "NoTargetMod3Collection", None)
        printErrorDict(errorDict)
        showMHWMod3ErrorWindow(errorDict)
        return False
    else:
        print(f"Target collection: {targetCollection.name}")
        bpy.context.scene["MHWMod3LastExportedCollection"] = targetCollection.name

    lodColDict = {}
    addedMaterialsSet = set()
    dg = bpy.context.evaluated_depsgraph_get()

    Mod3File = MHWMod3()

    newMod3DataList = []
    vertexGroupsSet = set()
    weightedBonesSet = set()

    cloneMeshNameDict = {}
    deleteCopiedMeshList = []
    boundingBoxCollection = None
    importedBoneBoundingBoxes = {}

    # 先按照子集合名称排序整个子集合列表，以保证LOD集合按从小到大的数字排列
    childColList = sorted(targetCollection.children, key=lambda col: col.name)
    maxLOD = 0
    pattern = re.compile(r'^LOD (ALL|\d+) -')  # 匹配 "LOD ALL -" 或 "LOD 数字 -"
    for childCol in childColList:
        match = pattern.match(childCol.name)
        if match:
            if match.group(1) == "ALL":
                lodColDict = {"ALL": (65535, childCol), **lodColDict}
            else:
                maxLOD = int(match.group(1))
                lodColDict[str(maxLOD)] = (2 ** maxLOD, childCol)
        elif childCol.get("~TYPE") == "MHW_MOD3_BOUNDING_BOX_COLLECTION":
            boundingBoxCollection = childCol

    if str(maxLOD) in lodColDict:
        lodColDict[str(maxLOD)] = (65536 - 2 ** maxLOD, lodColDict[str(maxLOD)][1])
    # print(lodColDict)

    # Find armature and parse it
    armatureObj = None
    for obj in targetCollection.objects:
        if obj.type == "ARMATURE":
            if armatureObj == None:
                armatureObj = obj
            else:
                addErrorToDict(errorDict, "MoreThanOneArmature", None)

    exportArmatureData = None
    boneIndexDict = {}

    if armatureObj != None:
        print(f"Armature: {armatureObj.name}")
        armatureBoneDict = armatureObj.data.bones
        Mod3File.skeleton = Skeleton()
        exportArmatureData = armatureObj.data.copy()

        Mod3File.skeleton.boneCount = len(exportArmatureData.bones)

        transform = scaleExportMatrix @ rotateNeg90Matrix @ armatureObj.matrix_world
        exportArmatureData.transform(transform)

        # boneIndexDict = {}
        bonePosDict = {}
        for index, bone in enumerate(exportArmatureData.bones):
            boneIndexDict[bone.name] = index
            bonePosDict[tuple(bone.head_local)] = index # 用于处理镜像骨骼

        for index, bone in enumerate(exportArmatureData.bones): # 考虑如果骨骼数量超过256，则添加报错
            boneInfo = BoneInfo()
            boneInfo.boneFunction = int(bone.name.split("MhBone_")[1]) # 考虑如果boneFunction大于等于512，则添加报错
            # boneInfo.boneName = bone.name # 考虑如果骨骼名称不符合格式（MhBone_xxx），则添加到errorList中
            # boneInfo.boneIndex = boneIndexDict[bone.name]
            boneInfo.boneUnkn = bone.get("mod3_unknfloat", 0.0)

            '''TO DO 重新处理镜像骨骼'''
            symmetryBonePos = (-bone.head_local[0], bone.head_local[1], bone.head_local[2])
            boneInfo.boneSymmetric = bonePosDict.get(symmetryBonePos, 255) # 考虑处理多个骨骼同一坐标位置的情况
            # print(parsedBone.symmetryBoneIndex)

            if bone.parent != None:
                boneInfo.boneParent = boneIndexDict[bone.parent.name]
                localMatrix = (bone.matrix_local.to_4x4().transposed()) @ (
                    bone.parent.matrix_local.to_4x4().transposed().inverted())
            else:
                boneInfo.boneParent = 255
                localMatrix = bone.matrix_local.transposed()

            worldMatrix = bone.matrix_local.to_4x4().transposed().inverted()

            boneVector = np.array(localMatrix[3][:3])  # 取最后一列的前3个元素
            boneInfo.boneLength = np.linalg.norm(boneVector)  # 直接计算模长
            boneInfo.bonePos.x, boneInfo.bonePos.y, boneInfo.bonePos.z = boneVector

            Mod3File.skeleton.boneInfoList.append(boneInfo)
            Mod3File.skeleton.localMatList.append([list(row) for row in localMatrix])
            Mod3File.skeleton.worldMatList.append([list(row) for row in worldMatrix])
            Mod3File.skeleton.boneRemapDict[index] = boneInfo.boneFunction
    else:
        print(f"Armature: None")
        armatureBoneDict = dict()

    # Get previously imported bounding boxes if option enabled
    if boundingBoxCollection != None and options["exportBoundingBoxes"]:
        pass # TODO


    if lodColDict == {}:
        lodColDict = {"ALL": (65535, targetCollection)}
    else:
        if not options["exportAllLODs"]:
            lodColDict = {"ALL": lodColDict.get("ALL"), "0": lodColDict.get("0")}
            maxLOD = 0
    # print(lodColDict)
    Mod3File.fileHeader.lodCount = maxLOD

    mod3DataStartTime = time.time()
    isFirstLOD = True
    # remapDict = dict()
    # weightedBones = list()
    # boneVertDict = dict()
    groupIDList = set()
    vertArrayList = []

    for lodIndex, lodTuple in lodColDict.items():
        if lodTuple == None:
            continue
        lodVal, lodCol = lodTuple
        # print(f"LOD {lodIndex} collection: {lodCol.name}")

        # Get all meshes inside the collection
        doubledUVList = []
        sharpEdgeSplitList = []
        Mod3File.meshDict[lodIndex] = []

        for obj in lodCol.objects:
            if options["selectedOnly"]:
                selected = obj in bpy.context.selected_objects
            else:
                selected = True

            if obj.type != "MESH" or obj.get("MeshExportExclude") or not selected:
                continue

            subMeshCount += 1
            cloneObj = obj.copy() # 克隆一份网格对象，用于处理重叠UV和分离锐边，同时不影响原网格对象
            cloneObj.name = "CLN_" + obj.name
            cloneObj.data = bpy.data.meshes.new_from_object(obj.evaluated_get(dg)) # 获取评估后的网格对象（相当于应用了所有修改器）
            clonedMeshCollection = getCollection("clonedMeshes")
            clonedMeshCollection.objects.link(cloneObj)
            # clonedMeshCollection = getCollection(lodCol.name)
            # lodCol.objects.link(cloneObj) # 将克隆网格对象链接到当前LOD集合中

            print(f"Created temporary clone of {obj.name}: {cloneObj.name}")
            cloneMeshNameDict[obj.name] = cloneObj.name # 创建原网格对象名称与克隆网格对象名称的字典
            deleteCopiedMeshList.append(cloneObj)

            '''获取groupID'''
            if "Group_" in obj.name:
                try:
                    groupID = int(obj.name.split("Group_")[1].split("_")[0])
                except:
                    print("Could not parse group ID in {obj.name}, setting to 0")
                    groupID = 0
            else:
                print("Could not parse group ID in {obj.name}, setting to 0")
                groupID = 0
            groupIDList.add(groupID) # 添加groupID到列表中（此处是集合，可以直接去重）

            # armatureBoneDict = armatureObj.data.bones if armatureObj else dict()

            hasWeights = False
            boneVertDict = dict()

            # 创建克隆网格对象的所有已使用的顶点组索引集合（即权重不为零的顶点组）
            used_vg_indices = {g.group for v in cloneObj.data.vertices for g in v.groups}
            for vg in obj.vertex_groups: # 遍历原网格对象的顶点组
                # 如果当前顶点组索引在索引集合中（即该顶点组有权重），且顶点组名称在骨骼字典中（即顶点组有对应的骨骼）
                if vg.index in used_vg_indices and vg.name in armatureBoneDict:
                    # weightedBonesSet.add(vg.name)
                    # weightedBones.append(vg.name)
                    if vg.name not in boneVertDict:
                        boneVertDict[vg.name] = []
                    hasWeights = True
                # else:
                #     remapDict[vg.name] = 0

            if armatureObj != None and not hasWeights:
                addErrorToDict(errorDict, "NoWeightsOnMesh", obj.name)
            # if armatureObj == None and len(remapDict) != 0:
            #     addErrorToDict(errorDict, "NoArmatureInCollection", obj.name)

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
            vertexGroupCount = len(obj.vertex_groups)  # For checking out of bound weight indices
            if any(len(face.vertices) != 3 for face in evaluatedData.polygons):
                # Triagulate only if there's non triangle faces
                print(f"Triangulated {obj.name}")
                triangulateMesh(evaluatedData)
            if len(evaluatedData.vertices) == 0:
                addErrorToDict(errorDict, "NoVerticesOnSubMesh", obj.name)
            if len((evaluatedData.polygons)) == 0:
                addErrorToDict(errorDict, "NoFacesOnSubMesh", obj.name)

            meshEntry = Mesh()
            meshInfo = meshEntry.meshInfo
            meshInfo.lod = lodVal
            meshInfo.groupID = groupID

            '''获取材质名'''
            materialName = "NO_ASSIGNED_MATERIAL"
            if options["useBlenderMaterialName"]:  # Material name from object material
                if evaluatedData.materials and len(evaluatedData.materials) > 0:
                    materialName = evaluatedData.materials[0].name.split(".")[0]
                else:
                    try:  # Get material from mesh name if it isn't found
                        materialName = obj.name.split("__", 1)[1].split(".")[0]
                    except:
                        addErrorToDict(errorDict, "NoMaterialOnSubMesh", obj.name)
            else:  # Material name from object name
                try:
                    materialName = obj.name.split("__", 1)[1].split(".")[0]
                except:  # Fall back to blender material name if object material name is missing
                    print(f"Couldn't split material name on {obj.name}, using blender material name instead")
                    if evaluatedData.materials and len(evaluatedData.materials) > 0:
                        materialName = evaluatedData.materials[0].name.split(".")[0]
                    else:
                        addErrorToDict(errorDict, "NoMaterialOnSubMesh", obj.name)
            if materialName not in addedMaterialsSet:
                addedMaterialsSet.add(materialName)
                Mod3File.materialNameList.append(materialName)
                meshInfo.materialID = len(Mod3File.materialNameList) - 1
            else:
                meshInfo.materialID = Mod3File.materialNameList.index(materialName)

            transform = scaleExportMatrix @ rotateNeg90Matrix @ obj.matrix_world
            evaluatedData.transform(transform)

            if bpy.app.version < (4, 0, 0):
                evaluatedData.use_auto_smooth = True
                evaluatedData.calc_normals_split()
            try:
                evaluatedData.calc_tangents()
            except:
                pass

            if len(evaluatedData.vertices) > MAX_VERTICES_PER:
                addErrorToDict(errorDict, "MaxVerticesExceeded", obj.name)
            meshInfo.vertexCount = len(evaluatedData.vertices)
            meshInfo.faceCount = len(evaluatedData.polygons) * 3
            vertexCount += len(evaluatedData.vertices)
            faceCount += len(evaluatedData.polygons)
            # vertexGroupIndexToRemapDict = {vgroup.index: boneIndexDict[vgroup.name]
            #                                for vgroup in obj.vertex_groups if vgroup.name in boneIndexDict}
            vertexGroupIndexToRemapDict = {vgroup.index: vgroup.name
                                           for vgroup in obj.vertex_groups if vgroup.name in boneIndexDict}


            vertexPosList, vertexNorList, vertexTanList,\
                vertexWeightList, vertexIndicesList, vertexColorList = (list() for _ in range(6))
            meshInfo.blockName = "PosNorTan"

            # Get Faces
            meshHasUV = [False] * 4
            meshHasColor = False
            meshEntry.faceList = [tuple(f.vertices) for f in evaluatedData.polygons]
            if 3 * len(meshEntry.faceList) > MAX_FACES_PER:
                addErrorToDict(errorDict, "MaxFacesExceeded", obj.name)
            if any([len(face) != 3 for face in meshEntry.faceList]):
                addErrorToDict(errorDict, "NonTriangulatedFace", obj.name)
            if len(evaluatedData.uv_layers) > 0:
                meshHasUV[0] = True
                meshEntry.vertexDict["UV"] = np.zeros((len(evaluatedData.vertices), 2))
                meshInfo.blockName += "UV"
            else:
                addErrorToDict(errorDict, "NoUVMapOnSubMesh", obj.name)
            if len(evaluatedData.uv_layers) > 1:
                meshHasUV[1] = True
                meshEntry.vertexDict["UV2"] = np.zeros((len(evaluatedData.vertices), 2))
                meshInfo.blockName += "UV2"
            # else:
            #     meshEntry.vertexDict["UV2"] = None
            if len(evaluatedData.vertex_colors) > 0:
                meshHasColor = True
                meshEntry.vertexDict["Color"] = np.zeros((len(evaluatedData.vertices), 4))
                if armatureObj == None:
                    if len(evaluatedData.uv_layers) > 2:
                        meshHasUV[2] = True
                        meshEntry.vertexDict["UV3"] = np.zeros((len(evaluatedData.vertices), 2))
                        meshInfo.blockName += "UV3"
                    if len(evaluatedData.uv_layers) > 3:
                        meshHasUV[3] = True
                        meshEntry.vertexDict["UV4"] = np.zeros((len(evaluatedData.vertices), 2))
                        meshInfo.blockName += "UV4"
                meshInfo.blockName += "Color"
            # else:
            #     meshEntry.vertexDict["Color"] = None

            sortedLoops = sorted(evaluatedData.loops, key=lambda loop: loop.vertex_index)
            previousIndex = -1

            # These are used to check if there's multiple uvs per vertex
            # If the current vert is already in the set, throw an error
            UVPoints, UV2Points, UV3Points, UV4Points = (dict() for _ in range(4))
            for loop in sortedLoops:
                currentVertIndex = loop.vertex_index
                # Vertex UV
                if meshHasUV[0]:
                    uv = evaluatedData.uv_layers[0].data[loop.index].uv
                    meshEntry.vertexDict["UV"][currentVertIndex] = uv

                    if currentVertIndex in UVPoints and UVPoints[currentVertIndex] != uv:
                        addErrorToDict(errorDict, "MultipleUVsAssignedToVertex", obj.name)
                    else:
                        UVPoints[currentVertIndex] = uv

                if meshHasUV[1]:
                    uv2 = evaluatedData.uv_layers[1].data[loop.index].uv
                    meshEntry.vertexDict["UV2"][currentVertIndex] = uv2

                    if currentVertIndex in UV2Points and UV2Points[currentVertIndex] != uv2:
                        addErrorToDict(errorDict, "MultipleUVsAssignedToVertex", obj.name)
                    else:
                        UV2Points[currentVertIndex] = uv2

                if meshHasUV[2]:
                    uv3 = evaluatedData.uv_layers[2].data[loop.index].uv
                    meshEntry.vertexDict["UV3"][currentVertIndex] = uv3

                    if currentVertIndex in UV3Points and UV3Points[currentVertIndex] != uv3:
                        addErrorToDict(errorDict, "MultipleUVsAssignedToVertex", obj.name)
                    else:
                        UV3Points[currentVertIndex] = uv3

                if meshHasUV[3]:
                    uv4 = evaluatedData.uv_layers[3].data[loop.index].uv
                    meshEntry.vertexDict["UV4"][currentVertIndex] = uv4

                    if currentVertIndex in UV4Points and UV4Points[currentVertIndex] != uv4:
                        addErrorToDict(errorDict, "MultipleUVsAssignedToVertex", obj.name)
                    else:
                        UV4Points[currentVertIndex] = uv4

                if currentVertIndex == previousIndex:  # Skip looping over vertices that have already been read
                    continue
                previousIndex = currentVertIndex

                # Vertex Pos
                vertex = evaluatedData.vertices[currentVertIndex]
                # meshEntry.vertexDict["Position"][currentVertIndex] = vertex.co
                vertexPosList.append(vertex.co)

                # Vertex Normal & Tangent
                loopTangent = loop.tangent * 1.001 * 127
                tx = int(floor(loopTangent[0])) & 0xFF
                ty = int(floor(loopTangent[1])) & 0xFF
                tz = int(floor(loopTangent[2])) & 0xFF
                sign = int(floor(loop.bitangent_sign * 127.0)) & 0xFF
                # meshEntry.vertexDict["NorTan"][0][currentVertIndex] = loop.normal
                # meshEntry.vertexDict["NorTan"][1][currentVertIndex] = (tx, ty, tz, sign)

                vertexNorList.append(loop.normal)
                vertexTanList.append((tx, ty, tz, sign))

                # Vertex Color
                if meshHasColor:
                    # meshEntry.vertexDict["Color"][currentVertIndex] = \
                    #     evaluatedData.vertex_colors[0].data[loop.index].color
                    vertexColorList.append(evaluatedData.vertex_colors[0].data[loop.index].color)

                # Bone Weights
                # MIN_WEIGHT = 0.002
                MIN_WEIGHT = 0.001 # If the weight is any lower than this, the engine freaks out and puts the vert at the origin
                boneWeightList = []
                boneIndicesList = []

                if armatureObj != None:
                    for g in vertex.groups:
                        if g.weight >= MIN_WEIGHT and g.group < vertexGroupCount and g.group in vertexGroupIndexToRemapDict:
                            # print(boneIndexDict[vertexGroupIndexToRemapDict[g.group]])
                            boneWeightList.append(g.weight)
                            # weightIndicesList.append(vertexGroupIndexToRemapDict[g.group])
                            boneIndicesList.append(boneIndexDict[vertexGroupIndexToRemapDict[g.group]])

                            # Gather vertex positions of bone weights to generate bone bounding box
                            # boneVertDict[parsedMesh.skeleton.weightedBones[weightIndicesList[-1]]].append(vertex.co)
                            boneVertDict[vertexGroupIndexToRemapDict[g.group]].append(vertex.co)

                    if len(boneWeightList) > maxWeightsPerVertex:
                        addErrorToDict(errorDict, "MaxWeightsPerVertexExceeded", obj.name)
                    vertexWeightList.append(list(pad(boneWeightList, size=8, padding=0.0)))
                    vertexIndicesList.append(list(pad(boneIndicesList, size=8, padding=0)))

            meshEntry.vertexDict["Position"] = np.array(vertexPosList)
            vertArrayList.extend(meshEntry.vertexDict["Position"])
            meshEntry.vertexDict["NorTan"] = [np.array(vertexNorList), np.array(vertexTanList)]
            if vertexColorList:
                meshEntry.vertexDict["Color"] = np.array(vertexColorList)

            maxLength = 0
            if vertexWeightList:
                vertexWeightArray = np.array(vertexWeightList)
                vertexIndicesArray = np.array(vertexIndicesList)
                weightString = "Weight8Bone8"
                maxLength = np.max(np.sum(vertexWeightArray != 0.0, axis=1)) # 计算每行权重中非零权重的最大长度
                if maxLength <= 4:
                    vertexWeightArray = vertexWeightArray[:, :4]
                    vertexIndicesArray = vertexIndicesArray[:, :4]
                    weightString = "Weight4Bone4"

                meshEntry.vertexDict["Weight"] = vertexWeightArray
                meshEntry.vertexDict["Bone"] = vertexIndicesArray
                meshInfo.blockName += weightString
            # print(meshEntry.vertexDict)

            meshInfo.weightDynamics = 8 * maxLength + 1 # 之后再研究weightDynamics为5的情况
            # print("weightDynamics:", meshInfo.weightDynamics)
            meshInfo.shadowFlag = obj.data.get("Mod3_Mesh_ShadowFlag", 19)
            meshInfo.renderMode = obj.data.get("Mod3_Mesh_RenderMode", 195)
            meshInfo.unkn3 = obj.data.get("Mod3_Mesh_Unkn", [0, 0, 0, 48])
            meshInfo.meshIndex = obj.data.get("Mod3_Mesh_Index", 1)

            Mod3File.meshDict[lodIndex].append(meshEntry)

            if any([vertIndex not in UVPoints for vertIndex in range(len(evaluatedData.vertices))]):
                addErrorToDict(errorDict, "LooseVerticesOnSubMesh", obj.name)

            # 计算sphere, bbox
            '''待做无骨骼绑定情况下的计算'''
            bboxCount = len(boneVertDict)
            if armatureObj != None:
                for boneName, vecList in boneVertDict.items():
                    if vecList == []:
                        bboxCount -= 1
                        continue

                    # bonePos = exportArmatureData.bones[boneName].head_local
                    # vecArray = np.array(vecList) - bonePos # 减掉骨骼的位置偏移
                    # minVec = np.min(vecArray, axis=0)
                    # maxVec = np.max(vecArray, axis=0)

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
                    # 计算AABB
                    minVec = np.min(vecArray_local, axis=0)
                    maxVec = np.max(vecArray_local, axis=0)

                    bboxEntry = BoneBoundingBox()
                    bboxEntry.boneIndex = boneIndexDict[boneName]

                    bboxEntry.aabb.min.x = minVec[0]
                    bboxEntry.aabb.min.y = minVec[1]
                    bboxEntry.aabb.min.z = minVec[2]
                    bboxEntry.aabb.max.x = maxVec[0]
                    bboxEntry.aabb.max.y = maxVec[1]
                    bboxEntry.aabb.max.z = maxVec[2]

                    # 包围球的球心固定在包围盒的中心点
                    center = (maxVec + minVec) / 2
                    radius = caculateBoundingSphere(vecArray_local, center)
                    bboxEntry.sphere.x = center[0]
                    bboxEntry.sphere.y = center[1]
                    bboxEntry.sphere.z = center[2]
                    bboxEntry.sphere.r = radius

                    if len(vecList) >= 2:
                        obbMat, halfSize = caculateOBB(vecArray_local)
                    else:
                        obbMat = np.eye(4)
                        obbMat[:3, 3] = center
                        obbMat = obbMat.T
                        halfSize = [0, 0, 0]
                    bboxEntry.obb_halfsize.x = halfSize[0]
                    bboxEntry.obb_halfsize.y = halfSize[1]
                    bboxEntry.obb_halfsize.z = halfSize[2]

                    bboxEntry.obb_matrix.matrix = [list(row) for row in obbMat]

                    Mod3File.BoneBoundingBoxList.append(bboxEntry)

                meshInfo.boundingBoxCount = bboxCount
    if vertexCount > MAX_VERTICES_TOTAL:
        print()
    if faceCount * 3 > MAX_FACES_TOTAL:
        print()

    if vertArrayList != []:
        # print(vertArrayList)
        fullVertArray = np.vstack(vertArrayList)
        minVec = np.min(fullVertArray, axis=0)
        maxVec = np.max(fullVertArray, axis=0)

        Mod3File.fileHeader.bbox.min.x = minVec[0]
        Mod3File.fileHeader.bbox.min.y = minVec[1]
        Mod3File.fileHeader.bbox.min.z = minVec[2]
        Mod3File.fileHeader.bbox.max.x = maxVec[0]
        Mod3File.fileHeader.bbox.max.y = maxVec[1]
        Mod3File.fileHeader.bbox.max.z = maxVec[2]

        # 包围球的球心固定在包围盒的中心点
        center = (maxVec + minVec) / 2
        radius = caculateBoundingSphere(fullVertArray, center)
        Mod3File.fileHeader.sphere.x = center[0]
        Mod3File.fileHeader.sphere.y = center[1]
        Mod3File.fileHeader.sphere.z = center[2]
        Mod3File.fileHeader.sphere.r = radius

    if Mod3File.skeleton != None and Mod3File.skeleton.boneCount > maxBones:
        print(f"\nMaximum Bones Exceeded! {Mod3File.skeleton.boneCount} / {maxBones}")
        addErrorToDict(errorDict, "MaxWeightedBonesExceeded", None)

    mod3DataEndTime = time.time()
    mod3DataExportTime = mod3DataEndTime - mod3DataStartTime
    print(f"Gathering mod3 data took {timeFormat % (mod3DataExportTime * 1000)} ms.")


    # Clear references
    # newMeshDataList.clear()
    evaluatedData = None
    if exportArmatureData != None:
        bpy.data.armatures.remove(exportArmatureData)
    for mesh in deleteCopiedMeshList:
        bpy.data.objects.remove(mesh, do_unlink=True)
        # bpy.data.meshes.remove(mesh)
    if "clonedMeshes" in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections["clonedMeshes"])
    deleteCopiedMeshList.clear()
    cloneMeshNameDict.clear()

    if subMeshCount == 0:
        addErrorToDict(errorDict, "NoMeshesInCollection", None)

    if errorDict != {}:
        printErrorDict(errorDict)
        showMHWMod3ErrorWindow(errorDict, targetCollection.name, armatureObj.name)
        return False

    Mod3File.fileHeader.meshCount = subMeshCount
    Mod3File.fileHeader.vertexCount = vertexCount
    Mod3File.fileHeader.faceCount = faceCount * 3

    mod3WriteStartTime = time.time()

    Mod3File = buildMod3File(Mod3File, targetCollection)
    writeMHWMod3(Mod3File, filePath)

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
    if Mod3File.skeleton != None:
        print(f"Armature Bone Count: {Mod3File.skeleton.boneCount}")

    print(f"Materials ({len(Mod3File.materialNameList)}):")
    for materialName in Mod3File.materialNameList:
        print(materialName)


    print("\033[92m__________________________________\nMHW Mod3 export finished.\033[0m")
    return True