import os
import bpy
from ...config import __addon_name__
from bpy.types import Panel
from .....common.types.framework import reg_order


@reg_order(109)
class OBJECT_PT_CTC_HeaderPropertiesPanel(Panel):
    bl_label = "CTC Header Properties"
    bl_idname = "OBJECT_PT_ctc_header_properties_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CTC Header Properties"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_CTC_HEADER"

    def draw(self, context):
        obj = context.active_object
        mhw_ctc_header = obj.mhw_ctc_header

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        box = layout.box()
        col = box.column()

        row = col.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Note: The header properties here will affect all chains.", icon="ERROR")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "AttributeFlags")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "StepTime")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "GravityScaling", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "GlobalDamping", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "GlobalTransForceCoef", text="Global TransForce", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "SpringScaling", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "WindScale")
        row.prop(mhw_ctc_header, "WindScaleMin", text="")
        row.prop(mhw_ctc_header, "WindScaleMax", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_header, "WindScaleWeight", index=0, text="Wind Weight")
        row.prop(mhw_ctc_header, "WindScaleWeight", index=1, text="")
        row.prop(mhw_ctc_header, "WindScaleWeight", index=2, text="")


@reg_order(110)
class OBJECT_PT_CTC_ChainPropertiesPanel(Panel):
    bl_label = "CTC Chain Properties"
    bl_idname = "OBJECT_PT_ctc_chain_properties_panel"
    bl_parent_id = "DATA_PT_shape_curve"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CTC Chain Properties"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_CTC_CHAIN"

    def draw(self, context):
        obj = context.active_object
        mhw_ctc_chain = obj.mhw_ctc_chain

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        box = layout.box()
        col = box.column()

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "CollisionAttrFlagValue")
        row.operator("mhw_ctc.set_collision_flags", icon='DOWNARROW_HLT', text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "ChainAttrFlagValue")
        row.operator("mhw_ctc.set_chain_flags", icon='DOWNARROW_HLT', text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "unknAttrFlag1", text="Unkn Flags")
        row.prop(mhw_ctc_chain, "unknAttrFlag2", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "Gravity", index=0, text="Gravity")
        row.prop(mhw_ctc_chain, "Gravity", index=1, text="")
        row.prop(mhw_ctc_chain, "Gravity", index=2, text="")

        # row = col.row(align=True)
        # row.scale_y = 1.1
        # row.label(text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "Damping", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "TransForceCoef", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "SpringCoef", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "WindRate", slider=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "WindLimit")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.label(text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "ColAttribute", text="Collider")
        row.prop(mhw_ctc_chain, "ColGroup", text="")
        row.prop(mhw_ctc_chain, "ColType", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_chain, "LimitForce", text="Other")
        row.prop(mhw_ctc_chain, "FrictionCoef", slider=True, text="")
        row.prop(mhw_ctc_chain, "ReflectCoef", slider=True, text="")

