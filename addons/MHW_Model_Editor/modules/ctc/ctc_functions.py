import re
import bpy
from ..common.message_functions import raiseWarning, showErrorMessageBox, addErrorToDict
from ..common.blender_functions import checkNameUsage, createCurveEmpty, createEmpty

from .ctc_properties import getCTCChain, getCTCNode
from .ctc_nodes import getConeGeoNodeTree, getChainMat


def searchArmatureObj(fileName, targetArmature=None):
    armatureObj = None  # 初始化armatureObj为None，表示未找到骨架对象

    if targetArmature:
        armatureObj = targetArmature
        return armatureObj

    if armatureObj == None:
        # 尝试查找与ctc或ccl文件名同名的mod3集合
        mod3ColName = fileName.replace(".ctc", ".mod3").replace(".ccl", ".mod3")
        if mod3ColName in bpy.data.collections:
            mod3Collection = bpy.data.collections[mod3ColName]
            # 若找到了同名的mod3集合，在集合内查找骨架对象
            for obj in mod3Collection.objects:
                if obj.type == "ARMATURE" and armatureObj != None:
                    # 如果找到多个骨架对象，则报错提示
                    showErrorMessageBox(
                        "More than one armature was found in the scene. Select an armature before importing the ctc file.")
                    return None
                if obj.type == "ARMATURE":
                    armatureObj = obj

    if armatureObj == None:
        try:
            # 若当前活动对象存在且为骨架类型，则将当前活动对象赋值给armature
            activeObj = bpy.context.active_object
            if activeObj != None and activeObj.type == "ARMATURE":
                armatureObj = activeObj
        except:
            pass

    # 如果仍然未找到骨架对象，则遍历当前场景中所有的对象
    if armatureObj == None:
        for obj in bpy.context.scene.objects:
            # 如果找到多个骨架对象，则报错提示
            if obj.type == "ARMATURE" and armatureObj != None:
                showErrorMessageBox(
                    "More than one armature was found in the scene. Select an armature before importing the ctc file.")
                return None
            if obj.type == "ARMATURE":
                armatureObj = obj

    # 如果到最后都没有找到骨架对象，则报错提示
    if armatureObj == None:
        showErrorMessageBox(
            "No armature in scene. The armature from the mod3 file must be present in order to import the ctc file.")
        return None

    return armatureObj

def findHeaderObj(ctcCollection=None):
    if ctcCollection == None:
        if bpy.context.scene.mhw_ctc_toolpanel.ctcCollection != None:
            ctcCollection = bpy.context.scene.mhw_ctc_toolpanel.ctcCollection

    if ctcCollection != None:
        objList = ctcCollection.all_objects
        headerList = [obj for obj in objList if obj.get("~TYPE",None) == "MHW_CTC_HEADER"]

        # 如果找到了至少一个Header空物体，则返回其中第一个
        if len(headerList) >= 1:
            return headerList[0]
        # 如果未找到任何Header空物体，则返回None
        else:
            return None
    else:
        return None

def getBoneParentsRecursive(bone,boneList,recursionAmount):
    boneList.append(bone)
    if recursionAmount > 0:
        try:
            getBoneParentsRecursive(bone.parent, boneList, recursionAmount - 1)
        except:
            raiseWarning(f"Could not get parent of bone {bone.name}")

def alignChains():
    for chain in [obj for obj in bpy.context.scene.objects if obj.get("~TYPE", None) == "MHW_CTC_CHAIN"]:
        if len(chain.children) > 0:
            currentNode = chain.children[0]
            nodeObjList = [currentNode]
            while len(currentNode.children) > 1:
                currentNode.location = (0.0, 0.0, 0.0)
                currentNode.rotation_euler = (0.0, 0.0, 0.0)
                currentNode.scale = (1.0, 1.0, 1.0)

                hasNodeChild = False
                for child in currentNode.children:
                    if child.get("~TYPE", None) == "MHW_CTC_NODE":
                        nodeObjList.append(child)
                        hasNodeChild = True

                        currentNode = child
                if not hasNodeChild:
                    break
            nodeObjList.reverse()
            for recurse in nodeObjList:
                if recurse.mhw_ctc_node.BoneColRadius != 0:
                    recurse.empty_display_size = 0.01 * recurse.mhw_ctc_node.BoneColRadius  # * 100
                else:
                    recurse.empty_display_size = .01

                for obj in nodeObjList:
                    try:
                        obj.constraints["BoneName"].inverse_matrix = obj.parent.matrix_world.inverted()
                    except:
                        pass
                bpy.context.view_layer.update()

