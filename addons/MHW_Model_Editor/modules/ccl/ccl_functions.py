import re
import bpy

from ..common.blender_functions import checkNameUsage, createCurveEmpty, lockObjTransforms,createFakeEmptySphere
from .ccl_properties import getCCLCollision
from .ccl_nodes import getCCLCapsuleGeoNodeTree, getCCLSphereGeoNodeTree
from ..common.message_functions import addErrorToDict
from ..ctc.ctc_functions import checkConstraintError


def alignCollisions():
    collisionTypeList = [
        "MHW_CCL_SPHERE",
        "MHW_CCL_CAPSULE",
        ]

    # for collisionObj in [obj for obj in bpy.context.scene.objects if (obj.get("~TYPE",None) in collisionTypeList)] :
    #     if collisionObj.get("~TYPE",None) == "MHW_CCL_SPHERE":
    #         collisionObj.constraints["BoneName"].inverse_matrix = collisionObj.parent.matrix_world.inverted()
    #         collisionObj.mhw_ccl_collision.radius = collisionObj.scale[0]

    for collisionObj in [obj for obj in bpy.context.scene.objects if (obj.get("~TYPE",None) in collisionTypeList)]:
        mhw_ccl_collision = collisionObj.mhw_ccl_collision

        if collisionObj.get("~TYPE",None) == "MHW_CCL_SPHERE":
            if collisionObj.parent != None:
                collisionObj.constraints["BoneName"].inverse_matrix = collisionObj.parent.matrix_world.inverted()
            else:
                collisionObj.constraints["BoneName"].inverse_matrix = ((1.0,0.0,0.0,0.0),(0.0,1.0,0.0,0.0),(0.0,0.0,1.0,0.0),(0.0,0.0,0.0,1.0))
            mhw_ccl_collision.radius = collisionObj.scale[0]
        else:
            for child in collisionObj.children:
                if child.get("~TYPE",None) == "MHW_CCL_CAPSULE_END" or child.get("~TYPE",None) == "MHW_CCL_CAPSULE_START":
                    child.constraints["BoneName"].inverse_matrix = child.parent.matrix_world.inverted()
                    if child["~TYPE"] == "MHW_CCL_CAPSULE_START":
                        mhw_ccl_collision.radius = child.scale[0]

        # 强制刷新
        mhw_ccl_collision.StartColOffset = mhw_ccl_collision.StartColOffset
        mhw_ccl_collision.EndColOffset = mhw_ccl_collision.EndColOffset
    bpy.context.view_layer.update()


