import bpy
from .....common.types.framework import reg_order
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )

@reg_order(18)
class OBJECT_PT_Mod3_MeshToolsPanel(Panel):
    bl_label = "MHW Mesh Tools"
    bl_idname = "OBJECT_PT_mod3_mesh_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Mesh"
    # bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context is not None and "HIDE_MHW_MRL3_EDITOR_TAB" not in context.scene

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        # row = col.row(align=True)
        # row.scale_y = 1.1
        # row.operator("mhw_mod3.create_mod3_collection")
        #
        # col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.rename_meshes")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.delete_loose_geometry")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.remove_empty_vertex_groups")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.limit_total_normalize")