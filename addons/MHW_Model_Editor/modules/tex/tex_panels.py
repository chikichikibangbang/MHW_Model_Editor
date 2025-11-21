import bpy
from .....common.types.framework import reg_order
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

@reg_order(20)
class OBJECT_PT_MHWTex_ToolsPanel(Panel):
    bl_label = "MHW Tex Tools"
    bl_idname = "OBJECT_PT_mhw_tex_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Mesh"
    # bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context is not None and "HIDE_MHW_MRL3_EDITOR_TAB" not in context.scene

    def draw(self, context):
        mhw_mrl3_toolpanel = context.scene.mhw_mrl3_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        # if bpy.app.version >= (4, 1, 0):
        #     row = col.row(align=True)
        #     row.emboss = "PULLDOWN_MENU"
        #     row.label(text="Drag files onto the 3D view to convert.")
        #     col.separator()

        split = col.row(align=True)
        row = split.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_tex.convert_mhw_tex_dds_files")
        row = split.row(align=True)
        row.scale_y = 1.1
        row.alignment = 'RIGHT'
        row.operator("mhw_tex.convert_settings", text="", icon='SETTINGS')

        col.separator()
        col.separator()
        col.separator()
        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Texture Directory")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_mrl3_toolpanel, "textureDirectory")

        col.separator()
        row = col.row(align=False)
        row.scale_y = 1.1
        row.operator("mhw_tex.convert_tex_directory")
        row.operator("mhw_tex.open_conversion_folder")

        col.separator()
        col.separator()
        col.separator()
        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Mod Directory")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_mrl3_toolpanel, "modDirectory")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_tex.copy_converted_tex")



