# # Author: NSA Cloud
# import bpy
# import os
# from bpy.props import (StringProperty,
#                        BoolProperty,
#                        IntProperty,
#                        FloatProperty,
#                        FloatVectorProperty,
#                        EnumProperty,
#                        PointerProperty,
#                        CollectionProperty,
#                        )
#
#
# def update_relPathToAbs(self, context):
#     try:
#         if "//" in self.path:
#             # print("updated path")
#             self.path = os.path.realpath(bpy.path.abspath(self.path))
#     except:
#         pass
#     if self.path == "":  # Check if path is empty
#         self.invalid = True
#     else:
#         self.invalid = False
#
#
# class MHWModelBatchExporterNodePG(bpy.types.PropertyGroup):
#     name: StringProperty(
#         name="",
#         description="",
#     )
#     icon: StringProperty(
#         name="",
#         description="",
#     )
#     enabled: BoolProperty(
#         name="",
#         description="",
#         default=True,
#
#     )
#     show: BoolProperty(
#         name="",
#         description="",
#         default=True
#     )
#     hasChild: BoolProperty(
#         name="",
#         description="",
#         default=False
#     )
#     expand: BoolProperty(
#         name="",
#         description="",
#         default=True
#     )
#
#     parentName: StringProperty(
#         name="",
#         description="",
#         default=""
#     )
#     hierarchyLevel: IntProperty(
#         name="",
#         description="",
#         default=0
#     )
#     exportType: StringProperty(
#         name="",
#         description="",
#         default=""
#     )
#     path: StringProperty(
#         name="",
#         subtype="FILE_PATH",
#         description="Path to where to export the file to",
#         update=update_relPathToAbs
#     )
#     invalid: BoolProperty(
#         name="",
#         description="",
#         default=False
#     )
#
#     # selectedOnly: BoolProperty(
#     #     name="Selected Objects Only",
#     #     description="Only export selected objects",
#     #     default=False)
#     # visibleOnly: BoolProperty(
#     #     name="Visible Objects Only",
#     #     description="Only export visible objects",
#     #     default=False)
#     autoSolveRepeatedUVs: BoolProperty(
#         name="Auto Solve Repeated UVs",
#         description="Splits connected UV islands if present. The mesh format does not allow for multiple uvs assigned to a vertex."
#                     "\nNOTE: This will modify the exported mesh. If auto smooth is disabled on the mesh, the normals may change",
#         default=True)
#     preserveSharpEdges: BoolProperty(
#         name="Split Sharp Edges",
#         description="Edge splits all edges marked as sharp to preserve them on the exported mesh."
#                     "\nNOTE: This will modify the exported mesh",
#         default=False)
#     useBlenderMaterialName: BoolProperty(
#         name="Use Blender Material Names",
#         description="If left unchecked, the exporter will get the material names to be used from the end of each object name."
#                     "\nFor example, if a mesh is named LOD_0_Group_0_Sub_0__Shirts_Mat, the material name is Shirts_Mat."
#                     "\nIf this option is enabled, the material name will instead be taken from the first material assigned to the object",
#         default=False)
#     invisibleMantlesModFix: BoolProperty(
#         name="Invisible Mantles Mod Fix",
#         description="The \"Invisible Mantles Mod\" has a bug where the glowing effects of the first material on the body part would be turned off when wearing the temporal mantle."
#                     "\nIf this option is enabled, the plugin will add an unused material as the first material to avoid this issue."
#                     "\nLeaving this option enabled is highly recommended",
#         default=True)
#
#     exportCCL: BoolProperty(
#         name="Export CCL Collision",
#         description="When exporting ctc file, also export collision objects as ccl file",
#         default=True)
#
#
# class MESH_UL_MHWModelBatchExporterList(bpy.types.UIList):
#
#     def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
#
#         row = layout.row()
#         if not item.hasChild and item.invalid:
#             row.alert = True
#         col1 = row.column()
#         # col1.prop(item,"expand")
#         col1.alignment = "RIGHT"
#         col1.label(text="      |    " * item.hierarchyLevel if item.hierarchyLevel != 0 else " ")
#         if not item.hasChild:
#             col2 = row.column()
#             col2.prop(item, "enabled")
#         col3 = row.column()
#         col3.label(icon=item.icon, text=item.name)
#         col4 = row.column()
#
#     # Disable double-click to rename
#     def invoke(self, context, event):
#         return {'PASS_THROUGH'}