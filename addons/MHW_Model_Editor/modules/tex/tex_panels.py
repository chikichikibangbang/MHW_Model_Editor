import bpy
from .....common.types.framework import reg_order
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

@reg_order(2)
class OBJECT_PT_Mrl3TexConversionPanel(Panel):
    bl_label = "MHW Tex Conversion"
    bl_idname = "OBJECT_PT_mrl3_tex_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Model Editor"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context is not None and "HIDE_MHW_MRL3_EDITOR_TAB" not in context.scene

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel

        layout.operator("mhw_tex.convert_mhw_tex_dds_files")

        layout.label(text="Convert Image Directory")
        layout.prop(mhw_mrl3_toolpanel, "textureDirectory")
        # layout.operator("mhw_tex.convert_tex_directory")
        # layout.prop(mhw_mrl3_toolpanel, "openConvertedFolder")
        # layout.operator("mhw_tex.copy_converted_tex")

        # if hasattr(bpy.types, "OBJECT_PT_re_pak_panel"):
        #     try:
        #         layout.operator("re_asset.create_pak_patch")
        #     except:
        #         pass

