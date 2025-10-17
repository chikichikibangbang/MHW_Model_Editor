import bpy
import os
from bpy.types import Operator, OperatorFileListElement, Panel
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty, EnumProperty, FloatProperty

from ...config import __addon_name__, editorVersion
from ..common.blender_functions import setModDirectoryFromFilePath
from ..common.message_functions import textColors, raiseWarning
from .blender_mod3 import importMHWMod3File, exportMHWMod3File
from .....common.types.framework import reg_order


# Used to circumvent the issue of properties not being able to used as defaults for other properties at startup
def setMod3ImportDefaults(self):
    preferences = bpy.context.preferences.addons[__addon_name__].preferences

    self.clearScene = preferences.default_clearScene
    self.addNestedCollections = preferences.default_addNestedCollections
    self.createCollections = preferences.default_createCollections
    self.importArmatureOnly = preferences.default_importArmatureOnly
    self.importAllLODs = preferences.default_importAllLODs
    self.importBoundingBoxes = preferences.default_importBoundingBoxes
    self.ArmatureDisplayType = preferences.default_ArmatureDisplayType
    self.BonesDisplaySize = preferences.default_BonesDisplaySize

    self.loadMaterials = preferences.default_loadMaterials
    self.loadMrl3Data = preferences.default_loadMrl3Data
    self.loadUnusedTextures = preferences.default_loadUnusedTextures
    self.loadUnusedProps = preferences.default_loadUnusedProps
    self.useBackfaceCulling = preferences.default_useBackfaceCulling
    self.reloadCachedTextures = preferences.default_reloadCachedTextures

    # self.loadCTC = preferences.default_loadCTC
    # self.loadCCL = preferences.default_loadCCL
    self.loadPhysics = preferences.default_loadPhysics

def setMod3ExportDefaults(self):
    preferences = bpy.context.preferences.addons[__addon_name__].preferences

    self.selectedOnly = preferences.default_selectedOnly
    self.visibleOnly = preferences.default_visibleOnly
    self.exportAllLODs = preferences.default_exportAllLODs
    self.autoSolveRepeatedUVs = preferences.default_autoSolveRepeatedUVs
    self.preserveSharpEdges = preferences.default_preserveSharpEdges
    self.useBlenderMaterialName = preferences.default_useBlenderMaterialName
    self.exportBoundingBoxes = preferences.default_exportBoundingBoxes

