import os
import shutil

import bpy
import time
from .....common.i18n.i18n import i18n
from bpy.types import Operator,OperatorFileListElement
from bpy.props import StringProperty,CollectionProperty
from bpy_extras.io_utils import ImportHelper
from ..common.message_functions import textColors, raiseWarning
from ...config import __addon_name__, editorVersion
from ..common.message_functions import showMessageBox, showErrorMessageBox
from .tex_function import convertTexDDSList
timeFormat = "%d"


class WM_OT_MHWTex_ConvertMHWDDSTexFile(Operator, ImportHelper):
    # bl_label = "Convert DDS & Tex Files"
    bl_label = "MHW Tex Conversion"
    bl_idname = "mhw_tex.convert_mhw_tex_dds_files"
    bl_description = "Opens a window to select textures to convert." \
                     "\nSelected .dds files will be converted to .tex, and .tex files will be converted to .dds." \
                     "\nIf you are using Blender 4.1 or higher, you can drag .tex or .dds files into the 3D view to convert them"
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
        lang = bpy.context.preferences.view.language
        fileList = [file.name for file in self.files]

        version = str(editorVersion[0]) + "." + str(editorVersion[1])
        print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
        print(f"{i18n('Blender Version')} {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
        print("https://github.com/chikichikibangbang/MHW_Model_Editor")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        print(f"\033[96m__________________________________\n{i18n('MHW Tex convert started.')}\033[0m")
        texConvertStartTime = time.time()

        successCount, failCount = convertTexDDSList(fileNameList=fileList, inDir=self.directory, outDir=self.directory,
                                                    addFolder=context.scene.mhw_mrl3_toolpanel.addConversionFolder,
                                                    addPrefix=context.scene.mhw_mrl3_toolpanel.addDXGIFormatPrefix,
                                                    languageCode=lang)

        texConvertEndTime = time.time()
        texConvertTime = texConvertEndTime - texConvertStartTime
        print(f"{i18n('Tex converted in')} {timeFormat % (texConvertTime * 1000)} ms.")

        print(f"\n{i18n('Conversion Info:')}")
        print(f"{i18n('Success Count:')} {successCount} / {len(fileList)}")
        print(f"{i18n('Failure Count:')} {failCount} / {len(fileList)}")

        print(f"\033[92m__________________________________\n{i18n('MHW Tex convert finished.')}\033[0m")

        if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
            try:
                bpy.ops.wm.console_toggle()
            except:
                pass

        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            showMessageBox(f"已转换 {successCount} / {len(fileList)} 张贴图.", title="MHW贴图转换")
            self.report({"INFO"}, f"已转换 {successCount} / {len(fileList)} 张贴图.")
        else:
            showMessageBox(f"Converted {successCount} / {len(fileList)} textures.", title="MHW Tex Conversion")
            self.report({"INFO"}, f"Converted {successCount} / {len(fileList)} textures.")

        return {"FINISHED"}

    def invoke(self, context, event):
        if self.directory:
            return self.execute(context)
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class WM_OT_MHWTex_ConvertSettings(Operator):
    bl_label = "Convert Settings"
    bl_description = "Detail settings for converting texture files"
    bl_idname = "mhw_tex.convert_settings"
    bl_options = {'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def check(self, context):
        # Important for changing options
        return True

    def draw(self, context):
        # box式绘制
        mhw_mrl3_toolpanel = context.scene.mhw_mrl3_toolpanel
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_mrl3_toolpanel, "addConversionFolder")
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_mrl3_toolpanel, "addDXGIFormatPrefix")


