import os
import zlib

import bpy
from ..common.general_function import splitNativesPath, string_reformat
from ..common.message_functions import addErrorToDict


def sortPropBlock(name):
    if name not in {"CBMaterialCommon__disclosure",
                    "CBSpeedTreeCollision__disclosure",
                    "CBMhMaterialIvyFloorLocal__disclosure",
                    "CBMhMaterialSlantFloorLocal__disclosure"}:
        return 0  # 第一位
    elif name in {"CBSpeedTreeCollision__disclosure",
                  "CBMhMaterialIvyFloorLocal__disclosure",
                  "CBMhMaterialSlantFloorLocal__disclosure"}:
        return 1  # 第二位
    else:  # CBMaterialCommon__disclosure
        return 2  # 第三位


def addResourceToList(resourceDict, mhw_mrl3_material):
    cBuffer = []

    for code, resource in resourceDict.items():
        if resource["name"].startswith("t"):
            newListItem = mhw_mrl3_material.mapList_items.add()
            newListItem.name = string_reformat(resource["name"])
            newListItem.value = resource["value"]
            newListItem.code = code

        elif resource["name"].startswith("SS"):
            newListItem = mhw_mrl3_material.samplerList_items.add()
            newListItem.name = string_reformat(resource["name"])
            newListItem.value = resource["value"]
            newListItem.code = code

        elif resource["name"].startswith("CB"):
            cBuffer.append((code, resource))

    cBuffer = sorted(cBuffer, key=lambda x: sortPropBlock(x[1]["name"]))  # 对propertyBlock进行排序，让主要的block显示在前面

    for code, resource in cBuffer:
        propertyBlock_item = mhw_mrl3_material.propertyBlock_items.add()
        propertyBlock_item.blockName = string_reformat(resource["name"])
        propertyBlock_item.code = code
        propertyBlock_item.propertyList_items.clear()  # 清空现有属性

        for propName, propInfo in resource["prop"].items():
            if propName.startswith("align"):  # 跳过对齐字段
                continue

            newListItem = propertyBlock_item.propertyList_items.add()
            newListItem.ori_name = propName
            newListItem.prop_name = string_reformat(propName)

            propValue = propInfo[0]
            propType = propInfo[1]

            if propType == "float":
                newListItem.data_type = "FLOAT"
                newListItem.float_value = propValue
            elif propType == "int":
                newListItem.data_type = "INT"
                newListItem.int_value = propValue
            elif propType == "uint":
                newListItem.data_type = "UINT"
                newListItem.uint_value = propValue
            elif propType == "bbool":
                newListItem.data_type = "BOOL"
                newListItem.bool_value = bool(propValue)
            elif propType == "float[2]":
                newListItem.data_type = "FLOAT[2]"
                newListItem.float2_value = propValue
            elif propType == "float[3]":
                if not propName.endswith("__uiColor"):
                    newListItem.data_type = "FLOAT[3]"
                    newListItem.float3_value = propValue
                else:
                    newListItem.data_type = "COLOR"
                    newListItem.color_value = propValue + [1.0]
            elif propType == "float[4]":
                if not propName.endswith("__uiColor"):
                    newListItem.data_type = "FLOAT[4]"
                    newListItem.float4_value = propValue
                else:
                    newListItem.data_type = "COLOR"
                    newListItem.color_value = propValue


def checkMrl3Error(objList, errorDict):
    matHashDict = dict()

    for obj in objList:
        if obj.get("~TYPE", None) == "MHW_MRL3_MATERIAL":
            if obj.mhw_mrl3_material.materialName.startswith("Unknown Hash"):
                matNameHash = int(obj.mhw_mrl3_material.materialNameHash)
            else:
                crc = zlib.crc32(obj.mhw_mrl3_material.materialName.encode())
                matNameHash = crc ^ 0xffffffff

            if matNameHash not in matHashDict:
                matHashDict[matNameHash] = [obj]
            else:
                matHashDict[matNameHash].append(obj)

    for objList in matHashDict.values():
        if len(objList) > 1:
            for obj in objList:
                addErrorToDict(errorDict, "MultipleSameMaterials", objectName=obj.name)

    return errorDict, matHashDict


def reindexMaterials(mrl3Collection):
    # if bpy.data.collections.get(collectionName, None) != None:
    #     mrl3Collection = bpy.data.collections[collectionName]
    # else:
    #     mrl3Collection = bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection
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


def fixTexPath(path):  # Fix potential path problems
    # path = path.replace(os.sep,"/").split(".tex")[0]
    path = path.replace("/", os.sep).split(".tex")[0]
    if "nativepc" in path.lower():
        splitPath = splitNativesPath(path)
        if splitPath != None:
            path = splitPath[1]  # Fix including the chunk root path in the tex path
    return path