'''
@reg_order(112)
class OBJECT_PT_CTC_ChainColAttrPanel(Panel):
    bl_label = "Collision AttrFlag Settings"
    bl_idname = "OBJECT_PT_ctc_chain_col_attr_panel"
    bl_parent_id = "OBJECT_PT_ctc_chain_settings_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        mhw_ctc_chain = object.mhw_ctc_chain

        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment = 'RIGHT'
        col2.use_property_split = True
        col2.prop(mhw_ctc_chain, "CollisionAttrFlagValue")
        col2.prop(mhw_ctc_chain, "CollisionSelfEnable")
        col2.prop(mhw_ctc_chain, "CollisionModelEnable")
        col2.prop(mhw_ctc_chain, "CollisionVGroundEnable")

@reg_order(113)
class OBJECT_PT_CTC_ChainAttrPanel(Panel):
    bl_label = "Chain AttrFlag Settings"
    bl_idname = "OBJECT_PT_ctc_chain_attr_panel"
    bl_parent_id = "OBJECT_PT_ctc_chain_settings_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        mhw_ctc_chain = object.mhw_ctc_chain

        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment = 'RIGHT'
        col2.use_property_split = True

        col2.prop(mhw_ctc_chain, "ChainAttrFlagValue")
        col2.prop(mhw_ctc_chain, "AngleLimitEnable")
        col2.prop(mhw_ctc_chain, "AngleLimitRestitutionEnable")
        col2.prop(mhw_ctc_chain, "EndRotConstraintEnable")
        col2.prop(mhw_ctc_chain, "TransAnimationEnable")
        col2.prop(mhw_ctc_chain, "AngleFreeEnable")
        col2.prop(mhw_ctc_chain, "StretchBothEnable")
        col2.prop(mhw_ctc_chain, "PartBlendEnable")

@reg_order(114)
class OBJECT_PT_CTC_ChainOtherSettingsPanel(Panel):
    bl_label = "Other Chain Settings"
    bl_idname = "OBJECT_PT_ctc_chain_other_settings_panel"
    bl_parent_id = "OBJECT_PT_ctc_chain_settings_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

    def draw(self, context):
        layout = self.layout
        object = context.active_object
        mhw_ctc_chain = object.mhw_ctc_chain

        split = layout.split(factor=0.01)
        col1 = split.column()
        col2 = split.column()
        col2.alignment = 'RIGHT'
        col2.use_property_split = True

        col2.prop(mhw_ctc_chain, "unknAttrFlag1")
        col2.prop(mhw_ctc_chain, "unknAttrFlag2")
        col2.label(text="")
        col2.prop(mhw_ctc_chain, "ColAttribute")
        col2.prop(mhw_ctc_chain, "ColGroup")
        col2.prop(mhw_ctc_chain, "ColType")
        col2.label(text="")
        col2.prop(mhw_ctc_chain, "Gravity")
        col2.label(text="")
        col2.prop(mhw_ctc_chain, "Damping", slider=True)
        col2.prop(mhw_ctc_chain, "TransForceCoef", slider=True)
        col2.prop(mhw_ctc_chain, "SpringCoef", slider=True)
        col2.label(text="")
        col2.prop(mhw_ctc_chain, "LimitForce")
        col2.prop(mhw_ctc_chain, "FrictionCoef", slider=True)
        col2.prop(mhw_ctc_chain, "ReflectCoef", slider=True)
        col2.label(text="")
        col2.prop(mhw_ctc_chain, "WindRate", slider=True)
        col2.prop(mhw_ctc_chain, "WindLimit")
'''

@reg_order(111)
class OBJECT_PT_CTC_NodePropertiesPanel(Panel):
    bl_label = "CTC Node Properties"
    bl_idname = "OBJECT_PT_ctc_node_properties_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CTC Node Properties"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.active_object is not None and context.active_object.get("~TYPE", None) == "MHW_CTC_NODE"

    def draw(self, context):
        obj = context.active_object
        mhw_ctc_node = obj.mhw_ctc_node

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        box = layout.box()
        col = box.column()

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "unknByte1", text="Unkn Flags")
        row.prop(mhw_ctc_node, "unknByte2", text="")
        row.operator("mhw_ctc.copy_node_unknflags", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "AngleMode")
        row.operator("mhw_ctc.copy_node_anglemode", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "CollisionShape")
        row.operator("mhw_ctc.copy_node_collisionshape", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "unknEnum")
        row.operator("mhw_ctc.copy_node_unknenum", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "BoneColRadius")
        row.operator("mhw_ctc.copy_node_bonecolradius", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "AngleLimitRadius", text="Angle Radius")
        row.operator("mhw_ctc.copy_node_angleradius", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "WidthRate", slider=True)
        row.operator("mhw_ctc.copy_node_widthrate", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "Mass")
        row.operator("mhw_ctc.copy_node_mass", icon="COPYDOWN", text="")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_node, "ElasticCoef", slider=True)
        row.operator("mhw_ctc.copy_node_elasticcoef", icon="COPYDOWN", text="")



