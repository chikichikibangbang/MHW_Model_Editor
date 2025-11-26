import bpy
import math

import numpy as np
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, \
                    FloatVectorProperty, EnumProperty, PointerProperty
from .file_ctc import ColAttrFlag, ChaAttrFlag
from .ctc_presets import reloadPresets
from ..common.blender_functions import findTempSpace


def update_NodeNameVis(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "MHW_CTC_NODE":
            obj.show_name = self.showNodeNames
def update_angleLimitConeVis(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "MHW_CTC_NODE_FRAME_HELPER" and not obj.get("isLastNode"):
            obj.hide_viewport = not self.showAngleLimitCones
def update_DrawChainsThroughObjects(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "MHW_CTC_CHAIN":
            obj.show_in_front = self.drawChainsThroughObjects
def update_DrawNodesThroughObjects(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "MHW_CTC_NODE" or obj.get("~TYPE",None) == "MHW_CTC_NODE_FRAME":
            obj.show_in_front = self.drawNodesThroughObjects
def update_DrawConesThroughObjects(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "MHW_CTC_NODE_FRAME_HELPER":
            obj.show_in_front = self.drawConesThroughObjects
def update_angleLimitSize(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "MHW_CTC_NODE_FRAME":
            obj.empty_display_size = 0.01*self.angleLimitDisplaySize
def update_coneSize(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE", None) == "MHW_CTC_NODE_FRAME_HELPER":

            xScaleModifier = 1.0
            yScaleModifier = 1.0
            zScaleModifier = 1.0

            if obj.parent != None and obj.parent.parent != None and obj.parent.parent.get("~TYPE") == "MHW_CTC_NODE":
                nodeObj = obj.parent.parent
                if nodeObj.mhw_ctc_node.AngleMode == "2":  # AngleMode_LimitHinge
                    zScaleModifier = .01
                elif nodeObj.mhw_ctc_node.AngleMode == "3":  # AngleMode_LimitOval
                    zScaleModifier = nodeObj.mhw_ctc_node.WidthRate
            obj.scale = (0.001*self.coneDisplaySize * xScaleModifier, 0.001*self.coneDisplaySize * yScaleModifier,
                         0.001*self.coneDisplaySize * zScaleModifier)

def update_chainSize(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE", None) == "MHW_CTC_CHAIN" and obj.type == "CURVE":
            obj.data.bevel_depth = 0.001 * self.chainDisplaySize

def update_AngleLimitMode(self, context):
    obj = self.id_data
    if type(obj).__name__ == "Object":
        if obj.get("~TYPE",None) == "MHW_CTC_NODE":
            for child in obj.children:
                if child.get("~TYPE",None) == "MHW_CTC_NODE_FRAME":
                    for frameChild in child.children:
                        if frameChild.get("~TYPE",None) == "MHW_CTC_NODE_FRAME_HELPER":

                            xScaleModifier = 1.0
                            yScaleModifier = 1.0
                            zScaleModifier = 1.0
                            if obj.mhw_ctc_node.AngleMode == "2":  # AngleMode_LimitHinge
                                zScaleModifier = .01
                            elif obj.mhw_ctc_node.AngleMode == "3":  # AngleMode_LimitOval
                                zScaleModifier = obj.mhw_ctc_node.WidthRate
                            frameChild.scale = (0.001*bpy.context.scene.mhw_ctc_toolpanel.coneDisplaySize*xScaleModifier,
                                                0.001*bpy.context.scene.mhw_ctc_toolpanel.coneDisplaySize*yScaleModifier,
                                                0.001*bpy.context.scene.mhw_ctc_toolpanel.coneDisplaySize*zScaleModifier)


def update_AngleLimitRad(self, context):
    obj = self.id_data
    if type(obj).__name__ == "Object":
        if obj.get("~TYPE", None) == "MHW_CTC_NODE":
            for child in obj.children:
                if child.get("~TYPE", None) == "MHW_CTC_NODE_FRAME":
                    for frameChild in child.children:
                        if frameChild.get("~TYPE", None) == "MHW_CTC_NODE_FRAME_HELPER":

                            if "CTCGeometryNodes" in frameChild.modifiers:
                                modifier = frameChild.modifiers["CTCGeometryNodes"]
                                if bpy.app.version < (4, 0, 0):
                                    modifier["Input_0"] = obj.mhw_ctc_node.AngleLimitRadius
                                else:
                                    modifier["Socket_0"] = obj.mhw_ctc_node.AngleLimitRadius
                                modifier.node_group.interface_update(context)
def update_NodeRadius(self, context):
    obj = self.id_data
    if type(obj).__name__ == "Object":
        if obj.mhw_ctc_node.BoneColRadius != 0:
            obj.empty_display_size = 0.01*obj.mhw_ctc_node.BoneColRadius
        else:
            obj.empty_display_size = 0.01

def update_chainColor(self, context):
    if "CTCChainMat" in bpy.data.materials:
        mat = bpy.data.materials["CTCChainMat"]
        mat.diffuse_color = self.chainColor
        mat.node_tree.nodes[0].inputs["Base Color"].default_value = bpy.context.scene.mhw_ctc_toolpanel.chainColor
        mat.node_tree.nodes[0].inputs["Alpha"].default_value = bpy.context.scene.mhw_ctc_toolpanel.chainColor[3]

def update_coneColor(self, context):
    if "CTCConeMat" in bpy.data.materials:
        mat = bpy.data.materials["CTCConeMat"]
        mat.diffuse_color = self.coneColor
        mat.node_tree.nodes[0].inputs["Base Color"].default_value = bpy.context.scene.mhw_ctc_toolpanel.coneColor
        mat.node_tree.nodes[0].inputs["Alpha"].default_value = bpy.context.scene.mhw_ctc_toolpanel.coneColor[3]
def update_RelationLinesVis(self, context):
    bpy.context.space_data.overlay.show_relationship_lines = self.showRelationLines
def update_hideLastNodeAngleLimit(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "MHW_CTC_NODE_FRAME_HELPER" and obj.get("isLastNode"):
            obj.hide_viewport = self.hideLastNodeAngleLimit

'''
ColAttrFlag = ColAttrFlag()
def update_CollisionAttrFlagFromInt(self, context):
    if not self.internal_changingFlagValues:
        try:
            ColAttrFlag.asInt32 = self.CollisionAttrFlagValue
            self.internal_changingFlagValues = True
            for field_name, field_type, _ in ColAttrFlag.flagValues._fields_:
                setattr(self,field_name,abs(getattr(ColAttrFlag.flagValues, field_name)))
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False
def update_IntFromCollisionAttrFlag(self, context):
    if not self.internal_changingFlagValues:
        try:
            ColAttrFlag.asInt32 = 0
            for field in ColAttrFlag.flagValues._fields_:
                fieldName = field[0]
                if fieldName in self:
                    setattr(ColAttrFlag.flagValues, fieldName, getattr(self, fieldName))

            self.internal_changingFlagValues = True
            self.CollisionAttrFlagValue = ColAttrFlag.asInt32
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False
ChaAttrFlag = ChaAttrFlag()
def update_ChainAttrFlagFromInt(self, context):
    if not self.internal_changingFlagValues:
        try:
            ChaAttrFlag.asInt32 = self.ChainAttrFlagValue
            self.internal_changingFlagValues = True
            for field_name, field_type, _ in ChaAttrFlag.flagValues._fields_:
                setattr(self,field_name,abs(getattr(ChaAttrFlag.flagValues, field_name)))
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False

def update_IntFromChainAttrFlag(self, context):
    if not self.internal_changingFlagValues:
        try:
            ChaAttrFlag.asInt32 = 0
            for field in ChaAttrFlag.flagValues._fields_:
                fieldName = field[0]
                if fieldName in self:
                    setattr(ChaAttrFlag.flagValues, fieldName, getattr(self, fieldName))

            self.internal_changingFlagValues = True
            self.ChainAttrFlagValue = ChaAttrFlag.asInt32
            self.internal_changingFlagValues = False
        except:
            self.internal_changingFlagValues = False
'''

def filterCTCCollection(self, collection):
    return True if collection.get("~TYPE") == "MHW_CTC_COLLECTION" else False
def updateExportCTCCollection(self, context):
    browserSpace = findTempSpace("FileSelectParams")
    if browserSpace and self.exportCTCCollection:
        colName = self.exportCTCCollection.name
        if ".ctc" in colName:
            browserSpace.params.filename = colName.split(".ctc")[0] + ".ctc"
def filterArmature(self, object):
    return True if object.type == "ARMATURE" else False

def filterActiveObj(self, object):
    return True if object.get("~TYPE", None) in {"MHW_CTC_HEADER", "MHW_CTC_CHAIN", "MHW_CTC_NODE", "MHW_CCL_SPHERE", "MHW_CCL_CAPSULE"} else False

class CTCToolPanelPG(bpy.types.PropertyGroup):
    lastImportCollection: StringProperty(default="")
    lastExportCollection: StringProperty(default="")

    importCTCCollection: PointerProperty(
        name="",
        description="Set the ctc collection to merge ctc objects with."
                    "\nUse this when you want to merge ctc objects from different files",
        type=bpy.types.Collection,
        poll=filterCTCCollection,
        # update=updateCTCCollection,
    )
    exportCTCCollection: PointerProperty(
        name="",
        description="Set the ctc collection to be exported",
        type=bpy.types.Collection,
        poll=filterCTCCollection,
        update=updateExportCTCCollection,
    )
    importCTCArmature: PointerProperty(
        name="",
        description="Set the armature to attach ctc objects to."
                    "\nIf uncheck, addon will try to find matching armature automatically."
                    "\nNOTE: If some bones that are used by ctc file are missing, corresponding ctc nodes won't be imported",
        type=bpy.types.Object,
        poll=filterArmature,
    )

    # activeObj: PointerProperty(
    #     name="",
    #     description="Set the armature to attach ctc objects to",
    #     type=bpy.types.Object,
    #     poll=filterActiveObj,
    # )
    def getCTCChainPresets(self, context):
        return reloadPresets("ChainPresets")

    CTCChainPresets: EnumProperty(
        name="",
        description="",
        items=getCTCChainPresets
    )
    applyPresetToChildNodes: BoolProperty(
        name="Apply to Child Nodes",
        description="Apply ctc node preset to all nodes that are a child of the selected node",
        default=False
    )
    ctcCollection: PointerProperty(
        name="",
        description="Set the collection containing the ctc file to edit."
                    "\nYou can create a new ctc collection by pressing the \"Create CTC Collection\" button."
                    "\nNote that ccl collision will also be included in the ctc collection",
        type=bpy.types.Collection,
        poll=filterCTCCollection,
        # update=update_ctcCollection
    )
    # # 对应姿态模式下CTC Tools面板的创建链按钮
    # ChainFromBoneLabelName: StringProperty(
    #     name="ChainFromBoneLabelName",
    #     default="Create CTC Chain From Bone",
    # )
    drawChainsThroughObjects: BoolProperty(
        name="Draw Chains Through Objects",
        description="Make all ctc chain objects render through any objects in front of them",
        default=True,
        update=update_DrawChainsThroughObjects
    )
    # 是否显示链节点名称
    showNodeNames: BoolProperty(
        name="Show Node Names",
        description="Show Node Names in 3D View",
        default=True,
        update=update_NodeNameVis
    )
    # 是否前置显示链节点对象
    drawNodesThroughObjects: BoolProperty(
        name="Draw Nodes Through Objects",
        description="Make all ctc node and frame objects render through any objects in front of them",
        default=True,
        update=update_DrawNodesThroughObjects
    )
    # 是否显示角度限制锥体
    showAngleLimitCones: BoolProperty(
        name="Show Cones",
        description="Show Angle Limit Cones in 3D View",
        default=True,
        update=update_angleLimitConeVis
    )
    # 是否前置显示角度限制锥体
    drawConesThroughObjects: BoolProperty(
        name="Draw Cones Through Objects",
        description="Make all angle limit cones render through any objects in front of them",
        default=True,
        update=update_DrawConesThroughObjects
    )
    # 角度限制轴的显示尺寸
    angleLimitDisplaySize: FloatProperty(
        name="Angle Limit Size",
        description="Set the display size of node angle limits",
        default=4.0,
        min=0.0,
        # soft_max=.4,
        # precision=3,
        step=10,
        update=update_angleLimitSize
    )
    # 角度限制锥体显示尺寸
    coneDisplaySize: FloatProperty(
        name="Cone Size",
        description="Set the display size of node angle limit cones",
        default=5.0,
        min=0.0,
        # soft_max=.2,
        # precision=3,
        step=10,
        update=update_coneSize
    )
    chainDisplaySize: FloatProperty(
        name="Chain Size",
        description="Set the thickness of chain lines",
        # default=0.006,
        default=6.0,
        min=0.0,
        # soft_max=.2,
        # precision=3,
        # step=.005,
        step=10,
        update=update_chainSize
    )
    chainColor: FloatVectorProperty(
        name="Chain Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0,0.0,0.0,0.75),
        update=update_chainColor
    )
    # 角度限制锥体的颜色
    coneColor: FloatVectorProperty(
        name="Angle Limit Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.6, 0.0, 0.4),
        update=update_coneColor
    )
    # 显示关系线
    showRelationLines: BoolProperty(
        name="Show Relation Lines",
        description="Show dotted lines indicating object parents.\nNote that this affects all objects, not just ctc objects",
        default=True,
        update=update_RelationLinesVis,
    )
    # 隐藏尾骨的角度限制锥体
    hideLastNodeAngleLimit: BoolProperty(
        name="Hide Last Node Cone",
        description="Hide the last ctc node's angle limit cone.\nThis is because the last node is typically unused and has a dummy rotation value",
        default=True,
        update=update_hideLastNodeAngleLimit,
    )
    alignBoneDirection: BoolProperty(
        name="Align Bone Direction",
        description="Align bones in a vertical and upward direction."
                    "\nNote this operation will apply all transformations of the current armature",
        default=True
    )
    reserveMeshObjects: BoolProperty(
        name="Reserve Mesh Objects",
        description="Reserve mesh objects when hiding other objects",
        default=False
    )


class CTCHeaderPG(bpy.types.PropertyGroup):
    # 完
    AttributeFlags: IntProperty(
        name="Attribute Flags",
        description="Determine certain movement properties of the chain."
                    "\nIt is actually a binary, and the maximum bit may be 8 bits from testing."
                    "\nThe most common value is 64 (mostly seen on armor), followed by 80 (mostly seen on pendants)."
                    "\n80 seems to make the chain move more violently than 64, you can refer to the fluttering pendant."
                    "\nThe main difference lies in the fifth and seventh bits of binary, and it is unclear what these bits mean",
        default=64,
        min=0,
    )
    # 完
    StepTime: FloatProperty(
        name="Step Time",
        description="The time interval between each update of the simulation by the physics engine."
                    "\nSetting the step time to 0.16666 seconds means that the physics engine updates 60 times per second, which matches a frame rate of 60FPS."
                    "\nPlease don't change this value",
        default=1 / 60,
    )
    # 完
    GravityScaling: FloatProperty(
        name="Gravity Scaling",
        description="Multiple of the gravity applied to the chain, Usually 1."
                    "\nWhen the value is negative, the direction of gravity reverses."
                    "\nWhen the value is 0, there is no gravity",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    GlobalDamping: FloatProperty(
        name="Global Damping",
        description="The greater the damping, the greater the resistance, and the slower and more difficult the movement of the chain."
                    "\nThe smaller the damping, the smaller the resistance, and the faster and more flexible the movement of the chain."
                    "\nNormally the damping is 0 or 0.1, shouldn't be set to too high."
                    "\nA negative value will cause the chain to gain additional energy and move automatically",
        default=0.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    GlobalTransForceCoef: FloatProperty(
        name="Global TransForce Coef",
        description="When the value is 1, the trans force is equal to the acting force. This is the usual value."
                    "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
                    "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
                    "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    SpringScaling: FloatProperty(
        name="Spring Scaling",
        description="Multiple of chain elasticity, Usually 1.\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    WindScale: FloatProperty(
        name="Wind Scale",
        description="The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
                    "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
                    "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value",
        default=0.6,
        soft_min=0.0,
    )
    # 完
    WindScaleMin: FloatProperty(
        name="Wind Scale Min",
        description="The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
                    "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
                    "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value",
        default=0.3,
        soft_min=0.0,
    )
    # 完
    WindScaleMax: FloatProperty(
        name="Wind Scale Max",
        description="The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
                    "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
                    "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value",
        default=1.0,
        soft_min=0.0,
    )
    # 完
    WindScaleWeight: FloatVectorProperty(
        name="Wind Scale Weight",
        description="Represents the wind weight (proportion) of each wind section, and the sum of the three values equals 1",
        size=3,
        default=(0.2, 0.7, 0.1),
        soft_min=0.0,
        soft_max=1.0,
    )

# 获取CTC Header数据
def getCTCHeader(data, targetObj):
    mhw_ctc_header = targetObj.mhw_ctc_header
    
    mhw_ctc_header.AttributeFlags = data.AttributeFlags
    mhw_ctc_header.StepTime = data.StepTime

    mhw_ctc_header.GravityScaling = data.GravityScaling
    mhw_ctc_header.GlobalDamping = data.GlobalDamping
    mhw_ctc_header.GlobalTransForceCoef = data.GlobalTransForceCoef
    mhw_ctc_header.SpringScaling = data.SpringScaling

    mhw_ctc_header.WindScale = data.WindScale
    mhw_ctc_header.WindScaleMin = data.WindScaleMin
    mhw_ctc_header.WindScaleMax = data.WindScaleMax
    mhw_ctc_header.WindScaleWeight = data.WindScaleWeight

# 设置CTC Header数据
def setCTCHeader(data, targetObj):
    mhw_ctc_header = targetObj.mhw_ctc_header
    
    data.AttributeFlags = mhw_ctc_header.AttributeFlags
    data.StepTime = mhw_ctc_header.StepTime

    data.GravityScaling = mhw_ctc_header.GravityScaling
    data.GlobalDamping = mhw_ctc_header.GlobalDamping
    data.GlobalTransForceCoef = mhw_ctc_header.GlobalTransForceCoef
    data.SpringScaling = mhw_ctc_header.SpringScaling

    data.WindScale = mhw_ctc_header.WindScale
    data.WindScaleMin = mhw_ctc_header.WindScaleMin
    data.WindScaleMax = mhw_ctc_header.WindScaleMax
    data.WindScaleWeight = mhw_ctc_header.WindScaleWeight


class CTCChainPG(bpy.types.PropertyGroup):
    # # 完
    # internal_changingFlagValues: BoolProperty(
    #     name="Change Flag Values",
    #     description="This value is inaccessible by the user, it is used to determine whether the user changed a value or an update function did so that an infinite loop doesn't happen",
    #     default=False,
    # )
    # 完
    CollisionAttrFlagValue: IntProperty(
        name="Collision Flags",
        # description="Accounting value of all flags.\nChanging this value will change all flags at the same time",
        description="Various attribute flags that define how chain collides",
        default=4,
        min=0,
        max=255,
        # update=update_CollisionAttrFlagFromInt
    )
    '''
    # 完
    CollisionFlags_None: BoolProperty(
        name="CollisionFlags_None",
        description="",
        default=False,
        update=update_IntFromCollisionAttrFlag
    )
    # 完
    CollisionSelfEnable: BoolProperty(
        name="CollisionSelfEnable",
        description="Whether the chain is allowed to collide with other chains",
        default=False,
        update=update_IntFromCollisionAttrFlag
    )
    # 完
    CollisionModelEnable: BoolProperty(
        name="CollisionModelEnable",
        description="Whether the chain is allowed to collide with ccl file",
        default=True,
        update=update_IntFromCollisionAttrFlag
    )
    # 完
    CollisionVGroundEnable: BoolProperty(
        name="CollisionVGroundEnable",
        description="Whether the chain is allowed to collide with the ground",
        default=False,
        update=update_IntFromCollisionAttrFlag
    )
    '''
    # 完
    ChainAttrFlagValue: IntProperty(
        name="Chain Flags",
        # description="Accounting value of all flags.\nChanging this value will change all flags at the same time",
        description="Various attribute flags that define how chain moves",
        default=39,
        min=0,
        max=255,
        # update=update_ChainAttrFlagFromInt
    )
    '''
    # 完
    AngleLimitEnable: BoolProperty(
        name="AngleLimitEnable",
        description="Whether to enable angle limit.\nUsually recommended to enable it, otherwise angle limit will be invalid",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    # 完
    AngleLimitRestitutionEnable: BoolProperty(
        name="AngleLimitRestitutionEnable",
        description="Whether to enable angle limit restitution",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    # 完
    EndRotConstraintEnable: BoolProperty(
        name="EndRotConstraintEnable",
        description="Whether to enable the rotation of end node (uncertain)",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    # 完
    TransAnimationEnable: BoolProperty(
        name="TransAnimationEnable",
        description="Whether to enable trans animation.\nAfter activating, the chain will stagnate in a motion stop posture, but the specific meaning is unclear",
        default=False,
        update=update_IntFromChainAttrFlag
    )
    # 完
    AngleFreeEnable: BoolProperty(
        name="AngleFreeEnable",
        description="Whether to enable angle free",
        default=False,
        update=update_IntFromChainAttrFlag
    )
    # 完
    StretchBothEnable: BoolProperty(
        name="StretchBothEnable",
        description="Whether to enable stretch (uncertain).\nDepends on the mass and elasticity of the nodes",
        default=True,
        update=update_IntFromChainAttrFlag
    )
    # 完
    PartBlendEnable: BoolProperty(
        name="PartBlendEnable",
        description="Whether to enable part blend.\nAfter activating, the chain seems to squeeze towards the center, but the specific meaning is unclear",
        default=False,
        update=update_IntFromChainAttrFlag
    )
    '''
    # 完
    unknAttrFlag1: IntProperty(
        name="Unkn Flag1",
        description="Actually binary. Common values are 0, 1, 17, 32. More testing is needed."
                    "\nTaking 1 for the 1 bits seems to make the chain harder (or recovers faster) than taking 0."
                    "\nTaking 1 for the 2 bits will force the chain to stretch, like a spring",
        default=0,
        min=0,
        max=255,
    )
    # 完
    unknAttrFlag2: IntProperty(
        name="Unkn Flag2",
        description="Actually binary, Usually the value is 0, rarely the value is 1",
        default=0,
        min=0,
        max=255,
    )
    # 完
    ColAttribute: IntProperty(
        name="Collider Attribute",
        description="Usually the value is -1",
        default=-1,
    )
    # 完
    ColGroup: IntProperty(
        name="Collider Group",
        description="Usually the value is 1",
        default=1,
    )
    # 完
    ColType: IntProperty(
        name="Collider Type",
        description="Usually the value is 1",
        default=1,
    )
    # 完
    Gravity: FloatVectorProperty(
        name="Gravity",
        description="Usually only need to change the Y axis gravity."
                    "\nWhen the value is negative, the direction of gravity reverses. When the value is 0, there is no gravity."
                    "\n\"Gravity Scaling\" with the header part can be viewed as a multiplier, so when both values are negative, the actual direction of gravity is still downward",
        default=(0.0, -9.8, 0.0),
        subtype="XYZ"
    )
    # 完
    Damping: FloatProperty(
        name="Damping",
        description="The greater the damping, the greater the resistance, and the slower and more difficult the movement of the chain."
                    "\nThe smaller the damping, the smaller the resistance, and the faster and more flexible the movement of the chain."
                    "\nNormally the damping is 0 or 0.1, shouldn't be set to too high."
                    "\nA negative value will cause the chain to gain additional energy and move automatically",
        default=0.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    TransForceCoef: FloatProperty(
        name="TransForce Coef",
        description="If \"Global TransForce\" is 1, it usually should be set to a value less than 1 here."
                    "\nWhen the value is 1, the trans force is equal to the acting force. This is the usual value."
                    "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
                    "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
                    "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    SpringCoef: FloatProperty(
        name="Spring Coef",
        description="If \"Spring Scaling\" is 1, it usually should be set to a value less than 1 here, even less than 0.1."
                    "\nThe greater the value, the harder the chain and the less the deformation."
                    "\nThe smaller the value, the softer the chain and the greater the deformation."
                    "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior",
        default=0.01,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    LimitForce: FloatProperty(
        name="Limit Force",
        description="Usually the value is 1.0",
        default=1.0,
    )
    # 完
    FrictionCoef: FloatProperty(
        name="Friction Coef",
        description="Usually the value is 0",
        default=0.0,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    ReflectCoef: FloatProperty(
        name="Reflect Coef",
        description="Usually the value is 0.1",
        default=0.1,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    WindRate: FloatProperty(
        name="Wind Rate",
        description="",
        default=0.1,
        soft_min=0.0,
        soft_max=1.0,
    )
    # 完
    WindLimit: IntProperty(
        name="Wind Limit",
        description="There is a hidden variable in memory called \"UseWindLimit\"."
                    "\nWhen the value here is a negative integer, UseWindLimit = 50."
                    "\nWhen the value here is a positive integer, UseWindLimit = WindLimit."
                    "\nOnly seen taking 10 in a few ctc files, so you can just default to -1",
        default=-1,
    )


def getCTCChain(data, targetObj):
    mhw_ctc_chain = targetObj.mhw_ctc_chain

    mhw_ctc_chain.CollisionAttrFlagValue = data.CollisionAttrFlag.asInt32
    mhw_ctc_chain.ChainAttrFlagValue = data.ChainAttrFlag.asInt32
    mhw_ctc_chain.unknAttrFlag1 = data.UnknAttrFlag1
    mhw_ctc_chain.unknAttrFlag2 = data.UnknAttrFlag2

    mhw_ctc_chain.ColAttribute = data.ColAttribute
    mhw_ctc_chain.ColGroup = data.ColGroup
    mhw_ctc_chain.ColType = data.ColType

    mhw_ctc_chain.Gravity = [data.Gravity[0]/100, data.Gravity[1]/100, data.Gravity[2]/100]

    mhw_ctc_chain.Damping = data.Damping
    mhw_ctc_chain.TransForceCoef = data.TransForceCoef
    mhw_ctc_chain.SpringCoef = data.SpringCoef

    mhw_ctc_chain.LimitForce = data.LimitForce / 100
    mhw_ctc_chain.FrictionCoef = data.FrictionCoef
    mhw_ctc_chain.ReflectCoef = data.ReflectCoef

    mhw_ctc_chain.WindRate = data.WindRate
    mhw_ctc_chain.WindLimit = data.WindLimit


def setCTCChain(data, targetObj):
    mhw_ctc_chain = targetObj.mhw_ctc_chain

    data.CollisionAttrFlag.asInt32 = mhw_ctc_chain.CollisionAttrFlagValue
    data.ChainAttrFlag.asInt32 = mhw_ctc_chain.ChainAttrFlagValue
    data.UnknAttrFlag1 = mhw_ctc_chain.unknAttrFlag1
    data.unknAttrFlag2 = mhw_ctc_chain.unknAttrFlag2

    data.ColAttribute = mhw_ctc_chain.ColAttribute
    data.ColGroup = mhw_ctc_chain.ColGroup
    data.ColType = mhw_ctc_chain.ColType

    data.Gravity = mhw_ctc_chain.Gravity * 100

    data.Damping = mhw_ctc_chain.Damping
    data.TransForceCoef = mhw_ctc_chain.TransForceCoef
    data.SpringCoef = mhw_ctc_chain.SpringCoef

    data.LimitForce = mhw_ctc_chain.LimitForce * 100
    data.FrictionCoef = mhw_ctc_chain.FrictionCoef
    data.ReflectCoef = mhw_ctc_chain.ReflectCoef

    data.WindRate = mhw_ctc_chain.WindRate
    data.WindLimit = mhw_ctc_chain.WindLimit


class CTCNodePG(bpy.types.PropertyGroup):
    # 完
    unknByte1: IntProperty(
        name="Unkn Flag1",
        description="Maybe actually binary, default to 0",
        default=0,
        min=0,
        max=255,
    )
    # 完
    unknByte2: IntProperty(
        name="Unkn Flag2",
        description="Maybe actually binary or boolean.\nTaking 1 may make the node more compact than taking 0 (uncertain).\nThe default is 0",
        default=0,
        min=0,
        max=255,
    )
    # 完
    AngleMode: EnumProperty(
        name="Angle Mode",
        description="",
        items=[("0", "Free", "Node will rotate in any direction"),
               ("1", "Cone", "Rotation of node will be limited to a cone"),
               ("2", "Hinge", "Rotation of node will be limited to rotation only along the z-axis"),
               ("3", "Oval", "Rotation of node will be limited to an oval cone"),
               ],
        update=update_AngleLimitMode,
        default=1,
    )
    # 完
    CollisionShape: EnumProperty(
        name="Collision Shape",
        description="",
        items=[("0", "None", "No Collision"),
               ("1", "Sphere", "The shape of collision is a sphere"),
               ("2", "Capsule", "The shape of collision is a capsule"),
               ],
        default=1,
    )
    # 完
    unknEnum: EnumProperty(
        name="Unkn Enum",
        description="Unknown enumeration, usually 1, but rarely used 0 and 2.\nNormally, you can default to 1",
        items=[("0", "0", ""),
               ("1", "1", ""),
               ("2", "2", ""),
               ],
        default=1,
    )
    # 完
    BoneColRadius: FloatProperty(
        name="Collision Radius",
        description="",
        default=0.0,
        step=10,
        soft_min=0.0,
        update=update_NodeRadius,
    )
    # 完
    AngleLimitRadius: FloatProperty(
        name="Angle Limit Radius",
        description="The amount the node is allowed to rotate from it's angle limit direction."
                    "\nIt is actually in radian, representing the top angle of a cone."
                    "\nThe bottom radius of the cone is used here to represent the top angle, which is incorrect but sufficient to represent the actual size",
        default=math.pi / 4,
        step=100,
        soft_min=0.0,
        soft_max=180.0,
        subtype="ANGLE",
        update=update_AngleLimitRad,
    )
    # 完
    WidthRate: FloatProperty(
        name="Width Rate",
        description="Rate of width to length of oval at the bottom of cone."
                    "\nEffective only when Angle Mode is \"Oval\"."
                    "\nWhen the value is 0, \"Oval\" has the same effect as \"Hinge\"",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
        update=update_AngleLimitMode,
    )
    # 完
    Mass: FloatProperty(
        name="Mass",
        description="Most ctc files default to 1, a few will have values greater than 1 or even around 10, and some will have values less than 1.\nIt is not clear how this parameter works",
        default=1.0,
        soft_min=0.0,
    )
    # 完
    ElasticCoef: FloatProperty(
        name="Elastic Coef",
        description="Note that the elastic coef here is different from the spring coef of chain."
                    "\nThe smaller the elastic coef, the easier the node is to be stretched."
                    "\nThe larger the elastic coef, the more likely the node will be to maintain its original length."
                    "\nChanging this value is not recommended，usually 1, which means that the node always maintains its original length",
        default=1.0,
        soft_min=0.0,
        soft_max=1.0,
    )


def getCTCNode(data, targetObj):
    mhw_ctc_node = targetObj.mhw_ctc_node
    
    mhw_ctc_node.unknByte1 = data.UnknByte1
    mhw_ctc_node.unknByte2 = data.UnknByte2
    mhw_ctc_node.AngleMode = str(data.AngleMode)
    mhw_ctc_node.CollisionShape = str(data.CollisionShape)
    mhw_ctc_node.unknEnum = str(data.UnknEnum)

    mhw_ctc_node.BoneColRadius = data.BoneColRadius
    mhw_ctc_node.AngleLimitRadius = data.AngleLimitRadius
    mhw_ctc_node.WidthRate = data.WidthRate
    mhw_ctc_node.Mass = data.Mass
    mhw_ctc_node.ElasticCoef = data.ElasticCoef


def setCTCNode(data, targetObj):
    mhw_ctc_node = targetObj.mhw_ctc_node
    
    data.UnknByte1 = mhw_ctc_node.unknByte1
    data.UnknByte2 = mhw_ctc_node.unknByte2
    data.AngleMode = int(mhw_ctc_node.AngleMode)
    data.CollisionShape = int(mhw_ctc_node.CollisionShape)
    data.UnknEnum = int(mhw_ctc_node.unknEnum)

    data.BoneColRadius = mhw_ctc_node.BoneColRadius
    data.AngleLimitRadius = mhw_ctc_node.AngleLimitRadius
    data.WidthRate = mhw_ctc_node.WidthRate
    data.Mass = mhw_ctc_node.Mass
    data.ElasticCoef = mhw_ctc_node.ElasticCoef

    if targetObj.parent.get("~TYPE", None) == "MHW_CTC_CHAIN":
        data.IsParent = 1
    else:
        data.IsParent = 0

    frameObj = None
    for child in targetObj.children:
        if child.get("~TYPE", None) == "MHW_CTC_NODE_FRAME":
            frameObj = child
            break

    frameMatrix = np.round(frameObj.matrix_local.normalized().transposed(), 6)
    # frameMatrix[np.abs(frameMatrix) < 1e-6] = 0.0
    data.NodeMatrix.matrix = frameMatrix.tolist()

    boneName = targetObj.constraints["BoneName"].subtarget
    data.BoneFunctionID = int(boneName.split("MhBone_")[1])


class CTCClipboardPG(bpy.types.PropertyGroup):
    ctc_type: StringProperty(default="NONE", options={'HIDDEN'})
    ctc_type_name: StringProperty(default="None", options={'HIDDEN'})

    node_prop_type: StringProperty(default="", options={'HIDDEN'})
    node_prop_name: StringProperty(default="", options={'HIDDEN'})

    mhw_ctc_header: PointerProperty(type=CTCHeaderPG)
    mhw_ctc_chain: PointerProperty(type=CTCChainPG)
    mhw_ctc_node: PointerProperty(type=CTCNodePG)
    frameOrientation: FloatVectorProperty(
        name="Frame Orientation",
        size=3,
        subtype="XYZ"
    )