def setChainBoneColor(armatureObj):
    # TODO Add theme option in preferences
    THEME = "THEME03"
    if armatureObj != None:
        if bpy.app.version < (4, 0, 0):
            if armatureObj.pose.bone_groups.get("CTC Chain Bones",None) != None:
                boneGroup = armatureObj.pose.bone_groups["CTC Chain Bones"]
            else:
                boneGroup = armatureObj.pose.bone_groups.new(name="CTC Chain Bones")
            boneGroup.color_set = THEME
        # ctcCollection = bpy.data.collections.get(bpy.context.scene.mhw_ctc_toolpanel.ctcCollection)
        ctcCollection = bpy.context.scene.mhw_ctc_toolpanel.ctcCollection
        if ctcCollection != None:
            objList = ctcCollection.all_objects
        else:
            objList = bpy.data.objects
        try:
            ctcBoneList = [obj.constraints["BoneName"].subtarget for obj in objList if obj.get("~TYPE",None) == "MHW_CTC_NODE"]
        except:
            ctcBoneList = []
        for ctcBone in ctcBoneList:
            if bpy.app.version < (4, 0, 0):
                poseBone = armatureObj.pose.bones.get(ctcBone,None)
                if poseBone != None:
                    poseBone.bone_group = boneGroup
            else:
                if ctcBone in armatureObj.data.bones:
                    bone = armatureObj.data.bones[ctcBone]
                    bone.color.palette = THEME