# # DIR_PATH = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
# # ICONS_PATH = os.path.join(DIR_PATH, "icons")
# # PCOLL = None
# # preview_collections = {}
# # @reg_order(17)
# # class CTCCredits(Panel):
# #     global PCOLL
# #     bl_label = "Credits"
# #     bl_idname = "OBJECT_PT_ctcccl_credits"
# #     bl_space_type = 'VIEW_3D'
# #     bl_region_type = 'UI'
# #     bl_category = "MHW CTC&CCL"
# #     bl_context = "objectmode"
# #     bl_options = {'DEFAULT_CLOSED'}
# #
# #
# #     def draw(self, context):
# #         layout = self.layout
# #         box = layout.box()
# #         col = box.column(align=True)
# #         row = col.row(align=False)
# #         row.label(text = f"MHW CTC&CCL Editor", icon_value=preview_collections["icons"]["korone"].icon_id)
# #         col.separator()
# #         row = col.row(align=False) ; row.scale_y = 0.75
# #         row.label(text = "Modified by:")
# #         row = col.row(align=False) ; row.scale_y = 0.75
# #         row.label(text = "Korone")
# #         col.separator()
# #         row = col.row(align=False) ; row.scale_y = 0.75
# #         row.label(text = "Special thanks:")
# #         row = col.row(align=False) ; row.scale_y = 0.75
# #         row.label(text = "NSACloud, xzhuah")
# #         col.separator()
# #         row = col.row() ; row.scale_y = 1.1
# #         button = row.operator("mhw_ctc.github_website", icon_value=preview_collections["icons"]["github"].icon_id)
# #         row = col.row() ; row.scale_y = 1.1
# #         button = row.operator("mhw_ctc.bilibili_website", icon_value=preview_collections["icons"]["bilibili"].icon_id)
# #         row = col.row() ; row.scale_y = 1.1
# #         button = row.operator("mhw_ctc.qq_website", icon_value=preview_collections["icons"]["qq"].icon_id)
# #         row = col.row() ; row.scale_y = 1.1
# #         button = row.operator("mhw_ctc.caimogu_website", icon_value=preview_collections["icons"]["caimogu"].icon_id)


@reg_order(100)
class OBJECT_PT_CTC_ToolsPanel(Panel):
    bl_label = "MHW CTC & CCL Tools"
    bl_idname = "OBJECT_PT_ctc_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "MHW Chain"
    # bl_context = "objectmode"

    @classmethod
    def poll(self, context: bpy.types.Context):
        return context is not None

    def draw(self, context: bpy.types.Context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        layout = self.layout
        box1 = layout.box()
        box2 = layout.box()
        col1 = box1.column(align=True)
        col2 = box2.column(align=True)

        row = col1.row(align=False)
        row.scale_y = 1.1
        row.operator("mhw_ctc.import_mhw_ctc", text="Import CTC")
        row.operator("mhw_ctc.export_mhw_ctc", text="Export CTC")

        col1.separator()
        row = col1.row(align=False)
        row.scale_y = 1.1
        row.operator("mhw_ccl.import_mhw_ccl", text="Import CCL")
        row.operator("mhw_ccl.export_mhw_ccl", text="Export CCL")

        row = col2.row(align=True)
        # row.scale_y = 0.75
        row.label(text="Active CTC Collection")

        col2.separator()
        row = col2.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_ctc_toolpanel, "ctcCollection", icon="COLLECTION_COLOR_02")

        if context.mode != "POSE":
            col2.separator()
            row = col2.row(align=True)
            row.scale_y = 1.1
            row.operator("mhw_ctc.create_ctc_collection")

            col2.separator()
            row = col2.row(align=True)
            row.scale_y = 1.1
            row.operator("mhw_ctc.align_frames", text="Align Angle Direction")

            col2.separator()
            row = col2.row(align=True)
            row.scale_y = 1.1
            row.operator("mhw_ctc.apply_angle_limit_ramp", text="Apply Angle Ramp")

            col2.separator()
            col2.separator()
            col2.separator()
            row = col2.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Create new chains in Pose Mode.")

            col2.separator()
            row = col2.row(align=True)
            row.scale_y = 1.1
            row.operator("mhw_ctc.switch_to_pose_mode")

        else:
            col2.separator()
            row = col2.row(align=False)
            row.scale_y = 1.1
            row.operator("mhw_ctc.create_chain_from_bone")
            row.operator("mhw_ccl.create_collision_from_bone")

            col2.separator()
            split = col2.row(align=True)
            row = split.row(align=True)
            row.scale_y = 1.1
            row.operator("mhw_ctc.rename_chain_bones")
            row = split.row(align=True)
            row.scale_y = 1.1
            row.alignment = 'RIGHT'
            row.operator("mhw_ctc.rename_bone_settings", text="", icon='SETTINGS')

            col2.separator()
            row = col2.row(align=True)
            row.scale_y = 1.1
            row.operator("mhw_ccl.create_full_body_collisions")

            col2.separator()
            col2.separator()
            col2.separator()
            row = col2.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Configure chains in Object Mode.")

            col2.separator()
            row = col2.row(align=True)
            row.scale_y = 1.1
            row.operator("mhw_ctc.switch_to_object_mode")


