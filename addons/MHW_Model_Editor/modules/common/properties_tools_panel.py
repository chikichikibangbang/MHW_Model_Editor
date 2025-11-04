from .....common.types.framework import reg_order
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


# @reg_order(200)
# class OBJECT_PT_MHW_ToolsPanel_PropertiesPanel(Panel):
#     bl_label = "MHW Tools"
#     bl_idname = "OBJECT_PT_mhw_tools_panel_properties_panel"
#     bl_space_type = "PROPERTIES"
#     bl_region_type = "WINDOW"
#     bl_category = "MHW Tools"
#     bl_context = "texture"
#
#     @classmethod
#     def poll(self, context):
#         # return context is not None and "HIDE_MHW_Mrl3_EDITOR_TAB" not in context.scene
#         return context is not None
#
#     def draw(self, context):
#         layout = self.layout
#         split = layout.split(factor=0.33)
#
#         box1 = split.box()
#         box1_split = box1.split(factor=0.33)
#         box1_1 = box1_split.box()
#         box1_1.label(text="Box 666 1")
#
#         box1_2 = box1_split.split().box()
#         box1_2.label(text="Box 666 2")
#
#         box1_3 = box1_split.box()
#         box1_3.label(text="Box 666 3")
#
#
#         box2 = split.split().box()
#         box2_split = box2.split(factor=0.33)
#         box2_1 = box2_split.box()
#         box2_1.label(text="Box 666 1")
#
#         box2_2 = box2_split.split().box()
#         box2_2.label(text="Box 666 2")
#
#         box2_3 = box2_split.box()
#         box2_3.label(text="Box 666 3")
#
#         box3 = split.box()
#         box3_split = box3.split(factor=0.33)
#         box3_1 = box3_split.box()
#         box3_1.label(text="Box 666 1")
#
#         box3_2 = box3_split.split().box()
#         box3_2.label(text="Box 666 2")
#
#         box3_3 = box3_split.box()
#         box3_3.label(text="Box 666 3")







        # mhw_mrl3_toolpanel = context.scene.mhw_mrl3_toolpanel
        # layout = self.layout
        # box1 = layout.box()
        # box2 = layout.box()
        # col1 = box1.column(align=True)
        # col2 = box2.column(align=True)
        #
        # row = col1.row(align=False)
        # row.scale_y = 1.1
        # row.operator("mhw_mod3.import_mhw_mod3", text="Import Mod3")
        # row.operator("mhw_mod3.export_mhw_mod3", text="Export Mod3")
        #
        # col1.separator()
        # row = col1.row(align=False)
        # row.scale_y = 1.1
        # row.operator("mhw_mrl3.import_mhw_mrl3", text="Import Mrl3")
        # row.operator("mhw_mrl3.export_mhw_mrl3", text="Export Mrl3")
        #
        # row = col2.row(align=True)
        # # row.scale_y = 0.75
        # row.label(text="Active Mrl3 Collection")
        #
        # col2.separator()
        # row = col2.row(align=True)
        # row.scale_y = 1.2
        # row.prop(mhw_mrl3_toolpanel, "mrl3Collection", icon="COLLECTION_COLOR_05")
        #
        # col2.separator()
        # row = col2.row(align=True)
        # row.scale_y = 1.1
        # row.operator("mhw_mrl3.create_mrl3_collection")
        #
        # col2.separator()
        # row = col2.row(align=True)
        # row.scale_y = 1.1
        # row.operator("mhw_mrl3.reindex_mrl3_materials")





#         layout = self.layout
#         scene = context.scene
#         mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel
#         layout.operator("mhw_mrl3.create_mrl3_collection")
#         layout.label(text="Active Mrl3 Collection")
#         layout.prop_search(mhw_mrl3_toolpanel, "mrl3Collection", bpy.data, "collections", icon="COLLECTION_COLOR_05")
#         layout.operator("mhw_mrl3.reindex_mrl3_materials")
# #         layout.label(text="Material Preset")
# #         layout.prop(mhw_mrl3_toolpanel, "materialPresets")
# #         layout.operator("mhw_mrl3.add_preset_material")
# #
# #         layout.operator("mhw_mrl3.save_selected_as_preset")
# #         layout.operator("mhw_mrl3.open_preset_folder")
#         layout.label(text="Apply Mrl3 to Mod3")
#         layout.label(text="Mod3 Collection")
#         layout.prop_search(mhw_mrl3_toolpanel, "mod3Collection", bpy.data, "collections", icon="COLLECTION_COLOR_01")
#         layout.label(text="Mod Directory")
#         layout.prop(mhw_mrl3_toolpanel, "modDirectory")
#         layout.operator("mhw_mrl3.apply_mrl3")