class WM_OT_MHWTex_ConvertFolderToTex(Operator):
    bl_label = "Convert Directory to Tex"
    bl_idname = "mhw_tex.convert_tex_directory"
    bl_description = "Converts all .dds files in the chosen directory to .tex." \
                     "\nConverted files will be saved inside a folder called \"Converted_MHW_Tex\"." \
                     "\nSave .dds with BC7 sRGB for color type textures, BC5 Linear for normal and BC7 Linear for anything else"

    @classmethod
    def poll(cls, context):
        return context.scene.mhw_mrl3_toolpanel.textureDirectory != ""

    def execute(self, context):
        lang = bpy.context.preferences.view.language
        # TODO Add support for other image formats, should be doable with texconv
        texDir = os.path.realpath(context.scene.mhw_mrl3_toolpanel.textureDirectory)
        convertedDir = os.path.join(texDir, "Converted_MHW_Tex")
        if os.path.isdir(texDir):
            otherImageConversionList = []
            ddsConversionList = []

            for entry in os.scandir(texDir):
                if entry.is_file() and entry.name.lower().endswith(".dds"):
                    ddsConversionList.append(entry.name)

            if ddsConversionList != []:
                version = str(editorVersion[0]) + "." + str(editorVersion[1])
                print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
                print(f"{i18n('Blender Version')} {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
                print("https://github.com/chikichikibangbang/MHW_Model_Editor")

                if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                    try:
                        bpy.ops.wm.console_toggle()
                    except:
                        pass

                print(f"\033[96m__________________________________\n{i18n('MHW Tex convert started.')}\033[0m")
                texConvertStartTime = time.time()

                successCount, failCount = convertTexDDSList(fileNameList=ddsConversionList, inDir=texDir, outDir=convertedDir, languageCode=lang)

                texConvertEndTime = time.time()
                texConvertTime = texConvertEndTime - texConvertStartTime
                print(f"{i18n('Tex converted in')} {timeFormat % (texConvertTime * 1000)} ms.")

                print(f"\n{i18n('Conversion Info:')}")
                print(f"{i18n('Success Count:')} {successCount} / {len(ddsConversionList)}")
                print(f"{i18n('Failure Count:')} {failCount} / {len(ddsConversionList)}")

                print(f"\033[92m__________________________________\n{i18n('MHW Tex convert finished.')}\033[0m")

                if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                    try:
                        bpy.ops.wm.console_toggle()
                    except:
                        pass

                if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                    showMessageBox(f"已转换 {successCount} / {len(ddsConversionList)} 张贴图.", title="MHW贴图转换")
                    self.report({"INFO"}, f"已转换 {successCount} / {len(ddsConversionList)} 张贴图.")
                else:
                    showMessageBox(f"Converted {successCount} / {len(ddsConversionList)} textures.", title="MHW Tex Conversion")
                    self.report({"INFO"}, f"Converted {successCount} / {len(ddsConversionList)} textures.")

                # self.report({"INFO"}, f"Converted {str(successCount)} textures.")
                # if bpy.context.scene.mhw_mrl3_toolpanel.openConvertedFolder:
                #     os.startfile(convertedDir)

            else:
                showErrorMessageBox(i18n("There are no .dds files in provided directory."))
        else:
            showErrorMessageBox(i18n("Provided texture directory is not a directory or does not exist."))
        return {"FINISHED"}


class WM_OT_MHWTex_OpenConversionFolder(Operator):
    bl_label = "Open Conversion Folder"
    bl_idname = "mhw_tex.open_conversion_folder"
    bl_description = "Open the folder containing the converted texture files in File Explorer"

    @classmethod
    def poll(cls, context):
        return context.scene.mhw_mrl3_toolpanel.textureDirectory != ""

    def execute(self, context):
        texDir = os.path.realpath(context.scene.mhw_mrl3_toolpanel.textureDirectory)
        convertedDir = os.path.join(texDir, "Converted_MHW_Tex")

        if os.path.isdir(texDir):
            if not os.path.exists(convertedDir):
                try:
                    os.makedirs(convertedDir)
                except:
                    pass

            os.startfile(convertedDir)
        else:
            showErrorMessageBox(i18n("Provided texture directory is not a directory or does not exist."))
        return {'FINISHED'}



class WM_OT_MHWTex_CopyConvertedTextures(Operator):
    bl_label = "Copy Converted Tex Files"
    bl_idname = "mhw_tex.copy_converted_tex"
    bl_options = {'UNDO'}
    bl_description = "Copies .tex files in conversion folder into the specified mod \"nativePC\" directory." \
                     "\nCopied files will be placed at the paths set in the active mrl3 collection"

    # @classmethod
    # def poll(cls, context):
    #     return context.scene.mhw_mrl3_toolpanel.textureDirectory != "" and context.scene.mhw_mrl3_toolpanel.modDirectory != ""

    def execute(self, context):
        lang = bpy.context.preferences.view.language
        # 确保贴图路径和mod路径都已被设置
        if context.scene.mhw_mrl3_toolpanel.textureDirectory == "" or context.scene.mhw_mrl3_toolpanel.modDirectory == "":
            showErrorMessageBox(i18n("Please set texture and mod directory first."))
            return {'CANCELLED'}

        mrl3Collection = context.scene.mhw_mrl3_toolpanel.mrl3Collection
        if mrl3Collection == None:  # 确保存在激活的mrl3集合
            showErrorMessageBox(i18n("Please set active mrl3 collection first."))
            return {'CANCELLED'}

        texDir = os.path.realpath(context.scene.mhw_mrl3_toolpanel.textureDirectory)
        modDir = os.path.realpath(context.scene.mhw_mrl3_toolpanel.modDirectory)
        convertedDir = os.path.join(texDir, "Converted_MHW_Tex")
        pathDict = {}
        copyCount = 0

        # if mrl3Collection != None and os.path.exists(modDir):
        # if os.path.exists(modDir):
        if os.path.isdir(modDir):
            for obj in mrl3Collection.all_objects:
                if obj.get("~TYPE") == "MHW_MRL3_MATERIAL":
                    for mapItem in obj.mhw_mrl3_material.mapList_items:
                        pathDict[os.path.split(mapItem.value)[1]] = mapItem.value
        else:
            showErrorMessageBox(i18n("Provided mod directory is not a directory or does not exist."))
            return {'CANCELLED'}

        if os.path.isdir(convertedDir):
            version = str(editorVersion[0]) + "." + str(editorVersion[1])
            print(f"\n{textColors.BOLD}MHW Model Editor V{version}{textColors.ENDC}")
            print(f"{i18n('Blender Version')} {bpy.app.version[0]}.{bpy.app.version[1]}.{bpy.app.version[2]}")
            print("https://github.com/chikichikibangbang/MHW_Model_Editor")

            if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                try:
                    bpy.ops.wm.console_toggle()
                except:
                    pass

            print(f"\033[96m__________________________________\n{i18n('MHW Tex copy started.')}\033[0m")

            for entry in os.scandir(convertedDir):
                if entry.is_file() and os.path.splitext(entry.name)[0] in pathDict:
                    path = os.path.join(convertedDir, entry.name)
                    outPath = os.path.realpath(os.path.join(modDir, pathDict[os.path.splitext(entry.name)[0]] +
                                                            os.path.splitext(entry.name)[1]))
                    os.makedirs(os.path.split(outPath)[0], exist_ok=True)
                    shutil.copyfile(path, outPath)
                    if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                        print(f"已复制 {os.path.split(path)[1]} 到 {outPath}")
                    else:
                        print(f"Copied {os.path.split(path)[1]} to {outPath}")
                    copyCount += 1

            print(f"\033[92m__________________________________\n{i18n('MHW Tex copy finished.')}\033[0m")

            if bpy.context.preferences.addons[__addon_name__].preferences.showConsole:
                try:
                    bpy.ops.wm.console_toggle()
                except:
                    pass

            if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                showMessageBox(f"已复制 {copyCount} 张贴图到mod目录.", title="MHW贴图复制")
                self.report({"INFO"}, f"已复制 {copyCount} 张贴图到mod目录.")
            else:
                showMessageBox(f"Copied {copyCount} textures to mod directory.", title="MHW Tex Copy")
                self.report({"INFO"}, f"Copied {copyCount} textures to mod directory.")
        # else:
        #     self.report({"ERROR"}, f"Texture directory does not exist.")
        else:
            showErrorMessageBox(i18n("Provided texture directory is not a directory or does not exist."))

        return {"FINISHED"}




# class WM_OT_MHWTex_CopyConvertedTextures(Operator):
#     bl_label = "Copy Converted Tex Files"
#     bl_idname = "mhw_tex.copy_converted_tex"
#     bl_options = {'UNDO'}
#     bl_description = "Copies .tex files in conversion folder into the specified mod \"nativePC\" directory." \
#                      "\nCopied files will be placed at the paths set in the active mrl3 collection." \
#                      "\nThe button will only be triggered if texture and mod directory both exists"
#
#     @classmethod
#     def poll(cls, context):
#         return context.scene.mhw_mrl3_toolpanel.textureDirectory != "" and context.scene.mhw_mrl3_toolpanel.modDirectory != ""
#
#     def execute(self, context):
#         texDir = os.path.realpath(context.scene.mhw_mrl3_toolpanel.textureDirectory)
#         modDir = os.path.realpath(context.scene.mhw_mrl3_toolpanel.modDirectory)
#         convertedDir = os.path.join(texDir, "Converted_MHW_Tex")
#         mrl3Collection = bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection
#         pathDict = {}
#         copyCount = 0
#
#         if mrl3Collection != None and os.path.exists(modDir):
#             for obj in mrl3Collection.all_objects:
#                 if obj.get("~TYPE") == "MHW_MRL3_MATERIAL":
#                     for mapItem in obj.mhw_mrl3_material.mapList_items:
#                         pathDict[os.path.split(mapItem.value)[1]] = mapItem.value
#         if os.path.isdir(convertedDir):
#             for entry in os.scandir(convertedDir):
#                 if entry.is_file() and os.path.splitext(entry.name)[0] in pathDict:
#                     path = os.path.join(convertedDir, entry.name)
#                     outPath = os.path.realpath(os.path.join(modDir, pathDict[os.path.splitext(entry.name)[0]] +
#                                                             os.path.splitext(entry.name)[1]))
#                     os.makedirs(os.path.split(outPath)[0], exist_ok=True)
#                     shutil.copyfile(path, outPath)
#                     print(f"Copied {os.path.split(path)[1]} to {outPath}")
#                     copyCount += 1
#             self.report({"INFO"}, f"Copied {str(copyCount)} textures to mod directory.")
#         else:
#             self.report({"ERROR"}, f"Texture directory does not exist.")
#
#         return {"FINISHED"}