import copy
import os
import time
import zlib
import bpy
import datetime
from ..common.general_function import string_reformat
from .mrl3_panels import tag_redraw
from .file_mrl3 import Mrl3File, Material, readMrl3File, writeMrl3File
from .mrl3_dicts import get_master_material_dict, clear_master_material_dict_cache, get_property_dict, clear_all_caches
from .mrl3_export_errors import printMrl3ErrorDict, showMHWMrl3ErrorWindow
from .mrl3_functions import reindexMaterials, fixTexPath, addResourceToList, checkMrl3Error
from ..common.blender_functions import createCollection, createEmpty, lockObjTransforms
from ..common.general_function import splitNativesPath
from ..common.message_functions import textColors, raiseWarning, showMessageBox, showErrorMessageBox, addErrorToDict
from ..common.rw_functions import unsignedToSigned
from .....common.i18n.i18n import i18n
timeFormat = "%d"


def importMHWMrl3File(filePath, options, warningList=[], isNested=False):
    """
    isNested: 是否属于嵌套导入（比如在导入ctc的同时导入ccl就属于嵌套导入）
    """
    lang = bpy.context.preferences.view.language
    # warningList = []
    errorList = []
    mrl3FileName = os.path.split(filePath)[1]

    if not isNested:
        print(f"\033[96m__________________________________\n{i18n('MHW Mrl3 import started.')}\033[0m")
    mrl3ImportStartTime = time.time()

    if not isNested:
        # 读取mrl3文件
        try:
            mrl3File = readMrl3File(filePath)
        except Exception as err:
            if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                warning = f"读取 {filePath} 时发生错误 - {i18n(str(err))}"
            else:
                warning = f"An error occurred while reading {filePath} - {str(err)}"
            raiseWarning(warning)
            warningList.append(warning)
            return False
    else:
        mrl3File = options["mrl3File"]

    mrl3File.parser(options["mod3MatHashDict"])
    if not isNested:
        print(i18n("Parsed mrl3."))

    if mrl3File.misMatHashList != []:
        print(f"{i18n('Mismatched Material Hashes')} ({len(mrl3File.misMatHashList)}):")
        for matHash in mrl3File.misMatHashList:
            print(matHash)

    materialList = mrl3File.materialList
    mrl3Collection = None
    mhw_mrl3_toolpanel = bpy.context.scene.mhw_mrl3_toolpanel

    mrl3Collection = createCollection(mrl3FileName, "COLOR_05", "MHW_MRL3_COLLECTION", options["parentCollection"])
    mhw_mrl3_toolpanel.mrl3Collection = mrl3Collection
    mhw_mrl3_toolpanel.lastImportCollection = mrl3Collection.name

    for index, material in enumerate(materialList):
        matInfo = material.matInfo

        name = f"Mrl3 Material {str(index).zfill(2)} ({matInfo.materialName})"
        matObj = createEmpty(name, [("~TYPE", "MHW_MRL3_MATERIAL")], None, mrl3Collection)
        # lockObjTransforms(matObj)

        mhw_mrl3_material = matObj.mhw_mrl3_material
        mhw_mrl3_material.materialName = matInfo.materialName
        mhw_mrl3_material.materialNameHash = str(matInfo.materialNameHash)

        mhw_mrl3_material.mmtrHash = str(matInfo.mmtrHash)
        mhw_mrl3_material.mmtrName = matInfo.mmtrName
        mhw_mrl3_material.shaderHash = str(matInfo.shaderHash)

        mhw_mrl3_material.surfaceCoef = matInfo.surfaceCoef
        mhw_mrl3_material.alphaCoef = matInfo.alphaCoef

        addResourceToList(material.resourceDict, mhw_mrl3_material)  # 添加resource到各自的属性列表

    tag_redraw(bpy.context)

    mrl3ImportEndTime = time.time()
    mrl3ImportTime = mrl3ImportEndTime - mrl3ImportStartTime
    print(f"{i18n('Mrl3 data imported in')} {timeFormat % (mrl3ImportTime * 1000)} ms.")

    # 格式化时间戳
    dt_object = datetime.datetime.fromtimestamp(mrl3File.fileHeader.timestamp)
    formatted_date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    totalCount = mrl3File.fileHeader.materialCount

    print(f"\n{i18n('Mrl3 Info:')}")
    print(f"{i18n('Mrl3 TimeStamp:')} {formatted_date_time}")
    print(f"{i18n('Material Count:')} {totalCount}")
    print(f"{i18n('Matched Material Count:')} {totalCount - len(mrl3File.misMatHashList)} / {totalCount}")
    # print(f"Valid Material Count: {len(materialList)} / {totalCount}")
    print(f"{i18n('Imported Material Count:')} {len(materialList)}")

    if not isNested:
        print(f"\033[92m__________________________________\n{i18n('MHW Mrl3 import finished.')}\033[0m")
    return True


