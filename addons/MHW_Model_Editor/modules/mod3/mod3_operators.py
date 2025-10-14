# Author: NSA Cloud
import re

import bpy
from bpy.types import Operator
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       )

from ..common.blender_functions import createCollection


class WM_OT_Mod3_CreateMod3Collection(Operator):
    bl_label = "Create Mod3 Collection"
    bl_idname = "mhw_mod3.create_mod3_collection"
    bl_description = "Create a mod3 collection for putting mod3 armature and mesh objects into"
    bl_options = {'UNDO'}

    collectionName: StringProperty(
        name="Mod3 Name",
        description="The name of the newly created mrl3 collection.\nUse the same name as the mod3 file",
        default="f_body026_0000"
    )
    # lodCount: IntProperty(name="LOD Amount",
    #                       description="The amount of lower quality model levels to switch between.\nLeave this at 1 unless you have a set of lower quality models",
    #                       default=1,
    #                       min=1,
    #                       max=8
    #                       )

    def execute(self, context):
        if self.collectionName.strip() != "":
            # 检查是否有mod3嵌套集合组
            if self.collectionName in bpy.data.collections:
                parentCollection = bpy.data.collections[self.collectionName.strip()]
            else:
                parentCollection = None

            mod3Collection = createCollection(self.collectionName.strip() + ".mod3", "COLOR_01", "MHW_MOD3_COLLECTION", parentCollection)
            bpy.context.scene.mhw_mrl3_toolpanel.mod3Collection = mod3Collection

            # TODO 创建LOD集合
            # if self.lodCount > 1:
            #     for i in range(self.lodCount):
            #         lodCollection = bpy.data.collections.new(f"Main Mesh LOD{str(i)} - {collection.name}")
            #         collection.children.link(lodCollection)

            self.report({"INFO"}, "Created new mod3 collection.")
            return {'FINISHED'}
        else:
            self.report({"ERROR"}, "Invalid mod3 collection name.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)



class WM_OT_Mod3_DeleteLoose(Operator):
    bl_label = "Delete Loose Geometry"
    bl_idname = "mhw_mod3.delete_loose"
    bl_description = "Deletes loose vertices and edges with no faces on selected meshes"
    bl_options = {'UNDO'}

    def execute(self, context):
        if context.selected_objects != []:
            selection = context.selected_objects
        else:
            selection = bpy.context.scene.objects
        for selectedObj in selection:
            if selectedObj.type == "MESH":
                context.view_layer.objects.active = selectedObj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                print(f"Deleted loose geometry on {selectedObj.name}")
                bpy.ops.mesh.delete_loose()
                bpy.ops.object.mode_set(mode='OBJECT')
        if context.selected_objects == []:
            self.report({"INFO"}, "Deleted loose geometry on all objects")
        else:
            self.report({"INFO"}, "Deleted loose geometry on selected objects")
        return {'FINISHED'}


class WM_OT_Mod3_RenameMeshToMHWFormat(Operator):
    bl_label = "Rename Meshes"
    bl_idname = "mhw_mod3.rename_meshes"
    bl_description = "Renames selected mesh object(s) to mod3 mesh naming scheme (Example: Group_0_Sub_0__Ch_Pl_Standard_Mt__1)"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True if context.selected_objects else False

    def execute(self, context):
        groupIndexDict = dict()
        meshObjCount = 0

        for obj in context.selected_objects:
            if obj.type != "MESH":  # 跳过非网格类型的对象
                continue

            meshObjCount += 1
            # 尝试解析groupID
            match = re.search(r"Group_(\d+)", obj.name)  # 匹配第一个符合的"Group_数字"
            if match:
                groupID = int(match.group(1))
            else:
                print(f"Could not parse group ID of {obj.name}, setting to 0.")
                groupID = 0

            if groupID not in groupIndexDict:
                groupIndexDict[groupID] = 0

            # 尝试获取材质名
            if obj.data.materials and obj.data.materials[0]:
                materialName = obj.data.materials[0].name.split(".", 1)[0].strip()
            else:
                materialName = "NO_MATERIAL"

            obj.name = f"Group_{str(groupID)}_Sub_{str(groupIndexDict[groupID])}__{materialName}"
            groupIndexDict[groupID] += 1

        if meshObjCount:
            self.report({"INFO"}, f"Renamed {meshObjCount} mesh object(s) to mod3 mesh format.")
        else:
            self.report({"INFO"}, "There are no meshes in selected objects.")
        return {'FINISHED'}


def checkMaxWeight(obj):
    gid_to_maxw = {}

    for g in obj.vertex_groups:
        gid_to_maxw[g.index] = 0

    for v in obj.data.vertices:
        for g in v.groups:
            gid = g.group
            w = obj.vertex_groups[gid].weight(v.index)
            if (gid_to_maxw.get(gid) is None or w > gid_to_maxw[gid]):
                gid_to_maxw[gid] = w

    return gid_to_maxw


class WM_OT_Mod3_RemoveEmptyVertexGroups(Operator):
    bl_label = "Remove Empty Vertex Groups"
    bl_idname = "mhw_mod3.remove_empty_vertex_groups"
    bl_description = "Remove all vertex groups that have no weight assigned to them"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True if context.selected_objects else False

    def execute(self, context):
        meshObjCount = 0

        for obj in context.selected_objects:
            if obj.type != "MESH":  # 跳过非网格类型的对象
                continue

            meshObjCount += 1

            gid_to_maxw = checkMaxWeight(obj)
            wait_to_del_gids = []

            for gid, maxw in gid_to_maxw.items():
                if maxw <= 0:
                    wait_to_del_gids.append(gid)

            wait_to_del_gids = sorted(wait_to_del_gids)[::-1]

            for gid in wait_to_del_gids:
                obj.vertex_groups.remove(obj.vertex_groups[gid])

        if meshObjCount:
            self.report({"INFO"}, f"Removed empty vertex groups on {meshObjCount} mesh object(s).")
        else:
            self.report({"INFO"}, "There are no meshes in selected objects.")
        return {'FINISHED'}


class WM_OT_Mod3_LimitTotalNormalizeAll(Operator):
    bl_label = "Limit Total and Normalize All"
    bl_idname = "mhw_mod3.limit_total_normalize"
    bl_description = "Limits the amount of bones influences per vertex to 8 and normalizes the weights of all vertex groups for all selected meshes"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True if context.selected_objects else False

    def execute(self, context):
        meshObjCount = 0

        for obj in context.selected_objects:
            if obj.type != "MESH":  # 跳过非网格类型的对象
                continue

            meshObjCount += 1

            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

            try:
                bpy.ops.object.vertex_group_limit_total(limit=8)
                bpy.ops.object.vertex_group_normalize_all(lock_active=False)
            except:
                pass

            bpy.ops.object.mode_set(mode='OBJECT')

        if meshObjCount:
            self.report({"INFO"}, f"Limited and normalized weights on {meshObjCount} mesh object(s).")
        else:
            self.report({"INFO"}, "There are no meshes in selected objects.")
        return {'FINISHED'}