def importChains(chainList, armatureObj, headerObj, ctcEntryCol, mergedChain):
    mhw_ctc_toolpanel = bpy.context.scene.mhw_ctc_toolpanel
    currentIndex = 0
    bones = armatureObj.data.bones

    for chain in chainList:
        # 检查名称是否已被使用
        name = "CTC_CHAIN_" + str(currentIndex).zfill(2)
        if mergedChain:
            while checkNameUsage(name, checkSubString=True):
                currentIndex += 1
                name = "CTC_CHAIN_" + str(currentIndex).zfill(2)
        else:
            currentIndex += 1

        # 创建chain链体
        name = f"{name} - {chain.NodeList[0].BoneName} > {chain.NodeList[-1].BoneName}"
        chainObj = createCurveEmpty(name, [("~TYPE", "MHW_CTC_CHAIN")], headerObj, ctcEntryCol, makeNew=True)
        getCTCChain(chain, chainObj)

        # 强制刷新数值
        chainObj.mhw_ctc_chain.CollisionAttrFlagValue = chainObj.mhw_ctc_chain.CollisionAttrFlagValue
        chainObj.mhw_ctc_chain.ChainAttrFlagValue = chainObj.mhw_ctc_chain.ChainAttrFlagValue
        # lockObjTransforms(chainObj)

        endBone = bones.get(chain.NodeList[-1].BoneName)
        boneList = []
        getBoneParentsRecursive(endBone, boneList, len(chain.NodeList) - 1)
        # print(boneList)

        # 设置曲线约束
        constraint = chainObj.constraints.new("COPY_LOCATION")
        constraint.target = armatureObj
        constraint.subtarget = boneList[-1].name  # TODO 处理能匹配到骨骼但是构不成一条独立链的情况

        chainObj.show_in_front = mhw_ctc_toolpanel.drawChainsThroughObjects
        spline = chainObj.data.splines.new("NURBS")
        spline.use_endpoint_u = True
        chainObj.data.bevel_depth = 0.001 * mhw_ctc_toolpanel.chainDisplaySize
        chainObj.data.dimensions = "3D"
        chainObj.data.use_fill_caps = True
        chainObj.data.materials.append(getChainMat())
        spline.points.add(len(boneList) - 1)

        for i, o in enumerate(boneList):
            p = spline.points[i]
            objPos = list((armatureObj.matrix_world @ o.matrix_local).to_translation())
            objPos.append(0.5)
            p.co = objPos
            h = chainObj.modifiers.new(o.name, 'HOOK')
            h.object = armatureObj
            h.subtarget = o.name
            h.vertex_indices_set([i])

        nodeParent = chainObj
        lightObj = None

        # 导入node
        for node in chain.NodeList:
            # 创建node空物体
            nodeObj = createEmpty(node.BoneName, [("~TYPE", "MHW_CTC_NODE")], nodeParent, ctcEntryCol)
            getCTCNode(node, nodeObj)
            nodeParent = nodeObj

            # nodeObj.empty_display_size = 2
            nodeObj.empty_display_type = "SPHERE"
            nodeObj.show_name = mhw_ctc_toolpanel.showNodeNames
            nodeObj.show_in_front = mhw_ctc_toolpanel.drawNodesThroughObjects

            # 将链节点约束到对应的骨骼
            constraint = nodeObj.constraints.new(type="COPY_LOCATION")
            constraint.target = armatureObj
            constraint.subtarget = node.BoneName
            constraint.name = "BoneName"
            constraint = nodeObj.constraints.new(type="COPY_ROTATION")
            constraint.target = armatureObj
            constraint.subtarget = node.BoneName
            constraint.name = "BoneRotation"
            constraint = nodeObj.constraints.new(type="COPY_SCALE")
            constraint.target = chainObj
            constraint.name = "BoneScale"

            # 创建角度限制空物体
            frame = createEmpty(nodeObj.name + "_ANGLE_LIMIT", [("~TYPE", "MHW_CTC_NODE_FRAME")], nodeObj, ctcEntryCol)
            frame.empty_display_type = "ARROWS"
            frame.empty_display_size = 0.01 * mhw_ctc_toolpanel.angleLimitDisplaySize
            frame.show_in_front = mhw_ctc_toolpanel.drawNodesThroughObjects

            constraint = frame.constraints.new(type="COPY_LOCATION")
            constraint.target = nodeObj
            constraint = frame.constraints.new(type="COPY_SCALE")
            constraint.target = nodeObj

            frame.matrix_local = node.NodeMatrix.matrix
            frame.rotation_mode = "XYZ"

            # 创建角度限制锥体
            lightObj = createCurveEmpty(nodeObj.name + "_ANGLE_LIMIT_HELPER",
                                        [("~TYPE", "MHW_CTC_NODE_FRAME_HELPER")], frame, ctcEntryCol)
            lightObj.matrix_world = frame.matrix_world
            lightObj.show_wire = True
            lightObj.hide_select = True
            lightObj.show_in_front = mhw_ctc_toolpanel.drawConesThroughObjects
            lightObj.hide_viewport = not mhw_ctc_toolpanel.showAngleLimitCones

            # 获取锥体的几何节点
            modifier = lightObj.modifiers.new(name="CTCGeometryNodes", type='NODES')
            nodeGroup = getConeGeoNodeTree()
            if modifier.node_group != None and modifier.node_group.name in bpy.data.node_groups:
                bpy.data.node_groups.remove(modifier.node_group)
            modifier.node_group = nodeGroup

            # 强制刷新
            nodeObj.mhw_ctc_node.AngleLimitRadius = nodeObj.mhw_ctc_node.AngleLimitRadius
            nodeObj.mhw_ctc_node.BoneColRadius = nodeObj.mhw_ctc_node.BoneColRadius

            # 设置锥体尺寸
            xScaleModifier = 1
            yScaleModifier = 1
            zScaleModifier = 1

            if nodeObj.mhw_ctc_node.AngleMode == "2":
                zScaleModifier = .01
            elif nodeObj.mhw_ctc_node.AngleMode == "3":
                zScaleModifier = nodeObj.mhw_ctc_node.WidthRate
            lightObj.scale = (0.001 * mhw_ctc_toolpanel.coneDisplaySize * xScaleModifier,
                              0.001 * mhw_ctc_toolpanel.coneDisplaySize * yScaleModifier,
                              0.001 * mhw_ctc_toolpanel.coneDisplaySize * zScaleModifier)

        # 隐藏尾骨的角度限制锥体
        lightObj["isLastNode"] = 1
        lightObj.hide_viewport = mhw_ctc_toolpanel.hideLastNodeAngleLimit

    alignChains()
    # 设置姿态模式下被创建链的骨骼的骨骼组颜色
    setChainBoneColor(armatureObj)


def checkConstraintError(obj, pattern, errorDict, boneNameDict):
    constraint = obj.constraints.get("BoneName")
    if constraint:
        if constraint.target not in {None, ""} and constraint.subtarget != "":
            boneName = constraint.subtarget
            if pattern.match(boneName):
                boneID = int(boneName.split("MhBone_")[1])

                # 若骨骼的boneFunction超过了最大限制511，则添加报错
                if boneID > 511:
                    addErrorToDict(errorDict, "IncorrectBoneNameFormat", boneName=boneName)

                # if boneName in boneNameSet:
                #     addErrorToDict(errorDict, "MultipleSameBones", objectName=obj.name)
                # else:
                #     boneNameSet.add(boneName)

                if boneID not in boneNameDict:
                    boneNameDict[boneID] = [obj.name]
                else:
                    boneNameDict[boneID].append(obj.name)
            else:
                # 若骨骼名称不符合MhBone_xxx的格式，则添加报错
                addErrorToDict(errorDict, "IncorrectBoneNameFormat", boneName=boneName)

        else:  # 若node的BoneName约束对象没有指定target或subtarget，则添加报错
            addErrorToDict(errorDict, "InvalidNodeConstraint", objectName=obj.name)
    else:
        # 若node没有BoneName约束对象，则添加报错
        addErrorToDict(errorDict, "NodeHasNoConstraint", objectName=obj.name)


