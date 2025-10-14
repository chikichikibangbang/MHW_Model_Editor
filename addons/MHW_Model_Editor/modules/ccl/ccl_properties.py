import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, \
                    FloatVectorProperty, EnumProperty, PointerProperty
from ..common.blender_functions import findTempSpace
from ..ctc.ctc_properties import filterCTCCollection, filterArmature


def update_collisionColor(self, context):
    if "CCLCollisionMat" in bpy.data.materials:
        mat = bpy.data.materials["CCLCollisionMat"]
        mat.diffuse_color = self.collisionColor
        mat.node_tree.nodes[0].inputs["Base Color"].default_value = bpy.context.scene.mhw_ccl_toolpanel.collisionColor
        mat.node_tree.nodes[0].inputs["Alpha"].default_value = bpy.context.scene.mhw_ccl_toolpanel.collisionColor[3]

def update_CollisionNameVis(self, context):
    collisionTypes = [
        "MHW_CCL_SPHERE",
        "MHW_CCL_CAPSULE_START",
        "MHW_CCL_CAPSULE_END"]
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) in collisionTypes:
            obj.show_name = self.showCollisionNames

def update_DrawCollisionsThroughObjects(self, context):
    collisionTypes = [
        "MHW_CCL_SPHERE",
        "MHW_CCL_CAPSULE",
        ]
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) in collisionTypes:
            obj.show_in_front = self.drawCollisionsThroughObjects

def update_DrawCapsuleHandlesThroughObjects(self, context):
    for obj in bpy.data.objects:
        if obj.get("~TYPE",None) == "CCL_CAPSULE_START" or obj.get("~TYPE",None) == "CCL_CAPSULE_END":
            obj.show_in_front = self.drawCapsuleHandlesThroughObjects


def update_CollisionOffset(self, context):
    obj = self.id_data
    if obj.get("~TYPE", None) != "MHW_CCL_CAPSULE":
        obj.location = 0.01 * obj.mhw_ccl_collision.StartColOffset  # * 100
    else:
        for child in obj.children:
            if child.get("~TYPE", None) == "MHW_CCL_CAPSULE_START":
                child.location = 0.01 * obj.mhw_ccl_collision.StartColOffset  # * 100


def update_EndCollisionOffset(self, context):
    obj = self.id_data
    if obj.get("~TYPE", None) != "MHW_CCL_CAPSULE" and obj.get("~TYPE", None) != "MHW_CCL_SPHERE":
        obj.location = 0.01 * obj.mhw_ccl_collision.EndColOffset  # * 100
    else:
        for child in obj.children:
            if child.get("~TYPE", None) == "MHW_CCL_CAPSULE_END":
                child.location = 0.01 * obj.mhw_ccl_collision.EndColOffset  # * 100


def update_CollisionRadius(self, context):
    obj = self.id_data
    if type(obj).__name__ == "Object":  # Check if it's an object to prevent issues with clipboard
        if obj.get("~TYPE", None) != "MHW_CCL_CAPSULE":
            obj.scale = [0.01 * obj.mhw_ccl_collision.ColRadius] * 3
        else:
            for child in obj.children:
                if child.get("~TYPE", None) == "MHW_CCL_CAPSULE_START" or child.get("~TYPE", None) == "MHW_CCL_CAPSULE_END":
                    child.scale = [0.01 * obj.mhw_ccl_collision.ColRadius] * 3

def updateExportCCLCollection(self, context):
    browserSpace = findTempSpace("FileSelectParams")
    if browserSpace and self.exportCTCCollection:
        colName = self.exportCTCCollection.name
        if ".ctc" in colName:
            browserSpace.params.filename = colName.split(".ctc")[0] + ".ccl"

