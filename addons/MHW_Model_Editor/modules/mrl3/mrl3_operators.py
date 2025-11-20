import bpy
import os

from .blender_mod3_mrl3 import importMHWMrl3
# from .blender_mrl3 import buildMrl3
from .mrl3_functions import reindexMaterials
from .mrl3_presets import saveAsPreset, readPresetJSON
from .mrl3_panels import tag_redraw
from ..common.message_functions import raiseWarning, showErrorMessageBox
from ..common.blender_functions import createEmpty, createCollection, getCollection
from bpy.types import Operator
from bpy.props import StringProperty


class WM_OT_Mrl3_CreateMrl3Collection(Operator):
    bl_label = "Create Mrl3 Collection"
    bl_idname = "mhw_mrl3.create_mrl3_collection"
    bl_options = {'UNDO'}
    bl_description = "Create a mrl3 collection for putting mrl3 material objects into.\nNOTE: The name of the collection is not important, you can rename it if you want to"
    collectionName: StringProperty(
        name="Mrl3 Name",
        description="The name of the newly created mrl3 collection.\nUse the same name as the mrl3 file",
        default="f_body026_0000"
    )

    def execute(self, context):
        if self.collectionName.strip() != "":
            # 检查是否有mod3嵌套集合组
            if self.collectionName in bpy.data.collections:
                parentCollection = bpy.data.collections[self.collectionName.strip()]
            else:
                # parentCollection = None
                parentCollection = getCollection(self.collectionName.strip(), makeNew=True)

            mrl3Collection = createCollection(self.collectionName.strip() + ".mrl3", "COLOR_05", "MHW_MRL3_COLLECTION", parentCollection)
            bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection = mrl3Collection

            self.report({"INFO"}, "Created new mrl3 collection.")
            return {'FINISHED'}
        else:
            self.report({"ERROR"}, "Invalid mrl3 collection name.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        # 根据上次导入的mod3集合的名称来修改当前预输入的mrl3集合名称
        mhw_mod3_toolpanel = context.scene.mhw_mod3_toolpanel
        mod3CollectionName = mhw_mod3_toolpanel.get("lastImportCollection")
        if mod3CollectionName != None and ".mod3" in mod3CollectionName:
            self.collectionName = mod3CollectionName.split(".mod3")[0]

        return context.window_manager.invoke_props_dialog(self)

class WM_OT_Mrl3_ReindexMrl3Materials(Operator):
    bl_label = "Reindex Mrl3 Materials"
    bl_description = "Reorders the mrl3 material objects and sets their names to the name set in the custom properties." \
                     "\nThe button will only be triggered if active mrl3 collection exists." \
                     "\nThis is done automatically upon exporting"
    bl_idname = "mhw_mrl3.reindex_mrl3_materials"

    @classmethod
    def poll(self, context):
        return context.scene.mhw_mrl3_toolpanel.mrl3Collection is not None

    def execute(self, context):
        reindexMaterials(bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection)
        self.report({"INFO"},"Reindexed mrl3 material objects.")
        return {'FINISHED'}


# class WM_OT_Mrl3_ApplyMrl3ToMod3Collection(Operator):
#     bl_label = "Apply Active Mrl3 Collection"
#     bl_description = "Applies the active mrl3 collection to the specified mod3 collection." \
#                      "\nThis will remove all materials on the mod3 mesh and rebuild them using the active mrl3 collection." \
#                      "\nTextures will be fetched from the chunk path in the addon preferences"
#     bl_idname = "mhw_mrl3.apply_mrl3"
#
#     def execute(self, context):
#         # reindexMaterials()
#         mhw_mrl3_toolpanel = bpy.context.scene.mhw_mrl3_toolpanel
#         mrl3Collection = mhw_mrl3_toolpanel.mrl3Collection
#         mod3Collection = mhw_mrl3_toolpanel.mod3Collection
#
#         modDir = os.path.realpath(mhw_mrl3_toolpanel.modDirectory) #这里有问题，如果modDirectory为空字符串的话，os.path.realpath会返回当前工作路径
#         # 这里需要检查chunk或nativePC文件夹是否在路径中，使用splitNativesPath函数
#
#         # removedMaterialSet = set()
#         if mrl3Collection != None and mod3Collection != None and os.path.isdir(modDir):
#             mrl3File = buildMrl3(mrl3Collection.name)
#             mod3MaterialDict = dict()
#             for obj in mod3Collection.all_objects:
#                 if obj.type == "MESH" and not obj.get("Mod3ExportExclude"):
#                     materialName = None
#                     # Fix UV map naming so materials work properly on non MHW meshes
#                     if len(obj.data.uv_layers) > 0:
#                         obj.data.uv_layers[0].name = "UVMap0"
#                         if len(obj.data.uv_layers) > 1:
#                             obj.data.uv_layers[1].name = "UVMap1"
#                     if "__" in obj.name:
#                         materialName = obj.name.split("__", 1)[1].split(".")[0]
#                         for material in obj.data.materials:
#                             if material.name.split(".")[0] == materialName: #这里有问题，如果网格有材质槽但是没有赋予材质，那么该材质槽是没有name这个type的
#                                 mod3MaterialDict[materialName] = material
#                         # removedMaterialSet.add(material)
#                     obj.data.materials.clear()
#                     if materialName not in mod3MaterialDict:
#                         if materialName != None:
#                             newMat = bpy.data.materials.new(name=materialName)
#                             newMat.use_nodes = True
#                             obj.data.materials.append(newMat)
#                             mod3MaterialDict[materialName] = newMat
#                         else:
#                             raiseWarning(f"No material in mesh name, cannot apply materials: {obj.name}")
#                     else:
#                         obj.data.materials.append(mod3MaterialDict[materialName])
#
#             importMHWMrl3(mrl3File, mod3MaterialDict, mhw_mrl3_toolpanel.loadUnusedTextures, mhw_mrl3_toolpanel.loadUnusedProps,
#                           mhw_mrl3_toolpanel.useBackfaceCulling, mhw_mrl3_toolpanel.reloadCachedTextures, chunkPath=modDir,
#                           mrl3Path="", arrangeNodes=True)
#             self.report({"INFO"}, "Applied mrl3 to Mod3 collection.")
#         else:
#             self.report({"ERROR"}, "Invalid mod3 or mrl3 collection.")
#         return {'FINISHED'}


class WM_OT_Mrl3_AddPresetMaterial(Operator):
    bl_label = "Add Preset Material"
    bl_description = "Add a new mrl3 material object with current material preset." \
                     "\nThe button will only be triggered if active mrl3 collection exists"
    bl_idname = "mhw_mrl3.add_preset_material"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return context.scene.mhw_mrl3_toolpanel.mrl3Collection is not None

    def execute(self, context):
        enumValue = bpy.context.scene.mhw_mrl3_toolpanel.Mrl3MaterialPresets

        if enumValue != "":
            presetsPath = os.path.join(os.path.dirname(__file__), "MaterialPresets")
            print("Reading Preset: " + enumValue)
            finished = readPresetJSON(os.path.join(presetsPath, enumValue))
        else:
            # finished = False
            showErrorMessageBox("There are currently no presets that can be added.")
            return {'CANCELLED'}

        tag_redraw(bpy.context)

        if finished:
            self.report({"INFO"}, "Added preset material.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}


class WM_OT_Mrl3_SavePreset(Operator):
    bl_label = "Save Selected As Preset"
    bl_idname = "mhw_mrl3.save_selected_as_preset"
    # bl_context = "objectmode"
    bl_description = "Save selected mrl3 material object as a preset for easy reuse and sharing." \
                     "\nThe button will only be triggered if a mrl3 material object is activated." \
                     "\nPresets can be accessed using the \"Open Preset Folder\" button"
    presetName: StringProperty(name="Preset Name", default="newPreset")

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_MRL3_MATERIAL"

    def execute(self, context):
        finished = saveAsPreset(context.active_object, self.presetName)
        if finished:
            self.report({"INFO"}, "Saved mrl3 material preset.")
            return {'FINISHED'}
        else:
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
        # return {'FINISHED'}

class WM_OT_Mrl3_OpenPresetFolder(Operator):
    bl_label = "Open Preset Folder"
    bl_description = "Open the preset folder in File Explorer"
    bl_idname = "mhw_mrl3.open_preset_folder"

    def execute(self, context):
        presetsPath = os.path.join(os.path.dirname(__file__), "MaterialPresets")

        if not os.path.exists(presetsPath):
            try:
                os.makedirs(presetsPath)
            except:
                pass

        os.startfile(presetsPath)
        return {'FINISHED'}


class WM_OT_Mrl3_ReplaceString(Operator):
    bl_label = "Replace String"
    bl_idname = "mhw_mrl3.replace_string"
    bl_options = {'UNDO'}
    bl_description = "Replace certain specific string in the texture path"

    originalString: StringProperty(
        name="Original String",
        description="The original string that needs to be replaced",
        default="",
    )
    replacedString: StringProperty(
        name="Replaced String",
        description="The string after being replaced",
        default="",
    )

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_MRL3_MATERIAL"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        matchString = False

        if self.originalString != "":
            for mapItem in obj.mhw_mrl3_material.mapList_items:
                if self.originalString not in mapItem.value:
                    continue

                matchString = True
                mapItem.value = mapItem.value.replace(self.originalString, self.replacedString)
                # print(mapItem.value)

        if matchString:
            self.report({"INFO"}, f"Replaced string \"{self.originalString}\" to \"{self.replacedString}\".")
        else:
            self.report({"ERROR"}, f"Unable to match the string \"{self.originalString}\".")
        return {'FINISHED'}


