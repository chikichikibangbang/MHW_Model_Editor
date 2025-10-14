import bpy
import os
import time
import glob

from .ctc_export_errors import printCTCErrorDict, showMHWCTCErrorWindow
from ..ccl.blender_ccl import importMHWCCLFile, exportMHWCCLFile
from ..common.blender_functions import createCollection, getCollection, createEmpty, lockObjTransforms
from ..common.message_functions import raiseWarning, addErrorToDict

from .file_ctc import readCTCFile, CTCFile, Chain, Node, writeCTCFile
from .ctc_functions import searchArmatureObj, findHeaderObj, importChains, checkCTCError
from .ctc_properties import getCTCHeader, setCTCHeader, setCTCChain, setCTCNode

timeFormat = "%d"


def loadCCL(filePath, armatureObj, warningList):
    # 确定ccl文件路径
    cclPath = f"{glob.escape(filePath.split('.ctc')[0])}.ccl"
    print("")

    if not os.path.isfile(cclPath):
        warning = f"An error occurred while reading {cclPath} - File is not found."
        raiseWarning(warning)
        warningList.append(warning)
        return

    options = {"targetArmature": armatureObj}
    importMHWCCLFile(cclPath, options, warningList=warningList, isNested=True)


def importMHWCTCFile(filePath, options, warningList=[], isNested=False):
    """
    isNested: 是否属于嵌套导入（比如在导入ctc的同时导入ccl就属于嵌套导入）
    """
    # warningList = []
    errorList = []
    ctcFileName = os.path.split(filePath)[1]

    if not isNested:
        print("\033[96m__________________________________\nMHW CTC import started.\033[0m")
    ctcImportStartTime = time.time()

    # 搜索骨架对象
    armatureObj = searchArmatureObj(ctcFileName, options["targetArmature"])
    if armatureObj == None:
        return False
    bones = armatureObj.data.bones

    # 读取ctc文件
    try:
        ctcFile = readCTCFile(filePath, bones)
    except Exception as err:
        warning = f"An error occurred while reading {filePath} - {str(err)}"
        raiseWarning(warning)
        warningList.append(warning)
        return False

    print("Parsed ctc.")
    print(f"Target Armature: {armatureObj.name}")

    if ctcFile.misBoneSet:
        misBoneList = sorted(ctcFile.misBoneSet)
        print(f"Mismatched Bones ({len(misBoneList)}):")
        for boneName in misBoneList:
            print(boneName)

    chainList = ctcFile.ChainList
    headerObj = None
    ctcCollection = None
    mergedChain = False
    mhw_ctc_toolpanel = bpy.context.scene.mhw_ctc_toolpanel
    
    # 导入header
    if options["mergeCollection"]:
        ctcCollection = options["mergeCollection"]
        mhw_ctc_toolpanel.lastImportCollection = ctcCollection.name
        headerObj = findHeaderObj(ctcCollection)
        mergedChain = True

    if headerObj == None:
        mergedChain = False

        # 检查当前骨架对象是否所属mod3集合，且mod3集合也属于嵌套集合
        parentCollection = None
        if len(armatureObj.users_collection) > 0 and armatureObj.users_collection[0].get("~TYPE") == "MHW_MOD3_COLLECTION":
            for collection in bpy.data.collections:
                if armatureObj.users_collection[0].name in collection.children:
                    parentCollection = collection
                    break

        # 如果找到包含mod3集合的父级集合，则将ctc集合也作为该集合的子级集合，否则以默认无父级集合创建ctc集合
        ctcCollection = createCollection(ctcFileName, "COLOR_02", "MHW_CTC_COLLECTION", parentCollection)
        mhw_ctc_toolpanel.ctcCollection = ctcCollection
        mhw_ctc_toolpanel.lastImportCollection = ctcCollection.name

        # 创建header空物体
        headerObj = createEmpty(f"CTC_HEADER {ctcFileName}", [("~TYPE", "MHW_CTC_HEADER")], None, ctcCollection)
        getCTCHeader(ctcFile.Header, headerObj)
        lockObjTransforms(headerObj)

    # 导入chain
    if chainList != []:
        ctcEntryCol = getCollection(f"Chain Entries - {ctcCollection.name}", ctcCollection, makeNew=not mergedChain)
        importChains(chainList, armatureObj, headerObj, ctcEntryCol, mergedChain)

    ctcImportEndTime = time.time()
    ctcImportTime = ctcImportEndTime - ctcImportStartTime
    print(f"CTC imported in {timeFormat % (ctcImportTime * 1000)} ms.")

    print("\nCTC Info:")
    print(f"Chain Count: {ctcFile.Header.ChainCount}")
    print(f"Matched Chain Count: {len(chainList)} / {ctcFile.Header.ChainCount}")
    # print(f"Valid Chain Count: {len(chainList)} / {ctcFile.Header.ChainCount}")
    # print(f"Imported Chain Count: {len(chainList)}")

    if options["loadCCL"]:
        loadCCL(filePath, armatureObj, warningList)

    if not isNested:
        print("\033[92m__________________________________\nMHW CTC import finished.\033[0m")
    return True




