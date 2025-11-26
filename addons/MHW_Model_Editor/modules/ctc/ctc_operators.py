import os
import re
import bpy
import math
import copy
from bpy.types import Scene, Operator
from mathutils import Matrix,Vector,Quaternion
from bpy.props import BoolProperty, EnumProperty, FloatProperty, IntProperty, StringProperty
from .....common.i18n.i18n import i18n
from ..common.blender_functions import createCollection, getCollection, createEmpty, createCurveEmpty, \
    lockObjTransforms, checkNameUsage, orientVectorPair
from ..common.message_functions import showErrorMessageBox

from .file_ctc import FileHeader, Chain, Node
from .ctc_nodes import getConeGeoNodeTree, getChainMat
from .ctc_presets import saveAsPreset, readPresetJSON
from .ctc_properties import getCTCHeader, getCTCChain, getCTCNode
from .ctc_functions import alignChains, setChainBoneColor, findHeaderObj


def tag_redraw(context, space_type="PROPERTIES", region_type="WINDOW"):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.spaces[0].type == space_type:
                for region in area.regions:
                    if region.type == region_type:
                        region.tag_redraw()

class AndFlags:
    def __init__(self):
        self.flagDict = {}

    def setFlagsFromInt(self,bitFlag):
        for key in self.flagDict:
            self.flagDict[key]["enabled"] = bool(bitFlag & self.flagDict[key]["andFlag"])
            #print(key+" = "+str(self.flagDict[key]["enabled"]))

    def getIntFromFlags(self):
        intValue = 0
        for key in self.flagDict:
            if self.flagDict[key]["enabled"]:
                intValue += self.flagDict[key]["andFlag"]
        return intValue
    def clearFlags(self,bitFlag):
        for key in self.flagDict:
            self.flagDict[key]["enabled"] = False


