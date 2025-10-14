import bpy
from .....common.types.framework import reg_order
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

# @reg_order(20)
# class OBJECT_PT_Mrl3_TexToolsPanel(Panel):
#     bl_label = "MHW Tex Conversion"
#     bl_idname = "OBJECT_PT_mrl3_tex_tools_panel"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "MHW Mesh"
#     # bl_context = "objectmode"
#
#     @classmethod
#     def poll(self, context):
#         return context is not None and "HIDE_MHW_MRL3_EDITOR_TAB" not in context.scene
#
#     def draw(self, context):
#         mhw_mrl3_toolpanel = context.scene.mhw_mrl3_toolpanel
#
#         layout = self.layout
#         box = layout.box()
#         col = box.column(align=True)
#
#         row = col.row(align=True)
#         row.scale_y = 1.1
#         row.operator("mhw_tex.convert_mhw_tex_dds_files")
#
#         col.separator()
#         col.separator()
#         col.separator()
#         row = col.row(align=True)
#         # row.scale_y = 0.75
#         row.label(text="Convert Image Directory")
#
#         col.separator()
#         row = col.row(align=True)
#         row.scale_y = 1.2
#         row.prop(mhw_mrl3_toolpanel, "textureDirectory")
#
#         col.separator()
#         row = col.row(align=True)
#         row.scale_y = 1.1
#         row.operator("mhw_tex.convert_tex_directory")
#
#
#
#         # layout.operator("mhw_tex.convert_mhw_tex_dds_files")
#         #
#         # layout.label(text="Convert Image Directory")
#         # layout.prop(mhw_mrl3_toolpanel, "textureDirectory")
#         # # layout.operator("mhw_tex.convert_tex_directory")
#         # # layout.prop(mhw_mrl3_toolpanel, "openConvertedFolder")
#         # # layout.operator("mhw_tex.copy_converted_tex")
#         #
#         # # if hasattr(bpy.types, "OBJECT_PT_re_pak_panel"):
#         # #     try:
#         # #         layout.operator("re_asset.create_pak_patch")
#         # #     except:
#         # #         pass
#


