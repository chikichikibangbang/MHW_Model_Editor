import os
import bpy
import time

from .ccl_export_errors import printCCLErrorDict, showMHWCCLErrorWindow
from ..common.blender_functions import getCollection, createEmpty, lockObjTransforms
from ..common.message_functions import raiseWarning, addErrorToDict
from .file_ccl import readCCLFile, CCLFile, writeCCLFile, Collision
from .ccl_functions import importCollisions, checkCCLError
from .ccl_properties import setCCLCollision
from ..ctc.ctc_functions import searchArmatureObj, findHeaderObj
from ..ctc.ctc_properties import getCTCHeader
from ..ctc.file_ctc import FileHeader

timeFormat = "%d"

def importMHWCCLFile(filePath, options, warningList=[], isNested=False):
    """
    isNested: 是否属于嵌套导入（比如在导入ctc的同时导入ccl就属于嵌套导入）
    """
    # warningList = []
    errorList = []
    cclFileName = os.path.split(filePath)[1]

    if not isNested:
        print("\033[96m__________________________________\nMHW CCL import started.\033[0m")
    cclImportStartTime = time.time()

    # 搜索骨架对象
    armatureObj = searchArmatureObj(cclFileName, options["targetArmature"])
    if armatureObj == None:
        return False
    bones = armatureObj.data.bones

    # 读取ccl文件
    try:
        cclFile = readCCLFile(filePath, bones)
    except Exception as err:
        warning = f"An error occurred while reading {filePath} - {str(err)}"
        raiseWarning(warning)
        warningList.append(warning)
        return False

    print("Parsed ccl.")
    print(f"Target Armature: {armatureObj.name}")

    if cclFile.misBoneSet:
        misBoneList = sorted(cclFile.misBoneSet)
        print(f"Mismatched Bones ({len(misBoneList)}):")
        for boneName in misBoneList:
            print(boneName)

    colList = cclFile.CollisionList
    ctcCollection = bpy.context.scene.mhw_ctc_toolpanel.ctcCollection
    bpy.context.scene.mhw_ccl_toolpanel.lastImportCollection = ctcCollection.name

    headerObj = findHeaderObj(ctcCollection)
    if headerObj == None:
        # 如果当前ctc集合内没有header空物体，则创建新的header空物体
        headerObj = createEmpty(f"CTC_HEADER {ctcCollection.name}", [("~TYPE", "MHW_CTC_HEADER")], None, ctcCollection)
        ctcHeader = FileHeader()
        getCTCHeader(ctcHeader, headerObj)
        lockObjTransforms(headerObj)

    # 导入collision
    if colList != []:
        makeNew = True if isNested else False
        cclEntryCol = getCollection(f"Collision Entries - {cclFileName}", ctcCollection, makeNew=makeNew)
        importCollisions(colList, armatureObj, headerObj, cclEntryCol)

    cclImportEndTime = time.time()
    cclImportTime = cclImportEndTime - cclImportStartTime
    print(f"CCL imported in {timeFormat % (cclImportTime * 1000)} ms.")

    print("\nCCL Info:")
    print(f"Collision Count: {cclFile.totalCount}")
    print(f"Matched Collision Count: {len(colList)} / {cclFile.totalCount}")
    # print(f"Valid Collision Count: {len(colList)} / {cclFile.Header.ColCount}")
    # print(f"Imported Collision Count: {len(colList)}")

    if not isNested:
        print("\033[92m__________________________________\nMHW CCL import finished.\033[0m")
    return True


def exportMHWCCLFile(filePath, options, isNested=False):
    # 需要报错的情况
    # 导出时未选择目标集合 ok
    # capsule collision没有head或tail ok
    # capsule collision有多个head或tail ok
    # sphere, head或tail的BoneName约束对象没有target骨架或subtarget骨骼 ok
    # sphere, head或tail没有BoneName约束对象 ok
    # sphere, head或tail的约束骨骼名称不符合MhBone_xxx格式，或骨骼后缀数字超过了最大限制511 ok

    errorDict = dict()

    if not isNested:
        print("\033[96m__________________________________\nMHW CCL export started.\033[0m")
    cclExportStartTime = time.time()

    # 获取要导出的ctc集合
    targetCollection = options["targetCollection"]
    if targetCollection != None:
        if not isNested:
            print(f"Target Collection: {targetCollection.name}")
        bpy.context.scene.mhw_ccl_toolpanel.lastExportCollection = targetCollection.name
    else:
        # 若导出时未选择ctc集合，则添加报错，并直接返回False
        addErrorToDict(errorDict, "NoTargetCTCCollection")
        printCCLErrorDict(errorDict, isNested)
        showMHWCCLErrorWindow(errorDict, "None", "None")
        return False

    objList = targetCollection.all_objects
    errorDict, colObjList = checkCCLError(objList, errorDict)

    if errorDict != {}:  # 若errorDict不为空，则打印报错信息到控制台，同时弹出报错信息窗口，然后直接退出函数，返回False
        printCCLErrorDict(errorDict, isNested)
        showMHWCCLErrorWindow(errorDict, targetCollection.name, "None")
        return False

    cclFile = CCLFile()
    cclFile.Header.ColCount = len(colObjList)
    cclFile.Header.ColTotalOffset = len(colObjList) * 64

    for colObj in colObjList:
        colEntry = Collision()
        setCCLCollision(colEntry, colObj)
        cclFile.CollisionList.append(colEntry)

    writeCCLFile(cclFile, filePath)
    print("Converting to ccl file finished.")

    cclExportEndTime = time.time()
    cclExportTime = cclExportEndTime - cclExportStartTime
    print(f"CCL exported in {timeFormat % (cclExportTime * 1000)} ms.")

    print("\nCCL Info:")
    print(f"Collision Count: {cclFile.Header.ColCount}")

    if not isNested:
        print("\033[92m__________________________________\nMHW CCL export finished.\033[0m")
    return True