@reg_order(101)
class OBJECT_PT_CTC_ClipboardPanel(Panel):
    bl_label = "Clipboard"
    bl_idname = "OBJECT_PT_ctc_clipboard_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Chain"
    # bl_context = "objectmode"

    @classmethod
    def poll(self,context):
        return context is not None

    def draw(self, context):
        mhw_ctc_clipboard = context.scene.mhw_ctc_clipboard
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        # row = col.row(align=True)
        # # row.scale_y = 0.75
        # row.label(text="Copy CTC Object Properties")
        # col.separator()

        row = col.row(align=False)
        row.scale_y = 1.1
        row.operator("mhw_ctc.copy_ctc_properties", icon="COPYDOWN")
        row.operator("mhw_ctc.paste_ctc_properties", icon="PASTEDOWN")

        col.separator()
        row = col.row(align=True)
        # row.scale_y = 0.75

        if mhw_ctc_clipboard.node_prop_name != "":
            row.label(text=f"Content: {mhw_ctc_clipboard.ctc_type_name} - {mhw_ctc_clipboard.node_prop_name}")
        else:
            row.label(text=f"Content: {mhw_ctc_clipboard.ctc_type_name}")

        # row = col.row(align=True)
        # row.label(text=str(context.scene.mhw_ctc_clipboard.ctc_type_name))

@reg_order(102)
class OBJECT_PT_CTC_PresetsPanel(Panel):
    bl_label = "Presets"
    bl_idname = "OBJECT_PT_ctc_presets_panel"
    # bl_parent_id = "OBJECT_PT_ctc_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Chain"
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self,context):
        return context is not None

    def draw(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        # row = col.row(align=True)
        # # row.scale_y = 0.75
        # row.label(text="CTC Chain Preset")
        # col.separator()

        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(mhw_ctc_toolpanel, "CTCChainPresets")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_ctc.apply_ctc_chain_preset", text="Apply Chain Preset")

        col.separator()
        row = col.row(align=False)
        row.scale_y = 1.1
        row.operator("mhw_ctc.save_selected_as_preset", text="Save Preset")
        row.operator("mhw_ctc.open_preset_folder")

@reg_order(103)
class OBJECT_PT_CTC_VisibilityPanel(Panel):
    bl_label = "Visibility"
    bl_idname = "OBJECT_PT_ctc_visibility_panel"
    # bl_parent_id = "OBJECT_PT_ctc_tools_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MHW Chain"
    # bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self,context):
        return context is not None

    def draw(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        # row = col.row(align=True)
        # row.scale_y = 1.1
        # row.prop(mhw_ctc_toolpanel, "reserveMeshObjects")
        # col.separator()

        row = col.row(align=False)
        row.scale_y = 1.1
        # row.label(text="Only Show:")
        row.operator("mhw_ctc.only_show_chains", text="Only Chains")
        row.operator("mhw_ccl.only_show_collisions", text="Only Collisions")

        col.separator()
        row = col.row(align=False)
        row.scale_y = 1.1
        row.operator("mhw_ctc.only_show_nodes", text="Only Nodes")
        row.operator("mhw_ctc.only_show_angle_limits", text="Only Angles")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.operator("mhw_ctc.show_all_objects")

@reg_order(104)
class OBJECT_PT_CTC_DisplayVisPanel(Panel):
    bl_label = "Display Settings"
    bl_idname = "OBJECT_PT_ctc_display_vis_panel"
    bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        mhw_ccl_toolpanel = context.scene.mhw_ccl_toolpanel
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "showRelationLines")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "showAngleLimitCones")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "hideLastNodeAngleLimit")

        col.separator()
        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "showNodeNames")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ccl_toolpanel, "showCollisionNames")

        col.separator()
        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "drawChainsThroughObjects")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "drawNodesThroughObjects")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "drawConesThroughObjects")

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ccl_toolpanel, "drawCollisionsThroughObjects")


