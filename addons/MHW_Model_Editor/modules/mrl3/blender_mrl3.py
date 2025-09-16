import copy
import os
import zlib

import bpy

from ..common.general_function import string_reformat
from .mrl3_panels import tag_redraw
from .file_mrl3 import MHWMrl3, Material, writeMHWMrl3
from .mrl3_dicts import get_master_material_dict, clear_master_material_dict_cache, get_property_dict
from ..common.blender_utils import showErrorMessageBox, showMessageBox
from ..common.general_function import raiseWarning, textColors, unsignedToSigned, splitNativesPath

# from .file_re_mdf import readMDF,writeMDF,MDFFile,Material,TextureBinding,Property,gameNameMDFVersionDict,getMDFVersionToGameName,MMTRSData,GPBFEntry
# from .ui_re_mdf_panels import tag_redraw

def createMrl3Collection(collectionName,parentCollection = None):
    collection = bpy.data.collections.new(collectionName)
    collection.color_tag = "COLOR_05"
    collection["~TYPE"] = "MHW_MRL3_COLLECTION"
    if parentCollection != None:
        parentCollection.children.link(collection)
    else:
        bpy.context.scene.collection.children.link(collection)
    bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection = collection
    return collection


def createEmpty(name, propertyList, parent=None, collection=None):
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_size = .10
    obj.empty_display_type = 'PLAIN_AXES'
    obj.parent = parent
    for property in propertyList:  # Reverse list so items get added in correct order
        obj[property[0]] = property[1]
    if collection == None:
        collection = bpy.context.scene.collection
    collection.objects.link(obj)
    return obj


def addMapToMapList(obj,resourceDict):
    if 2 not in resourceDict:
        return
    for resource in resourceDict[2]:
        # if resource.resourceType & 0xF != 2:
        #     continue
        newListItem = obj.mhw_mrl3_material.mapList_items.add()
        # newListItem.resourceType = resource.resourceType
        newListItem.mapType = string_reformat(resource.resourceName)
        newListItem.mapPath = resource.resourcePath
        # newListItem.resourceBytes = resource.unkn_bytes
        newListItem.resourceHash = str(resource.resourceHash)

def addSamplerToSamplerList(obj,resourceDict):
    if 1 not in resourceDict:
        return
    for resource in resourceDict[1]:
        # if resource.resourceType & 0xF != 1:
        #     continue
        newListItem = obj.mhw_mrl3_material.samplerList_items.add()
        newListItem.samplerType = string_reformat(resource.resourceName)
        newListItem.samplerIndex = resource.resourceValueIndex
        # newListItem.resourceBytes = resource.unkn_bytes
        newListItem.resourceHash = str(resource.resourceHash)

def sortPropBlock(resource):
    propBlockType = resource.resourceName
    if propBlockType not in {"CBMaterialCommon__disclosure", "CBSpeedTreeCollision__disclosure", "CBMhMaterialIvyFloorLocal__disclosure", "CBMhMaterialSlantFloorLocal__disclosure"}:
        return 0  # 第一位
    elif propBlockType in {"CBSpeedTreeCollision__disclosure", "CBMhMaterialIvyFloorLocal__disclosure", "CBMhMaterialSlantFloorLocal__disclosure"}:
        return 1  # 第二位
    else:  # CBMaterialCommon__disclosure
        return 2  # 第三位

def addPropsToPropList(obj,resourceDict):
    """将resource的属性添加到资源项的属性列表中"""
    if 0 not in resourceDict:
        return
    sortedResourceDict = sorted(resourceDict[0], key=sortPropBlock)
    for resource in sortedResourceDict:
        propertyBlock_item = obj.mhw_mrl3_material.propertyBlock_items.add()
        propertyBlock_item.propertyBlockType = resource.resourceName
        # propertyBlock_item.resourceBytes = resource.unkn_bytes
        # propertyBlock_item.blockOffset = resource.resourceValueIndex
        propertyBlock_item.resourceHash = str(resource.resourceHash)
        propertyBlock_item.propertyList_items.clear()  # 清空现有属性

        for key, key_value in resource.propertyDict.items():
            if key.startswith("align"): # 跳过对齐字段
                continue

            newListItem = propertyBlock_item.propertyList_items.add()
            newListItem.prop_name = string_reformat(key)

            prop_type = key_value[0]
            prop_value = key_value[1]

            if prop_type == "float":
                newListItem.data_type = "FLOAT"
                newListItem.float_value = prop_value
            elif prop_type == "int":
                newListItem.data_type = "INT"
                newListItem.int_value = prop_value
            elif prop_type == "uint":
                newListItem.data_type = "UINT"
                newListItem.uint_value = prop_value
            elif prop_type == "bbool":
                newListItem.data_type = "BOOL"
                newListItem.bool_value = bool(prop_value)
            elif prop_type == "float[2]":
                newListItem.data_type = "FLOAT[2]"
                newListItem.float2_value = prop_value
            elif prop_type == "float[3]":
                if not key.endswith("__uiColor"):
                    newListItem.data_type = "FLOAT[3]"
                    newListItem.float3_value = prop_value
                else:
                    newListItem.data_type = "COLOR"
                    newListItem.color_value = prop_value + [1.0]
            elif prop_type == "float[4]":
                if not key.endswith("__uiColor"):
                    newListItem.data_type = "FLOAT[4]"
                    newListItem.float4_value = prop_value
                else:
                    newListItem.data_type = "COLOR"
                    newListItem.color_value = prop_value