def exportMHWMrl3File(filePath, options):
    # 需要报错的情况
    # 导出时未选择目标集合 ok
    # 存在重复的材质名 ok
    # 某个贴图的贴图路径长度超过了256  # 暂时通过StringProperty的maxlen参数进行限制

    # 可能需要警告的情况
    # mod3网格对象的材质名没有对应的mrl3空物体对象  # TODO

    lang = bpy.context.preferences.view.language
    errorDict = dict()

    print(f"\033[96m__________________________________\n{i18n('MHW Mrl3 export started.')}\033[0m")
    mrl3ExportStartTime = time.time()

    # 获取要导出的mrl3集合
    targetCollection = options["targetCollection"]
    if targetCollection != None:
        print(f"{i18n('Target Collection:')} {targetCollection.name}")
        bpy.context.scene.mhw_mrl3_toolpanel.lastExportCollection = targetCollection.name
    else:
        # 若导出时未选择mrl3集合，则添加报错，并直接返回False
        addErrorToDict(errorDict, "NoTargetMrl3Collection")
        printMrl3ErrorDict(errorDict)
        showMHWMrl3ErrorWindow(errorDict, "None", "None")
        return False

    # reindexMaterials(targetCollection)
    objList = targetCollection.all_objects
    errorDict, matHashDict = checkMrl3Error(objList, errorDict)

    if errorDict != {}:  # 若errorDict不为空，则打印报错信息到控制台，同时弹出报错信息窗口，然后直接退出函数，返回False
        printMrl3ErrorDict(errorDict)
        showMHWMrl3ErrorWindow(errorDict, targetCollection.name, "None")
        return False

    mrl3File = Mrl3File()
    textureIndex = 0  # 贴图序号

    try:
        mmtrDict = get_master_material_dict()
        propDict = get_property_dict()

        # for matObj in matObjList:
        for matHash, matObjList in matHashDict.items():
            # mhw_mrl3_material = matObj.mhw_mrl3_material
            mhw_mrl3_material = matObjList[0].mhw_mrl3_material
            if mhw_mrl3_material.mmtrHash not in mmtrDict:
                continue

            entry = Material()
            matInfo = entry.matInfo
            mmtrData = mmtrDict[mhw_mrl3_material.mmtrHash]

            # if mhw_mrl3_material.materialName.startswith("Unknown Hash"):
            #     matInfo.materialNameHash = int(mhw_mrl3_material.materialNameHash)
            # else:
            #     crc = zlib.crc32(mhw_mrl3_material.materialName.encode())
            #     matInfo.materialNameHash = crc ^ 0xffffffff
            matInfo.materialNameHash = matHash
            matInfo.mmtrHash = int(mhw_mrl3_material.mmtrHash)
            matInfo.shaderHash = mmtrData["shaderHash"]
            matInfo.blockSize = mmtrData["blockSize"]
            matInfo.surfaceCoef = mhw_mrl3_material.surfaceCoef
            matInfo.resourceCount = mmtrData["resourceCount"] * 2
            matInfo.alphaCoef = mhw_mrl3_material.alphaCoef

            entry.resourceDict = copy.deepcopy(mmtrData["resourceDict"])

            if mhw_mrl3_material.mapList_items:
                for mapItem in mhw_mrl3_material.mapList_items:
                    if mapItem.code not in entry.resourceDict or not mapItem.value:
                        continue

                    fixedPath = fixTexPath(mapItem.value)
                    if fixedPath not in mrl3File.textureDict:
                        mrl3File.textureDict[fixedPath] = textureIndex
                        textureIndex += 1

                    entry.resourceDict[mapItem.code]["value"] = mrl3File.textureDict[fixedPath] + 1

            if mhw_mrl3_material.samplerList_items:
                for samplerItem in mhw_mrl3_material.samplerList_items:
                    if samplerItem.code not in entry.resourceDict:
                        continue
                    entry.resourceDict[samplerItem.code]["value"] = samplerItem.value

            if mhw_mrl3_material.propertyBlock_items:
                # entry.resourceDict["props"] = []
                for propBlockItem in mhw_mrl3_material.propertyBlock_items:
                    if propBlockItem.code not in entry.resourceDict:
                        continue

                    tempDict = copy.deepcopy(propDict[propBlockItem.code]["fields"])
                    for prop in propBlockItem.propertyList_items:
                        if prop.ori_name not in tempDict:
                            continue

                        if prop.data_type == "INT":
                            value = prop.int_value
                        elif prop.data_type == "UINT":
                            value = prop.uint_value
                        elif prop.data_type == "BOOL":
                            value = 1 if prop.bool_value else 0
                        elif prop.data_type == "FLOAT[2]":
                            value = list(prop.float2_value)
                        elif prop.data_type == "FLOAT[3]":
                            value = list(prop.float3_value)
                        elif prop.data_type == "FLOAT[4]":
                            value = list(prop.float4_value)
                        elif prop.data_type == "COLOR":
                            value = list(prop.color_value)
                        else:  # float
                            value = prop.float_value

                        tempDict[prop.ori_name][0] = value

                    entry.resourceDict[propBlockItem.code]["props"] = tempDict
                    # entry.resourceDict["props"].append(tempDict)

            mrl3File.materialList.append(entry)

    finally:
        clear_all_caches()

    mrl3File.writeResourceBuffers()
    writeMrl3File(mrl3File, filePath)
    print(i18n("Converting to mrl3 file finished."))

    mrl3ExportEndTime = time.time()
    mrl3ExportTime = mrl3ExportEndTime - mrl3ExportStartTime
    print(f"{i18n('Mrl3 exported in')} {timeFormat % (mrl3ExportTime * 1000)} ms.")

    print(f"\n{i18n('Mrl3 Info:')}")
    print(f"{i18n('Texture Count:')} {mrl3File.fileHeader.textureCount}")
    print(f"{i18n('Material Count:')} {mrl3File.fileHeader.materialCount}")

    print(f"\033[92m__________________________________\n{i18n('MHW Mrl3 export finished.')}\033[0m")
    return True