def importCollisions(colList, armatureObj, headerObj, cclEntryCol):
    """
    导入从ccl文件读取的碰撞体对象

    colList: 从ccl文件读取的碰撞体列表
    armatureObj: 用于绑定碰撞体的目标骨架对象
    headerObj: ctc集合中的header空物体
    cclEntryCol: 用于放置碰撞体的子集合
    """
    mhw_ccl_toolpanel = bpy.context.scene.mhw_ccl_toolpanel
    currentIndex = 0

    for col in colList:
        # 检查名称是否已被使用
        subName = "CCL_" + str(currentIndex).zfill(2)
        while checkNameUsage(subName, checkSubString=True):
            currentIndex += 1
            subName = "CCL_" + str(currentIndex).zfill(2)

        if col.ColShape != 1:
            shape = "SPHERE"
            startName = f"{subName}_{shape} {col.StartName}"
            colSphereObj = createCurveEmpty(startName, [("~TYPE", "MHW_CCL_SPHERE")], headerObj, cclEntryCol, makeNew=True)
            getCCLCollision(col, colSphereObj)

            colSphereObj.mhw_ccl_collision.StartColOffset = col.StartPos

            constraint = colSphereObj.constraints.new(type="CHILD_OF")
            constraint.target = armatureObj
            constraint.subtarget = col.StartName
            constraint.name = "BoneName"

            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False

            colSphereObj.show_name = mhw_ccl_toolpanel.showCollisionNames
            colSphereObj.show_in_front = mhw_ccl_toolpanel.drawCollisionsThroughObjects

            modifier = colSphereObj.modifiers.new(name="CCLGeometryNodes", type='NODES')
            nodeGroup = getCCLSphereGeoNodeTree()

            if modifier.node_group != None and modifier.node_group.name in bpy.data.node_groups:
                bpy.data.node_groups.remove(modifier.node_group)
            modifier.node_group = nodeGroup

        else:
            shape = "CAPSULE"
            rootName = f"{subName}_{shape} - {col.StartName} > {col.EndName}"
            colCapsuleRootObj = createCurveEmpty(rootName, [("~TYPE", "MHW_CCL_CAPSULE")], headerObj, cclEntryCol,
                                                 makeNew=True)
            lockObjTransforms(colCapsuleRootObj)
            getCCLCollision(col, colCapsuleRootObj)

            colCapsuleRootObj.show_in_front = mhw_ccl_toolpanel.drawCollisionsThroughObjects

            startName = f"{subName}_{shape}_HEAD {col.StartName}"
            colCapsuleStartObj = createFakeEmptySphere(startName, [("~TYPE", "MHW_CCL_CAPSULE_START")],
                                                       colCapsuleRootObj, cclEntryCol)

            colCapsuleStartObj.mhw_ccl_collision.StartColOffset = col.StartPos

            constraint = colCapsuleStartObj.constraints.new(type="CHILD_OF")
            constraint.target = armatureObj
            constraint.subtarget = col.StartName
            constraint.name = "BoneName"

            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False

            colCapsuleStartObj.show_name = mhw_ccl_toolpanel.showCollisionNames
            colCapsuleStartObj.show_in_front = mhw_ccl_toolpanel.drawCapsuleHandlesThroughObjects

            endName = f"{subName}_{shape}_TAIL {col.EndName}"
            colCapsuleEndObj = createFakeEmptySphere(endName, [("~TYPE", "MHW_CCL_CAPSULE_END")], colCapsuleRootObj,
                                                     cclEntryCol)
            colCapsuleEndObj.mhw_ccl_collision.EndColOffset = col.EndPos

            constraint = colCapsuleEndObj.constraints.new(type="CHILD_OF")
            constraint.target = armatureObj
            constraint.subtarget = col.EndName
            constraint.name = "BoneName"

            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False

            constraint2 = colCapsuleEndObj.constraints.new(type="COPY_SCALE")
            constraint2.target = colCapsuleStartObj

            colCapsuleEndObj.show_name = mhw_ccl_toolpanel.showCollisionNames
            colCapsuleEndObj.show_in_front = mhw_ccl_toolpanel.drawCapsuleHandlesThroughObjects

            # 强制刷新
            colCapsuleRootObj.mhw_ccl_collision.ColRadius = colCapsuleRootObj.mhw_ccl_collision.ColRadius

            modifier = colCapsuleRootObj.modifiers.new(name="CCLGeometryNodes", type='NODES')
            nodeGroup = getCCLCapsuleGeoNodeTree()

            if modifier.node_group != None and modifier.node_group.name in bpy.data.node_groups:
                bpy.data.node_groups.remove(modifier.node_group)
            modifier.node_group = nodeGroup

            if bpy.app.version < (4, 0, 0):
                modifier["Input_0"] = colCapsuleStartObj
                modifier["Input_1"] = colCapsuleEndObj
            else:
                modifier["Socket_0"] = colCapsuleStartObj
                modifier["Socket_1"] = colCapsuleEndObj

    alignCollisions()


def checkCCLError(objList, errorDict):
    MAX_BONE_FUNCTION = 511
    pattern = re.compile(r'^MhBone_\d{3}$')  # 严格匹配 "MhBone__xxx"
    boneNameDict = {}
    colObjList = []

    # Check that there is ctc data collection
    # Check that there is only one header
    # Check that all capsule collisions have both ends
    # Check that all ccl objects are parented to the header
    # Check that parenting structure is valid
    # Check that ccl collision objects have valid child of constraints

    for obj in objList:
        if obj.get("~TYPE", None) == "MHW_CCL_SPHERE":
            colObjList.append(obj)
            checkConstraintError(obj, pattern, errorDict, boneNameDict)

        elif obj.get("~TYPE", None) == "MHW_CCL_CAPSULE":
            colObjList.append(obj)

            startCapsule = None
            for child in obj.children:
                if child.get("~TYPE", None) == "MHW_CCL_CAPSULE_START":
                    if startCapsule != None:
                        # 若capsule有多个head，则添加报错
                        addErrorToDict(errorDict, "CapsuleHasMultipleHeads", objectName=obj.name)
                    else:
                        startCapsule = child

            if startCapsule == None:
                # 若capsule没有head，则添加报错
                addErrorToDict(errorDict, "CapsuleHasNoHead", objectName=obj.name)
            else:
                checkConstraintError(startCapsule, pattern, errorDict, boneNameDict)

            endCapsule = None
            for child in obj.children:
                if child.get("~TYPE", None) == "MHW_CCL_CAPSULE_END":
                    if endCapsule != None:
                        # 若capsule有多个tail，则添加报错
                        addErrorToDict(errorDict, "CapsuleHasMultipleTails", objectName=obj.name)
                    else:
                        endCapsule = child

            if endCapsule == None:
                # 若capsule没有tail，则添加报错
                addErrorToDict(errorDict, "CapsuleHasNoTail", objectName=obj.name)
            else:
                checkConstraintError(endCapsule, pattern, errorDict, boneNameDict)

    return errorDict, colObjList