def importMHWMrl3File(mrl3File, filePath, materialDict={}, parentCollection=None):
    # materialHashDict = {zlib.crc32(key.encode()) ^ 0xffffffff: key for key in materialDict}

    # mrl3File = readMHWMrl3(filePath,  materialDict)
    mrl3FileName = os.path.split(filePath)[1]

    mrl3Collection = createMrl3Collection(mrl3FileName, parentCollection)


    # MATERIALS IMPORT
    for index, material in enumerate(mrl3File.materialList):
        name = "Mrl3 Material " + str(index).zfill(2) + " ("+material.materialName+")"
        materialObj = createEmpty(name, [("~TYPE", "MHW_MRL3_MATERIAL")], None, mrl3Collection)

        # resourceOrder = []
        # for key in material.resourceDict.keys():
        #     resourceOrder.append(key)
        # materialObj["~ORDER"] = resourceOrder

        # materialObj.mhw_mrl3_material.headID = str(material.headID)
        materialObj.mhw_mrl3_material.materialName = material.materialName
        materialObj.mhw_mrl3_material.shaderHash1 = str(material.shaderHash1)
        materialObj.mhw_mrl3_material.shaderHash2 = str(material.shaderHash2)
        materialObj.mhw_mrl3_material.mastermaterialType = material.mastermaterialType
        # materialObj.mhw_mrl3_material.materialBlockSize = material.materialBlockSize
        materialObj.mhw_mrl3_material.surfaceDirection = str(format(material.surfaceDirection, 'x'))
        # materialObj.mhw_mrl3_material.resourceCount = material.resourceCount
        materialObj.mhw_mrl3_material.alphaCoef = material.alpha_bytes

        # getMDFFlags(materialObj, material.flags)
        addMapToMapList(materialObj, material.resourceDict)
        addSamplerToSamplerList(materialObj, material.resourceDict)
        addPropsToPropList(materialObj, material.resourceDict)

    tag_redraw(bpy.context)
    print("Finished loading mrl3 data.")
    return True


def reindexMaterials(collectionName):
    if bpy.data.collections.get(collectionName, None) != None:
        mrl3Collection = bpy.data.collections[collectionName]
    else:
        mrl3Collection = bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection
    if mrl3Collection != None:

        currentIndex = 0
        for obj in sorted(mrl3Collection.all_objects, key=lambda item: item.name):

            if obj.get("~TYPE", None) == "MHW_MRL3_MATERIAL":
                # Change the material name in the mrl3 material settings to the one in the object name
                # This allows for the user to set the material name by either method of renaming the object or setting it in the mrl3 material settings
                if "Mrl3 Material" in obj.name and "(" in obj.name:
                    objMaterialName = obj.name.rsplit("(", 1)[1].split(")")[0]
                    if objMaterialName != obj.mhw_mrl3_material.materialName:
                        obj.mhw_mrl3_material.materialName = objMaterialName
                obj.name = "Mrl3 Material " + str(currentIndex).zfill(2) + " (" + obj.mhw_mrl3_material.materialName + ")"
                currentIndex += 1