def checkCTCError(objList, errorDict):
    MAX_BONE_FUNCTION = 511
    pattern = re.compile(r'^MhBone_\d{3}$')  # 严格匹配 "MhBone__xxx"
    headerCount = 0
    boneNameDict = {}
    ctcObjDict = {"header": None, "chain": [], "node": []}

    for obj in objList:
        if obj.get("~TYPE", None) == "MHW_CTC_HEADER":
            ctcObjDict["header"] = obj
            headerCount += 1
            if obj.parent != None:  # 若header是其他对象的子级，则添加报错
                addErrorToDict(errorDict, "HeaderHasParent", objectName=obj.name)

        elif obj.get("~TYPE", None) == "MHW_CTC_NODE":
            ctcObjDict["node"].append(obj)
            childFrame = None
            childNode = None
            for child in obj.children:
                if child.get("~TYPE") == "MHW_CTC_NODE":
                    if childNode != None:  # 若node有多个直接子级的node（分叉），则添加报错
                        addErrorToDict(errorDict, "ChainHasBranch", objectName=obj.name)
                    else:
                        childNode = child

                if child.get("~TYPE", None) == "MHW_CTC_NODE_FRAME":
                    if childFrame != None:  # 若node有多个角度限制子级，则添加报错
                        addErrorToDict(errorDict, "NodeHasMoreThanOneFrame", objectName=obj.name)
                    else:
                        childFrame = child

            if childFrame == None:  # 若node没有角度限制子级，则添加报错
                addErrorToDict(errorDict, "NodeHasNoFrame", objectName=obj.name)

            validParentTypeSet = {"MHW_CTC_CHAIN", "MHW_CTC_NODE"}
            if obj.parent != None:
                if obj.parent.get("~TYPE", None) not in validParentTypeSet:
                    # 若node的父级对象不正确，则添加报错
                    addErrorToDict(errorDict, "IncorrectNodeParent", objectName=obj.name)
            else:
                # 若node没有父级对象，则添加报错
                addErrorToDict(errorDict, "IncorrectNodeParent", objectName=obj.name)

            checkConstraintError(obj, pattern, errorDict, boneNameDict)

        elif obj.get("~TYPE", None) == "MHW_CTC_CHAIN":
            ctcObjDict["chain"].append(obj)
            validParentTypeList = ["MHW_CTC_HEADER"]
            if obj.parent != None:
                if obj.parent.get("~TYPE", None) not in validParentTypeList:
                    # 若chain的父级对象不是header，则添加报错
                    addErrorToDict(errorDict, "IncorrectChainParent", objectName=obj.name)
            else:
                # 若chain没有父级对象，则添加报错
                addErrorToDict(errorDict, "IncorrectChainParent", objectName=obj.name)

            validChainGroup = False
            childNode = None
            for child in obj.children:
                if child.get("~TYPE") == "MHW_CTC_NODE":
                    if childNode != None:  # 若chain有多个直接子级的node（分叉），则添加报错
                        addErrorToDict(errorDict, "ChainHasBranch", objectName=obj.name)
                    else:
                        childNode = child

                    for nodeChild in child.children:
                        if nodeChild.get("~TYPE") == "MHW_CTC_NODE":
                            validChainGroup = True

            if not validChainGroup:
                # 若chain没有或只有1个子级node，则添加报错
                addErrorToDict(errorDict, "ChainHasLessThanTwoNodes", objectName=obj.name)

    # 若ctc集合中没有header，则添加报错
    if headerCount == 0:
        addErrorToDict(errorDict, "NoCTCHeader")
    # 若ctc集合中有多个header，则添加报错
    elif headerCount > 1:
        addErrorToDict(errorDict, "MoreThanOneCTCHeader")

    for nameList in boneNameDict.values():
        if len(nameList) > 1:
            for objName in nameList:  # 若有多个node对应相同的骨骼，则添加报错
                addErrorToDict(errorDict, "MultipleSameBones", objectName=objName)

    return errorDict, ctcObjDict