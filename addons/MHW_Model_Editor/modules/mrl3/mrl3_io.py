import bpy
from .blender_mrl3 import exportMHWMrl3File
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty
from bpy.types import Operator, OperatorFileListElement
from ..common.general_function import textColors, raiseWarning, splitNativesPath
from ...config import __addon_name__

def update_targetMrl3Collection(self,context):
    temp = bpy.data.screens.get("temp")
    browserSpace = None
    if temp != None:
        for area in temp.areas:
            for space in area.spaces:
                if type(space.params).__name__ == "FileSelectParams":
                    browserSpace = space
                    break
    if browserSpace != None:
        #print(browserSpace.params.filename)
        if ".mrl3" in self.targetCollection:
            browserSpace.params.filename = self.targetCollection.split(".mrl3")[0]+".mrl3"



class ExportMHWMrl3(Operator, ExportHelper):
    '''导出MHW MRL3文件'''
    bl_idname = "mhw_mrl3.export_mhw_mrl3"
    bl_label = "Export MHW Mrl3"
    bl_description = "Export MHW Mrl3 Files."
    bl_options = {'PRESET'}
    filename_ext = ".mrl3"
    targetCollection: StringProperty(
        name="",
        description="Set the mrl3 collection to be exported\nNote: mrl3 collections are blue and end with .mrl3",
        default="",
        update=update_targetMrl3Collection,
    )
    filter_glob: StringProperty(default="*.mrl3", options={'HIDDEN'})

    def invoke(self, context, event):
        if bpy.data.collections.get(self.targetCollection, None) == None:
            if bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection:
                self.targetCollection = bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection.name
                if self.targetCollection.endswith(".mrl3"):
                    self.filepath = self.targetCollection
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Mrl3 Collection:")
        layout.prop_search(self, "targetCollection", bpy.data, "collections", icon="COLLECTION_COLOR_05")

        if self.targetCollection in bpy.data.collections:
            collection = bpy.data.collections[self.targetCollection]
            if not collection.get("~TYPE") == "MHW_MRL3_COLLECTION" and not collection.name.endswith(".mrl3"):
                row = layout.row()
                row.alert = True
                row.label(icon="ERROR", text="Collection is not a mrl3 collection.")
        elif self.targetCollection == "":
            row = layout.row()
            row.alert = True
            row.label(icon="ERROR", text="Collection is not a mrl3 collection.")
        else:
            row = layout.row()
            row.label(icon="ERROR", text="Chosen collection doesn't exist.")
            row.alert = True

    def execute(self, context):
        # editorVersion = str(bl_info["version"][0]) + "." + str(bl_info["version"][1])
        # print(f"\n{textColors.BOLD}RE MDF Editor V{editorVersion}{textColors.ENDC}")
        print(f"\n{textColors.BOLD}MHW Model Editor{textColors.ENDC}")
        print(f"Blender Version {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        success = exportMHWMrl3File(self.filepath, self.targetCollection)
        if success:
            self.report({"INFO"}, "Successfully exported MHW Mrl3 file.")

            # if bpy.context.scene.mhw_mrl3_toolpanel.modDirectory == "":
            #     setModDirectoryFromFilePath(self.filepath)

            '''批量导出面板之后再说'''
            # # Add batch export entry to RE Toolbox if it doesn't already have one
            # if hasattr(bpy.types, "OBJECT_PT_re_tools_quick_export_panel"):
            #     if not any(item.path == self.filepath for item in
            #                bpy.context.scene.re_toolbox_toolpanel.batchExportList_items):
            #         newExportItem = bpy.context.scene.re_toolbox_toolpanel.batchExportList_items.add()
            #         newExportItem.fileType = "MDF"
            #         newExportItem.path = self.filepath
            #         newExportItem.mdfCollection = self.targetCollection
            #         print("Added path to RE Toolbox Batch Export list.")

            return {"FINISHED"}
        else:
            self.report({"INFO"}, "Failed to export MHW Mrl3 file. Check Window > Toggle System Console for details.")
            return {"CANCELLED"}