def Mrl3ErrorCheck(collectionName):
    print("\nChecking for problems with mrl3 structure...")
    # 检查是否存在mrl3集合
    # 检查重复的材质名
    # 检查mod3网格对象的材质名是否存在于mrl3集合中

    errorList = []
    warningList = []
    materialNameSet = set()
    mod3MaterialSet = set()

    #如果名称为collectionName的mrl3集合存在，则将该集合下的所有对象存为列表，否则报错
    if bpy.data.collections.get(collectionName, None) != None:
        objList = bpy.data.collections[collectionName].all_objects
    else:
        errorList.append("Mrl3 objects must be grouped in a collection.")
        objList = []

    # headerCount = 0
    # if bpy.context.active_object != None and bpy.context.active_object.get("~TYPE", None) == "MHW_MRL3_HEADER":
    #     findHeader = False
    #     headerCount = 1
    # else:
    #     findHeader = True

    for obj in objList: #如果上一步成功获取到对象列表，则进行遍历
        if obj.get("~TYPE", None) == "MHW_MRL3_MATERIAL":
            #如果当前mrl3空物体的材质面板中的材质名不在materialNameSet中，则将该材质名添加进materialNameSet，否则报错，防止存在重复的材质名
            if obj.mhw_mrl3_material.materialName not in materialNameSet:
                materialNameSet.add(obj.mhw_mrl3_material.materialName)
            else:
                errorList.append("Duplicate material name on " + obj.name + ". Set the material name in the custom properties of the material object to a different name.")

    #获取mrl3集合对应的mod3集合
    mod3CollectionName = collectionName.replace(".mrl3", ".mod3", 1)
    mod3Collection = bpy.data.collections.get(mod3CollectionName, None)
    if mod3Collection != None:
        for obj in mod3Collection.all_objects:
            if obj.type == "MESH" and not "Mod3ExportExclude" in obj and "__" in obj.name: #有Mod3ExportExclude自定义属性的网格是boundingbox
                matName = obj.name.split("__", 1)[1].split(".")[0]
                mod3MaterialSet.add(matName)
                if matName not in materialNameSet:
                    warningList.append("The material (" + matName + ") on mesh " + obj.name + " does not exist in the mrl3.")
    else:
        raiseWarning(f"Could not find mod3 collection ({mod3CollectionName}) to check materials against.")

    '''世界的mrl3不需要这一步检查'''
    # if len(mod3MaterialSet) != 0 and len(materialNameSet.difference(mod3MaterialSet)) != 0:
    #     materialString = ""
    #     for materialName in materialNameSet.difference(mod3MaterialSet):
    #         materialString += materialName + "\n"
    #         warningList.append(f"The following materials exist in the mrl3 ({collectionName}) but do not exist in the mesh ({mod3CollectionName}):\n{materialString}")

    if warningList != []:
        # warningList.append("If this mod3 is supposed to be used with this mrl3, the number of materials and name of materials in the mrl3 must match the mesh.\nThe material will appear as a checkerboard texture in game.")
        warningList.append("The missing materials will appear as a checkerboard texture in game.")
        for warning in warningList:
            raiseWarning(warning)

    if errorList == []:
        print("No errors found.")
        if warningList != []:
            showMessageBox("Warnings occured during export. Check Window > Toggle System Console for details.", title="Export Warning", icon="ERROR")
        return True
    else:
        errorString = ""
        for error in errorList:
            errorString += textColors.FAIL + "ERROR: " + error + textColors.ENDC + "\n"
        showMessageBox("Mrl3 structure contains errors and cannot export. Check Window > Toggle System Console for details.", title="Export Error", icon="ERROR")
        print(errorString)
        print(textColors.FAIL + "__________________________________\nMHW Mrl3 export failed." + textColors.ENDC)
        return False


def getPropValue(propType, property):
    # if property.data_type == "FLOAT":
    #     value = property.float_value
    if property.data_type == "INT":
        value = property.int_value
    elif property.data_type == "UINT":
        value = property.uint_value
    elif property.data_type == "BOOL":
        # value = 1.0 if property.bool_value else 0.0
        value = property.bool_value
    elif property.data_type == "FLOAT[2]":
        value = [property.float2_value[0], property.float2_value[1]]
    elif property.data_type == "FLOAT[3]":
        value = [property.float3_value[0], property.float3_value[1], property.float3_value[2]]
    elif property.data_type == "FLOAT[4]":
        value = [property.float4_value[0], property.float4_value[1], property.float4_value[2], property.float4_value[3]]
    elif property.data_type == "COLOR":
        if propType == 'float[4]':
            value = [property.color_value[0], property.color_value[1], property.color_value[2], property.color_value[3]]
        else:
            value = [property.color_value[0], property.color_value[1], property.color_value[2]]
    else:
        value = property.float_value

    return value

def fixTexPath(path):#Fix potential path problems
    # path = path.replace(os.sep,"/").split(".tex")[0]
    path = path.replace( "/", os.sep).split(".tex")[0]
    if "nativepc" in path.lower():
        splitPath = splitNativesPath(path)
        if splitPath != None:
            path = splitPath[1]#Fix including the chunk root path in the tex path
    return path

