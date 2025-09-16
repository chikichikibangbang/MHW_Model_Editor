import bpy
import os
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty
from bpy.types import Operator, OperatorFileListElement
from ..common.general_function import textColors, raiseWarning, splitNativesPath
from ...config import __addon_name__

class ImportMHWCTC(Operator, ImportHelper):
    '''导入MHW CTC文件'''
    bl_idname = "mhw_ctc.import_mhw_ctc"
    bl_label = "Import MHW CTC"
    bl_description = "Import MHW CTC Files.\nNOTE: Before importing ctc, make sure that at least one mod3 armature exists in the current scene"
    bl_options = {"PRESET", "REGISTER", "UNDO"}
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
    )
    filename_ext = ".ctc"
    filter_glob: StringProperty(default="*.ctc", options={'HIDDEN'})
    loadCCL: BoolProperty(
        name="Load CCL File",
        description="When importing ctc file, also import ccl file with the same file name under current path",
        default=True)
    # targetArmature: StringProperty(
    #     name="",
    #     description="The armature to attach ctc objects to.\nNOTE: If some bones that are used by the ctc file are missing on the armature, corresponding ctc nodes using those bones won't be imported",
    #     default="")
    # mergeChain: StringProperty(
    #     name="",
    #     description="Merges the imported ctc objects with an existing ctc collection",
    #     default="")

    def invoke(self, context, event):
        # armature = None
        # if bpy.data.armatures.get(self.targetArmature, None) == None:
        #     try:  # Pick selected armature if one is selected
        #         if armature == None and bpy.context.active_object != None and bpy.context.active_object.type == "ARMATURE":
        #             armature = bpy.context.active_object
        #     except:
        #         pass
        #     if armature == None:
        #         for obj in bpy.context.scene.objects:
        #             if obj.type == "ARMATURE":
        #                 armature = obj
        #
        #     if armature != None:
        #         self.targetArmature = armature.data.name

        # scene = context.scene
        # mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel

        # if not bpy.context.scene.get("MHWCTCDefaultImportSettingsLoaded"):
        #     setCTCImportDefaults(self)

        if self.directory:
            if bpy.context.preferences.addons[__addon_name__].preferences.dragDropImportOptions:
                return context.window_manager.invoke_props_dialog(self)
            else:
                return self.execute(context)

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel
        layout.prop(self, "loadCCL")
        layout.label(text="Target Armature:")
        # layout.prop_search(self, "targetArmature", bpy.data, "armatures")
        # layout.prop_search(mhw_ctc_toolpanel, "importCTCArmature", bpy.data, "objects", icon="OUTLINER_OB_ARMATURE")
        layout.prop(mhw_ctc_toolpanel, "importCTCArmature", icon="OUTLINER_OB_ARMATURE")
        layout.label(text="Merge With CTC Collection:")
        # layout.prop_search(self, "mergeChain", bpy.data, "collections", icon="COLLECTION_COLOR_02")
        layout.prop(mhw_ctc_toolpanel, "importCTCCollection", icon="COLLECTION_COLOR_02")


    def execute(self, context):
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel
        options = {"targetArmature": mhw_ctc_toolpanel.importCTCArmature,
                   "mergeCollection": mhw_ctc_toolpanel.importCTCCollection, "loadCCL": self.loadCCL}

        print(f"\n{textColors.BOLD}MHW Model Editor{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        # bpy.context.scene["MHWCTCDefaultImportSettingsLoaded"] = 1

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        success = True
        # success = importCTCFile(self.filepath, options)
        if success:
            if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                try:
                    bpy.ops.wm.console_toggle()
                except:
                    pass
            self.report({"INFO"}, "Successfully imported MHW CTC file.")
            return {"FINISHED"}
        else:
            self.report({"INFO"}, "Failed to import MHW CTC file. Check Window > Toggle System Console for details.")
            return {"CANCELLED"}



class ExportMHWCTC(Operator, ExportHelper):
    bl_idname = "mhw_ctc.export_mhw_ctc"
    bl_label = "Export MHW CTC"
    bl_description = "Export MHW CTC Files"
    bl_options = {'PRESET'}
    filename_ext = ".ctc"
    filter_glob: StringProperty(default="*.ctc*", options={'HIDDEN'})
    # targetCollection: StringProperty(
    #     name="",
    #     description="Set the ctc collection to be exported",
    #     default="")
    exportCCL: BoolProperty(
        name="Export CCL File",
        description="When exporting ctc file, also export ccl file with the same file name into current path",
        default=True)


    def invoke(self, context, event):
        # if bpy.data.collections.get(self.targetCollection, None) == None:
        #     if bpy.data.collections.get(bpy.context.scene.ctc_toolpanel.ctcCollection):
        #         self.targetCollection = bpy.context.scene.ctc_toolpanel.ctcCollection
        #         if ".ctc" in self.targetCollection:
        #             self.filepath = self.targetCollection.split(".ctc")[0] + ".ctc"

        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel

        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel
        layout.prop(self, "exportCCL")
        layout.label(text="CTC Collection:")
        # layout.prop_search(self, "targetCollection", bpy.data, "collections", icon="COLLECTION_COLOR_02")
        layout.prop(mhw_ctc_toolpanel, "exportCTCCollection", icon="COLLECTION_COLOR_02")

    def execute(self, context):
        scene = context.scene
        mhw_ctc_toolpanel = scene.mhw_ctc_toolpanel
        options = {"targetCollection": mhw_ctc_toolpanel.exportCTCCollection, "exportCCL": self.exportCCL}
        success = True
        # success = exportCTCFile(self.filepath, options)
        if success:
            self.report({"INFO"}, "Successfully exported MHW CTC file.")
        else:
            self.report({"INFO"}, "Failed to export MHW CTC file. Check Window > Toggle System Console for details.")
        return {"FINISHED"}