class ImportMHWMod3(Operator, ImportHelper):
    """导入MHW MOD3文件"""
    bl_idname = "mhw_mod3.import_mhw_mod3"
    bl_label = "Import MHW MOD3"
    bl_description = "Import MHW MOD3 Files."
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

    # mod3导入设置
    addNestedCollections: BoolProperty(
        name="Add Nested Collections",
        description="Add a general parent collection to place other collections of various imported files."
                    "\nThis will make the collection structure look clearer."
                    "\nLeaving this option enabled is recommended",
        default=True)
    createCollections: BoolProperty(
        name="Create Collections",
        description="Create a collection for the mod3 and for each LOD level."
                    "\nNote that collections are required for exporting LODs and applying mrl3 changes."
                    "\nLeaving this option enabled is recommended",
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
    ArmatureDisplayType: EnumProperty(
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
    BonesDisplaySize: FloatProperty(
        name="",
        description="Set the display size of the bones to be imported",
        # default=0.004,
        default=5,
        step=100,
        soft_min=0.0,
    )

    # mrl3导入设置
    loadMrl3Data: BoolProperty(
        name="Load Material Data",
        description="Imports the mrl3 materials as objects inside a collection in the outliner."
                    "\nYou can make changes to mrl3 materials by selecting the Material objects in the outliner."
                    "\nUnder the Object Properties tab (orange square), there's a panel called \"MHW Mrl3 Material Settings\"."
                    "\nMake any changes to mrl3 materials there."
                    "\nIf you're not modding MHW, you can uncheck this option since it won't be needed",
        default=False)
    loadMaterials: BoolProperty(
        name="Load Mesh Materials",
        description="Load materials from the mrl3 file. This may increase the time the model takes to import",
        default=True)
    loadUnusedTextures: BoolProperty(
        name="Load Unused Textures",
        description="Loads textures that have no function assigned to them in the material shader graph."
                    "\nLeaving this disabled will make materials load faster."
                    "\nOnly enable this if you plan on editing the material shader graph",
        default=False)
    loadUnusedProps: BoolProperty(
        name="Load Unused Properties",
        description="Loads material properties that have no function assigned to them in the material shader graph."
                    "\nLeaving this disabled will make materials load faster."
                    "\nOnly enable this if you plan on editing the material shader graph",
        default=False)
    useBackfaceCulling: BoolProperty(
        name="Use Backface Culling",
        description="Enables backface culling on materials. May improve Blender's performance on high poly meshes."
                    "\nBackface culling will only be enabled on materials without the two sided flag",
        default=False)
    reloadCachedTextures: BoolProperty(
        name="Reload Cached Textures",
        description="Convert all textures again instead of reading from already converted textures."
                    "\nUse this if you make changes to textures and need to reload them",
        default=False)
    mrl3Path: StringProperty(
        name="",
        description="Manually set the path of the mrl3 file."
                    "\nThe Mrl3 is found automatically if this is left blank."
                    "\nTip: Hold shift and right click the mrl3 file and click \"Copy as path\", then paste into this field",
        default="",
    )

    # ctc & ccl导入设置
    loadPhysics: BoolProperty(
        name="Load Chains & Collisions",
        description="Load physical chain and collision objects from the ctc & ccl file",
        default=False)
    # loadCTC: BoolProperty(
    #     name="Load CTC Chain",
    #     description="Load physical chain objects from the ctc file",
    #     default=False)
    # loadCCL: BoolProperty(
    #     name="Load CCL Collision",
    #     description="Load physical collision objects from the ccl file",
    #     default=False)

    showMod3Options: BoolProperty(
        name="Show Mod3 Options",
        default=True)
    showMrl3Options: BoolProperty(
        name="Show Mrl3 Options",
        default=True)
    showCTCCCLOptions: BoolProperty(
        name="Show CTC & CCL Options",
        default=True)

    def invoke(self, context, event):
        if not bpy.context.scene.mhw_mod3_toolpanel.importSettingsLoaded:
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
        # row = layout.row()
        layout.scale_y = 1.1
        layout.prop(self, "clearScene")

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showMod3Options else "RIGHTARROW"
        row.prop(self, "showMod3Options", icon=icon, icon_only=True, emboss=False)
        row.label(text="Mod3 Options")
        if self.showMod3Options:
            box = layout.box()
            col = box.column(align=True)

            row = col.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Armature Display Type:")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "ArmatureDisplayType", text="")
            col.separator()

            row = col.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Bones Display Size:")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "BonesDisplaySize", text="")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "addNestedCollections")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "createCollections")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "importAllLODs")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "importArmatureOnly")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "importBoundingBoxes")

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showMrl3Options else "RIGHTARROW"
        row.prop(self, "showMrl3Options", icon=icon, icon_only=True, emboss=False)
        row.label(text="Mrl3 Options")
        if self.showMrl3Options:
            box = layout.box()
            col = box.column(align=True)

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "loadMrl3Data")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "loadMaterials")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "reloadCachedTextures")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "loadUnusedTextures")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "loadUnusedProps")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "useBackfaceCulling")
            # # col.separator()

            row = col.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Manual Mrl3 Path:")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "mrl3Path")

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showCTCCCLOptions else "RIGHTARROW"
        row.prop(self, "showCTCCCLOptions", icon=icon, icon_only=True, emboss=False)
        row.label(text="CTC & CCL Options")
        if self.showCTCCCLOptions:
            box = layout.box()
            col = box.column(align=True)

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "loadPhysics")

    def execute(self, context):
        try:
            os.makedirs(bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath, exist_ok=True)
        except:
            raiseWarning("Could not create texture cache directory at " +
                         bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath)

        options = {"clearScene":self.clearScene, "loadMaterials":self.loadMaterials, "loadMrl3Data":self.loadMrl3Data,
                   "loadUnusedTextures":self.loadUnusedTextures, "loadUnusedProps":self.loadUnusedProps,
                   "useBackfaceCulling":self.useBackfaceCulling, "reloadCachedTextures":self.reloadCachedTextures,
                   "mrl3Path":self.mrl3Path.replace("\"",""), "ArmatureDisplayType":self.ArmatureDisplayType,
                   "BonesDisplaySize":self.BonesDisplaySize, "createCollections":self.createCollections,
                   "importArmatureOnly":self.importArmatureOnly, "importAllLODs":self.importAllLODs,
                   "importBoundingBoxes":self.importBoundingBoxes, "loadPhysics":self.loadPhysics,
                   "addNestedCollections":self.addNestedCollections}

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        bpy.context.scene.mhw_mod3_toolpanel.importSettingsLoaded = True

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
                print(f"Multi MOD3 Import ({index + 1} / {len(self.files)})")

            if os.path.isfile(filepath):
                success = importMHWMod3File(filepath, options)
                options["clearScene"] = False  # 导入第一个mod3文件后关掉清理场景的选项
                if not success:
                    hasImportErrors = True
            else:
                hasImportErrors = True
                raiseWarning(f"Path does not exist, cannot import file."
                             f"If you are importing multiple files at once, they must all be in the same directory."
                             f"\nInvalid Path: {filepath}")

        if not hasImportErrors:
            if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                try:
                    bpy.ops.wm.console_toggle()
                except:
                    pass

            if not multiFileImport:
                self.report({"INFO"}, "Successfully imported MHW MOD3 file.")
            else:
                self.report({"INFO"}, f"Successfully imported {len(self.files)} MHW MOD3 files.")

            return {"FINISHED"}
        else:
            if not multiFileImport:
                self.report({"INFO"}, "Failed to import MHW MOD3 file. Check Window > Toggle System Console for details.")
            else:
                self.report({"INFO"},
                            "Some MHW MOD3 files failed to import. Check Window > Toggle System Console for details.")

            return {"CANCELLED"}