def buildMrl3(mrl3CollectionName):
    mrl3Collection = bpy.data.collections.get(mrl3CollectionName)
    reindexMaterials(mrl3CollectionName)

    if mrl3Collection != None:
        valid = Mrl3ErrorCheck(mrl3CollectionName)
    else:
        showErrorMessageBox("Mrl3 collection is not set, cannot export")
        valid = False

    if valid:
        # #将mrl3空物体对象按名称排序
        # materialObjList = sorted([child for child in mrl3Collection.all_objects if child.get("~TYPE", None) == "MHW_MRL3_MATERIAL"], key=lambda item: item.name)
        materialObjList = [child for child in mrl3Collection.all_objects if child.get("~TYPE", None) == "MHW_MRL3_MATERIAL"]
        newMrl3File = MHWMrl3()

        textureDict = {} #用于存放所有贴图的字典
        textureIndex = 0 #贴图序号
        try:
            for materialObj in materialObjList:
                materialEntry = Material()
                mhw_mrl3_material = materialObj.mhw_mrl3_material
                master_material_dict = get_master_material_dict() #获取主材质字典
                property_dict = get_property_dict()

                crc = zlib.crc32(mhw_mrl3_material.materialName.encode())
                materialEntry.materialNameHash = crc ^ 0xffffffff

                # shaderHash1 = mhw_mrl3_material.shaderHash1
                mmtrDict = master_material_dict[mhw_mrl3_material.shaderHash1]

                materialEntry.shaderHash1 = int(mhw_mrl3_material.shaderHash1)
                materialEntry.shaderHash2 = mmtrDict["shaderHash2"]
                materialEntry.materialBlockSize = mmtrDict["matBlockSize"]
                materialEntry.resourceCount = mmtrDict["resourceCount"]
                surfaceDirection = int(mhw_mrl3_material.surfaceDirection, 16)
                materialEntry.surfaceDirection = unsignedToSigned(surfaceDirection)
                materialEntry.alpha_bytes = mhw_mrl3_material.alphaCoef
                materialEntry.resourceDict = copy.deepcopy(mmtrDict["resourceDict"])

                for resource in mhw_mrl3_material.mapList_items:
                    if resource.mapPath:
                        fixedPath = fixTexPath(resource.mapPath)

                        if fixedPath not in textureDict:
                            textureDict[fixedPath] = textureIndex
                            textureIndex += 1

                        resourceHash = int(resource.resourceHash) >> 12
                        if str(resourceHash) in materialEntry.resourceDict:
                            materialEntry.resourceDict[str(resourceHash)]["value"] = textureDict[fixedPath] + 1

                for resource in mhw_mrl3_material.propertyBlock_items:
                    resourceHash = int(resource.resourceHash) >> 12
                    if str(resourceHash) in materialEntry.resourceDict:
                        materialEntry.resourceDict[str(resourceHash)]["propDict"] = copy.deepcopy(property_dict[str(resourceHash)]["fields"])
                        propertyIndex = 0
                        # for property in resource.propertyList_items:
                        for propName, propType in list(materialEntry.resourceDict[str(resourceHash)]["propDict"].items()):
                            if propName.startswith("align"):  # 跳过对齐字段
                                continue
                            property = resource.propertyList_items[propertyIndex]
                            materialEntry.resourceDict[str(resourceHash)]["propDict"][propName] = [materialEntry.resourceDict[str(resourceHash)]["propDict"][propName]]
                            materialEntry.resourceDict[str(resourceHash)]["propDict"][propName].append(getPropValue(propType, property))
                            propertyIndex += 1
                    # print(materialEntry.resourceDict[str(resourceHash)]["propDict"])

                for resource in mhw_mrl3_material.samplerList_items:
                    resourceHash = int(resource.resourceHash) >> 12
                    if str(resourceHash) in materialEntry.resourceDict:
                        materialEntry.resourceDict[str(resourceHash)]["value"] = resource.samplerIndex

                newMrl3File.materialList.append(materialEntry)
        finally:
            clear_master_material_dict_cache() # 仅清理大字典
        newMrl3File.textureDict = textureDict
        return newMrl3File
    else:
        return None


def exportMHWMrl3File(filepath,mrl3CollectionName = ""):
    mrl3File = buildMrl3(mrl3CollectionName)
    if mrl3File != None:
        writeMHWMrl3(mrl3File,filepath)
        return True
    else:
        return False