def exportMHWCTCFile(filePath, options):
    # 需要报错的情况
    # 导出时未选择目标集合 ok
    # header是其他对象的子级 ok
    # node没有角度限制子级 ok
    # node有多个角度限制子级 ok
    # node的父级对象不正确，或node没有父级对象 ok
    # node的BoneName约束对象没有target骨架或subtarget骨骼 ok
    # node没有BoneName约束对象 ok
    # node的约束骨骼名称不符合MhBone_xxx格式，或骨骼后缀数字超过了最大限制511 ok
    # 有多个node对应相同的骨骼 ok
    # chain的父级对象不正确，或chain没有父级对象 ok
    # chain没有子级node ok
    # chain只有一个子级node ok
    # ctc集合中没有header ok
    # ctc集合中有多个header ok
    # chain有分叉 ok

    errorDict = dict()

    print("\033[96m__________________________________\nMHW CTC export started.\033[0m")
    ctcExportStartTime = time.time()

    # 获取要导出的ctc集合
    targetCollection = options["targetCollection"]
    if targetCollection != None:
        print(f"Target Collection: {targetCollection.name}")
        bpy.context.scene.mhw_ctc_toolpanel.lastExportCollection = targetCollection.name
    else:
        # 若导出时未选择ctc集合，则添加报错，并直接返回False
        addErrorToDict(errorDict, "NoTargetCTCCollection")
        printCTCErrorDict(errorDict)
        showMHWCTCErrorWindow(errorDict, "None", "None")
        return False

    objList = targetCollection.all_objects
    errorDict, ctcObjDict = checkCTCError(objList, errorDict)

    if errorDict != {}:  # 若errorDict不为空，则打印报错信息到控制台，同时弹出报错信息窗口，然后直接退出函数，返回False
        printCTCErrorDict(errorDict)
        showMHWCTCErrorWindow(errorDict, targetCollection.name, "None")
        return False

    ctcFile = CTCFile()

    ctcFile.Header.ChainCount = len(ctcObjDict["chain"])
    ctcFile.Header.NodeCount = len(ctcObjDict["node"])
    setCTCHeader(ctcFile.Header, ctcObjDict["header"])

    for chainObj in ctcObjDict["chain"]:
        ctcChain = Chain()
        setCTCChain(ctcChain, chainObj)

        currentNode = chainObj.children[0]
        nodeCount = 0
        hasChildNode = True

        # 遍历每个chain的子级node，以获取node的数量
        while hasChildNode:
            nodeCount += 1
            currentNodeHasChildNode = False

            for child in currentNode.children:
                if child.get("~TYPE", None) == "MHW_CTC_NODE":
                    currentNode = child
                    currentNodeHasChildNode = True

            if not currentNodeHasChildNode:
                hasChildNode = False

        ctcChain.NodeCount = nodeCount
        ctcFile.ChainList.append(ctcChain)

    for nodeObj in ctcObjDict["node"]:
        ctcNode = Node()
        setCTCNode(ctcNode, nodeObj)
        ctcFile.NodeList.append(ctcNode)

    writeCTCFile(ctcFile, filePath)
    print("Converting to ctc file finished.")

    ctcExportEndTime = time.time()
    ctcExportTime = ctcExportEndTime - ctcExportStartTime
    print(f"CTC exported in {timeFormat % (ctcExportTime * 1000)} ms.")

    print("\nCTC Info:")
    print(f"Chain Count: {ctcFile.Header.ChainCount}")
    print(f"Node Count: {ctcFile.Header.NodeCount}")

    if options["exportCCL"]:
        cclPath = f"{glob.escape(filePath.split('.ctc')[0])}.ccl"
        print("")

        # options = {"targetCollection": targetCollection}
        exportMHWCCLFile(cclPath, options, isNested=True)

    print("\033[92m__________________________________\nMHW CTC export finished.\033[0m")
    return True










