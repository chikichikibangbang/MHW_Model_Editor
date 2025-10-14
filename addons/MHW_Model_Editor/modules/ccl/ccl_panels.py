from bpy.types import Panel
from .....common.types.framework import reg_order

@reg_order(9)
class OBJECT_PT_CCL_ColPropertiesPanel(Panel):
    bl_label = "CCL Collision Properties"
    bl_idname = "OBJECT_PT_ccl_col_properties_panel"
    bl_parent_id = "DATA_PT_shape_curve"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_category = "CCL Collision Properties"
    bl_context = "data"

    @classmethod
    def poll(self, context):
        return context.active_object is not None \
            and context.active_object.get("~TYPE", None) in {"MHW_CCL_SPHERE", "MHW_CCL_CAPSULE"}

    def draw(self, context):
        obj = context.active_object
        mhw_ccl_collision = obj.mhw_ccl_collision

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        box = layout.box()
        col = box.column()

        row = col.row(align=True)
        row.scale_y = 1.1
        row.prop(mhw_ccl_collision, "ColRadius")

        if obj.get("~TYPE", None) == "MHW_CCL_SPHERE":
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "StartColOffset", text="Collision Offset")

        elif obj.get("~TYPE", None) == "MHW_CCL_CAPSULE":
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "StartColOffset")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(mhw_ccl_collision, "EndColOffset")