class CCLToolPanelPG(bpy.types.PropertyGroup):
    lastImportCollection: StringProperty(default="")
    lastExportCollection: StringProperty(default="")

    # importCTCCollection: PointerProperty(
    #     name="",
    #     description="Set the ctc collection to merge collision objects with."
    #                 "\nUse this when you want to merge collision objects from different files",
    #     type=bpy.types.Collection,
    #     poll=filterCTCCollection,
    #     # update=updateCTCCollection,
    # )
    exportCTCCollection: PointerProperty(
        name="",
        description="Set the ctc collection to be exported",
        type=bpy.types.Collection,
        poll=filterCTCCollection,
        update=updateExportCCLCollection,
    )
    importCTCArmature: PointerProperty(
        name="",
        description="Set the armature to attach collision objects to."
                    "\nIf uncheck, addon will try to find matching armature automatically."
                    "\nNOTE: If some bones that are used by ccl file are missing, corresponding collision objects won't be imported",
        type=bpy.types.Object,
        poll=filterArmature,
    )

    # 碰撞体颜色
    collisionColor: FloatVectorProperty(
        name="Collision Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.003, 0.426, 0.8, 0.3),
        update=update_collisionColor
    )
    # 是否显示碰撞体名称
    showCollisionNames: BoolProperty(
        name="Show Collision Names",
        description="Show CCL Collision Names in 3D View",
        default=True,
        update=update_CollisionNameVis
    )
    # 是否前置显示碰撞体
    drawCollisionsThroughObjects: BoolProperty(
        name="Draw Collisions Through Objects",
        description="Make all ccl collision objects render through any objects in front of them",
        default=True,
        update=update_DrawCollisionsThroughObjects
    )
    drawCapsuleHandlesThroughObjects: BoolProperty(
        name="Draw Handles Through Objects",
        description="Make all capsule handle objects render through any objects in front of them",
        default=True,
        update=update_DrawCapsuleHandlesThroughObjects
    )

class CCLCollisionPG(bpy.types.PropertyGroup):
    # 完
    StartColOffset: FloatVectorProperty(
        name="Head Offset",
        description="Set position of the head collision object",
        step=10,
        subtype="XYZ",
        update=update_CollisionOffset
    )
    # 完
    EndColOffset: FloatVectorProperty(
        name="Tail Offset",
        description="Set position of the tail collision object",
        step=10,
        subtype="XYZ",
        update=update_EndCollisionOffset
    )
    # 完
    ColRadius: FloatProperty(
        name="Collision Radius",
        description="",
        default=0.00,
        step=10,
        soft_min=0.00,
        update=update_CollisionRadius,
    )


def getCCLCollision(data, targetObj):
    mhw_ccl_collision = targetObj.mhw_ccl_collision

    mhw_ccl_collision.ColRadius = data.ColRadius
    mhw_ccl_collision.StartColOffset = data.StartPos
    mhw_ccl_collision.EndColOffset = data.EndPos

def setCCLCollision(data, targetObj):
    mhw_ccl_collision = targetObj.mhw_ccl_collision

    data.ColRadius = 100 * targetObj.scale[0]
    data.StartPos = 100 * targetObj.location
    data.EndPos = 100 * mhw_ccl_collision.EndColOffset

    if targetObj.get("~TYPE", None) != "MHW_CCL_CAPSULE":
        boneName = targetObj.constraints["BoneName"].subtarget
        boneID = int(boneName.split("MhBone_")[1])
        data.StartID = boneID
        data.EndID = boneID
        data.ColShape = 0
        mhw_ccl_collision.StartColOffset = 100 * targetObj.location
        mhw_ccl_collision.ColRadius = 100 * targetObj.scale[0]
    else:
        data.ColShape = 1
        startCapsule = None
        endCapsule = None

        for child in targetObj.children:
            if child.get("~TYPE", None) == "MHW_CCL_CAPSULE_START":
                startCapsule = child
            elif child.get("~TYPE", None) == "MHW_CCL_CAPSULE_END":
                endCapsule = child

        if startCapsule != None:
            data.ColRadius = 100 * startCapsule.scale[0]
            boneName = startCapsule.constraints["BoneName"].subtarget
            boneID = int(boneName.split("MhBone_")[1])
            data.StartID = boneID
            data.StartPos = 100 * startCapsule.location

            mhw_ccl_collision.StartColOffset = 100 * startCapsule.location
            mhw_ccl_collision.ColRadius = 100 * startCapsule.scale[0]

        if endCapsule != None:
            boneName = endCapsule.constraints["BoneName"].subtarget
            boneID = int(boneName.split("MhBone_")[1])
            data.EndID = boneID
            data.EndPos = 100 * endCapsule.location

            mhw_ccl_collision.EndColOffset = 100 * endCapsule.location

        else:
            data.EndID = data.StarteID
