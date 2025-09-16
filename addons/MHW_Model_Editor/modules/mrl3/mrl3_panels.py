import bpy

from ...config import __addon_name__
from .....common.i18n.i18n import i18n
from .....common.types.framework import reg_order
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


def tag_redraw(context, space_type="PROPERTIES", region_type="WINDOW"):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.spaces[0].type == space_type:
                for region in area.regions:
                    if region.type == region_type:
                        region.tag_redraw()




@reg_order(0)
class OBJECT_PT_Mrl3ObjectModePanel(Panel):
    bl_label = "MHW Mrl3 Tools"
    bl_idname = "OBJECT_PT_mrl3_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Model Editor"
    bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        return context is not None and "HIDE_MHW_Mrl3_EDITOR_TAB" not in context.scene

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel
        layout.operator("mhw_mrl3.create_mrl3_collection")
        layout.label(text="Active Mrl3 Collection")
        layout.prop_search(mhw_mrl3_toolpanel, "mrl3Collection", bpy.data, "collections", icon="COLLECTION_COLOR_05")
        layout.operator("mhw_mrl3.reindex_mrl3_materials")
#         layout.label(text="Material Preset")
#         layout.prop(mhw_mrl3_toolpanel, "materialPresets")
#         layout.operator("mhw_mrl3.add_preset_material")
#
#         layout.operator("mhw_mrl3.save_selected_as_preset")
#         layout.operator("mhw_mrl3.open_preset_folder")
        layout.label(text="Apply Mrl3 to Mod3")
        layout.label(text="Mod3 Collection")
        layout.prop_search(mhw_mrl3_toolpanel, "mod3Collection", bpy.data, "collections", icon="COLLECTION_COLOR_01")
        layout.label(text="Mod Directory")
        layout.prop(mhw_mrl3_toolpanel, "modDirectory")
        layout.operator("mhw_mrl3.apply_mrl3")

@reg_order(1)
class OBJECT_PT_Mrl3MaterialLoadSettingsPanel(Panel):
    bl_label = "Mrl3 Load Settings"
    bl_idname = "OBJECT_PT_mrl3_material_load_settings_panel"
    bl_parent_id = "OBJECT_PT_mrl3_tools_panel"  # Specify the ID of the parent panel
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Model Editor"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel
        split = layout.split(factor=0.025)  # Indent list slightly to make it more clear it's a part of a sub panel
        col1 = split.column()
        col2 = split.column()
        col2.alignment = 'RIGHT'
        col2.prop(mhw_mrl3_toolpanel, "reloadCachedTextures")
        col2.prop(mhw_mrl3_toolpanel, "loadUnusedTextures")
        col2.prop(mhw_mrl3_toolpanel, "loadUnusedProps")
        col2.prop(mhw_mrl3_toolpanel, "useBackfaceCulling")



# @reg_order(2)
# class OBJECT_PT_Mrl3TexConversionPanel(Panel):
#     bl_label = "MHW Tex Conversion"
#     bl_idname = "OBJECT_PT_mrl3_tex_tools_panel"
#     bl_space_type = "VIEW_3D"
#     bl_region_type = "UI"
#     bl_category = "MHW Model Editor"
#     bl_context = "objectmode"
#
#     @classmethod
#     def poll(self, context):
#         return context is not None and "HIDE_MHW_MRL3_EDITOR_TAB" not in context.scene
#
#     def draw(self, context):
#         layout = self.layout
#         scene = context.scene
#         mhw_mrl3_toolpanel = scene.mhw_mrl3_toolpanel
#
#         layout.operator("mhw_tex.convert_mhw_tex_dds_files")
#
#         layout.label(text="Convert Image Directory")
#         layout.prop(mhw_mrl3_toolpanel, "textureDirectory")
#         # layout.operator("mhw_tex.convert_tex_directory")
#         # layout.prop(mhw_mrl3_toolpanel, "openConvertedFolder")
#         # layout.operator("mhw_tex.copy_converted_tex")
#
#         # if hasattr(bpy.types, "OBJECT_PT_re_pak_panel"):
#         #     try:
#         #         layout.operator("re_asset.create_pak_patch")
#         #     except:
#         #         pass


