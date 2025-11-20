import re
from mathutils import Vector
import bpy
from bpy.types import Operator
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       IntVectorProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       )

from .mod3_functions import rotateNeg90Matrix
from ..common.blender_functions import createCollection, getCollection, createEmpty, lockObjTransforms
from ..ctc.ctc_properties import getCTCHeader
from ..ctc.file_ctc import FileHeader


class WM_OT_Mod3_CreateMod3Collection(Operator):
    bl_label = "Create Mod3 Collection"
    bl_idname = "mhw_mod3.create_mod3_collection"
    bl_description = "Create a mod3 collection for putting armature and meshes into." \
                     "\nIf you are making armor models, you can use this button." \
                     "\nOtherwise, it is highly recommended to import a mod3 file to inherit the custom properties of the collection"
    bl_options = {'UNDO'}

    collectionName: StringProperty(
        name="Mod3 Name",
        description="The name of the newly created mod3 collection.\nUse the same name as the mod3 file",
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
                # parentCollection = None
                parentCollection = getCollection(self.collectionName.strip(), makeNew=True)

            mod3Collection = createCollection(self.collectionName.strip() + ".mod3", "COLOR_01", "MHW_MOD3_COLLECTION", parentCollection)
            mod3Collection["Mod3_Group_000"] = [0, -20, 0, 90]

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


class WM_OT_Mod3_CreateNestedCollections(Operator):
    bl_label = "Create Nested Collections"
    bl_idname = "mhw_mod3.create_nested_collections"
    bl_description = "Create nested collections containing mod3, mrl3 and ctc collections." \
                     "\nThis will make the collection structure look clearer"
    bl_options = {'UNDO'}

    collectionName: StringProperty(
        name="Collection Name",
        description="The name of the newly created nested collections",
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
            parentCollection = bpy.data.collections.new(self.collectionName.strip())
            bpy.context.scene.collection.children.link(parentCollection)

            mod3Collection = createCollection(self.collectionName.strip() + ".mod3", "COLOR_01", "MHW_MOD3_COLLECTION", parentCollection)
            mod3Collection["Mod3_Group_000"] = [0, -20, 0, 90]
            bpy.context.scene.mhw_mrl3_toolpanel.mod3Collection = mod3Collection

            mrl3Collection = createCollection(self.collectionName.strip() + ".mrl3", "COLOR_05", "MHW_MRL3_COLLECTION", parentCollection)
            bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection = mrl3Collection

            ctcCollection = createCollection(self.collectionName.strip() + ".ctc", "COLOR_02", "MHW_CTC_COLLECTION", parentCollection)
            bpy.context.scene.mhw_ctc_toolpanel.ctcCollection = ctcCollection

            headerObj = createEmpty(f"CTC_HEADER {self.collectionName}.ctc", [("~TYPE", "MHW_CTC_HEADER")], None, ctcCollection)
            ctcHeader = FileHeader()
            getCTCHeader(ctcHeader, headerObj)
            lockObjTransforms(headerObj)
            # bpy.context.view_layer.objects.active = headerObj

            # TODO 创建LOD集合
            # if self.lodCount > 1:
            #     for i in range(self.lodCount):
            #         lodCollection = bpy.data.collections.new(f"Main Mesh LOD{str(i)} - {collection.name}")
            #         collection.children.link(lodCollection)

            self.report({"INFO"}, "Created new nested collections.")
            return {'FINISHED'}
        else:
            self.report({"ERROR"}, "Invalid collection name.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class WM_OT_Mod3_RenameMeshToMHWFormat(Operator):
    bl_label = "Rename Meshes"
    bl_idname = "mhw_mod3.rename_meshes"
    bl_description = "Renames selected meshes to mod3 mesh naming scheme (Example: Group_0_Sub_0__Ch_Pl_Standard_Mt__1)"
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


# class WM_OT_Mod3_SetMeshProperties(Operator):
#     bl_label = "Set Mesh Properties"
#     bl_idname = "mhw_mod3.set_mesh_properties"
#     bl_description = "Set mod3 mesh properties (like shadowFlag and renderMode) on selected meshes." \
#                      "\nIf some meshes don't have properties, they will be automatically added"
#     bl_options = {'UNDO'}
#
#     meshIndex: IntProperty(name="Mesh Index", description="", default=1, min=0, max=65535)
#     shadowFlag: IntProperty(name="Shadow Flag", description="", default=19, min=0, max=65535)
#     renderMode: IntProperty(name="Render Mode", description="", default=195, min=0, max=255)
#     meshUnkn: IntVectorProperty(name="Mesh Unkn", description="", size=4, min=0, max=255, default=(0,0,0,48))
#
#     @classmethod
#     def poll(cls, context):
#         return True if context.selected_objects else False
#
#     def invoke(self, context, event):
#         return context.window_manager.invoke_props_dialog(self)
#
#     def execute(self, context):
#         meshObjs = [obj for obj in context.selected_objects if obj.type == "MESH"]
#
#         for obj in meshObjs:
#             obj.data["Mod3_Mesh_ShadowFlag"] = self.shadowFlag
#             obj.data["Mod3_Mesh_RenderMode"] = self.renderMode
#             obj.data["Mod3_Mesh_Unkn"] = self.meshUnkn
#             obj.data["Mod3_Mesh_Index"] = self.meshIndex
#
#         if meshObjs != []:
#             self.report({"INFO"}, f"Set mesh properties on {len(meshObjs)} mesh object(s).")
#         else:
#             self.report({"INFO"}, "There are no meshes in selected objects.")
#         return {'FINISHED'}


class WM_OT_Mod3_SetMeshGroupID(Operator):
    bl_label = "Set Mesh Group ID"
    bl_idname = "mhw_mod3.set_mesh_group_id"
    bl_description = "Quickly set mesh group ID on selected meshes"
    bl_options = {'UNDO'}

    groupID: IntProperty(name="Group ID", description="", default=0, min=0, max=65535)

    @classmethod
    def poll(cls, context):
        return True if context.selected_objects else False

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        meshObjs = [obj for obj in context.selected_objects if obj.type == "MESH"]
        setCount = 0

        for obj in meshObjs:
            match = re.search(r"(Group_)(\d+)(.*)", obj.name)

            if match:
                # 提取前缀和后缀
                prefix = match.group(1)  # "Group_"
                suffix = match.group(3)  # "_Sub_0__Ch_Pl_Standard_Mt__1"

                obj.name = f"{prefix}{self.groupID}{suffix}"
                setCount += 1
            else:
                print(f"Could not parse group ID of {obj.name}, skipping...")

        if meshObjs != []:
            if setCount:
                self.report({"INFO"}, f"Set group ID {self.groupID} on {setCount} mesh object(s).")
            else:
                self.report({"INFO"}, "There are no meshes that can be parsed group ID.")
        else:
            self.report({"INFO"}, "There are no meshes in selected objects.")
        return {'FINISHED'}



class WM_OT_Mod3_DeleteLooseGeometry(Operator):
    bl_label = "Delete Loose Geometry"
    bl_idname = "mhw_mod3.delete_loose_geometry"
    bl_description = "Deletes loose vertices and edges with no faces on selected meshes"
    bl_options = {'UNDO'}

    @classmethod
    def poll(cls, context):
        return True if context.selected_objects else False

    def execute(self, context):
        meshObjs = [obj for obj in context.selected_objects if obj.type == "MESH"]

        for obj in meshObjs:
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            print(f"Deleted loose geometry on {obj.name}.")
            bpy.ops.mesh.delete_loose()
            bpy.ops.object.mode_set(mode='OBJECT')

        if meshObjs != []:
            self.report({"INFO"}, f"Deleted loose geometry on {len(meshObjs)} mesh object(s).")
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
        meshObjs = [obj for obj in context.selected_objects if obj.type == "MESH"]

        for obj in meshObjs:
            gid_to_maxw = checkMaxWeight(obj)
            wait_to_del_gids = []

            for gid, maxw in gid_to_maxw.items():
                if maxw <= 0:
                    wait_to_del_gids.append(gid)

            wait_to_del_gids = sorted(wait_to_del_gids)[::-1]

            for gid in wait_to_del_gids:
                obj.vertex_groups.remove(obj.vertex_groups[gid])

        if meshObjs != []:
            self.report({"INFO"}, f"Removed empty vertex groups on {len(meshObjs)} mesh object(s).")
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
        meshObjs = [obj for obj in context.selected_objects if obj.type == "MESH"]

        for obj in meshObjs:
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

            try:
                bpy.ops.object.vertex_group_limit_total(limit=8)
                bpy.ops.object.vertex_group_normalize_all(lock_active=False)
            except:
                pass

            bpy.ops.object.mode_set(mode='OBJECT')

        if meshObjs != []:
            self.report({"INFO"}, f"Limited and normalized weights on {len(meshObjs)} mesh object(s).")
        else:
            self.report({"INFO"}, "There are no meshes in selected objects.")
        return {'FINISHED'}


# From https://github.com/Philipp-Seifried/Blender-Normals-To-Vertex-Color
class WM_OT_Mod3_BakeNormalToVertexColor(Operator):
    bl_label = "Bake Normal To Vertex Color"
    bl_idname = "mhw_mod3.bake_normal_to_vertex_color"
    bl_description = "Bakes the world normal to vertex color on selected meshes." \
                     "\nBaked vertex color will be saved in the channel called \"World Space Normal\"." \
                     "\nIf you select too many meshes, this operation may consume a lot of time"
    bl_options = {'UNDO'}

    layer_name: StringProperty(name="Layer Name", description="", default="World Space Normal")
    space_items = (
        ('WORLD', "World", "Normals are encoded in world space"),
        ('LOCAL', "Local", "Normals are encoded in local space"),
    )
    space: EnumProperty(
        name="Space",
        items=space_items,
        default='WORLD',
    )

    swizzle_items = (
        ('+Z', '+Z', '+Z'),
        ('-Z', '-Z', '-Z'),
        ('+Y', '+Y', '+Y'),
        ('-Y', '-Y', '-Y'),
        ('+X', '+X', '+X'),
        ('-X', '-X', '-X'),
    )
    swizzle_x: EnumProperty(
        name="red / x-Axis",
        items=swizzle_items,
        default='+X',
    )
    swizzle_y: EnumProperty(
        name="green / y-Axis",
        items=swizzle_items,
        default='+Y',
    )
    swizzle_z: EnumProperty(
        name="blue / z-Axis",
        items=swizzle_items,
        default='+Z',
    )

    # @classmethod
    # def poll(cls, context):
    #     return (context.mode == 'PAINT_VERTEX')

    @classmethod
    def poll(cls, context):
        return True if context.selected_objects else False

    def swizzle(self, result, vec, index, prop):
        if prop == '+X':
            result[index] = vec[0]
        elif prop == '-X':
            result[index] = -vec[0]
        elif prop == '+Y':
            result[index] = vec[1]
        elif prop == '-Y':
            result[index] = -vec[1]
        elif prop == '+Z':
            result[index] = vec[2]
        elif prop == '-Z':
            result[index] = -vec[2]

    def execute(self, context):
        meshObjs = [obj for obj in context.selected_objects if obj.type == "MESH"]

        for obj in meshObjs:
            meshData = obj.data

            color_layer = meshData.vertex_colors.get(self.layer_name)  # 先尝试获取指定名称的顶点色通道
            if not color_layer:  # 如果获取不到指定名称的通道，则新建一个顶点色通道
                color_layer = meshData.vertex_colors.new(name=self.layer_name)

            # 较新版本的blender使用obj.data.vertex_colors.new()新建顶点色通道后不会同时激活该通道，所以此处需要强行激活通道
            meshData.vertex_colors.active = color_layer

            # if not meshData.vertex_colors:
            #     meshData.vertex_colors.new(name="World Space Normal")

            # color_layer = meshData.vertex_colors.active

            if bpy.app.version < (4, 0, 0):
                meshData.calc_normals_split()
                meshData.update()

            for poly in meshData.polygons:
                for loop_index in poly.loop_indices:
                    normal = meshData.loops[loop_index].normal.copy()
                    if self.space == 'WORLD':
                        normal = (rotateNeg90Matrix @ obj.matrix_world).to_3x3() @ normal
                        normal.normalize()

                    orig_normal = normal.copy()
                    self.swizzle(normal, orig_normal, 0, self.swizzle_x)
                    self.swizzle(normal, orig_normal, 1, self.swizzle_y)
                    self.swizzle(normal, orig_normal, 2, self.swizzle_z)

                    color = (normal * 0.5) + Vector((0.5,) * 3)
                    color.resize_4d()

                    meshData.vertex_colors.active.data[loop_index].color = color

            if bpy.app.version < (4, 0, 0):
                meshData.free_normals_split()
                meshData.update()

        if meshObjs != []:
            self.report({"INFO"}, f"Baked normal to vertex color on {len(meshObjs)} mesh object(s).")
        else:
            self.report({"INFO"}, "There are no meshes in selected objects.")
        return {'FINISHED'}



