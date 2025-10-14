import bpy
import os
from bpy.types import Operator, OperatorFileListElement, Panel
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty, EnumProperty, FloatProperty

from ...config import __addon_name__, editorVersion
from ..common.blender_functions import setModDirectoryFromFilePath
from ..common.message_functions import textColors, raiseWarning
from .blender_ccl import importMHWCCLFile, exportMHWCCLFile


class ImportMHWCCL(Operator, ImportHelper):
    """导入MHW CCL文件"""
    bl_idname = "mhw_ccl.import_mhw_ccl"
    bl_label = "Import MHW CCL"
    bl_description = "Import MHW CCL Files." \
                     "\nThe button will only be triggered if active ctc collection exists." \
                     "\nNOTE: Before importing ccl, make sure that at least one mod3 armature exists in the current scene"
    bl_options = {"PRESET", "REGISTER", "UNDO"}

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
        options={'SKIP_SAVE'},
    )
    filename_ext = ".ccl"
    filter_glob: StringProperty(default="*.ccl", options={'HIDDEN'})

    @classmethod
    def poll(self, context):
        return context.scene.mhw_ctc_toolpanel.ctcCollection is not None

    def invoke(self, context, event):
        if self.directory:
            if bpy.context.preferences.addons[__addon_name__].preferences.dragDropImportOptions:
                return context.window_manager.invoke_props_dialog(self)
            else:
                return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        scene = context.scene
        mhw_ccl_toolpanel = scene.mhw_ccl_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Target Armature:")
        col.separator()

        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_ccl_toolpanel, "importCTCArmature", icon="OUTLINER_OB_ARMATURE")
        col.separator()

        # row = col.row(align=True)
        # # row.scale_y = 0.75
        # row.label(text="Merge With CTC Collection:")
        # col.separator()
        #
        # row = col.row(align=True)
        # row.scale_y = 1.2
        # row.prop(mhw_ccl_toolpanel, "importCTCCollection", icon="COLLECTION_COLOR_02")

    def execute(self, context):
        scene = context.scene
        mhw_ccl_toolpanel = scene.mhw_ccl_toolpanel
        options = {"targetArmature": mhw_ccl_toolpanel.importCTCArmature}

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        # print(f"\n{textColors.BOLD}MHW Model Editor{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

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
                print(f"Multi CCL Import ({index + 1} / {len(self.files)})")

            if os.path.isfile(filepath):
                success = importMHWCCLFile(filepath, options)
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
                self.report({"INFO"}, "Successfully imported MHW CCL file.")
            else:
                self.report({"INFO"}, f"Successfully imported {len(self.files)} MHW CCL files.")

            return {"FINISHED"}
        else:
            if not multiFileImport:
                self.report({"INFO"},
                            "Failed to import MHW CCL file. Check Window > Toggle System Console for details.")
            else:
                self.report({"INFO"},
                            "Some MHW CCL files failed to import. Check Window > Toggle System Console for details.")
            return {"CANCELLED"}


class ExportMHWCCL(Operator, ExportHelper):
    """导出MHW CCL文件"""
    bl_idname = "mhw_ccl.export_mhw_ccl"
    bl_label = "Export MHW CCL"
    bl_description = "Export MHW CCL File"
    bl_options = {'PRESET'}
    filename_ext = ".ccl"
    filter_glob: StringProperty(default="*.ccl", options={'HIDDEN'})

    def invoke(self, context, event):
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel
        mhw_ccl_toolpanel = scene.mhw_ccl_toolpanel

        # 依次按照上一次导出的ctc集合、当前激活的ctc集合、上一次导入的ctc集合的顺序来获取导出时的集合和文件名
        col = None
        exportCollection = mhw_ccl_toolpanel.lastExportCollection
        if exportCollection in bpy.data.collections:
            col = bpy.data.collections[exportCollection]
        else:
            if mhw_ctc_toolpanel.ctcCollection:
                col = mhw_ctc_toolpanel.ctcCollection
            else:
                prevCollection = mhw_ccl_toolpanel.lastImportCollection
                if prevCollection in bpy.data.collections:
                    col = bpy.data.collections[prevCollection]

        mhw_ccl_toolpanel.exportCTCCollection = col
        if col and ".ctc" in col.name:
            self.filepath = col.name.split(".ctc")[0] + ".ccl"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        scene = context.scene
        mhw_ccl_toolpanel = scene.mhw_ccl_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="CTC Collection:")
        col.separator()

        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_ccl_toolpanel, "exportCTCCollection", icon="COLLECTION_COLOR_02")
        if not mhw_ccl_toolpanel.exportCTCCollection:
            col.separator()
            row = col.row(align=True)
            row.alert = True
            row.label(icon="ERROR", text="Must select a ctc collection first !!!")

    def execute(self, context):
        scene = context.scene
        mhw_ccl_toolpanel = scene.mhw_ccl_toolpanel
        options = {"targetCollection": mhw_ccl_toolpanel.exportCTCCollection}

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        success = exportMHWCCLFile(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW CCL file.")
            if scene.mhw_mrl3_toolpanel.modDirectory == "":
                setModDirectoryFromFilePath(self.filepath)
        else:
            self.report({"INFO"}, "Failed to export MHW CCL file. Check Window > Toggle System Console for details.")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        return {"FINISHED"}