import bpy
import os
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty
from bpy.types import Operator, OperatorFileListElement
from ..common.general_function import textColors, raiseWarning, splitNativesPath
from ...config import __addon_name__
from .blender_mod3 import importMHWMod3File, exportMHWMod3File


def filterExportMod3Collection(self, collection):
    return True if collection.get("~TYPE") == "MHW_MOD3_COLLECTION" else False
def filterExportMrl3Collection(self, collection):
    return True if collection.get("~TYPE") == "MHW_MRL3_COLLECTION" else False

def updateExportCollection(self,context):
    temp = bpy.data.screens.get("temp")
    browserSpace = None
    if temp != None:
        for area in temp.areas:
            for space in area.spaces:
                try:
                    if type(space.params).__name__ == "FileSelectParams":
                        browserSpace = space
                        break
                except:
                    pass
    if browserSpace != None:
        if self.targetMod3Collection:
            if ".mod3" in self.targetMod3Collection.name:
                browserSpace.params.filename = self.targetMod3Collection.name.split(".mod3")[0]+".mod3"
            # elif ".mrl3" in self.targetMrl3Collection.name:
            #     browserSpace.params.filename = self.targetMrl3Collection.name.split(".mrl3")[0] + ".mrl3"

class MHWExportCollectionPG(bpy.types.PropertyGroup):
    targetMod3Collection: PointerProperty(
        name="",
        description="Set the mod3 collection to be exported",
        type=bpy.types.Collection,
        poll=filterExportMod3Collection,
        update=updateExportCollection,
    )
    targetMrl3Collection: PointerProperty(
        name="",
        description="Set the mrl3 collection to be exported",
        type=bpy.types.Collection,
        poll=filterExportMrl3Collection,
        update=updateExportCollection,
    )

# Used to circumvent the issue of properties not being able to used as defaults for other properties at startup
def setMod3ImportDefaults(self):
    self.clearScene = bpy.context.preferences.addons[__addon_name__].preferences.default_clearScene
    self.loadMaterials = bpy.context.preferences.addons[__addon_name__].preferences.default_loadMaterials
    self.loadMrl3Data = bpy.context.preferences.addons[__addon_name__].preferences.default_loadMrl3Data
    self.loadUnusedTextures = bpy.context.preferences.addons[__addon_name__].preferences.default_loadUnusedTextures
    self.loadUnusedProps = bpy.context.preferences.addons[__addon_name__].preferences.default_loadUnusedProps
    self.useBackfaceCulling = bpy.context.preferences.addons[__addon_name__].preferences.default_useBackfaceCulling
    self.reloadCachedTextures = bpy.context.preferences.addons[__addon_name__].preferences.default_reloadCachedTextures
    self.createCollections = bpy.context.preferences.addons[__addon_name__].preferences.default_createCollections
    self.importArmatureOnly = bpy.context.preferences.addons[__addon_name__].preferences.default_importArmatureOnly
    self.importAllLODs = bpy.context.preferences.addons[__addon_name__].preferences.default_importAllLODs

    self.importBoundingBoxes = bpy.context.preferences.addons[__addon_name__].preferences.default_importBoundingBoxes

    self.default_ArmatureDisplayType = bpy.context.preferences.addons[__addon_name__].preferences.default_ArmatureDisplayType
    self.default_BonesDisplaySize = bpy.context.preferences.addons[__addon_name__].preferences.default_BonesDisplaySize

def setMod3ExportDefaults(self):
    self.selectedOnly = bpy.context.preferences.addons[__addon_name__].preferences.default_selectedOnly
    self.visibleOnly = bpy.context.preferences.addons[__addon_name__].preferences.default_visibleOnly
    self.exportAllLODs = bpy.context.preferences.addons[__addon_name__].preferences.default_exportAllLODs

    self.autoSolveRepeatedUVs = bpy.context.preferences.addons[__addon_name__].preferences.default_autoSolveRepeatedUVs
    self.preserveSharpEdges = bpy.context.preferences.addons[__addon_name__].preferences.default_preserveSharpEdges
    self.useBlenderMaterialName = bpy.context.preferences.addons[__addon_name__].preferences.default_useBlenderMaterialName

    self.exportBoundingBoxes = bpy.context.preferences.addons[__addon_name__].preferences.default_exportBoundingBoxes


