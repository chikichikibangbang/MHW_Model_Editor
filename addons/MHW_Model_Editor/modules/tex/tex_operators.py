from bpy.types import Operator,OperatorFileListElement
from bpy.props import StringProperty,CollectionProperty
from bpy_extras.io_utils import ImportHelper
from ..common.blender_utils import showMessageBox
from .tex_function import convertTexDDSList

class WM_OT_Tex_ConvertMHWDDSTexFile(Operator, ImportHelper):
    bl_label = "Convert DDS/Tex Files"
    bl_idname = "mhw_tex.convert_mhw_tex_dds_files"
    bl_description = "Opens a window to select textures to convert. Selected .dds files will be converted to .tex and tex files will be converted to dds.\nIf you are using Blender 4.1 or higher, you can drag .tex or .dds files into the 3D view to convert them"
    filter_glob: StringProperty(default="*.dds;*.tex", options={'HIDDEN'})
    files: CollectionProperty(
        name="File Path",
        type=OperatorFileListElement,
    )
    directory: StringProperty(
        subtype='DIR_PATH',
        options={"SKIP_SAVE"}
    )

    def execute(self, context):
        fileList = [file.name for file in self.files]
        successCount, failCount = convertTexDDSList(fileNameList=fileList, inDir=self.directory, outDir=self.directory)
        showMessageBox(f"Converted {str(successCount)} textures.", title="Texture Conversion")
        self.report({"INFO"}, f"Converted {str(successCount)} textures.")

        return {"FINISHED"}

    def invoke(self, context, event):
        if self.directory:
            return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


# class WM_OT_Tex_ConvertMHWDDSFolderToTex(Operator):
#     bl_label = "Convert Directory to Tex"
#     bl_idname = "mhw_tex.convert_tex_directory"
#     bl_description = "Converts all dds files in the chosen directory to tex" \
#                      "\nConverted files will be saved inside a folder called \"converted\"" \
#                      "\nSave dds files with compression settings set to BC7 sRGB for albedo/color textures and BC7 Linear for anything else"
#
#     def execute(self, context):
#         # TODO Add support for other image formats, should be doable with texconv
#         # Also add streaming texture generation, should also be doable with texconv's resize option
#         texDir = os.path.realpath(bpy.context.scene.mhw_mrl3_toolpanel.textureDirectory)
#         convertedDir = os.path.join(texDir, "converted")
#         if os.path.isdir(texDir):
#             otherImageConversionList = []
#             ddsConversionList = []
#
#             for entry in os.scandir(texDir):
#                 if entry.is_file() and entry.name.lower().endswith(".dds"):
#                     ddsConversionList.append(entry.name)
#
#             if ddsConversionList != []:
#                 successCount, failCount = convertTexDDSList(fileNameList=ddsConversionList, inDir=texDir,
#                                                             outDir=convertedDir,
#                                                             gameName=bpy.context.scene.re_mdf_toolpanel.activeGame,
#                                                             createStreamingTex=False)
#                 self.report({"INFO"}, f"Converted {str(successCount)} textures")
#                 if bpy.context.scene.re_mdf_toolpanel.openConvertedFolder:
#                     os.startfile(convertedDir)
#             else:
#                 showErrorMessageBox("No .dds files in provided directory")
#         else:
#             showErrorMessageBox("Provided Image Directory is not a directory or does not exist")
#         return {"FINISHED"}