@reg_order(3)
class OBJECT_PT_Mrl3MaterialPanel(Panel):
    bl_label = "MHW Mrl3 Material Settings"
    bl_idname = "OBJECT_PT_mrl3_material_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "MHW Mrl3 Material Settings"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context and context.object.mode == "OBJECT" and context.active_object.get("~TYPE", None) == "MHW_MRL3_MATERIAL" and not "HIDE_MHW_MRL3_EDITOR_PANEL" in context.scene

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mhw_mrl3_material = obj.mhw_mrl3_material

        split = layout.split(factor=0.025)
        col1 = split.column()
        col2 = split.column()
        # col2.label(text=f"Material Shader Hash: {mhw_mrl3_material.shaderHash1} {mhw_mrl3_material.shaderHash2}")
        if mhw_mrl3_material.mastermaterialType != "":
            col2.label(text=f"Master Material Type: {mhw_mrl3_material.mastermaterialType}")
        else:
            col2.label(text=f"Master Material Type: Unknown")
        split = layout.split(factor=0.01)
        col3 = split.column()
        col4 = split.column()
        col4.alignment = 'RIGHT'
        col4.use_property_split = True

        col4.prop(mhw_mrl3_material, "materialName")
        # col4.prop(mhw_mrl3_material, "shaderHash1")
        # col4.prop(mhw_mrl3_material, "shaderHash2")
        col4.prop(mhw_mrl3_material, "surfaceDirection")

        col4.prop(mhw_mrl3_material, "alphaCoef")
        col4.prop(mhw_mrl3_material, "linkedMaterial")
#
#
# class OBJECT_PT_MDFFlagsPanel(Panel):
#     bl_label = "Flags"
#     bl_idname = "OBJECT_PT_mdf_material_flags_panel"
#     bl_parent_id = "OBJECT_PT_mdf_material_panel"  # Specify the ID of the parent panel
#     bl_space_type = 'PROPERTIES'
#     bl_region_type = 'WINDOW'
#     bl_options = {'DEFAULT_CLOSED'}
#
#     def draw(self, context):
#         layout = self.layout
#         obj = context.active_object
#         flags = obj.re_mdf_material.flags
#         split = layout.split(factor=0.025)  # Indent list slightly to make it more clear it's a part of a sub panel
#         col1 = split.column()
#         col2 = split.column()
#         col2.alignment = 'RIGHT'
#         col2.prop(flags, "ver32Unknown")
#         col2.prop(flags, "ver32Unknown1")
#         col2.prop(flags, "ver32Unknown2")
#         col2.prop(flags, "flagIntValue")
#
#         col2.prop(flags, "BaseTwoSideEnable")
#         col2.prop(flags, "BaseAlphaTestEnable")
#         col2.prop(flags, "ShadowCastDisable")
#         col2.prop(flags, "VertexShaderUsed")
#         col2.prop(flags, "EmissiveUsed")
#         col2.prop(flags, "TessellationEnable")
#         col2.prop(flags, "EnableIgnoreDepth")
#         col2.prop(flags, "AlphaMaskUsed")
#         col2.prop(flags, "ForcedTwoSideEnable")
#         col2.prop(flags, "TwoSideEnable")
#         col2.prop(flags, "TessFactor")
#         col2.prop(flags, "PhongFactor")
#         col2.prop(flags, "RoughTransparentEnable")
#         col2.prop(flags, "ForcedAlphaTestEnable")
#         col2.prop(flags, "AlphaTestEnable")
#         col2.prop(flags, "SSSProfileUsed")
#         col2.prop(flags, "EnableStencilPriority")
#         col2.prop(flags, "RequireDualQuaternion")
#         col2.prop(flags, "PixelDepthOffsetUsed")
#         col2.prop(flags, "NoRayTracing")
#
#
@reg_order(4)
class OBJECT_PT_Mrl3MaterialMapListPanel(Panel):
    bl_label = "Map List"
    bl_idname = "OBJECT_PT_mrl3_material_maplist_panel"
    bl_parent_id = "OBJECT_PT_mrl3_material_panel"  # Specify the ID of the parent panel
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(self, context):
        obj = context.active_object
        mhw_mrl3_material = obj.mhw_mrl3_material
        return mhw_mrl3_material.mapList_items

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mhw_mrl3_material = obj.mhw_mrl3_material
        rows = 6
        split = layout.split(factor=0.025)  # Indent list slightly to make it more clear it's a part of a sub panel
        col1 = split.column()
        col2 = split.column()
        col2.label(text=f"Map Count: {str(len(obj.mhw_mrl3_material.mapList_items))}")

        if len(mhw_mrl3_material.mapList_items) < 6:
            rows = len(mhw_mrl3_material.mapList_items)

        col2.template_list(
            listtype_name="MESH_UL_Mrl3MapList",
            list_id="",
            dataptr=mhw_mrl3_material,
            propname="mapList_items",
            active_dataptr=mhw_mrl3_material,
            active_propname="mapList_index",
            rows=rows,
            type='DEFAULT'
        )