class WM_OT_CTC_CreateCTCCollection(Operator):
    bl_idname = "mhw_ctc.create_ctc_collection"
    bl_label = "Create CTC Collection"
    bl_options = {'UNDO'}
    bl_description = "Create a ctc collection for putting ctc & ccl objects into." \
                     "\nNote that a ctc header object will also be created, and all ctc & cll objects must be parented to it"

    collectionName: StringProperty(
        name="CTC Name",
        description="The name of the newly created ctc collection.\nUse the same name as the ctc file",
        default="f_body026_0000"
    )

    def execute(self, context: bpy.types.Context):
        if self.collectionName.strip() != "":

            # 检查是否有mod3嵌套集合组
            if self.collectionName in bpy.data.collections:
                parentCollection = bpy.data.collections[self.collectionName.strip()]
            else:
                # parentCollection = None
                parentCollection = getCollection(self.collectionName.strip(), makeNew=True)

            ctcCollection = createCollection(self.collectionName.strip() + ".ctc", "COLOR_02", "MHW_CTC_COLLECTION", parentCollection)
            bpy.context.scene.mhw_ctc_toolpanel.ctcCollection = ctcCollection

            headerObj = createEmpty(f"CTC_HEADER {self.collectionName}.ctc", [("~TYPE", "MHW_CTC_HEADER")], None, ctcCollection)
            ctcHeader = FileHeader()
            getCTCHeader(ctcHeader, headerObj)
            lockObjTransforms(headerObj)
            bpy.context.view_layer.objects.active = headerObj

            self.report({"INFO"}, "Created new ctc collection.")
            return {'FINISHED'}
        else:
            self.report({"ERROR"}, "Invalid ctc collection name.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # 根据上次导入的mod3集合的名称来修改当前预输入的ctc集合名称
        mhw_mod3_toolpanel = context.scene.mhw_mod3_toolpanel
        mod3CollectionName = mhw_mod3_toolpanel.get("lastImportCollection")
        if mod3CollectionName != None and ".mod3" in mod3CollectionName:
            self.collectionName = mod3CollectionName.split(".mod3")[0]

        return context.window_manager.invoke_props_dialog(self)


class WM_OT_CTC_SwitchToPoseMode(Operator):
    bl_label = "Switch To Pose Mode"
    bl_description = "Switch to pose mode to add new ctc chains or ccl collisions"
    bl_idname = "mhw_ctc.switch_to_pose_mode"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            armature = None
            if bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
                armature = bpy.context.active_object
            else:
                for obj in bpy.context.scene.objects:
                    if obj.type == "ARMATURE":
                        armature = obj
                        break
            if armature != None:
                if bpy.context.mode == "OBJECT":
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = armature

                bpy.ops.object.mode_set(mode='POSE')
        except:
            pass
        return {'FINISHED'}

class WM_OT_CTC_SwitchToObjectMode(Operator):
    bl_label = "Switch To Object Mode"
    bl_description = "Switch to object mode to configure ctc chains or ccl collisions"
    bl_idname = "mhw_ctc.switch_to_object_mode"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        return {'FINISHED'}

class WM_OT_CTC_CreateChainFromBone(Operator):
    # bl_label = "Create CTC Chain From Bone"
    bl_label = "Create Chain"
    bl_idname = "mhw_ctc.create_chain_from_bone"
    bl_options = {'UNDO'}
    bl_description = "Create new ctc chain objects starting from the selected bone and ending at the last child bone." \
                     "\nThe button will only be triggered if active ctc collection exists." \
                     "\nBones in a chain must be named with format \"MhBone_xxx\""

    @classmethod
    def poll(self, context):
        return context.scene.mhw_ctc_toolpanel.ctcCollection is not None

    def execute(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel

        ctcCollection = mhw_ctc_toolpanel.ctcCollection

        headerObj = findHeaderObj(ctcCollection)
        if headerObj == None:
            # 如果当前ctc集合内没有header空物体，则创建新的header空物体
            headerObj = createEmpty(f"CTC_HEADER {ctcCollection.name}", [("~TYPE", "MHW_CTC_HEADER")], None,
                                    ctcCollection)
            ctcHeader = FileHeader()
            getCTCHeader(ctcHeader, headerObj)
            lockObjTransforms(headerObj)

        # # 若能同时获取到CTC集合和其内的header空物体
        # if ctcCollection != None and headerObj != None:
        # 获取姿态模式选中的骨骼
        selected = bpy.context.selected_pose_bones
        chainList = []

        if len(selected) == 1:
            startBone = selected[0]
            # 获取头骨骼的所有子级骨骼
            chainList = startBone.children_recursive
            # 将头骨也并入链骨骼名单
            chainList.insert(0, startBone)
            # print(chainList)
        else:
            # 必须只选中头骨以创建链，不选或选中多个骨骼无法创建链。
            showErrorMessageBox(i18n("Select only the chain start bone."))
            return {'CANCELLED'}

        # 如果链骨骼名单只有一个骨骼，也就是只有头骨，那么无法创建链，一个链必须至少有2个骨骼。
        if len(chainList) == 1:
            showErrorMessageBox(i18n("A chain must have at least 2 bones."))
            return {'CANCELLED'}

        # 如果当前链中有某些骨骼不以MhBone_xxx格式命名，则无法创建链。
        for bone in chainList:
            match = re.match(r'^MhBone_\d{3}$', bone.name)
            if not match:
                showErrorMessageBox(i18n("Current chain has some bones that are not named with format \"MhBone_xxx\"."))
                return {'CANCELLED'}

        valid = True
        for bone in chainList:
            if len(bone.children) > 1:
                valid = False
                break
        # 如果当前链中有任何一个骨骼有多个直接子级，则表示链有分叉，则无法创建链。
        if not valid:
            showErrorMessageBox(i18n("Cannot have branching bones in a chain."))
            return {'CANCELLED'}

        ctcEntryCol = getCollection(f"Chain Entries - {ctcCollection.name}", ctcCollection, makeNew=False)

        # 检查名称是否已被使用
        currentIndex = 0
        name = "CTC_CHAIN_" + str(currentIndex).zfill(2)
        while checkNameUsage(name, checkSubString=True):
            currentIndex += 1
            name = "CTC_CHAIN_" + str(currentIndex).zfill(2)

        # 创建chain链体
        name = f"{name} - {chainList[0].name} > {chainList[-1].name}"
        chainObj = createCurveEmpty(name, [("~TYPE", "MHW_CTC_CHAIN")], headerObj, ctcEntryCol, makeNew=True)
        ctcChain = Chain()
        getCTCChain(ctcChain, chainObj)

        # 强制刷新属性值
        chainObj.mhw_ctc_chain.CollisionAttrFlagValue = chainObj.mhw_ctc_chain.CollisionAttrFlagValue
        chainObj.mhw_ctc_chain.ChainAttrFlagValue = chainObj.mhw_ctc_chain.ChainAttrFlagValue
        # lockObjTransforms(chainObj)

        armatureObj = chainList[0].id_data

        boneList = chainList[::-1]  # 反转骨骼列表
        # 设置曲线约束
        constraint = chainObj.constraints.new("COPY_LOCATION")
        constraint.target = armatureObj
        constraint.subtarget = boneList[-1].name

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
            objPos = list((armatureObj.matrix_world @ o.matrix).to_translation())
            objPos.append(0.5)
            p.co = objPos
            h = chainObj.modifiers.new(o.name, 'HOOK')
            h.object = armatureObj
            h.subtarget = o.name
            h.vertex_indices_set([i])

        nodeParent = chainObj
        lightObj = None

        # 获取尾骨编号
        lastBoneIndex = len(chainList) - 1

        for boneIndex, bone in enumerate(chainList):
            # 创建node空物体
            nodeObj = createEmpty(bone.name, [("~TYPE", "MHW_CTC_NODE")], nodeParent, ctcEntryCol)
            ctcNode = Node()
            getCTCNode(ctcNode, nodeObj)
            nodeParent = nodeObj

            # nodeObj.empty_display_size = 2
            nodeObj.empty_display_type = "SPHERE"
            nodeObj.show_name = mhw_ctc_toolpanel.showNodeNames
            nodeObj.show_in_front = mhw_ctc_toolpanel.drawNodesThroughObjects

            # 将链节点约束到对应的骨骼
            constraint = nodeObj.constraints.new(type="COPY_LOCATION")
            constraint.target = armatureObj
            constraint.subtarget = bone.name
            constraint.name = "BoneName"
            constraint = nodeObj.constraints.new(type="COPY_ROTATION")
            constraint.target = armatureObj
            constraint.subtarget = bone.name
            constraint.name = "BoneRotation"
            constraint = nodeObj.constraints.new(type="COPY_SCALE")
            constraint.target = chainObj
            constraint.name = "BoneScale"

            # 创建角度限制空物体
            frame = createEmpty(nodeObj.name + "_ANGLE_LIMIT", [("~TYPE", "MHW_CTC_NODE_FRAME")], nodeObj, ctcEntryCol)
            frame.empty_display_type = "ARROWS"
            frame.empty_display_size = 0.01 * mhw_ctc_toolpanel.angleLimitDisplaySize
            frame.show_in_front = mhw_ctc_toolpanel.drawNodesThroughObjects

            # 更新依赖图
            bpy.context.evaluated_depsgraph_get().update()

            constraint = frame.constraints.new(type="COPY_LOCATION")
            constraint.target = nodeObj
            constraint = frame.constraints.new(type="COPY_SCALE")
            constraint.target = nodeObj

            # 校正角度限制方向
            if boneIndex == lastBoneIndex:  # 若当前骨骼是链的尾骨
                # 定义一个对齐轴，这里选择的是x轴
                axis_align = Vector((1.0, 0.0, 0.0))
                M = orientVectorPair(axis_align, Vector((0.0, 0.0, 0.0)))
            else:
                targetBone = chainList[boneIndex + 1]
                a = armatureObj.matrix_world @ armatureObj.data.bones[bone.name].head_local
                b = armatureObj.matrix_world @ armatureObj.data.bones[targetBone.name].head_local

                # 计算从当前骨骼头部到目标骨骼头部的方向向量，并进行归一化
                direction = (b - a)

                # 修正向量为旋转90度后的结果
                directionCopy = copy.deepcopy(direction)
                direction[0] = directionCopy[0]
                direction[1] = directionCopy[2]
                direction[2] = -directionCopy[1]

                # 定义一个对齐轴，这里选择的是x轴
                axis_align = Vector((1.0, 0.0, 0.0))
                M = orientVectorPair(axis_align, direction)

            # 令框架的本地矩阵等于刚计算出的旋转矩阵
            frame.matrix_local = M.to_4x4()
            frame.rotation_mode = "XYZ"
            frame.location = nodeObj.location
            frame.scale = nodeObj.scale

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

        self.report({"INFO"}, "Created ctc chain from bone.")
        # else:
        #     # self.report({"ERROR"}, "No ctc chain was created because the active ctc collection is not set.")
        #     self.report({"ERROR"}, "Cannot create chain because there is no ctc header object in active ctc collection.")
        return {'FINISHED'}



class WM_OT_CTC_CopyProperties(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_ctc_properties"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy properties from a ctc object." \
                     "\nThe button will only be triggered if a ctc object is activated"

    @classmethod
    def poll(cls, context):
        # return bpy.context.selected_objects != []
        return context.active_object is not None \
            and context.active_object.get("~TYPE", None) in {"MHW_CTC_HEADER", "MHW_CTC_CHAIN", "MHW_CTC_NODE",
                                                             "MHW_CTC_NODE_FRAME"}

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        if ctcObjType == "MHW_CTC_HEADER":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "CTC Header"
            # initialize clipboard entry
            ctcHeader = FileHeader()
            getCTCHeader(ctcHeader, clipboard)
            for key, value in activeObj.mhw_ctc_header.items():
                clipboard.mhw_ctc_header[key] = value
        elif ctcObjType == "MHW_CTC_CHAIN":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "CTC Chain"
            # initialize clipboard entry
            ctcChain = Chain()
            getCTCChain(ctcChain, clipboard)
            for key, value in activeObj.mhw_ctc_chain.items():
                clipboard.mhw_ctc_chain[key] = value
        elif ctcObjType == "MHW_CTC_NODE":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "CTC Node"
            # initialize clipboard entry
            ctcNode = Node()
            getCTCNode(ctcNode, clipboard)
            for key, value in activeObj.mhw_ctc_node.items():
                clipboard.mhw_ctc_node[key] = value
        elif ctcObjType == "MHW_CTC_NODE_FRAME":
            clipboard.ctc_type = ctcObjType
            clipboard.ctc_type_name = "Angle Limit Orientation"
            activeObj.rotation_mode = "XYZ"
            clipboard.frameOrientation = activeObj.rotation_euler
        # else:
        #     showErrorMessageBox("A ctc object must be selected.")
        #     return {'CANCELLED'}

        # 将ctc node的参数类型和名称重新设为默认值
        clipboard.node_prop_type = ""
        clipboard.node_prop_name = ""

        self.report({"INFO"}, "Copied properties of " + clipboard.ctc_type_name.lower() + " object to clipboard.")
        return {'FINISHED'}


class WM_OT_CTC_CopyNode_UnknFlags(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_unknflags"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "UnknFlags"
        clipboard.node_prop_name = "Unkn Flags"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}



class WM_OT_CTC_CopyNode_AngleMode(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_anglemode"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "AngleMode"
        clipboard.node_prop_name = "Angle Mode"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}

class WM_OT_CTC_CopyNode_CollisionShape(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_collisionshape"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "CollisionShape"
        clipboard.node_prop_name = "Collision Shape"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}


class WM_OT_CTC_CopyNode_UnknEnum(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_unknenum"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "unknEnum"
        clipboard.node_prop_name = "Unkn Enum"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}


class WM_OT_CTC_CopyNode_BoneColRadius(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_bonecolradius"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "BoneColRadius"
        clipboard.node_prop_name = "Collision Radius"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}


class WM_OT_CTC_CopyNode_AngleRadius(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_angleradius"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "AngleLimitRadius"
        clipboard.node_prop_name = "Angle Radius"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}


class WM_OT_CTC_CopyNode_WidthRate(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_widthrate"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "WidthRate"
        clipboard.node_prop_name = "Width Rate"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}


class WM_OT_CTC_CopyNode_Mass(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_mass"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "Mass"
        clipboard.node_prop_name = "Mass"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}


class WM_OT_CTC_CopyNode_ElasticCoef(Operator):
    bl_label = "Copy"
    bl_idname = "mhw_ctc.copy_node_elasticcoef"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}
    bl_description = "Copy a specific property from a ctc node object to clipboard"

    def execute(self, context):
        activeObj = bpy.context.active_object
        ctcObjType = activeObj.get("~TYPE", None)
        clipboard = bpy.context.scene.mhw_ctc_clipboard

        clipboard.ctc_type = ctcObjType
        clipboard.ctc_type_name = "CTC Node"
        clipboard.node_prop_type = "ElasticCoef"
        clipboard.node_prop_name = "Elastic Coef"

        # initialize clipboard entry
        ctcNode = Node()
        getCTCNode(ctcNode, clipboard)
        for key, value in activeObj.mhw_ctc_node.items():
            clipboard.mhw_ctc_node[key] = value

        # self.report({"INFO"}, f"Copied properties of {clipboard.ctc_type_name.lower()} object to clipboard.")
        self.report({"INFO"}, f"Copied {clipboard.node_prop_name.lower()} property to clipboard.")
        return {'FINISHED'}



class WM_OT_CTC_PasteCTCProperties(Operator):
    bl_label = "Paste"
    bl_idname = "mhw_ctc.paste_ctc_properties"
    bl_options = {'UNDO'}
    # bl_context = "objectmode"
    bl_description = "Paste properties from a ctc object to selected objects." \
                     "\nSelect at least one ctc object of the same type as the clipboard content to paste"

    @classmethod
    def poll(cls, context):
        return bpy.context.selected_objects != []

    def execute(self, context):
        clipboard = bpy.context.scene.mhw_ctc_clipboard
        # activeObj = bpy.context.active_object

        hasCTCObj = False
        hasEqualObj = False
        for activeObj in bpy.context.selected_objects:
            ctcObjType = activeObj.get("~TYPE", None)
            if ctcObjType not in {"MHW_CTC_HEADER", "MHW_CTC_CHAIN", "MHW_CTC_NODE", "MHW_CTC_NODE_FRAME"}:
                continue

            hasCTCObj = True
            if clipboard.ctc_type != ctcObjType:
                continue

            hasEqualObj = True
            if ctcObjType == "MHW_CTC_HEADER":
                for key, value in clipboard.mhw_ctc_header.items():
                    activeObj.mhw_ctc_header[key] = value
            elif ctcObjType == "MHW_CTC_CHAIN":
                for key, value in clipboard.mhw_ctc_chain.items():
                    activeObj.mhw_ctc_chain[key] = value
            elif ctcObjType == "MHW_CTC_NODE":
                # 添加对ctc node单个特定参数的粘贴功能
                if clipboard.node_prop_type != "":
                    if clipboard.node_prop_type == "UnknFlags":
                        activeObj.mhw_ctc_node["unknByte1"] = clipboard.mhw_ctc_node["unknByte1"]
                        activeObj.mhw_ctc_node["unknByte2"] = clipboard.mhw_ctc_node["unknByte2"]
                    else:
                        activeObj.mhw_ctc_node[clipboard.node_prop_type] = clipboard.mhw_ctc_node[clipboard.node_prop_type]
                else:
                    for key, value in clipboard.mhw_ctc_node.items():
                        activeObj.mhw_ctc_node[key] = value

                # 强制刷新数值
                activeObj.mhw_ctc_node.AngleLimitRadius = activeObj.mhw_ctc_node.AngleLimitRadius
                activeObj.mhw_ctc_node.AngleMode = activeObj.mhw_ctc_node.AngleMode
                activeObj.mhw_ctc_node.BoneColRadius = activeObj.mhw_ctc_node.BoneColRadius
            elif ctcObjType == "MHW_CTC_NODE_FRAME":
                activeObj.rotation_mode = "XYZ"
                activeObj.rotation_euler = clipboard.frameOrientation

        tag_redraw(bpy.context)  # Redraw property panel

        if hasEqualObj:
            if clipboard.node_prop_name != "":
                self.report({"INFO"}, f"Pasted {clipboard.node_prop_name.lower()} property from clipboard.")
            else:
                self.report({"INFO"},
                        "Pasted properties of " + clipboard.ctc_type_name.lower() + " object from clipboard.")
        else:
            if hasCTCObj:
                showErrorMessageBox(i18n("Select at least one ctc object of the same type as the clipboard content to paste."))
            else:
                showErrorMessageBox(i18n("Select at least one ctc object to paste."))
        return {'FINISHED'}


# 隐藏非CTC Chains对象
class WM_OT_CTC_OnlyShowChains(Operator):
    bl_label = "Only Show Chains"
    # bl_description = "Hide all objects that aren't ctc chains to make selecting and configuring them easier." \
    #                  "\nPress the \"Unhide All\" button to unhide"
    bl_description = "Hide other objects and only show ctc chain objects." \
                     "\nPress the \"Show All Objects\" button to recover"
    bl_idname = "mhw_ctc.only_show_chains"
    bl_options = {'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("~TYPE", None) not in {"MHW_CTC_CHAIN", "MHW_CTC_NODE_FRAME_HELPER"}:
                if bpy.context.scene.mhw_ctc_toolpanel.reserveMeshObjects:
                    if obj.type == "MESH":
                        obj.hide_viewport = False
                    else:
                        obj.hide_viewport = True
                else:
                    obj.hide_viewport = True
            else:
                if not obj.get("isLastNode") and bpy.context.scene.mhw_ctc_toolpanel.hideLastNodeAngleLimit:
                    obj.hide_viewport = False
        self.report({"INFO"}, "Hid all non ctc chain objects.")
        return {'FINISHED'}

# 隐藏非CTC Nodes对象
class WM_OT_CTC_OnlyShowNodes(Operator):
    bl_label = "Only Show Nodes"
    # bl_description = "Hide all objects that aren't ctc nodes to make selecting and configuring them easier." \
    #                  "\nPress the \"Unhide All\" button to unhide"
    bl_description = "Hide other objects and only show ctc node objects." \
                     "\nPress the \"Show All Objects\" button to recover"
    bl_idname = "mhw_ctc.only_show_nodes"
    bl_options = {'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("~TYPE",None) not in {"MHW_CTC_NODE", "MHW_CTC_NODE_FRAME_HELPER"}:
                if bpy.context.scene.mhw_ctc_toolpanel.reserveMeshObjects:
                    if obj.type == "MESH":
                        obj.hide_viewport = False
                    else:
                        obj.hide_viewport = True
                else:
                    obj.hide_viewport = True
            else:
                if not obj.get("isLastNode") and bpy.context.scene.mhw_ctc_toolpanel.hideLastNodeAngleLimit:
                    obj.hide_viewport = False
        self.report({"INFO"}, "Hid all non ctc node objects.")
        return {'FINISHED'}

# 隐藏非CCL Collision对象
class WM_OT_CCL_OnlyShowCollisions(Operator):
    bl_label = "Only Show Collisions"
    bl_description = "Hide other objects and only show ccl collision objects." \
                     "\nPress the \"Show All Objects\" button to recover"
    bl_idname = "mhw_ccl.only_show_collisions"
    bl_options = {'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("~TYPE", None) not in {"MHW_CCL_SPHERE", "MHW_CCL_CAPSULE", "MHW_CCL_CAPSULE_START", "MHW_CCL_CAPSULE_END"}:
                if bpy.context.scene.mhw_ctc_toolpanel.reserveMeshObjects:
                    if obj.type == "MESH":
                        obj.hide_viewport = False
                    else:
                        obj.hide_viewport = True
                else:
                    obj.hide_viewport = True
            else:
                obj.hide_viewport = False
        self.report({"INFO"}, "Hid all non ccl collision objects.")
        return {'FINISHED'}

# 隐藏非角度限制坐标轴对象
class WM_OT_CTC_OnlyShowAngleLimits(Operator):
    bl_label = "Only Show Angle Limits"
    bl_description = "Hide other objects and only show angle limit objects." \
                     "\nPress the \"Show All Objects\" button to recover"
    bl_idname = "mhw_ctc.only_show_angle_limits"
    bl_options = {'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("~TYPE", None) not in {"MHW_CTC_NODE_FRAME", "MHW_CTC_NODE_FRAME_HELPER"}:
                if bpy.context.scene.mhw_ctc_toolpanel.reserveMeshObjects:
                    if obj.type == "MESH":
                        obj.hide_viewport = False
                    else:
                        obj.hide_viewport = True
                else:
                    obj.hide_viewport = True
            else:
                if not obj.get("isLastNode") and bpy.context.scene.mhw_ctc_toolpanel.hideLastNodeAngleLimit:
                    obj.hide_viewport = False
        self.report({"INFO"}, "Hid all non angle limit objects.")
        return {'FINISHED'}

# 取消隐藏全部
class WM_OT_CTC_ShowAllObjects(Operator):
    bl_label = "Show All Objects"
    bl_description = "Unhide all objects hidden with above buttons"
    bl_idname = "mhw_ctc.show_all_objects"
    bl_options = {'UNDO'}

    def execute(self, context):
        for obj in bpy.context.scene.objects:
            if obj.get("~TYPE",None) != "MHW_CTC_NODE_FRAME_HELPER":
                obj.hide_viewport = False
            else:
                if bpy.context.scene.mhw_ctc_toolpanel.showAngleLimitCones \
                        and not (obj.get("isLastNode") and bpy.context.scene.mhw_ctc_toolpanel.hideLastNodeAngleLimit):
                    obj.hide_viewport = False
        self.report({"INFO"}, "Unhid all objects.")
        return {'FINISHED'}


class WM_OT_CTC_AlignFrames(Operator):
    bl_label = "Align Angle Limit Direction"
    bl_idname = "mhw_ctc.align_frames"
    bl_description = "Aligns angle limit direction with the next node in the chain." \
                     "\nYou can select one or more ctc chain objects to align." \
                     "\nNote that additional adjustments may be required for the angle limit to work properly"

    # bl_context = "objectmode"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return context.scene.mhw_ctc_toolpanel.ctcCollection is not None

    def execute(self, context):
        chainList = []
        if bpy.context.selected_objects != []:
            for selectedObject in bpy.context.selected_objects:
                if selectedObject.get("~TYPE", None) == "MHW_CTC_CHAIN":
                    for childObject in selectedObject.children:
                        if childObject.get("~TYPE", None) == "MHW_CTC_NODE":
                            currentNode = childObject
                            currentNodeObjList = [childObject]
                            while len(currentNode.children) > 1:
                                for child in currentNode.children:
                                    if child.get("~TYPE", None) == "MHW_CTC_NODE":
                                        currentNodeObjList.append(child)
                                        currentNode = child
                            chainList.append(currentNodeObjList)

        if chainList == []:
            ctcCollection = context.scene.mhw_ctc_toolpanel.ctcCollection
            if ctcCollection != None:
                for selectedObject in ctcCollection.all_objects:
                    if selectedObject.get("~TYPE", None) == "MHW_CTC_CHAIN":
                        for childObject in selectedObject.children:
                            if childObject.get("~TYPE", None) == "MHW_CTC_NODE":
                                currentNode = childObject
                                currentNodeObjList = [childObject]
                                while len(currentNode.children) > 1:
                                    for child in currentNode.children:
                                        if child.get("~TYPE", None) == "MHW_CTC_NODE":
                                            currentNodeObjList.append(child)
                                            currentNode = child
                                chainList.append(currentNodeObjList)

        if chainList != []:
            for chain in chainList:
                lastNodeIndex = len(chain) - 1
                for nodeIndex, node in enumerate(chain):
                    frame = None
                    for child in node.children:
                        if child.get("~TYPE", None) == "MHW_CTC_NODE_FRAME":
                            frame = child

                    armatureObj = node.constraints["BoneName"].target
                    boneName = str(node.constraints["BoneName"].subtarget)

                    # 校正角度限制方向
                    if nodeIndex == lastNodeIndex:  # 若当前骨骼是链的尾骨
                        # 定义一个对齐轴，这里选择的是x轴
                        axis_align = Vector((1.0, 0.0, 0.0))
                        M = orientVectorPair(axis_align, Vector((0.0, 0.0, 0.0)))
                    else:
                        targetBoneName = chain[nodeIndex + 1].constraints["BoneName"].subtarget
                        a = armatureObj.matrix_world @ armatureObj.data.bones[boneName].head_local
                        b = armatureObj.matrix_world @ armatureObj.data.bones[targetBoneName].head_local

                        # 计算从当前骨骼头部到目标骨骼头部的方向向量，并进行归一化
                        direction = (b - a)

                        # 修正向量为旋转90度后的结果
                        directionCopy = copy.deepcopy(direction)
                        direction[0] = directionCopy[0]
                        direction[1] = directionCopy[2]
                        direction[2] = -directionCopy[1]

                        # 定义一个对齐轴，这里选择的是x轴
                        axis_align = Vector((1.0, 0.0, 0.0))
                        M = orientVectorPair(axis_align, direction)

                    if frame != None:
                        # 令框架的本地矩阵等于刚计算出的旋转矩阵
                        frame.matrix_local = M.to_4x4()
                        frame.rotation_mode = "XYZ"
                        frame.location = node.location
                        frame.scale = node.scale

            self.report({"INFO"}, "Aligned angle limit directions.")
            return {'FINISHED'}
        else:
            showErrorMessageBox(i18n("No chains found in selected objects or active ctc collection."))
            return {'CANCELLED'}


class WM_OT_CTC_ApplyAngleLimitRamp(Operator):
    bl_label = "Apply Angle Limit Ramp"
    bl_idname = "mhw_ctc.apply_angle_limit_ramp"
    bl_description = "Apply an increasing angle limit radius on each ctc node as it gets further away." \
                     "\nYou can select one or more ctc chain objects to apply ramp"
    # bl_context = "objectmode"
    bl_options = {'UNDO'}

    maxAngleLimit: FloatProperty(
        name="Max Angle Limit",
        description="The maximum angle limit radius after the max iteration number is reached."
                    "\nFor example, if the max angle limit is 60 and the max iteration is 4, the first node angle limit will be 15, the second will be 30 and so on."
                    "\nOnce the max iteration is reached, all nodes after that will be the max angle limit value",
        default=math.pi/3,
        step=100,
        soft_min=0.0,
        soft_max=180.0,
        subtype="ANGLE",
    )
    maxIteration: IntProperty(
        name="Max Iteration",
        description="The amount of ctc nodes until the angle limit radius is at it's maximum value",
        default=4,
        min=1,
    )

    @classmethod
    def poll(self, context):
        # return context.active_object is not None and context.active_object.get("~TYPE") == "MHW_CTC_CHAIN"
        if not context.selected_objects:
            return False

        for obj in context.selected_objects:
            if obj.get("~TYPE") == "MHW_CTC_CHAIN":
                return True

        return False

    def execute(self, context):
        chainList = []
        for selectedObject in bpy.context.selected_objects:
            if selectedObject.get("~TYPE", None) == "MHW_CTC_CHAIN":
                for childObject in selectedObject.children:
                    if childObject.get("~TYPE", None) == "MHW_CTC_NODE":
                        currentNode = childObject
                        currentNodeObjList = [childObject]
                        while len(currentNode.children) > 1:
                            for child in currentNode.children:
                                if child.get("~TYPE", None) == "MHW_CTC_NODE":
                                    currentNodeObjList.append(child)
                                    currentNode = child
                        chainList.append(currentNodeObjList)

        if chainList != []:
            angleLimitStep = self.maxAngleLimit / self.maxIteration
            for chain in chainList:
                for nodeIndex, node in enumerate(chain):
                    if nodeIndex + 1 < self.maxIteration:
                        node.mhw_ctc_node.AngleLimitRadius = angleLimitStep * (nodeIndex + 1)
                    else:
                        node.mhw_ctc_node.AngleLimitRadius = self.maxAngleLimit
            self.report({"INFO"}, "Applied angle limit ramp to selected ctc chains.")
            return {'FINISHED'}
        else:
            showErrorMessageBox(i18n("Must select one or more ctc chain objects to apply ramp."))
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


def alignBoneDirectionFunc(chainList):
    armatureObj = chainList[0].id_data
    bpy.ops.object.mode_set(mode='OBJECT')

    prevSelection = bpy.context.selected_objects
    for obj in prevSelection:
        obj.select_set(False)

    armatureObj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    armatureObj.select_set(False)

    for obj in prevSelection:
        obj.select_set(True)

    bpy.context.view_layer.objects.active = armatureObj
    bpy.ops.object.mode_set(mode="EDIT")

    for bone in chainList:
        editBone = armatureObj.data.edit_bones[bone.name]
        editBone.use_connect = False  # 断开骨骼连接

    for bone in chainList:
        editBone = armatureObj.data.edit_bones[bone.name]
        boneLength = editBone.length
        tailAddVector = Vector((boneLength, boneLength, boneLength)) * Vector((0.0, 0.0, 1.0))
        editBone.tail = editBone.head + tailAddVector
        editBone.roll = 0

    bpy.ops.object.mode_set(mode="POSE")


class WM_OT_CTC_RenameChainBones(Operator):
    bl_label = "Rename Chain Bones"
    bl_description = "Rename all bones in a chain with format \"MhBone_xxx\"." \
                     "\nIf a ctc chain has been created, all node names in the chain will also be renamed." \
                     "\nCheck button on the right for detailed settings"
    bl_idname = "mhw_ctc.rename_chain_bones"
    # bl_context = "posemode"
    bl_options = {'UNDO'}

    newStartBoneID: IntProperty(
        name="Start Bone ID",
        description="Current chain will be sorted backwards and renamed with the ID entered",
        default=150,
        min=0,
        max=511,
    )

    @classmethod
    def poll(self, context):
        return context.active_object is not None

    def execute(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        ctcCollection = mhw_ctc_toolpanel.ctcCollection
        selected = bpy.context.selected_pose_bones
        chainList = []

        if len(selected) == 1:
            startBone = selected[0]
            # 获取头骨骼的所有子级骨骼
            chainList = startBone.children_recursive
            # 将头骨也并入链骨骼名单
            chainList.insert(0, startBone)
            # print(chainList)
        else:
            # 必须只选中头骨以重命名整条链，不选或选中多个骨骼无法重命名。
            showErrorMessageBox(i18n("Select only the chain start bone."))
            return {'CANCELLED'}

        # 如果链骨骼名单只有一个骨骼，也就是只有头骨，那么无法重命名整条链，一个链必须至少有2个骨骼。
        if len(chainList) == 1:
            showErrorMessageBox(i18n("A chain must have at least 2 bones."))
            return {'CANCELLED'}

        valid = True
        for bone in chainList:
            if len(bone.children) > 1:
                valid = False
                break
        # 如果当前链中有任何一个骨骼有多个直接子级，则表示链有分叉，则无法重命名整条链。
        if not valid:
            showErrorMessageBox(i18n("Cannot have branching bones in a chain."))
            return {'CANCELLED'}

        armatureObj = chainList[0].id_data
        boneNameSet = {b.name for b in armatureObj.data.bones}

        # 首次遍历检查输入的头骨ID值是否会导致骨骼名冲突
        for index, bone in enumerate(chainList):
            newBoneName = "MhBone_" + str(self.newStartBoneID + index).zfill(3)
            if newBoneName in boneNameSet:
                showErrorMessageBox(i18n("Current start ID will result in duplicate bone names. Please select another start ID."))
                return {'CANCELLED'}

        if ctcCollection == None:  # 如果没有指定当前的ctc集合，则只修改骨骼的名称
            for index, bone in enumerate(chainList):
                newBoneName = "MhBone_" + str(self.newStartBoneID + index).zfill(3)
                bone.name = newBoneName
        else:  # 如果指定了当前的ctc集合，则同时修改骨骼名称，以及ctc集合内包含该骨骼名称的所有对象的名称
            targetObjects = [
                obj for obj in ctcCollection.all_objects
                if obj.get("~TYPE", None) in {"MHW_CTC_CHAIN", "MHW_CTC_NODE", "MHW_CTC_NODE_FRAME",
                                              "MHW_CTC_NODE_FRAME_HELPER", "MHW_CCL_SPHERE", "MHW_CCL_CAPSULE",
                                              "MHW_CCL_CAPSULE_START", "MHW_CCL_CAPSULE_END"}
            ]

            for index, bone in enumerate(chainList):
                newBoneName = "MhBone_" + str(self.newStartBoneID + index).zfill(3)

                for obj in targetObjects:
                    if bone.name in obj.name:
                        obj.name = obj.name.replace(bone.name, newBoneName)  # 直接替换匹配的字符串
                bone.name = newBoneName

        # 累加计算下一次重命名应该使用的头骨ID
        self.newStartBoneID += len(chainList)

        # 校正骨骼朝向
        if mhw_ctc_toolpanel.alignBoneDirection:
            alignBoneDirectionFunc(chainList)

        self.report({"INFO"}, "Renamed chain bones.")
        return {'FINISHED'}

    def invoke(self, context, event):
        pattern = re.compile(r'^MhBone_\d{3}$')  # 严格匹配 "MhBone__xxx"
        ctcCollection = context.scene.mhw_ctc_toolpanel.ctcCollection
        armatureObj = bpy.context.active_object
        bones = armatureObj.data.bones

        # 计算当前ctc集合中的node总数量
        self.totalNodeCount = 0
        if ctcCollection:
            self.totalNodeCount = sum(1 for obj in ctcCollection.all_objects if obj.get("~TYPE", None) == "MHW_CTC_NODE")

        self.validBoneCount = 0
        self.unusedBoneIDSet = set(range(150, 200))

        for bone in bones:
            if pattern.match(bone.name):
                boneID = int(bone.name.split("MhBone_")[1])

                # if boneID < 150 or boneID >= 200:
                if boneID not in self.unusedBoneIDSet:
                    continue

                self.validBoneCount += 1
                self.unusedBoneIDSet.remove(boneID)

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        languageCode = bpy.context.preferences.view.language
        ctcCollection = context.scene.mhw_ctc_toolpanel.ctcCollection

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        # row.scale_y = 0.75

        # if languageCode in {"zh_CN", "zh_TW"}:
        #     row.label(text="头骨ID值:")
        # else:
        row.label(text="Start Bone ID:")

        col.separator()

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "newStartBoneID", text="")
        col.separator()

        if ctcCollection != None:
            row = col.row(align=True)
            # row.scale_y = 0.75

            # if languageCode in {"zh_CN", "zh_TW"}:
            #     row.label(text=f"当前集合内的节点数量: {self.totalNodeCount}")
            # else:
            row.label(text=f"{i18n('Count Of Nodes In Collection:')} {self.totalNodeCount}")

        unusedBoneIDList = sorted(self.unusedBoneIDSet)
        row = col.row(align=True)
        # row.scale_y = 0.75

        # if languageCode in {"zh_CN", "zh_TW"}:
        #     row.label(text=f"未使用的ID数量 (150~200): {len(unusedBoneIDList)}")
        # else:
        row.label(text=f"{i18n('Count Of Unused IDs (150~200):')} {len(unusedBoneIDList)}")

        row = col.row(align=True)
        # row.scale_y = 0.75

        # if languageCode in {"zh_CN", "zh_TW"}:
        #     row.label(text="未使用的ID (150~200):")
        # else:
        row.label(text="Unused IDs (150~200):")

        # 每行显示10个ID值
        for i in range(0, len(unusedBoneIDList), 10):
            row = col.row(align=True)
            for boneID in unusedBoneIDList[i:i + 10]:
                row.label(text=str(boneID))

        # 如果不足10个，补空位
        remaining = len(unusedBoneIDList) % 10
        if remaining > 0:
            for _ in range(10 - remaining):
                row.label(text="   ")


class WM_OT_CTC_RenameBoneSettings(Operator):
    bl_label = "Rename Bone Settings"
    bl_description = "Detail settings for renaming chain bones"
    bl_idname = "mhw_ctc.rename_bone_settings"
    # bl_context = "posemode"
    bl_options = {'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def check(self, context):
        # Important for changing options
        return True

    def draw(self, context):
        # box式绘制
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "alignBoneDirection")


'''
# 已知的常见Header AttributeFlags数值
AttrFlagsItems = [
    ("0", "AttrFlags_0", ""),
    ("16", "AttrFlags_16", ""),
    ("64", "AttrFlags_64", ""),
    ("80", "AttrFlags_80", ""),
]

class WM_OT_CTC_SetAttrFlags(Operator):
    bl_label = "Set Attribute Flags"
    bl_description = "Set header attribute flag value from a list of known values"
    bl_idname = "mhw_ctc.set_attr_flags"
    # bl_context = "objectmode"
    bl_options = {'UNDO', 'INTERNAL'}
    AttrFlagsEnum: EnumProperty(
        name="Attribute Flags",
        description="Set Attribute Flags value",
        items=AttrFlagsItems,
        default="64",
    )

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_CTC_HEADER"

    def execute(self, context):
        activeObject = bpy.context.active_object
        if activeObject != None:
            activeObjectType = activeObject.get("~TYPE", None)
            if activeObjectType == "MHW_CTC_HEADER":
                activeObject.mhw_ctc_header.AttributeFlags = int(self.AttrFlagsEnum)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
'''

class CollisionAttrFlags(AndFlags):
    def __init__(self):
        self.flagDict = {
            "None": {"enabled": False, "andFlag": 0},
            "CollisionSelfEnable": {"enabled": False, "andFlag": 2},
            "CollisionModelEnable": {"enabled": False, "andFlag": 4},
            "CollisionVGroundEnable": {"enabled": False, "andFlag": 8},
        }


class WM_OT_CTC_SetCollisionFlags(Operator):
    bl_label = "Set Collision Flags"
    bl_description = "Set flags from a list of detail values"
    bl_idname = "mhw_ctc.set_collision_flags"
    # bl_context = "objectmode"
    bl_options = {'UNDO', 'INTERNAL'}

    # 完
    CollisionSelfEnable: BoolProperty(
        name="Collision Self Enable",
        description="Whether the chain is allowed to collide with other chains",
        default=False,
    )
    # 完
    CollisionModelEnable: BoolProperty(
        name="Collision Model Enable",
        description="Whether the chain is allowed to collide with ccl file",
        default=True,
    )
    # 完
    CollisionVGroundEnable: BoolProperty(
        name="Collision VGround Enable",
        description="Whether the chain is allowed to collide with the ground",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "CollisionSelfEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "CollisionModelEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "CollisionVGroundEnable")

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_CTC_CHAIN"

    def execute(self, context):
        flagClass = CollisionAttrFlags()

        for key in flagClass.flagDict:
            if hasattr(self, key):
                # print(key)
                flagClass.flagDict[key]["enabled"] = getattr(self, key)
        bitFlag = flagClass.getIntFromFlags()

        # 如果选择了多个chain空物体，则一同修改它们的标志数值
        activeObj = bpy.context.active_object
        if activeObj != None:
            activeObjType = activeObj.get("~TYPE", None)
            activeObj.mhw_ctc_chain.CollisionAttrFlagValue = bitFlag

            for selectedObj in bpy.context.selected_objects:
                selectedObjType = selectedObj.get("~TYPE", None)
                if selectedObjType == activeObjType and selectedObjType == "MHW_CTC_CHAIN":
                    selectedObj.mhw_ctc_chain.CollisionAttrFlagValue = bitFlag

            self.report({"INFO"}, "Set collision flags.")
            tag_redraw(bpy.context)
        return {'FINISHED'}

    def invoke(self, context, event):
        flagClass = CollisionAttrFlags()
        flagClass.setFlagsFromInt(context.active_object.mhw_ctc_chain.CollisionAttrFlagValue)

        for key in flagClass.flagDict:
            if hasattr(self, key):
                # print(key)
                setattr(self, key, flagClass.flagDict[key]["enabled"])

        return context.window_manager.invoke_props_dialog(self)


class ChainAttrFlags(AndFlags):
    def __init__(self):
        self.flagDict = {
            "None": {"enabled": False, "andFlag": 0},
            "AngleLimitEnable": {"enabled": False, "andFlag": 1},
            "AngleLimitRestitutionEnable": {"enabled": False, "andFlag": 2},
            "EndRotConstraintEnable": {"enabled": False, "andFlag": 4},
            "TransAnimationEnable": {"enabled": False, "andFlag": 8},
            "AngleFreeEnable": {"enabled": False, "andFlag": 16},
            "StretchBothEnable": {"enabled": False, "andFlag": 32},
            "PartBlendEnable": {"enabled": False, "andFlag": 64},
        }


class WM_OT_CTC_SetChainFlags(Operator):
    bl_label = "Set Chain Flags"
    bl_description = "Set flags from a list of detail values"
    bl_idname = "mhw_ctc.set_chain_flags"
    # bl_context = "objectmode"
    bl_options = {'UNDO', 'INTERNAL'}

    # 完
    AngleLimitEnable: BoolProperty(
        name="Angle Limit Enable",
        description="Whether to enable angle limit.\nUsually recommended to enable it, otherwise angle limit will be invalid",
        default=True,
    )
    # 完
    AngleLimitRestitutionEnable: BoolProperty(
        name="Angle Limit Restitution Enable",
        description="Whether to enable angle limit restitution",
        default=True,
    )
    # 完
    EndRotConstraintEnable: BoolProperty(
        name="End Rot Constraint Enable",
        description="Whether to enable the rotation of end node (uncertain)",
        default=True,
    )
    # 完
    TransAnimationEnable: BoolProperty(
        name="Trans Animation Enable",
        description="Whether to enable trans animation.\nAfter activating, the chain will stagnate in a motion stop posture, but the specific meaning is unclear",
        default=False,
    )
    # 完
    AngleFreeEnable: BoolProperty(
        name="Angle Free Enable",
        description="Whether to enable angle free",
        default=False,
    )
    # 完
    StretchBothEnable: BoolProperty(
        name="Stretch Both Enable",
        description="Whether to enable stretch (uncertain).\nDepends on the mass and elasticity of the nodes",
        default=True,
    )
    # 完
    PartBlendEnable: BoolProperty(
        name="Part Blend Enable",
        description="Whether to enable part blend.\nAfter activating, the chain seems to squeeze towards the center, but the specific meaning is unclear",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "AngleLimitEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "AngleLimitRestitutionEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "EndRotConstraintEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "TransAnimationEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "AngleFreeEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "StretchBothEnable")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "PartBlendEnable")

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_CTC_CHAIN"

    def execute(self, context):
        flagClass = ChainAttrFlags()

        for key in flagClass.flagDict:
            if hasattr(self, key):
                # print(key)
                flagClass.flagDict[key]["enabled"] = getattr(self, key)
        bitFlag = flagClass.getIntFromFlags()

        # 如果选择了多个chain空物体，则一同修改它们的标志数值
        activeObj = bpy.context.active_object
        if activeObj != None:
            activeObjType = activeObj.get("~TYPE", None)
            activeObj.mhw_ctc_chain.ChainAttrFlagValue = bitFlag

            for selectedObj in bpy.context.selected_objects:
                selectedObjType = selectedObj.get("~TYPE", None)
                if selectedObjType == activeObjType and selectedObjType == "MHW_CTC_CHAIN":
                    selectedObj.mhw_ctc_chain.ChainAttrFlagValue = bitFlag

            self.report({"INFO"}, "Set chain flags.")
            tag_redraw(bpy.context)
        return {'FINISHED'}

    def invoke(self, context, event):
        flagClass = ChainAttrFlags()
        flagClass.setFlagsFromInt(context.active_object.mhw_ctc_chain.ChainAttrFlagValue)

        for key in flagClass.flagDict:
            if hasattr(self, key):
                # print(key)
                setattr(self, key, flagClass.flagDict[key]["enabled"])

        return context.window_manager.invoke_props_dialog(self)


class WM_OT_CTC_SavePreset(Operator):
    bl_label = "Save Selected As Preset"
    bl_idname = "mhw_ctc.save_selected_as_preset"
    # bl_context = "objectmode"
    bl_description = "Save selected ctc chain object as a preset for easy reuse and sharing." \
                     "\nThe button will only be triggered if a ctc object is activated." \
                     "\nPresets can be accessed using the \"Open Preset Folder\" button"
    presetName: StringProperty(name="Preset Name", default="newPreset")

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_CTC_CHAIN"

    def execute(self, context):
        finished = saveAsPreset(context.active_object, self.presetName)
        if finished:
            self.report({"INFO"}, "Saved ctc chain preset.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        # return {'FINISHED'}


class WM_OT_CTC_OpenPresetFolder(Operator):
    bl_label = "Open Preset Folder"
    bl_description = "Open the preset folder in File Explorer"
    bl_idname = "mhw_ctc.open_preset_folder"

    def execute(self, context):
        # presetsPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]),"presets")
        presetsPath = os.path.join(os.path.dirname(__file__), "ChainPresets")

        if not os.path.exists(presetsPath):
            try:
                os.makedirs(presetsPath)
            except:
                pass

        os.startfile(presetsPath)
        return {'FINISHED'}

class WM_OT_CTC_ApplyChainPreset(Operator):
    bl_label = "Apply CTC Chain Preset"
    bl_idname = "mhw_ctc.apply_ctc_chain_preset"
    bl_description = "Apply preset to selected ctc chain objects"
    bl_options = {'UNDO', 'INTERNAL'}

    def execute(self, context):
        enumValue = bpy.context.scene.mhw_ctc_toolpanel.CTCChainPresets
        finished = False

        if enumValue != "":
            presetsPath = os.path.join(os.path.dirname(__file__), "ChainPresets")
            print(i18n("Reading Preset: ") + enumValue)

            for activeObj in bpy.context.selected_objects:
                if activeObj.get("~TYPE", None) != "MHW_CTC_CHAIN":
                    continue
                finished = readPresetJSON(os.path.join(presetsPath, enumValue), activeObj)
        else:
            # finished = False
            showErrorMessageBox(i18n("There are currently no presets that can be applied."))
            return {'CANCELLED'}

        tag_redraw(bpy.context)

        if finished:
            self.report({"INFO"}, "Applied ctc chain preset.")
            return {'FINISHED'}
        else:
            showErrorMessageBox(i18n("Must select a ctc chain object (named with \"CTC_CHAIN_XX...\") to apply preset."))
            return {'CANCELLED'}