class ExportMHWMod3(Operator, ExportHelper):
    """导出MHW MOD3文件"""
    bl_idname = "mhw_mod3.export_mhw_mod3"
    bl_label = "Export MHW MOD3"
    bl_description = "Export MHW MOD3 Files"
    bl_options = {'PRESET'}

    filename_ext = ".mod3"
    filter_glob: StringProperty(default="*.mod3", options={'HIDDEN'})

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
                    "\nNOTE: LOD meshes must be grouped inside a collection for each level, and that collection must be contained in mod3 collection."
                    "\nImport a mod3 file with \"Import All LODs\" option to see how it looks",
        default=True)
    autoSolveRepeatedUVs: BoolProperty(
        name="Auto Solve Repeated UVs",
        description="Splits connected UV islands if present. The mesh format does not allow for multiple uvs assigned to a vertex."
                    "\nNOTE: This will modify the exported mesh. If auto smooth is disabled on the mesh, the normals may change",
        default=True)
    preserveSharpEdges: BoolProperty(
        name="Split Sharp Edges",
        description="Edge splits all edges marked as sharp to preserve them on the exported mesh."
                    "\nNOTE: This will modify the exported mesh",
        default=False)
    useBlenderMaterialName: BoolProperty(
        name="Use Blender Material Names",
        description="If left unchecked, the exporter will get the material names to be used from the end of each object name."
                    "\nFor example, if a mesh is named LOD_0_Group_0_Sub_0__Shirts_Mat, the material name is Shirts_Mat."
                    "\nIf this option is enabled, the material name will instead be taken from the first material assigned to the object",
        default=False)
    exportBoundingBoxes: BoolProperty(
        name="Export Bounding Boxes",
        description="Exports the original bounding boxes from the \"Import Bounding Boxes\" import option."
                    "\nNew bounding boxes will be generated for any bones that do not have them",
        default=False)

    # mrl3导出设置

    showMod3Options: BoolProperty(
        name="Show Mod3 Options",
        default=True)
    showMrl3Options: BoolProperty(
        name="Show Mrl3 Options",
        default=True)
    showCTCCCLOptions: BoolProperty(
        name="Show CTC & CCL Options",
        default=True)

    def invoke(self, context, event):
        scene = context.scene
        mhw_mod3_toolpanel = scene.mhw_mod3_toolpanel
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel

        if not mhw_mod3_toolpanel.exportSettingsLoaded:
            setMod3ExportDefaults(self)

        # 依次按照上一次导出的mod3集合、当前激活的mod3集合、上一次导入的mod3集合的顺序来获取导出时的集合和文件名
        col = None
        exportCollection = mhw_mod3_toolpanel.lastExportCollection
        if exportCollection in bpy.data.collections:
            col = bpy.data.collections[exportCollection]
        else:
            if mhw_mrl3_toolpanel.mod3Collection:
                col = mhw_mrl3_toolpanel.mod3Collection
            else:
                prevCollection = mhw_mod3_toolpanel.lastImportCollection
                if prevCollection in bpy.data.collections:
                    col = bpy.data.collections[prevCollection]

        mhw_mod3_toolpanel.exportMod3Collection = col
        if col and ".mod3" in col.name:
            self.filepath = col.name.split(".mod3")[0] + ".mod3"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        mhw_mod3_toolpanel = context.scene.mhw_mod3_toolpanel

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showMod3Options else "RIGHTARROW"
        row.prop(self, "showMod3Options", icon=icon, icon_only=True, emboss=False)
        row.label(text="Mod3 Options")
        if self.showMod3Options:
            box = layout.box()
            col = box.column(align=True)

            row = col.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Mod3 Collection:")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.2
            row.prop(mhw_mod3_toolpanel, "exportMod3Collection", icon="COLLECTION_COLOR_01")
            if not mhw_mod3_toolpanel.exportMod3Collection:
                col.separator()
                row = col.row(align=True)
                row.alert = True
                row.label(icon="ERROR", text="Must select a mod3 collection first !!!")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "selectedOnly")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "visibleOnly")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "exportAllLODs")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "autoSolveRepeatedUVs")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "preserveSharpEdges")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "useBlenderMaterialName")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "exportBoundingBoxes")

    def execute(self, context):
        scene = context.scene
        mhw_mod3_toolpanel = scene.mhw_mod3_toolpanel
        options = {"targetCollection": mhw_mod3_toolpanel.exportMod3Collection, "selectedOnly": self.selectedOnly,
                   "visibleOnly": self.visibleOnly, "exportAllLODs": self.exportAllLODs,
                   "useBlenderMaterialName": self.useBlenderMaterialName, "exportBoundingBoxes": self.exportBoundingBoxes,
                   "autoSolveRepeatedUVs": self.autoSolveRepeatedUVs, "preserveSharpEdges": self.preserveSharpEdges}

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        mhw_mod3_toolpanel.exportSettingsLoaded = True

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        success = exportMHWMod3File(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW MOD3 file.")
            if scene.mhw_mrl3_toolpanel.modDirectory == "":
                setModDirectoryFromFilePath(self.filepath)
        else:
            self.report({"INFO"}, "Failed to export MHW MOD3 file. Check Window > Toggle System Console for details.")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        return {"FINISHED"}






