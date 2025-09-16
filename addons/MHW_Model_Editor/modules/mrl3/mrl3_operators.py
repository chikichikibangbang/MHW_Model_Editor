import bpy
import os

from .blender_mod3_mrl3 import importMHWMrl3
from .blender_mrl3 import createMrl3Collection, reindexMaterials, buildMrl3
from ..common.general_function import raiseWarning
from bpy.types import Operator
from bpy.props import StringProperty


class WM_OT_Mrl3_NewMrl3Header(Operator):
    bl_label = "Create Mrl3 Collection"
    bl_idname = "mhw_mrl3.create_mrl3_collection"
    bl_options = {'UNDO'}
    bl_description = "Create an mrl3 collection for putting mrl3 material objects into.\nNOTE: The name of the collection is not important, you can rename it if you want to"
    collectionName: StringProperty(
        name="Mrl3 Name",
        description="The name of the newly created mrl3 collection.\nUse the same name as the mod3 file",
        default="newMrl3"
    )

    def execute(self, context):
        if self.collectionName.strip() != "":
            createMrl3Collection(self.collectionName.strip() + ".mrl3")
            self.report({"INFO"}, "Created new mhw mrl3 collection.")
            return {'FINISHED'}
        else:
            self.report({"ERROR"}, "Invalid mrl3 collection name.")
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

class WM_OT_Mrl3_ReindexMrl3Materials(Operator):
    bl_label = "Reindex Mrl3 Materials"
    bl_description = "Reorders the mrl3 material objects and sets their names to the name set in the custom properties.\nThis is done automatically upon exporting"
    bl_idname = "mhw_mrl3.reindex_mrl3_materials"

    def execute(self, context):
        reindexMaterials(bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection.name)
        self.report({"INFO"},"Reindexed mrl3 material objects.")
        return {'FINISHED'}


class WM_OT_Mrl3_ApplyMrl3ToMod3Collection(Operator):
    bl_label = "Apply Active Mrl3 Collection"
    bl_description = "Applies the active mrl3 collection to the specified mod3 collection." \
                     "\nThis will remove all materials on the mod3 mesh and rebuild them using the active mrl3 collection." \
                     "\nTextures will be fetched from the chunk path in the addon preferences"
    bl_idname = "mhw_mrl3.apply_mrl3"

    def execute(self, context):
        # reindexMaterials()
        mhw_mrl3_toolpanel = bpy.context.scene.mhw_mrl3_toolpanel
        mrl3Collection = mhw_mrl3_toolpanel.mrl3Collection
        mod3Collection = mhw_mrl3_toolpanel.mod3Collection

        modDir = os.path.realpath(mhw_mrl3_toolpanel.modDirectory) #这里有问题，如果modDirectory为空字符串的话，os.path.realpath会返回当前工作路径
        # 这里需要检查chunk或nativePC文件夹是否在路径中，使用splitNativesPath函数

        # removedMaterialSet = set()
        if mrl3Collection != None and mod3Collection != None and os.path.isdir(modDir):
            mrl3File = buildMrl3(mrl3Collection.name)
            mod3MaterialDict = dict()
            for obj in mod3Collection.all_objects:
                if obj.type == "MESH" and not obj.get("Mod3ExportExclude"):
                    materialName = None
                    # Fix UV map naming so materials work properly on non MHW meshes
                    if len(obj.data.uv_layers) > 0:
                        obj.data.uv_layers[0].name = "UVMap0"
                        if len(obj.data.uv_layers) > 1:
                            obj.data.uv_layers[1].name = "UVMap1"
                    if "__" in obj.name:
                        materialName = obj.name.split("__", 1)[1].split(".")[0]
                        for material in obj.data.materials:
                            if material.name.split(".")[0] == materialName: #这里有问题，如果网格有材质槽但是没有赋予材质，那么该材质槽是没有name这个type的
                                mod3MaterialDict[materialName] = material
                        # removedMaterialSet.add(material)
                    obj.data.materials.clear()
                    if materialName not in mod3MaterialDict:
                        if materialName != None:
                            newMat = bpy.data.materials.new(name=materialName)
                            newMat.use_nodes = True
                            obj.data.materials.append(newMat)
                            mod3MaterialDict[materialName] = newMat
                        else:
                            raiseWarning(f"No material in mesh name, cannot apply materials: {obj.name}")
                    else:
                        obj.data.materials.append(mod3MaterialDict[materialName])

            importMHWMrl3(mrl3File, mod3MaterialDict, mhw_mrl3_toolpanel.loadUnusedTextures, mhw_mrl3_toolpanel.loadUnusedProps,
                          mhw_mrl3_toolpanel.useBackfaceCulling, mhw_mrl3_toolpanel.reloadCachedTextures, chunkPath=modDir,
                          mrl3Path="", arrangeNodes=True)
            self.report({"INFO"}, "Applied mrl3 to Mod3 collection.")
        else:
            self.report({"ERROR"}, "Invalid mod3 or mrl3 collection.")
        return {'FINISHED'}