def setModDirectoryFromFilePath(filePath):
    if "nativepc" in filePath.lower():
        try:
            bpy.context.scene.mhw_mrl3_toolpanel.modDirectory = splitNativesPath(filePath)[0]
            print(f"Set mod directory to {bpy.context.scene.mhw_mrl3_toolpanel.modDirectory}")
        except:
            print("ERROR: Failed to set mod directory, exported file path probably does not follow the chunk naming scheme.")



'''导入窗口部分，mod3导入基本完毕，mrl3导入待做'''
class ImportMHWMod3(Operator, ImportHelper):
    '''导入MHW MOD3文件'''
    bl_idname = "mhw_mod3.import_mhw_mod3"
    bl_label = "Import MHW Mod3"
    bl_description = "Import MHW Mod3 Files."
    bl_options = {"PRESET", "REGISTER", "UNDO"}
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
        options={'SKIP_SAVE'},
    )
    filename_ext = ".mod3"
    filter_glob: StringProperty(default="*.mod3", options={'HIDDEN'})
    clearScene: BoolProperty(
        name="Clear Scene",
        description="Clear all objects before importing the mod3 file",
        default=False)

    # mrl3导入设置
    loadMaterials: BoolProperty(
        name="Load Materials",
        description="Load materials from the mrl3 file. This may increase the time the model takes to import",
        default=True)
    loadMrl3Data: BoolProperty(
        name="Load Mrl3 Material Data",
        description="Imports the mrl3 materials as objects inside a collection in the outliner.\nYou can make changes to mrl3 materials by selecting the Material objects in the outliner.\nUnder the Object Properties tab (orange square), there's a panel called \"MHW Mrl3 Material Settings\".\nMake any changes to mrl3 materials there.\nIf you're not modding MHW, you can uncheck this option since it won't be needed",
        default=False)
    loadUnusedTextures: BoolProperty(
        name="Load Unused Textures",
        description="Loads textures that have no function assigned to them in the material shader graph.\nLeaving this disabled will make materials load faster.\nOnly enable this if you plan on editing the material shader graph",
        default=False)
    loadUnusedProps: BoolProperty(
        name="Load Unused Material Properties",
        description="Loads material properties that have no function assigned to them in the material shader graph.\nLeaving this disabled will make materials load faster.\nOnly enable this if you plan on editing the material shader graph",
        default=False)
    useBackfaceCulling: BoolProperty(
        name="Use Backface Culling",
        description="Enables backface culling on materials. May improve Blender's performance on high poly meshes.\nBackface culling will only be enabled on materials without the two sided flag",
        default=False)
    reloadCachedTextures: BoolProperty(
        name="Reload Cached Textures",
        description="Convert all textures again instead of reading from already converted textures. Use this if you make changes to textures and need to reload them",
        default=False)
    mrl3Path: StringProperty(
        name="",
        description="Manually set the path of the mrl3 file. The Mrl3 is found automatically if this is left blank.\nTip:Hold shift and right click the mrl3 file and click \"Copy as path\", then paste into this field",
        default="",
    )
    # mod3导入设置
    createCollections: BoolProperty(
        name="Create Collections",
        description="Create a collection for the mod3 and for each LOD level."
                    "\nNote that collections are required for exporting LODs and applying mrl3 changes.\nLeaving this option enabled is recommended",
        default=True)
    importArmatureOnly: BoolProperty(
        name="Only Import Armature",
        description="Only import the armature of the mod3 file",
        default=False)
    importAllLODs: BoolProperty(
        name="Import All LODs",
        description="Import all LOD (level of detail) meshes in mod3 file."
                    "\nIf unchecked, only the highest LOD meshes will be imported",
        default=False)
    importBoundingBoxes: BoolProperty(
        name="Import Bounding Boxes",
        description="Import mesh and bone bounding boxes for debugging purposes",
        default=False)
    ArmatureDisplayType: bpy.props.EnumProperty(
        name="Armature Display Type",
        # description="Set the display type of armature to be imported",
        items=[("OCTAHEDRAL", "Octahedral", "Display bones as octahedral shape (default)"),
               ("STICK", "Stick", "Display bones as simple 2D lines with dots"),
               ("BBONE", "B-Bone", "Display bones as boxes, showing subdivision and B-Splines"),
               ("ENVELOPE", "Envelope", "Display bones as extruded spheres, showing deformation influence volume"),
               ("WIRE", "Wire", "Display bones as thin wires, showing subdivision and B-Splines"),
               ],
        default=1,
    )
    BonesDisplaySize: bpy.props.FloatProperty(
        name="",
        description="Set the display size of the bones to be imported",
        # default=0.004,
        default=5,
        step=100,
        soft_min=0.0,
    )
    # 下拉菜单
    showMod3Options: BoolProperty(
        name="Show Mod3 Options",
        default=True)
    showMrl3Options: BoolProperty(
        name="Show Mrl3 Options",
        default=True)

    def invoke(self, context, event):
        if not bpy.context.scene.get("MHWMod3DefaultImportSettingsLoaded"):
            setMod3ImportDefaults(self)

        if self.directory:
            if bpy.context.preferences.addons[__addon_name__].preferences.dragDropImportOptions:
                return context.window_manager.invoke_props_dialog(self)
            else:
                return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "clearScene")

        row = layout.row()
        icon = 'DOWNARROW_HLT' if self.showMod3Options else 'RIGHTARROW'
        row.prop(self, 'showMod3Options', icon=icon, icon_only=True)
        row.label(text='Mod3 Options')
        split = layout.split(factor=0.01)
        column = split.column()
        column2 = split.column()
        if self.showMod3Options:
            column2.label(text="Armature Display Type")
            column2.prop(self, "ArmatureDisplayType", text="")
            column2.label(text="Bones Display Size")
            column2.prop(self, "BonesDisplaySize", text="")
            column2.separator()
            column2.prop(self, "createCollections")
            column2.prop(self, "importAllLODs")
            column2.prop(self, "importArmatureOnly")
            column2.prop(self, "importBoundingBoxes")

        row = layout.row()
        icon = 'DOWNARROW_HLT' if self.showMrl3Options else 'RIGHTARROW'
        row.prop(self, 'showMrl3Options', icon=icon, icon_only=True)
        row.label(text='Mrl3 Options')
        split = layout.split(factor=0.01)
        column = split.column()
        column2 = split.column()
        if self.showMrl3Options:
            column2.prop(self, "loadMaterials")
            column2.prop(self, "loadMrl3Data")
            column2.prop(self, "reloadCachedTextures")
            column2.prop(self, "loadUnusedTextures")
            column2.prop(self, "loadUnusedProps")
            column2.prop(self, "useBackfaceCulling")
            column2.label(text="Manual Mrl3 Path")
            column2.prop(self, "mrl3Path")


    def execute(self, context):
        try:
            os.makedirs(bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath, exist_ok=True)
        except:
            raiseWarning("Could not create texture cache directory at " + bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath)

        options = {"clearScene":self.clearScene, "loadMaterials":self.loadMaterials, "loadMrl3Data":self.loadMrl3Data, "loadUnusedTextures":self.loadUnusedTextures, "loadUnusedProps":self.loadUnusedProps, "useBackfaceCulling":self.useBackfaceCulling, "reloadCachedTextures":self.reloadCachedTextures, "mrl3Path":self.mrl3Path.replace("\"",""), "ArmatureDisplayType":self.ArmatureDisplayType, "BonesDisplaySize":self.BonesDisplaySize, "createCollections":self.createCollections, "importArmatureOnly":self.importArmatureOnly, "importAllLODs":self.importAllLODs, "importBoundingBoxes":self.importBoundingBoxes}

        '''获取bl_info暂时有问题（容易无限循环），等做完再说'''
        # editorVersion = str(bl_info["version"][0]) + "." + str(bl_info["version"][1])
        # print(f"\n{textColors.BOLD}MHW Model Editor V{editorVersion}{textColors.ENDC}")
        print(f"\n{textColors.BOLD}MHW Model Editor{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        bpy.context.scene["MHWMod3DefaultImportSettingsLoaded"] = 1

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        multiFileImport = len(self.files) > 1
        hasImportErrors = False

        for index, file in enumerate(self.files):
            filepath = os.path.join(self.directory, file.name)
            if multiFileImport:
                print(f"Multi Mod3 Import ({index + 1}/{len(self.files)})")

            if os.path.isfile(filepath):
                success = importMHWMod3File(filepath, options)
                options["clearScene"] = False  # Disable clear scene after first mesh is imported
                if not success: hasImportErrors = True
            else:
                hasImportErrors = True
                raiseWarning(f"Path does not exist, cannot import file. If you are importing multiple files at once, they must all be in the same directory.\nInvalid Path:{filepath}")

        if not hasImportErrors:
            if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                try:
                    bpy.ops.wm.console_toggle()
                except:
                    pass
            if not multiFileImport:
                self.report({"INFO"}, "Successfully imported MHW Mod3 file.")
            else:
                self.report({"INFO"}, f"Successfully imported {str(len(self.files))} MHW Mod3 files.")

            return {"FINISHED"}
        else:
            self.report({"INFO"}, "Failed to import MHW Mod3 file. Check Window > Toggle System Console for details.")
            return {"CANCELLED"}

# def update_targetMod3Collection(self,context):
#     temp = bpy.data.screens.get("temp")
#     browserSpace = None
#     if temp != None:
#         for area in temp.areas:
#             for space in area.spaces:
#                 try:
#                     if type(space.params).__name__ == "FileSelectParams":
#                         browserSpace = space
#                         break
#                 except:
#                     pass
#     if browserSpace != None:
#         if ".mod3" in self.targetCollection:
#             browserSpace.params.filename = self.targetCollection.split(".mod3")[0]+".mod3"


class ExportMHWMod3(Operator, ExportHelper):
    bl_idname = "mhw_mod3.export_mhw_mod3"
    bl_label = "Export MHW Mod3"
    bl_description = "Export MHW Mod3 Files"
    bl_options = {'PRESET'}

    filename_ext = ".mod3"
    filter_glob: StringProperty(default="*.mod3*", options={'HIDDEN'})
    # targetCollection: StringProperty(
    #     name="",
    #     description="Set the mod3 collection to be exported\nNote: mod3 collections are red and end with .mod3",
    #     update=update_targetMod3Collection
    # )

    # mod3导出设置
    selectedOnly: BoolProperty(
        name="Selected Objects Only",
        description="Only export selected objects",
        default=False)
    visibleOnly: BoolProperty(
        name="Visible Objects Only",
        description="Only export visible objects",
        default=False)  # 考虑增加只导出可见网格的选项
    exportAllLODs: BoolProperty(
        name="Export All LODs",
        description="Export all LOD meshes. If unchecked, only the highest LOD meshes will be exported."
                    "\nNote that LODs meshes must be grouped inside a collection for each level, and that collection must be contained in mod3 collection."
                    "\nImport a mod3 file with \"Import All LODs\" option to see how it looks",
        default=True)
    autoSolveRepeatedUVs: BoolProperty(
        name="Auto Solve Repeated UVs",
        description="Splits connected UV islands if present. The mesh format does not allow for multiple uvs assigned to a vertex.\nNOTE: This will modify the exported mesh. If auto smooth is disabled on the mesh, the normals may change",
        default=True)
    preserveSharpEdges: BoolProperty(
        name="Split Sharp Edges",
        description="Edge splits all edges marked as sharp to preserve them on the exported mesh.\nNOTE: This will modify the exported mesh",
        default=False)
    useBlenderMaterialName: BoolProperty(
        name="Use Blender Material Names",
        description="If left unchecked, the exporter will get the material names to be used from the end of each object name. For example, if a mesh is named LOD_0_Group_0_Sub_0__Shirts_Mat, the material name is Shirts_Mat. If this option is enabled, the material name will instead be taken from the first material assigned to the object",
        default=False)
    exportBoundingBoxes: BoolProperty(
        name="Export Bounding Boxes",
        description="Exports the original bounding boxes from the \"Import Bounding Boxes\" import option. New bounding boxes will be generated for any bones that do not have them",
        default=False)

    # mrl3导出设置

    # 下拉菜单
    showMod3Options: BoolProperty(
        name="Show Mod3 Options",
        default=True)

    def invoke(self, context, event):
        scene = context.scene
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel
        mhw_export_collection = scene.mhw_export_collection

        if not scene.get("MHWMod3DefaultExportSettingsLoaded"):
            setMod3ExportDefaults(self)

        '''之后再看看这个索引逻辑和顺序'''
        # 依次按照上一次导出的mod3集合、当前激活的mod3集合、上一次导入的mod3集合的顺序来获取导出时的集合和文件名
        # Get last exported collection, if there isn't one, get last imported
        exportCollection = context.scene.get("MHWMod3LastExportedCollection", "")
        if exportCollection in bpy.data.collections:
            mhw_export_collection.targetMod3Collection = bpy.data.collections[exportCollection]
            if ".mod3" in exportCollection:  # Remove blender suffix after .mod3 if it exists
                self.filepath = exportCollection.split(".mod3")[0] + ".mod3"
        else:
            if mhw_mrl3_toolpanel.mod3Collection:
                mhw_export_collection.targetMod3Collection = mhw_mrl3_toolpanel.mod3Collection
                self.filepath = mhw_export_collection.targetMod3Collection.name.split(".mod3")[0] + ".mod3"
            else:
                prevCollection = context.scene.get("MHWMod3LastImportedCollection", "")
                if prevCollection in bpy.data.collections:
                    mhw_export_collection.targetMod3Collection = bpy.data.collections[prevCollection]
                if ".mod3" in prevCollection:  # Remove blender suffix after .mod3 if it exists
                    self.filepath = prevCollection.split(".mod3")[0] + ".mod3"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mhw_export_collection = scene.mhw_export_collection
        layout.label(text="Mod3 Collection:")
        # layout.prop_search(self, "targetCollection", bpy.data, "collections", icon="COLLECTION_COLOR_01")
        layout.prop_search(mhw_export_collection, "targetMod3Collection", bpy.data, "collections", icon="COLLECTION_COLOR_01")
        if not mhw_export_collection.targetMod3Collection:
            row = layout.row()
            row.alert = True
            row.label(icon="ERROR", text="Must select a mod3 collection first.")
        row = layout.row()
        icon = 'DOWNARROW_HLT' if self.showMod3Options else 'RIGHTARROW'
        row.prop(self, 'showMod3Options', icon=icon, icon_only=True)
        row.label(text='Mod3 Options')
        split = layout.split(factor=0.01)
        column = split.column()
        column2 = split.column()
        if self.showMod3Options:
            column2.prop(self, "selectedOnly")
            # column2.prop(self, "visibleOnly")
            column2.prop(self, "exportAllLODs")
            column2.prop(self, "autoSolveRepeatedUVs")
            column2.prop(self, "preserveSharpEdges")
            column2.prop(self, "useBlenderMaterialName")
            column2.prop(self, "exportBoundingBoxes")



    def execute(self, context):
        scene = context.scene
        mhw_export_collection = scene.mhw_export_collection
        options = {"targetCollection": mhw_export_collection.targetMod3Collection, "selectedOnly": self.selectedOnly,
                   "visibleOnly": self.visibleOnly, "exportAllLODs": self.exportAllLODs,
                   "useBlenderMaterialName": self.useBlenderMaterialName, "exportBoundingBoxes": self.exportBoundingBoxes,
                   "autoSolveRepeatedUVs": self.autoSolveRepeatedUVs, "preserveSharpEdges": self.preserveSharpEdges}

        '''获取bl_info暂时有问题（容易无限循环），等做完再说'''
        # editorVersion = str(bl_info["version"][0]) + "." + str(bl_info["version"][1])
        # print(f"\n{textColors.BOLD}MHW Model Editor V{editorVersion}{textColors.ENDC}")
        print(f"\n{textColors.BOLD}MHW Model Editor{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        bpy.context.scene["MHWMod3DefaultExportSettingsLoaded"] = 1

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        success = exportMHWMod3File(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW Mod3 file.")
        else:
            self.report({"INFO"}, "Failed to export MHW Mod3 file. Check Window > Toggle System Console for details.")

        if bpy.context.scene.mhw_mrl3_toolpanel.modDirectory == "":
            setModDirectoryFromFilePath(self.filepath)

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        return {"FINISHED"}





