import os
import re
import bpy
from bpy.types import Scene, Operator

from .blender_ccl import importMHWCCLFile
from ..common.message_functions import showErrorMessageBox
from ..common.blender_functions import lockObjTransforms, getCollection, checkNameUsage, createCurveEmpty, \
    createFakeEmptySphere, createEmpty
from ..ctc.ctc_functions import findHeaderObj
from ..ctc.ctc_properties import getCTCHeader
from ..ctc.file_ctc import FileHeader


from .file_ccl import Collision
from .ccl_functions import alignCollisions
from .ccl_properties import getCCLCollision
from .ccl_nodes import getCCLSphereGeoNodeTree, getCCLCapsuleGeoNodeTree


class WM_OT_CCL_CreateCollisionFromBone(Operator):
    # bl_label = "Create CCL Collision From Bone"
    bl_label = "Create Collision"
    bl_idname = "mhw_ccl.create_collision_from_bone"
    bl_options = {'UNDO'}
    bl_description = "Create new ccl collision objects from selected bone(s)." \
                     "\nThe button will only be triggered if active ctc collection exists." \
                     "\nSelect one bone to create a sphere or two bones to create a capsule"

    @classmethod
    def poll(self, context):
        return context.scene.mhw_ctc_toolpanel.ctcCollection is not None

    def execute(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        mhw_ccl_toolpanel = context.scene.mhw_ccl_toolpanel

        ctcCollection = mhw_ctc_toolpanel.ctcCollection

        headerObj = findHeaderObj(ctcCollection)
        if headerObj == None:
            # 如果当前ctc集合内没有header空物体，则创建新的header空物体
            headerObj = createEmpty(f"CTC_HEADER {ctcCollection.name}", [("~TYPE", "MHW_CTC_HEADER")], None, ctcCollection)
            ctcHeader = FileHeader()
            getCTCHeader(ctcHeader, headerObj)
            lockObjTransforms(headerObj)

        # 若能同时获取到CTC集合和其内的header空物体
        # if ctcCollection != None and headerObj != None:
        # 获取姿态模式选中的骨骼
        selected = bpy.context.selected_pose_bones
        startBone = None
        endBone = None
        shape = "SPHERE"

        if len(selected) == 1:
            startBone = selected[0]

            # 如果选中的骨骼不以MhBone_xxx格式命名，则无法创建碰撞。
            match = re.match(r'^MhBone_\d{3}$', startBone.name)
            if not match:
                showErrorMessageBox("Selected bone(s) must be named with format \"MhBone_xxx\".")
                return {'CANCELLED'}

            shape = "SPHERE"
            valid = True
        elif len(selected) == 2:
            startBone = selected[0]
            endBone = selected[1]

            # 如果选中的骨骼不以MhBone_xxx格式命名，则无法创建碰撞。
            match1 = re.match(r'^MhBone_\d{3}$', startBone.name)
            match2 = re.match(r'^MhBone_\d{3}$', endBone.name)
            if not match1 or not match2:
                showErrorMessageBox("Selected bone(s) must be named with format \"MhBone_xxx\".")
                return {'CANCELLED'}

            shape = "CAPSULE"
            valid = True
        else:
            valid = False

        if not valid:
            showErrorMessageBox("Select one bone to create a sphere or two bones to create a capsule.")
            return {'CANCELLED'}

        # cclName = ctcCollection.name.split(".")[0]
        cclName = ctcCollection.name.replace("ctc", "ccl")
        cclEntryCol = getCollection(f"Collision Entries - {cclName}", ctcCollection, makeNew=False)

        # 检查名称是否已被使用
        currentIndex = 0
        subName = "CCL_" + str(currentIndex).zfill(2)
        while checkNameUsage(subName, checkSubString=True):
            currentIndex += 1
            subName = "CCL_" + str(currentIndex).zfill(2)

        armatureObj = startBone.id_data

        if shape == "SPHERE":
            startName = f"{subName}_{shape} {startBone.name}"
            # name = "CCL_" + str(currentIndex).zfill(2) + "_" + shape + " " + startBone.name
            colSphereObj = createCurveEmpty(startName, [("~TYPE", "MHW_CCL_SPHERE")], headerObj, cclEntryCol, makeNew=True)
            cclCollision = Collision()
            getCCLCollision(cclCollision, colSphereObj)

            colSphereObj.mhw_ccl_collision.StartColOffset = cclCollision.StartPos

            constraint = colSphereObj.constraints.new(type="CHILD_OF")
            constraint.target = armatureObj
            constraint.subtarget = startBone.name
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

        elif shape == "CAPSULE":
            rootName = f"{subName}_{shape} - {startBone.name} > {endBone.name}"
            colCapsuleRootObj = createCurveEmpty(rootName, [("~TYPE", "MHW_CCL_CAPSULE")], headerObj, cclEntryCol, makeNew=True)
            lockObjTransforms(colCapsuleRootObj)
            colCapsuleRootObj.show_in_front = mhw_ccl_toolpanel.drawCollisionsThroughObjects

            cclCollision = Collision()
            getCCLCollision(cclCollision, colCapsuleRootObj)

            startName = f"{subName}_{shape}_HEAD {startBone.name}"
            colCapsuleStartObj = createFakeEmptySphere(startName, [("~TYPE", "MHW_CCL_CAPSULE_START")], colCapsuleRootObj, cclEntryCol)

            colCapsuleStartObj.mhw_ccl_collision.StartColOffset = cclCollision.StartPos

            constraint = colCapsuleStartObj.constraints.new(type="CHILD_OF")
            constraint.target = armatureObj
            constraint.subtarget = startBone.name
            constraint.name = "BoneName"

            constraint.use_scale_x = False
            constraint.use_scale_y = False
            constraint.use_scale_z = False

            colCapsuleStartObj.show_name = mhw_ccl_toolpanel.showCollisionNames
            colCapsuleStartObj.show_in_front = mhw_ccl_toolpanel.drawCapsuleHandlesThroughObjects

            endName = f"{subName}_{shape}_TAIL {endBone.name}"
            colCapsuleEndObj = createFakeEmptySphere(endName, [("~TYPE", "MHW_CCL_CAPSULE_END")], colCapsuleRootObj, cclEntryCol)
            colCapsuleEndObj.mhw_ccl_collision.EndColOffset = cclCollision.EndPos

            constraint = colCapsuleEndObj.constraints.new(type="CHILD_OF")
            constraint.target = armatureObj
            constraint.subtarget = endBone.name
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
        self.report({"INFO"}, "Created ccl collision from bone.")
        # else:
        #     self.report({"ERROR"},
        #                 "Cannot create collision because there is no ctc header object in active ctc collection.")
        return {'FINISHED'}


class WM_OT_CCL_CreateFullBodyCollisions(Operator):
    bl_label = "Create Full Body Collisions"
    bl_idname = "mhw_ccl.create_full_body_collisions"
    bl_options = {'UNDO'}
    bl_description = "Create collisions that covers the full body (only for player models)." \
                     "\nThe button will only be triggered if active ctc collection exists"

    @classmethod
    def poll(self, context):
        return context.scene.mhw_ctc_toolpanel.ctcCollection is not None

    def execute(self, context):
        filePath = os.path.join(os.path.dirname(__file__), "full_body.ccl")
        options = {"targetArmature": bpy.context.active_object}

        print("\033[96m__________________________________\nMHW CCL import started.\033[0m")
        importMHWCCLFile(filePath, options, isNested=True)
        print("\033[92m__________________________________\nMHW CCL import finished.\033[0m")

        self.report({"INFO"}, "Created full body collisions.")
        return {'FINISHED'}
