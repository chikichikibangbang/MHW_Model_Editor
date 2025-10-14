import bpy
import os
from bpy.types import Operator, OperatorFileListElement, Panel
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty, EnumProperty, FloatProperty

from ...config import __addon_name__, editorVersion
from ..common.blender_functions import setModDirectoryFromFilePath
from ..common.message_functions import textColors, raiseWarning
from .blender_ctc import importMHWCTCFile, exportMHWCTCFile


class ImportMHWCTC(Operator, ImportHelper):
    """导入MHW CTC文件"""
    bl_idname = "mhw_ctc.import_mhw_ctc"
    bl_label = "Import MHW CTC"
    bl_description = "Import MHW CTC Files." \
                     "\nNOTE: Before importing ctc, make sure that at least one mod3 armature exists in the current scene"
    bl_options = {"PRESET", "REGISTER", "UNDO"}

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
        options={'SKIP_SAVE'},
    )
    filename_ext = ".ctc"
    filter_glob: StringProperty(default="*.ctc", options={'HIDDEN'})

    loadCCL: BoolProperty(
        name="Load CCL Collision",
        description="Load physical collision objects from the ccl file",
        default=True)

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
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "loadCCL")

        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Target Armature:")
        col.separator()

        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_ctc_toolpanel, "importCTCArmature", icon="OUTLINER_OB_ARMATURE")
        col.separator()

        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Merge With CTC Collection:")
        col.separator()

        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_ctc_toolpanel, "importCTCCollection", icon="COLLECTION_COLOR_02")

    def execute(self, context):
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel
        options = {"targetArmature": mhw_ctc_toolpanel.importCTCArmature,
                   "mergeCollection": mhw_ctc_toolpanel.importCTCCollection, "loadCCL": self.loadCCL}

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
                print(f"Multi CTC Import ({index + 1} / {len(self.files)})")

            if os.path.isfile(filepath):
                success = importMHWCTCFile(filepath, options)
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
                self.report({"INFO"}, "Successfully imported MHW CTC file.")
            else:
                self.report({"INFO"}, f"Successfully imported {len(self.files)} MHW CTC files.")

            return {"FINISHED"}
        else:
            if not multiFileImport:
                self.report({"INFO"},
                            "Failed to import MHW CTC file. Check Window > Toggle System Console for details.")
            else:
                self.report({"INFO"},
                            "Some MHW CTC files failed to import. Check Window > Toggle System Console for details.")
            return {"CANCELLED"}


class ExportMHWCTC(Operator, ExportHelper):
    """导出MHW CTC文件"""
    bl_idname = "mhw_ctc.export_mhw_ctc"
    bl_label = "Export MHW CTC"
    bl_description = "Export MHW CTC File"
    bl_options = {'PRESET'}
    filename_ext = ".ctc"
    filter_glob: StringProperty(default="*.ctc", options={'HIDDEN'})

    exportCCL: BoolProperty(
        name="Export CCL Collision",
        description="When exporting ctc file, also export collision objects as ccl file",
        default=True)

    def invoke(self, context, event):
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel

        # 依次按照上一次导出的ctc集合、当前激活的ctc集合、上一次导入的ctc集合的顺序来获取导出时的集合和文件名
        col = None
        exportCollection = mhw_ctc_toolpanel.lastExportCollection
        if exportCollection in bpy.data.collections:
            col = bpy.data.collections[exportCollection]
        else:
            if mhw_ctc_toolpanel.ctcCollection:
                col = mhw_ctc_toolpanel.ctcCollection
            else:
                prevCollection = mhw_ctc_toolpanel.lastImportCollection
                if prevCollection in bpy.data.collections:
                    col = bpy.data.collections[prevCollection]

        mhw_ctc_toolpanel.exportCTCCollection = col
        if col and ".ctc" in col.name:
            self.filepath = col.name.split(".ctc")[0] + ".ctc"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(self, "exportCCL")

        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="CTC Collection:")
        col.separator()

        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_ctc_toolpanel, "exportCTCCollection", icon="COLLECTION_COLOR_02")
        if not mhw_ctc_toolpanel.exportCTCCollection:
            col.separator()
            row = col.row(align=True)
            row.alert = True
            row.label(icon="ERROR", text="Must select a ctc collection first !!!")

    def execute(self, context):
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel
        options = {"targetCollection": mhw_ctc_toolpanel.exportCTCCollection, "exportCCL": self.exportCCL}

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        success = exportMHWCTCFile(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW CTC file.")
            if scene.mhw_mrl3_toolpanel.modDirectory == "":
                setModDirectoryFromFilePath(self.filepath)
        else:
            self.report({"INFO"}, "Failed to export MHW CTC file. Check Window > Toggle System Console for details.")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        return {"FINISHED"}