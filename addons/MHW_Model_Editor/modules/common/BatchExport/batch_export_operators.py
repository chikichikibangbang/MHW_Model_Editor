# # Author: NSA Cloud
# import bpy
# import os
# from bpy.types import Operator
# from bpy.props import StringProperty, IntProperty, CollectionProperty, BoolProperty
#
# from MHW_Model_Editor.addons.MHW_Model_Editor.modules.common.BatchExport.batch_export_properties import MHWModelBatchExporterNodePG
# from MHW_Model_Editor.addons.MHW_Model_Editor.modules.common.general_function import splitNativesPath
# from MHW_Model_Editor.addons.MHW_Model_Editor.modules.common.message_functions import showErrorMessageBox
#
# EXPORTER_WINDOW_SIZE = 800
# SPLIT_FACTOR = .4
#
#
# def update_checkAllItems(self, context):
#     if self.checkAllItems == True:
#         for item in self.itemList_items:
#             item.enabled = True
#         self.checkAllItems = False
#
#
# def update_uncheckAllItems(self, context):
#     if self.uncheckAllItems == True:
#         for item in self.itemList_items:
#             item.enabled = False
#         self.uncheckAllItems = False
#
#
# COLLECTION_TYPES = frozenset([
#     "MHW_MOD3_COLLECTION",
#     "MHW_MRL3_COLLECTION",
#     "MHW_CTC_COLLECTION",
# ])
#
#
# def checkForChildMHWCollectionsRecursive(
#         collection):  # For checking if a collection should be included in the export list
#     if collection.get("~TYPE") in COLLECTION_TYPES:
#         return True
#     else:
#         for child in collection.children:
#             if checkForChildMHWCollectionsRecursive(child):
#                 return True
#     return False
#
#
# def determineExportPath(modDirectory, exportType, assetPath, scene):
#     filePath = os.path.join(modDirectory, assetPath)
#     return filePath
#
#
# def populateCollectionList(itemList, collection, recursionLevel, parentName):
#     item = itemList.add()
#     item.name = collection.name
#     if collection.color_tag == "NONE":
#         item.icon = "OUTLINER_COLLECTION"
#     else:
#         item.icon = f"COLLECTION_{collection.color_tag}"
#     item.hierarchyLevel = recursionLevel
#     item.parentName = parentName
#
#     recursionLevel += 1
#     if collection.get("~TYPE") not in COLLECTION_TYPES:
#         for child in collection.children:
#             if checkForChildMHWCollectionsRecursive(child):
#                 item.hasChild = True
#                 populateCollectionList(itemList, child, recursionLevel, parentName=collection.name)
#     else:
#         item.invalid = True  # Will be set to valid once a usable path is entered
#         if "BatchExport_enabled" in collection:
#             item.enabled = bool(collection["BatchExport_enabled"])
#         if "BatchExport_path" in collection:
#             item.path = collection["BatchExport_path"]
#         # print(f"Batch Export: Loaded previous values for {item.name}")
#
#         if collection["~TYPE"] == "MHW_MOD3_COLLECTION":
#             item.exportType = "MOD3"
#
#             if "BatchExport_autoSolveRepeatedUVs" in collection:
#                 try:
#                     item.autoSolveRepeatedUVs = collection["BatchExport_autoSolveRepeatedUVs"]
#                     item.preserveSharpEdges = collection["BatchExport_preserveSharpEdges"]
#                     item.useBlenderMaterialName = collection["BatchExport_useBlenderMaterialName"]
#                     item.invisibleMantlesModFix = collection["BatchExport_invisibleMantlesModFix"]
#                 except Exception as err:
#                     print(f"Failed to load default values for {item.name} - {str(err)}")
#
#         elif collection["~TYPE"] == "MHW_MRL3_COLLECTION":
#             item.exportType = "MRL3"
#         elif collection["~TYPE"] == "MHW_CTC_COLLECTION":
#             item.exportType = "CTC & CCL"
#
#             if "BatchExport_exportCCL" in collection:
#                 try:
#                     item.exportCCL = collection["BatchExport_exportCCL"]
#                 except Exception as err:
#                     print(f"Failed to load default values for {item.name} - {str(err)}")
#
#         if item.path == "":
#             if bpy.context.scene.mhw_mrl3_toolpanel.modDirectory != "":
#                 try:
#                     split = splitNativesPath(bpy.context.scene.mhw_mrl3_toolpanel.modDirectory)
#                     if split != None:
#                         assetPath = collection.get("~ASSETPATH", None)
#                         if assetPath != None:
#                             item.path = determineExportPath(split[0], item.exportType, assetPath.replace("/", os.sep), bpy.context.scene)
#                 except Exception as err:
#                     print(f"Batch Export: Cannot auto determine path for {item.name}: {str(err)}")
#
#
# class WM_OT_MHWModel_BatchExporter(Operator):
#     bl_label = "Batch Exporter"
#     bl_idname = "mhw_model.batch_exporter"
#     bl_description = "Export all selected MHW Model (mod3, mrl3, ctc, ccl) files quickly"
#     bl_options = {'INTERNAL'}
#
#     itemList_items: CollectionProperty(type=MHWModelBatchExporterNodePG)
#     itemList_index: IntProperty(name="")
#
#     checkAllItems: BoolProperty(
#         name="Check All Items",
#         description="Select all files to be exported",
#         default=False,
#         update=update_checkAllItems
#     )
#     uncheckAllItems: BoolProperty(
#         name="Uncheck All Items",
#         description="Deselect all files to be exported",
#         default=False,
#         update=update_uncheckAllItems
#     )
#
#     def execute(self, context):
#         print("Batch export started.")
#
#         # Save which files are enabled
#         for item in self.itemList_items:
#             if item.exportType != "":
#                 bpy.data.collections[item.name]["BatchExport_enabled"] = item.enabled
#                 # if item.exportType == "FBXSKEL":
#                 #     bpy.data.objects[item.name]["BatchExport_enabled"] = item.enabled
#                 # else:
#                 #     bpy.data.collections[item.name]["BatchExport_enabled"] = item.enabled
#
#         exportItemList = [item for item in self.itemList_items if
#                           not item.hasChild and item.enabled and item.exportType != ""]
#         failCount = 0
#         for index, exportItem in enumerate(exportItemList):
#             if exportItem.invalid:
#                 print(f"Skipping {exportItem.name} ({index + 1} / {len(exportItemList)}) due to an invalid export path: {exportItem.path}")
#                 failCount += 1
#                 continue
#
#             print(f"Exporting File: {exportItem.name} ({index + 1} / {len(exportItemList)})")
#             os.makedirs(os.path.split(exportItem.path)[0], exist_ok=True)
#
#             if exportItem.exportType == "MOD3":
#                 try:
#                     bpy.ops.mhw_mod3.export_mhw_mod3(
#                         filepath=exportItem.path,
#                         targetCollection=bpy.data.collections.get(exportItem.name),
#                         autoSolveRepeatedUVs=exportItem.autoSolveRepeatedUVs,
#                         preserveSharpEdges=exportItem.preserveSharpEdges,
#                         useBlenderMaterialName=exportItem.useBlenderMaterialName,
#                         invisibleMantlesModFix=exportItem.invisibleMantlesModFix,
#                     )
#                 except Exception as err:
#                     print(f"Mod3 Export Failed: {str(err)}")
#                     failCount += 1
#             elif exportItem.exportType == "MRL3":
#                 try:
#                     bpy.ops.mhw_mrl3.export_mhw_mrl3(
#                         filepath=exportItem.path,
#                         targetCollection=bpy.data.collections.get(exportItem.name),
#                     )
#                 except Exception as err:
#                     print(f"Mrl3 Export Failed: {str(err)}")
#                     failCount += 1
#             elif exportItem.exportType == "CTC & CCL":
#                 try:
#                     bpy.ops.mhw_ctc.export_mhw_ctc(
#                         filepath=exportItem.path,
#                         targetCollection=bpy.data.collections.get(exportItem.name),
#                         exportCCL=exportItem.exportCCL,
#                     )
#                 except Exception as err:
#                     print(f"CTC & CCL Export Failed: {str(err)}")
#                     failCount += 1
#             else:
#                 print(f"Unsupported file type ({exportItem.exportType}), skipping...")
#                 failCount += 1
#         if failCount != 0:
#             showErrorMessageBox(
#                 f"{failCount}/{len(exportItemList)} files failed to export.\nSee console for details. (Window > Toggle System Console)")
#         else:
#             self.report({"INFO"}, "Batch export finished successfully.")
#         return {'FINISHED'}
#
#     def invoke(self, context, event):
#         window = context.window
#         centerX = window.width // 2
#         centerY = window.height // 2
#
#         # region = bpy.context.region
#         # centerX = region.width // 2
#         # centerY = region.height
#
#         # currentX = event.mouse_region_X
#         # currentY = event.mouse_region_Y
#
#         parentDict = {None: None}
#         for collection in bpy.data.collections:
#             parentDict[collection] = None
#
#         for collection in bpy.data.collections:
#             for child in collection.children:
#                 parentDict[child] = collection
#         collectionRoots = set()
#         for collection in bpy.data.collections:
#             if collection.get("~TYPE") in COLLECTION_TYPES:
#                 parentCol = parentDict[collection]
#                 # print(f"Found supported collection: {collection.name},Parent:{parentDict[collection]}")
#
#                 while parentDict[parentCol] != None:
#                     parentCol = parentDict[parentCol]
#                 else:
#                     # print(f"Root collection:{parentCol.name}")
#                     if parentCol == None:
#                         collectionRoots.add(collection)
#                     else:
#                         collectionRoots.add(parentCol)
#
#         # Populate list
#         self.itemList_items.clear()
#         for collection in collectionRoots:
#             populateCollectionList(self.itemList_items, collection, recursionLevel=0, parentName="")
#
#         # # Add fbxskel armatures for export
#         # for armatureObj in [obj for obj in bpy.data.objects if obj.type == "ARMATURE" and (
#         #         ".fbxskel" in obj.name.lower() or (".skeleton" in obj.name.lower()))]:
#         #     item = self.itemList_items.add()
#         #     item.name = armatureObj.name
#         #     item.icon = "ARMATURE_DATA"
#         #     item.exportType = "FBXSKEL"
#         #     item.invalid = True
#         #     if "BatchExport_enabled" in armatureObj:
#         #         item.enabled = bool(armatureObj["BatchExport_enabled"])
#         #     if "BatchExport_path" in armatureObj:
#         #         item.path = armatureObj["BatchExport_path"]
#         #     if item.path == "":
#         #         if bpy.context.scene.re_mdf_toolpanel.modDirectory != "":
#         #             try:
#         #                 split = splitNativesPath(bpy.context.scene.re_mdf_toolpanel.modDirectory)
#         #                 if split != None:
#         #                     assetPath = armatureObj.get("~ASSETPATH", None)
#         #                     if assetPath != None:
#         #                         item.path = determineExportPath(split[0], item.exportType,
#         #                                                         assetPath.replace("/", os.sep), bpy.context.scene)
#         #             except Exception as err:
#         #                 print(f"Batch Export: Cannot auto determine path for {item.name}: {str(err)}")
#
#         # Move cursor to center so extract window is at the center of the window
#         context.window.cursor_warp(centerX, centerY)
#
#         # return context.window_manager.invoke_props_dialog(self, width=EXPORTER_WINDOW_SIZE, confirm_text="Batch Export Files")
#         return context.window_manager.invoke_props_dialog(self, width=EXPORTER_WINDOW_SIZE)
#
#     def draw(self, context):
#         layout = self.layout
#         rowCount = 13
#         uifontscale = 9 * context.preferences.view.ui_scale
#         max_label_width = int((EXPORTER_WINDOW_SIZE * (1 - SPLIT_FACTOR) * (2 - SPLIT_FACTOR)) // uifontscale)
#         row = layout.row().separator()
#         split = layout.split(
#             factor=SPLIT_FACTOR)  # Indent list slightly to make it more clear it's a part of a sub panel
#         col1 = split.column()
#         split2 = col1.split()
#         col1sub1 = split2.column()
#         col1sub1.alignment = "LEFT"
#         col1sub1.label(
#             text=f"Files ({sum(1 for item in self.itemList_items if (not item.hasChild and item.enabled))} selected)")
#         col1sub2 = col1.column()
#         row = split2.row()
#         row.alignment = "RIGHT"
#         row.prop(self, "checkAllItems", icon="CHECKMARK", icon_only=True)
#         row.prop(self, "uncheckAllItems", icon="X", icon_only=True)
#         col1.template_list(
#             listtype_name="MESH_UL_MHWModelBatchExporterList",
#             list_id="itemList",
#             dataptr=self,
#             propname="itemList_items",
#             active_dataptr=self,
#             active_propname="itemList_index",
#             rows=rowCount,
#             type='DEFAULT'
#         )
#         col2 = split.column()
#         col2.label(text="Export Settings")
#         box = col2.box()
#         if self.itemList_index != -1:
#             item = self.itemList_items[self.itemList_index]
#             if not item.hasChild and item.exportType != "":
#                 box.label(text=f"Type: {item.exportType}")
#                 box.label(text="Export Path")
#
#                 box.prop(item, "path")
#                 if item.invalid:
#                     row = box.row()
#                     row.alert = True
#                     row.label(text="Path is empty.", icon="ERROR")
#                 if item.exportType == "MOD3":
#                     box.prop(item, "autoSolveRepeatedUVs")
#                     box.prop(item, "preserveSharpEdges")
#                     box.prop(item, "useBlenderMaterialName")
#                     box.prop(item, "invisibleMantlesModFix")
#                 elif item.exportType == "CTC & CCL":
#                     box.prop(item, "exportCCL")
#             else:
#                 box.label(text=f"Select a file from the list to configure export settings.")