import os

import bpy
from .....common.i18n.i18n import i18n
from ..common.blender_functions import setModDirectoryFromFilePath
from .blender_mrl3 import exportMHWMrl3File, importMHWMrl3File
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty
from bpy.types import Operator, OperatorFileListElement
from ..common.general_function import splitNativesPath
from ..common.message_functions import textColors, raiseWarning
from ...config import __addon_name__, editorVersion


class ImportMHWMrl3(Operator, ImportHelper):
    """导入MHW MRL3文件"""
    bl_idname = "mhw_mrl3.import_mhw_mrl3"
    bl_label = "Import MHW MRL3"
    bl_description = "Import MHW MRL3 Files"
    bl_options = {"PRESET", "REGISTER", "UNDO"}

    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
        options={'SKIP_SAVE'},
    )
    filename_ext = ".mrl3"
    filter_glob: StringProperty(default="*.mrl3", options={'HIDDEN'})

    def invoke(self, context, event):
        if self.directory:
            # if bpy.context.preferences.addons[__addon_name__].preferences.dragDropImportOptions:
            #     return context.window_manager.invoke_props_dialog(self)
            # else:
            #     return self.execute(context)
            return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        lang = bpy.context.preferences.view.language
        options = {"mrl3File": None, "mod3MatHashDict": {}, "parentCollection": None}

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        print(f"{i18n('Blender Version')} {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
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
                print(f"{i18n('Multi MRL3 Import')} ({index + 1} / {len(self.files)})")

            if os.path.isfile(filepath):
                success = importMHWMrl3File(filepath, options)
                if not success:
                    hasImportErrors = True
            else:
                hasImportErrors = True
                raiseWarning(f"{i18n('Path does not exist, cannot import file.')}"
                             f"\n{i18n('If you are importing multiple files at once, they must all be in the same directory.')}"
                             f"\n{i18n('Invalid Path:')} {filepath}")

        if not hasImportErrors:
            if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                try:
                    bpy.ops.wm.console_toggle()
                except:
                    pass

            if not multiFileImport:
                self.report({"INFO"}, "Successfully imported MHW MRL3 file.")
            else:
                if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                    self.report({"INFO"}, f"成功导入 {len(self.files)} 个MHW MRL3文件.")
                else:
                    self.report({"INFO"}, f"Successfully imported {len(self.files)} MHW MRL3 files.")

            return {"FINISHED"}
        else:
            if not multiFileImport:
                self.report({"INFO"}, "Failed to import MHW MRL3 file. Check Window > Toggle System Console for details.")
            else:
                self.report({"INFO"},
                            "Some MHW MRL3 files failed to import. Check Window > Toggle System Console for details.")

            return {"CANCELLED"}


class ExportMHWMrl3(Operator, ExportHelper):
    """导出MHW MRL3文件"""
    bl_idname = "mhw_mrl3.export_mhw_mrl3"
    bl_label = "Export MHW MRL3"
    bl_description = "Export MHW MRL3 File"
    bl_options = {'PRESET'}
    filename_ext = ".mrl3"
    filter_glob: StringProperty(default="*.mrl3", options={'HIDDEN'})

    def invoke(self, context, event):
        scene = context.scene
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel

        # 依次按照上一次导出的mrl3集合、当前激活的mrl3集合、上一次导入的mrl3集合的顺序来获取导出时的集合和文件名
        col = None
        exportCollection = mhw_mrl3_toolpanel.lastExportCollection
        if exportCollection in bpy.data.collections:
            col = bpy.data.collections[exportCollection]
        else:
            if mhw_mrl3_toolpanel.mrl3Collection:
                col = mhw_mrl3_toolpanel.mrl3Collection
            else:
                prevCollection = mhw_mrl3_toolpanel.lastImportCollection
                if prevCollection in bpy.data.collections:
                    col = bpy.data.collections[prevCollection]

        mhw_mrl3_toolpanel.exportMrl3Collection = col
        if col and ".mrl3" in col.name:
            self.filepath = col.name.split(".mrl3")[0] + ".mrl3"

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        scene = context.scene
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Mrl3 Collection:")
        col.separator()

        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_mrl3_toolpanel, "exportMrl3Collection", icon="COLLECTION_COLOR_05")
        if not mhw_mrl3_toolpanel.exportMrl3Collection:
            col.separator()
            row = col.row(align=True)
            row.alert = True
            row.label(icon="ERROR", text="Must select a mrl3 collection first !!!")

    def execute(self, context):
        scene = context.scene
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel
        options = {"targetCollection": mhw_mrl3_toolpanel.exportMrl3Collection}

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        print(f"{i18n('Blender Version')} {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        success = exportMHWMrl3File(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW Mrl3 file.")
            if mhw_mrl3_toolpanel.modDirectory == "":
                setModDirectoryFromFilePath(self.filepath)
        else:
            self.report({"INFO"}, "Failed to export MHW Mrl3 file. Check Window > Toggle System Console for details.")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        return {"FINISHED"}


