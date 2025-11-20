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
        box1 = layout.box()
        box2 = layout.box()
        col1 = box1.column(align=True)
        col2 = box2.column(align=True)

        row = col1.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.create_mod3_collection")

        col1.separator()
        row = col1.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.create_nested_collections")

        col1.separator()
        row = col1.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.rename_meshes")

        # col1.separator()
        # row = col1.row(align=True)
        # row.scale_y = 1.1
        # row.operator("mhw_mod3.set_mesh_properties")

        col1.separator()
        row = col1.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.set_mesh_group_id")



        row = col2.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.bake_normal_to_vertex_color")

        col2.separator()
        row = col2.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.delete_loose_geometry")

        col2.separator()
        row = col2.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.remove_empty_vertex_groups")

        col2.separator()
        row = col2.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_mod3.limit_total_normalize")

        # col2.separator()
        # row = col2.row(align=True)
        # row.scale_y = 1.1
        # row.operator("mhw_model.batch_exporter")