@reg_order(105)
class OBJECT_PT_CTC_SizeVisPanel(Panel):
    bl_label = "Size Settings"
    bl_idname = "OBJECT_PT_ctc_size_vis_panel"
    bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        mhw_ccl_toolpanel = context.scene.mhw_ccl_toolpanel
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "chainDisplaySize")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "angleLimitDisplaySize")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "coneDisplaySize")

# @reg_order(106)
# class OBJECT_PT_CCL_CollisionVisPanel(Panel):
#     bl_label = "Collision Settings"
#     bl_idname = "OBJECT_PT_ccl_collision_vis_panel"
#     bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_options = {'DEFAULT_CLOSED'}
#
#     def draw(self, context):
#         mhw_ccl_toolpanel = context.scene.mhw_ccl_toolpanel
#         layout = self.layout
#         box = layout.box()
#         col = box.column(align=True)
#
#         row = col.row(align=True)
#         row.scale_y = 1.1
#         row.prop(mhw_ccl_toolpanel, "showCollisionNames")
#
#         row = col.row(align=True)
#         row.scale_y = 1.1
#         row.prop(mhw_ccl_toolpanel, "drawCollisionsThroughObjects")
#
#         # row = col.row(align=True)
#         # row.scale_y = 1.1
#         # row.prop(mhw_ccl_toolpanel, "drawCapsuleHandlesThroughObjects")


@reg_order(107)
class OBJECT_PT_CTC_ColorVisPanel(Panel):
    bl_label = "Color Settings"
    bl_idname = "OBJECT_PT_ctc_color_vis_panel"
    bl_parent_id = "OBJECT_PT_ctc_visibility_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel
        mhw_ccl_toolpanel = context.scene.mhw_ccl_toolpanel

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "chainColor")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ctc_toolpanel, "coneColor")

        col.separator()
        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ccl_toolpanel, "collisionColor")