@reg_order(5)
class OBJECT_PT_Mrl3MaterialPropertyListPanel(Panel):
    bl_label = "Property List"
    bl_idname = "OBJECT_PT_mrl3_material_proplist_panel"
    bl_parent_id = "OBJECT_PT_mrl3_material_panel"  # Specify the ID of the parent panel
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(self, context):
        obj = context.active_object
        mhw_mrl3_material = obj.mhw_mrl3_material
        return mhw_mrl3_material.propertyBlock_items

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mhw_mrl3_material = obj.mhw_mrl3_material

        for index, propertyBlock in enumerate(mhw_mrl3_material.propertyBlock_items):
            rows = 6
            if propertyBlock.propertyList_items:
                split = layout.split(factor=0.025)  # Indent list slightly to make it more clear it's a part of a sub panel
                col1 = split.column()
                col2 = split.column()
                col2.label(text=f"{propertyBlock.propertyBlockType}    Property Count: {str(len(propertyBlock.propertyList_items))}")
                # col2.label(text=f"Property Count: {str(len(propertyBlock.propertyList_items))}")

                if len(propertyBlock.propertyList_items) < 6:
                    rows = len(propertyBlock.propertyList_items)

                col2.template_list(
                    listtype_name="MESH_UL_Mrl3PropertyList",
                    list_id=f"propertyBlock_{index}",
                    dataptr=propertyBlock,
                    propname="propertyList_items",
                    active_dataptr=propertyBlock,
                    active_propname="propertyList_index",
                    rows=rows,
                    type='DEFAULT'
                )


@reg_order(6)
class OBJECT_PT_Mrl3MaterialSamplerListPanel(Panel):
    bl_label = "Sampler List"
    bl_idname = "OBJECT_PT_mrl3_material_samplerlist_panel"
    bl_parent_id = "OBJECT_PT_mrl3_material_panel"  # Specify the ID of the parent panel
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    @classmethod
    def poll(self, context):
        obj = context.active_object
        mhw_mrl3_material = obj.mhw_mrl3_material
        return mhw_mrl3_material.samplerList_items

    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        mhw_mrl3_material = obj.mhw_mrl3_material
        rows = 6
        split = layout.split(factor=0.025)  # Indent list slightly to make it more clear it's a part of a sub panel
        col1 = split.column()
        col2 = split.column()
        col2.label(text=f"Sampler Count: {str(len(obj.mhw_mrl3_material.samplerList_items))}")

        if len(mhw_mrl3_material.samplerList_items) < 6:
            rows = len(mhw_mrl3_material.samplerList_items)

        col2.template_list(
            listtype_name="MESH_UL_Mrl3SamplerList",
            list_id="",
            dataptr=mhw_mrl3_material,
            propname="samplerList_items",
            active_dataptr=mhw_mrl3_material,
            active_propname="samplerList_index",
            rows=rows,
            type='DEFAULT'
        )