# def buildMrl3(mrl3CollectionName):
#     mrl3Collection = bpy.data.collections.get(mrl3CollectionName)
#     reindexMaterials(mrl3CollectionName)
#
#     if mrl3Collection != None:
#         valid = Mrl3ErrorCheck(mrl3CollectionName)
#     else:
#         showErrorMessageBox("Mrl3 collection is not set, cannot export")
#         valid = False
#
#     if valid:
#         # #将mrl3空物体对象按名称排序
#         # materialObjList = sorted([child for child in mrl3Collection.all_objects if child.get("~TYPE", None) == "MHW_MRL3_MATERIAL"], key=lambda item: item.name)
#         materialObjList = [child for child in mrl3Collection.all_objects if child.get("~TYPE", None) == "MHW_MRL3_MATERIAL"]
#         newMrl3File = MHWMrl3()
#
#         textureDict = {} #用于存放所有贴图的字典
#         textureIndex = 0 #贴图序号
#         try:
#             for materialObj in materialObjList:
#                 materialEntry = Material()
#                 mhw_mrl3_material = materialObj.mhw_mrl3_material
#                 master_material_dict = get_master_material_dict() #获取主材质字典
#                 property_dict = get_property_dict()
#
#                 crc = zlib.crc32(mhw_mrl3_material.materialName.encode())
#                 materialEntry.materialNameHash = crc ^ 0xffffffff
#
#                 # shaderHash1 = mhw_mrl3_material.shaderHash1
#                 mmtrDict = master_material_dict[mhw_mrl3_material.shaderHash1]
#
#                 materialEntry.shaderHash1 = int(mhw_mrl3_material.shaderHash1)
#                 materialEntry.shaderHash2 = mmtrDict["shaderHash2"]
#                 materialEntry.materialBlockSize = mmtrDict["matBlockSize"]
#                 materialEntry.resourceCount = mmtrDict["resourceCount"]
#                 surfaceDirection = int(mhw_mrl3_material.surfaceDirection, 16)
#                 materialEntry.surfaceDirection = unsignedToSigned(surfaceDirection)
#                 materialEntry.alpha_bytes = mhw_mrl3_material.alphaCoef
#                 materialEntry.resourceDict = copy.deepcopy(mmtrDict["resourceDict"])
#
#                 for resource in mhw_mrl3_material.mapList_items:
#                     if resource.mapPath:
#                         fixedPath = fixTexPath(resource.mapPath)
#
#                         if fixedPath not in textureDict:
#                             textureDict[fixedPath] = textureIndex
#                             textureIndex += 1
#
#                         resourceHash = int(resource.resourceHash) >> 12
#                         if str(resourceHash) in materialEntry.resourceDict:
#                             materialEntry.resourceDict[str(resourceHash)]["value"] = textureDict[fixedPath] + 1
#
#                 for resource in mhw_mrl3_material.propertyBlock_items:
#                     resourceHash = int(resource.resourceHash) >> 12
#                     if str(resourceHash) in materialEntry.resourceDict:
#                         materialEntry.resourceDict[str(resourceHash)]["propDict"] = copy.deepcopy(property_dict[str(resourceHash)]["fields"])
#                         propertyIndex = 0
#                         # for property in resource.propertyList_items:
#                         for propName, propType in list(materialEntry.resourceDict[str(resourceHash)]["propDict"].items()):
#                             if propName.startswith("align"):  # 跳过对齐字段
#                                 continue
#                             property = resource.propertyList_items[propertyIndex]
#                             materialEntry.resourceDict[str(resourceHash)]["propDict"][propName] = [materialEntry.resourceDict[str(resourceHash)]["propDict"][propName]]
#                             materialEntry.resourceDict[str(resourceHash)]["propDict"][propName].append(getPropValue(propType, property))
#                             propertyIndex += 1
#                     # print(materialEntry.resourceDict[str(resourceHash)]["propDict"])
#
#                 for resource in mhw_mrl3_material.samplerList_items:
#                     resourceHash = int(resource.resourceHash) >> 12
#                     if str(resourceHash) in materialEntry.resourceDict:
#                         materialEntry.resourceDict[str(resourceHash)]["value"] = resource.samplerIndex
#
#                 newMrl3File.materialList.append(materialEntry)
#         finally:
#             clear_master_material_dict_cache() # 仅清理大字典
#         newMrl3File.textureDict = textureDict
#         return newMrl3File
#     else:
#         return None