@reg_order(108)
class OBJECT_PT_CTC_PropertiesPanel(Panel):
    bl_label = "Properties"
    bl_idname = "OBJECT_PT_ctc_properties_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = "MHW Chain"
    # bl_context = "objectmode"

    @classmethod
    def poll(self, context):
        showProp = bpy.context.preferences.addons[__addon_name__].preferences.showCTCProperties
        return showProp and context.active_object is not None \
            and context.active_object.get("~TYPE", None) in {"MHW_CTC_HEADER", "MHW_CTC_CHAIN", "MHW_CTC_NODE",
                                                             "MHW_CCL_SPHERE", "MHW_CCL_CAPSULE"}

    def draw(self, context: bpy.types.Context):
        mhw_ctc_toolpanel = context.scene.mhw_ctc_toolpanel

        obj = context.active_object

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # box1 = layout.box()
        # col1 = box1.column(align=True)
        #
        # row = col1.row(align=True)
        # # row.scale_y = 0.75
        # row.label(text=f"Active Object: {obj.name}")

        # layout.label(text=f"Active Object: {obj.name}")
        layout.label(text=obj.name)

        if obj.get("~TYPE", None) == "MHW_CTC_HEADER":
            box2 = layout.box()
            col2 = box2.column()
            mhw_ctc_header = obj.mhw_ctc_header

            row = col2.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Header Properties")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "AttributeFlags")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "StepTime")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.label(text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "GravityScaling", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "GlobalDamping", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "GlobalTransForceCoef", text="Global TransForce", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "SpringScaling", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.label(text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "WindScale")
            row.prop(mhw_ctc_header, "WindScaleMin", text="")
            row.prop(mhw_ctc_header, "WindScaleMax", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_header, "WindScaleWeight", index=0, text="Wind Weight")
            row.prop(mhw_ctc_header, "WindScaleWeight", index=1, text="")
            row.prop(mhw_ctc_header, "WindScaleWeight", index=2, text="")

        elif obj.get("~TYPE", None) == "MHW_CTC_CHAIN":
            box2 = layout.box()
            col2 = box2.column()
            mhw_ctc_chain = obj.mhw_ctc_chain

            row = col2.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Chain Properties")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "CollisionAttrFlagValue")
            row.operator("mhw_ctc.set_collision_flags", icon='DOWNARROW_HLT', text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "ChainAttrFlagValue")
            row.operator("mhw_ctc.set_chain_flags", icon='DOWNARROW_HLT', text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "unknAttrFlag1", text="Unkn Flags")
            row.prop(mhw_ctc_chain, "unknAttrFlag2", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.label(text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "Gravity", index=0, text="Gravity")
            row.prop(mhw_ctc_chain, "Gravity", index=1, text="")
            row.prop(mhw_ctc_chain, "Gravity", index=2, text="")

            # row = col2.row(align=True)
            # row.scale_y = 1.1
            # row.label(text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "Damping", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "TransForceCoef", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "SpringCoef", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.label(text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "WindRate", slider=True)

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "WindLimit")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.label(text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "ColAttribute", text="Collider")
            row.prop(mhw_ctc_chain, "ColGroup", text="")
            row.prop(mhw_ctc_chain, "ColType", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_chain, "LimitForce", text="Other")
            row.prop(mhw_ctc_chain, "FrictionCoef", slider=True, text="")
            row.prop(mhw_ctc_chain, "ReflectCoef", slider=True, text="")

        elif obj.get("~TYPE", None) == "MHW_CTC_NODE":
            box2 = layout.box()
            col2 = box2.column()
            mhw_ctc_node = obj.mhw_ctc_node

            row = col2.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Node Properties")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "unknByte1", text="Unkn Flags")
            row.prop(mhw_ctc_node, "unknByte2", text="")
            row.operator("mhw_ctc.copy_node_unknflags", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "AngleMode")
            row.operator("mhw_ctc.copy_node_anglemode", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "CollisionShape")
            row.operator("mhw_ctc.copy_node_collisionshape", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "unknEnum")
            row.operator("mhw_ctc.copy_node_unknenum", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "BoneColRadius")
            row.operator("mhw_ctc.copy_node_bonecolradius", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "AngleLimitRadius", text="Angle Radius")
            row.operator("mhw_ctc.copy_node_angleradius", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "WidthRate", slider=True)
            row.operator("mhw_ctc.copy_node_widthrate", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "Mass")
            row.operator("mhw_ctc.copy_node_mass", icon="COPYDOWN", text="")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ctc_node, "ElasticCoef", slider=True)
            row.operator("mhw_ctc.copy_node_elasticcoef", icon="COPYDOWN", text="")

        elif obj.get("~TYPE", None) == "MHW_CCL_SPHERE":
            box2 = layout.box()
            col2 = box2.column()
            mhw_ccl_collision = obj.mhw_ccl_collision

            row = col2.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Collision Properties")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "ColRadius")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "StartColOffset", text="Collision Offset")

        elif obj.get("~TYPE", None) == "MHW_CCL_CAPSULE":
            box2 = layout.box()
            col2 = box2.column()
            mhw_ccl_collision = obj.mhw_ccl_collision

            row = col2.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Collision Properties")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "ColRadius")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "StartColOffset")

            row = col2.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "EndColOffset")






