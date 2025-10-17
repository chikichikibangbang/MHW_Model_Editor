import os
import bpy
from ..config import __addon_name__
from ....import addon_updater_ops
from bpy.props import StringProperty, IntProperty, BoolProperty, CollectionProperty, EnumProperty, FloatProperty, \
    FloatVectorProperty
from bpy.types import AddonPreferences, Operator, PropertyGroup
from datetime import datetime
from ..modules.common.general_function import formatByteSize, getFolderSize


class AddItemOperator(Operator):
    bl_idname = "mhw_mod3.chunk_path_list_add_item"
    bl_description = "Add path to the extracted chunk folder.\n" + r"Example: D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC"
    bl_label = "Add Chunk Path"

    def execute(self, context):
        # Add an item to the list
        context.preferences.addons[__addon_name__].preferences.chunkPathList_items.add()
        return {'FINISHED'}


# Operator to remove an item from the list
class RemoveItemOperator(Operator):
    bl_idname = "mhw_mod3.chunk_path_list_remove_item"
    bl_description = "Remove chunk path from the list"
    bl_label = "Remove Selected Path"

    def execute(self, context):
        chunkList = bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_items
        index = bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_index
        chunkList.remove(index)
        bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_index = min(max(0, index - 1),
                                                                                       len(chunkList) - 1)
        return {'FINISHED'}


# Operator to reorder items in the list
class ReorderItemOperator(Operator):
    bl_idname = "mhw_mod3.chunk_path_list_reorder_item"
    bl_description = "Change the order in which files will be searched"
    bl_label = "Reorder Item"

    direction: bpy.props.EnumProperty(
        items=[('UP', "Up", ""), ('DOWN', "Down", "")],
        default='UP'
    )

    def move_index(self):
        index = bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_index
        list_length = len(bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_items)
        new_index = index + (-1 if self.direction == 'UP' else 1)
        bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_index = max(0, min(new_index, list_length))

    def execute(self, context):
        chunkList = bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_items
        index = bpy.context.preferences.addons[__addon_name__].preferences.chunkPathList_index

        neighbor = index + (-1 if self.direction == 'UP' else 1)
        chunkList.move(neighbor, index)
        self.move_index()
        return {'FINISHED'}

class MOD3_UL_ChunkPathList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.scale_y = 1.1
        layout.prop(item, "path")
def checkTextureCacheSize():
    try:
        bpy.context.preferences.addons[__addon_name__].preferences.textureCacheSizeString = formatByteSize(getFolderSize(bpy.path.abspath(bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath)))
        timestamp = str(datetime.now()).split(".")[0]
        bpy.context.preferences.addons[__addon_name__].preferences.textureCacheCheckDate = timestamp
    except:
        pass

class WM_OT_OpenTextureCacheFolder(Operator):
    bl_label = "Open Cache Folder"
    bl_description = "Opens the texture cache folder in File Explorer"
    bl_idname = "mhw_mod3.open_texture_cache_folder"

    def execute(self, context):
        try:
            os.startfile(bpy.path.abspath(bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath))
        except:
            pass
        checkTextureCacheSize()
        return {'FINISHED'}


class WM_OT_CheckTextureCacheSize(Operator):
    bl_label = "Check Cache Size"
    bl_description = "Shows the current size of the texture cache folder."
    bl_idname = "mhw_mod3.check_texture_cache_size"

    def execute(self, context):
        checkTextureCacheSize()
        return {'FINISHED'}


class WM_OT_ClearTextureCacheFolder(Operator):
    bl_label = "Clear Cache Folder"
    bl_description = "Deletes all cached converted textures. Note that any saved blend files will lose their textures if the cache is cleared."
    bl_idname = "mhw_mod3.clear_texture_cache_folder"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Are you sure you want to delete all cached textures?")
        layout.label(text=f"Directory:")
        layout.label(text=f"{bpy.path.abspath(bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath)}")

    def invoke(self, context, event):
        checkTextureCacheSize()
        return context.window_manager.invoke_props_dialog(self, width=400)

    def execute(self, context):
        imageExtensions = (".dds", ".png", ".tga", ".tif", ".tiff", ".exr")
        deletionList = []
        # I could do shutil.rmtree but deleting everything from a directory could be potentially dangerous if the path is somehow wrong.
        # So in order to minimize potential damage, it loops through and only deletes image files in the directory.
        for root, dirs, files in os.walk(
                bpy.path.abspath(bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath)):
            for file in files:
                if file.lower().endswith(imageExtensions):
                    deletionList.append(os.path.join(root, file))

        print(f"Deleting {len(deletionList)} image files...")
        for path in deletionList:
            try:
                os.remove(path)
            except Exception as err:
                print(f"Failed to delete {path} - {str(err)}")
        self.report({"INFO"}, "Cleared texture cache.")
        checkTextureCacheSize()
        return {'FINISHED'}

class Mod3ChunkPathPropertyGroup(PropertyGroup):
    path: StringProperty(
        name="Path",
        subtype="DIR_PATH",
        description="Set the path to the nativePC or Chunk folder inside the extracted chunk files."
                    "\nThis determines where textures will be imported from."
                    "\n"+r"Example: D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC"
    )


class MHWModelAddonPreferences(AddonPreferences):
    # this must match the add-on name (the folder name of the unzipped file)
    bl_idname = __addon_name__

    # https://docs.blender.org/api/current/bpy.props.html
    # The name can't be dynamically translated during blender programming running as they are defined
    # when the class is registered, i.e. we need to restart blender for the property name to be correctly translated.

    showExternalLinks: BoolProperty(
        name="Show External Links",
        default=True)
    showAdvancedOptions: BoolProperty(
        name="Show Advanced Options",
        default=True)
    showMod3ImportOptions: BoolProperty(
        name="Show Mod3 Import Options",
        default=False)
    showMod3ExportOptions: BoolProperty(
        name="Show Mod3 Export Options",
        default=False)
    showCTCVisibilityOptions: BoolProperty(
        name="Show CTC Visibility Options",
        default=False)
    showTextureCache: BoolProperty(
        name="Show Texture Cache",
        default=True)
    showChunkPath: BoolProperty(
        name="Show Chunk Path",
        default=True)
    showAutoUpdate: BoolProperty(
        name="Show Auto Update",
        default=True)

    textureCacheSizeString: StringProperty(
        default="",
    )
    textureCacheCheckDate: StringProperty(
        default="",
    )

    dragDropImportOptions: BoolProperty(
        name="Show Drag and Drop Import Options (Blender 4.1+)",
        description="Show import options when dragging files into the 3D View."
                    "\nIf this is disabled, the default import options will be used."
                    "\nDrag and drop importing is only supported on Blender 4.1+",
        default=False if bpy.app.version < (4, 1, 0) else True
    )
    showConsole: BoolProperty(
        name="Show Console During Import / Export",
        description="When importing or exporting a file, the console will be opened so that progress can be viewed."
                    "\nNote that if the console is already opened before import or export, it will be closed instead."
                    "\n This is a limitation of Blender, there's no way to get the active state of the console window",
        default=True
    )
    useDDS: BoolProperty(
        name="Use DDS Textures (Blender 4.2+)",
        description="Use DDS textures instead of converting to TIF."
                    "\nThis greatly improves mesh import speed but is only usable on Blender 4.2+."
                    "\nIf the Blender version is less than 4.2, this option will do nothing",
        # default=False if bpy.app.version < (4, 2, 0) else True
        default=False
    )
    showCTCProperties: BoolProperty(
        name="Show CTC & CCL Properties In Sub Panel",
        description="Synchronously show ctc & ccl properties in \"MHW Chain\" panel."
                    "\nIf checked, when activating a ctc & ccl object, the properties will also be shown in the \"Properties\" subpanel",
        default=False
    )
    textureCachePath: StringProperty(
        name="Texture Cache Path",
        subtype='DIR_PATH',
        description="Location to save converted textures",
        default=os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]), "modules", "TextureCache")
    )

    '''只有导入mod3同时导入材质时才会添加路径'''
    saveChunkPaths: BoolProperty(
        name="Save Chunk Paths Automatically",
        description="If a chunk path is detected when a mod3 is imported, add it to the chunk path list automatically",
        default=True
    )
    chunkPathList_items: CollectionProperty(type=Mod3ChunkPathPropertyGroup)
    chunkPathList_index: IntProperty(name="")

    # addon updater preferences
    auto_check_update: BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
    )

    updater_interval_months: IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
    )
    updater_interval_days: IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
    )
    updater_interval_hours: IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
    )
    updater_interval_minutes: IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
    )


    # Default import settings
    default_clearScene: BoolProperty(
        name="Clear Scene",
        description="Clear all objects before importing the mod3 file",
        default=False)

    default_loadMrl3Data: BoolProperty(
        name="Load Material Data",
        description="Imports the mrl3 materials as objects inside a collection in the outliner.\nYou can make changes to mrl3 materials by selecting the Material objects in the outliner.\nUnder the Object Properties tab (orange square), there's a panel called \"MHW Mrl3 Material Settings\".\nMake any changes to mrl3 materials there.\nIf you're not modding MHW, you can uncheck this option since it won't be needed",
        default=True)
    default_loadMaterials: BoolProperty(
        name="Load Mesh Materials",
        description="Load materials from the mrl3 file. This may increase the time the model takes to import",
        default=True)
    default_loadUnusedTextures: BoolProperty(
        name="Load Unused Textures",
        description="Loads textures that have no function assigned to them in the material shader graph.\nLeaving this disabled will make materials load faster.\nOnly enable this if you plan on editing the material shader graph",
        default=False)
    default_loadUnusedProps: BoolProperty(
        name="Load Unused Properties",
        description="Loads material properties that have no function assigned to them in the material shader graph.\nLeaving this disabled will make materials load faster.\nOnly enable this if you plan on editing the material shader graph",
        default=False)
    default_useBackfaceCulling: BoolProperty(
        name="Use Backface Culling",
        description="Enables backface culling on materials. May improve Blender's performance on high poly meshes.\nBackface culling will only be enabled on materials without the two sided flag",
        default=False)
    default_reloadCachedTextures: BoolProperty(
        name="Reload Cached Textures",
        description="Convert all textures again instead of reading from already converted textures. Use this if you make changes to textures and need to reload them",
        default=False)

    default_addNestedCollections: BoolProperty(
        name="Add Nested Collections",
        description="Add a general parent collection to place other collections of various imported files."
                    "\nThis will make the collection structure look clearer."
                    "\nLeaving this option enabled is recommended",
        default=True)
    default_createCollections: BoolProperty(
        name="Create Collections",
        description="Create a collection for the mod3 and for each LOD level.\nNote that collections are required for exporting LODs and applying mrl3 changes.\nLeaving this option enabled is recommended",
        default=True)
    default_importArmatureOnly: BoolProperty(
        name="Only Import Armature",
        description="Only import the armature of the mod3 file",
        default=False)
    default_importAllLODs: BoolProperty(
        name="Import All LODs",
        description="Imports all LOD (level of detail) meshes in mod3 file.\nIf unchecked, only the highest LOD of each mesh will be imported",
        default=False)
    default_importBoundingBoxes: BoolProperty(
        name="Import Bounding Boxes",
        description="Import mesh and bone bounding boxes for debugging purposes",
        default=False)
    default_ArmatureDisplayType: EnumProperty(
        name="Armature Display Type",
        # description="Set the display type of armature to be imported",
        items=[("OCTAHEDRAL", "Octahedral", "Display bones as octahedral shape (default)"),
               ("STICK", "Stick", "Display bones as simple 2D lines with dots"),
               ("BBONE", "B-Bone", "Display bones as boxes, showing subdivision and B-Splines"),
               ("ENVELOPE", "Envelope", "Display bones as extruded spheres, showing deformation influence volume"),
               ("WIRE", "Wire", "Display bones as thin wires, showing subdivision and B-Splines"),
               ],
        default=1,
    )
    default_BonesDisplaySize: FloatProperty(
        name="",
        description="Set the display size of the bones to be imported",
        # default=0.004,
        default=5,
        step=100,
        soft_min=0.0,
    )
    # default_loadCTC: BoolProperty(
    #     name="Load CTC Chain",
    #     description="Load physical chain objects from the ctc file",
    #     default=False)
    # default_loadCCL: BoolProperty(
    #     name="Load CCL Collision",
    #     description="Load physical collision objects from the ccl file",
    #     default=False)
    default_loadPhysics: BoolProperty(
        name="Load Chains & Collisions",
        description="Load physical chain and collision objects from the ctc & ccl file",
        default=False)

    '''导出部分，待修改'''
    # Default export options
    default_selectedOnly: BoolProperty(
        name="Selected Objects Only",
        description="Limit export to selected objects",
        default=False)
    default_visibleOnly: BoolProperty(
        name="Visible Objects Only",
        description="Limit export to visible objects",
        default=False)
    default_exportAllLODs: BoolProperty(
        name="Export All LODs",
        description="Export all LODs. If disabled, only LOD0 will be exported. Note that LODs meshes must be grouped inside a collection for each level and that collection must be contained in another collection. See a mesh with LODs imported for reference on how it should look. A target collection must also be set",
        default=True)
    default_autoSolveRepeatedUVs: BoolProperty(
        name="Auto Solve Repeated UVs",
        description="Splits connected UV islands if present. The mesh format does not allow for multiple uvs assigned to a vertex.\nNOTE: This will modify the exported mesh. If auto smooth is disabled on the mesh, the normals may change",
        default=True)
    default_preserveSharpEdges: BoolProperty(
        name="Split Sharp Edges",
        description="Edge splits all edges marked as sharp to preserve them on the exported mesh.\nNOTE: This will modify the exported mesh",
        default=False)
    default_useBlenderMaterialName: BoolProperty(
        name="Use Blender Material Names",
        description="If left unchecked, the exporter will get the material names to be used from the end of each object name. For example, if a mesh is named LOD_0_Group_0_Sub_0__Shirts_Mat, the material name is Shirts_Mat. If this option is enabled, the material name will instead be taken from the first material assigned to the object",
        default=False)
    default_exportBoundingBoxes: BoolProperty(
        name="Export Bounding Boxes",
        description="Exports the original bounding boxes from the \"Import Bounding Boxes\" import option. New bounding boxes will be generated for any bones that do not have them",
        default=False)

    default_drawChainsThroughObjects: BoolProperty(
        name="Draw Chains Through Objects",
        description="Make all ctc chain objects render through any objects in front of them",
        default=True)
    # 是否显示链节点名称
    default_showNodeNames: BoolProperty(
        name="Show Node Names",
        description="Show Node Names in 3D View",
        default=True)
    # 是否前置显示链节点对象
    default_drawNodesThroughObjects: BoolProperty(
        name="Draw Nodes Through Objects",
        description="Make all ctc node and frame objects render through any objects in front of them",
        default=True)
    # 是否显示角度限制锥体
    default_showAngleLimitCones: BoolProperty(
        name="Show Cones",
        description="Show Angle Limit Cones in 3D View",
        default=True)
    # 是否前置显示角度限制锥体
    default_drawConesThroughObjects: BoolProperty(
        name="Draw Cones Through Objects",
        description="Make all angle limit cones render through any objects in front of them",
        default=True)
    # 角度限制轴的显示尺寸
    default_angleLimitDisplaySize: FloatProperty(
        name="Angle Limit Size",
        description="Set the display size of node angle limits",
        default=4.0,
        min=0.0,
        # soft_max=.4,
        # precision=3,
        step=10)
    # 角度限制锥体显示尺寸
    default_coneDisplaySize: FloatProperty(
        name="Cone Size",
        description="Set the display size of node angle limit cones",
        default=5.0,
        min=0.0,
        # soft_max=.2,
        # precision=3,
        step=10)
    default_chainDisplaySize: FloatProperty(
        name="Chain Size",
        description="Set the thickness of chain lines",
        # default=0.006,
        default=6.0,
        min=0.0,
        # soft_max=.2,
        # precision=3,
        # step=.005,
        step=10)
    default_chainColor: FloatVectorProperty(
        name="Chain Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 0.0, 0.0, 0.75))
    # 角度限制锥体的颜色
    default_coneColor: FloatVectorProperty(
        name="Angle Limit Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.6, 0.0, 0.4))
    # 显示关系线
    default_showRelationLines: BoolProperty(
        name="Show Relation Lines",
        description="Show dotted lines indicating object parents.\nNote that this affects all objects, not just ctc objects",
        default=True)
    # 隐藏尾骨的角度限制锥体
    default_hideLastNodeAngleLimit: BoolProperty(
        name="Hide Last Node Cone",
        description="Hide the last ctc node's angle limit cone.\nThis is because the last node is typically unused and has a dummy rotation value",
        default=True)

    # 碰撞体颜色
    default_collisionColor: FloatVectorProperty(
        name="Collision Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(0.003, 0.426, 0.8, 0.3))
    # 是否显示碰撞体名称
    default_showCollisionNames: BoolProperty(
        name="Show Collision Names",
        description="Show CCL Collision Names in 3D View",
        default=True)
    # 是否前置显示碰撞体
    default_drawCollisionsThroughObjects: BoolProperty(
        name="Draw Collisions Through Objects",
        description="Make all ccl collision objects render through any objects in front of them",
        default=True)
    default_drawCapsuleHandlesThroughObjects: BoolProperty(
        name="Draw Handles Through Objects",
        description="Make all capsule handle objects render through any objects in front of them",
        default=True)

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showExternalLinks else "RIGHTARROW"
        row.prop(self, "showExternalLinks", icon=icon, icon_only=True, emboss=False)
        row.label(text="External Links")
        if self.showExternalLinks:
            box = layout.box()
            col = box.column(align=True)

            row = col.row()
            row.scale_y = 1.1
            row.operator("mhw_model.open_github_website")
            row.operator("mhw_model.open_bilibili_website")
            row.operator("mhw_model.open_qq_website")
            row.operator("mhw_model.open_caimogu_website")

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showAdvancedOptions else "RIGHTARROW"
        row.prop(self, "showAdvancedOptions", icon=icon, icon_only=True, emboss=False)
        row.label(text="Advanced Options")
        if self.showAdvancedOptions:
            box = layout.box()
            col = box.column(align=True)

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "dragDropImportOptions")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "showConsole")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "useDDS")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "showCTCProperties")

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showMod3ImportOptions else "RIGHTARROW"
        row.prop(self, "showMod3ImportOptions", icon=icon, icon_only=True, emboss=False)
        row.label(text="Mod3 Import Options")
        if self.showMod3ImportOptions:
            box = layout.box()
            col = box.column(align=True)

            row = col.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Armature Display Type:")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_ArmatureDisplayType", text="")
            col.separator()

            row = col.row(align=True)
            # row.scale_y = 0.75
            row.label(text="Bones Display Size:")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_BonesDisplaySize", text="")
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_addNestedCollections")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "default_createCollections")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_importAllLODs")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_importArmatureOnly")
            col.separator()
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_loadMrl3Data")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_loadMaterials")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_reloadCachedTextures")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_loadUnusedTextures")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_loadUnusedProps")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "default_useBackfaceCulling")
            col.separator()
            col.separator()

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_loadPhysics")

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showMod3ExportOptions else "RIGHTARROW"
        row.prop(self, "showMod3ExportOptions", icon=icon, icon_only=True, emboss=False)
        row.label(text="Mod3 Export Options")
        if self.showMod3ExportOptions:
            box = layout.box()
            col = box.column(align=True)

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_selectedOnly")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_visibleOnly")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "default_exportAllLODs")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_autoSolveRepeatedUVs")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_preserveSharpEdges")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_useBlenderMaterialName")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "default_exportBoundingBoxes")

        '''
        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showCTCVisibilityOptions else "RIGHTARROW"
        row.prop(self, "showCTCVisibilityOptions", icon=icon, icon_only=True, emboss=False)
        row.label(text="CTC Visibility Options")
        if self.showCTCVisibilityOptions:
            box = layout.box()
            box.use_property_split = True
            box.use_property_decorate = False
            col = box.column(align=True)

            # row = col.row(heading="Show Options", align=True)
            # row.scale_y = 1.1
            # row.prop(self, "default_showRelationLines")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "default_showAngleLimitCones")

            row = col.row(heading="Show Options", align=True)
            row.scale_y = 1.1
            row.prop(self, "default_hideLastNodeAngleLimit")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_showNodeNames")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_showCollisionNames")
            col.separator()
            col.separator()

            row = col.row(heading="Draw Options", align=True)
            row.scale_y = 1.1
            row.prop(self, "default_drawChainsThroughObjects")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_drawNodesThroughObjects")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_drawConesThroughObjects")

            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_drawCollisionsThroughObjects")

            # row = col.row(align=True)
            # row.scale_y = 1.1
            # row.prop(self, "default_drawCapsuleHandlesThroughObjects")

            col.separator()
            col.separator()
            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_chainDisplaySize")

            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_coneDisplaySize")

            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_angleLimitDisplaySize")

            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_chainColor")

            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_coneColor")

            col.separator()
            row = col.row(align=True)
            row.scale_y = 1.1
            row.prop(self, "default_collisionColor")
        '''

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showTextureCache else "RIGHTARROW"
        row.prop(self, "showTextureCache", icon=icon, icon_only=True, emboss=False)
        row.label(text="Texture Cache")
        if self.showTextureCache:
            box = layout.box()
            row = box.row()

            row.scale_y = 1.1
            if len(self.textureCachePath) > 110:
                row.alert = True
                row.prop(self, "textureCachePath")
                box.label(text="Texture cache path is very long.", icon="ERROR")
                box.label(text="File paths may exceed the max length of 255 characters and fail to convert.")
                box.label(text="Consider changing this to a shorter path such as D:\MHWMod3\TextureCache.")
            else:
                row.prop(self, "textureCachePath")
            row = box.row()
            if self.textureCacheCheckDate == "":
                checkTextureCacheSize()
            row.label(text=f"Cache Size: {self.textureCacheSizeString}")
            row.scale_y = 1.1
            row.operator("mhw_mod3.check_texture_cache_size", icon="FILE_REFRESH", text="")
            box.label(text=f"Last Checked: {self.textureCacheCheckDate}")
            row = box.row()
            row.scale_y = 1.1
            row.operator("mhw_mod3.open_texture_cache_folder")
            row.operator("mhw_mod3.clear_texture_cache_folder")

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showChunkPath else "RIGHTARROW"
        row.prop(self, "showChunkPath", icon=icon, icon_only=True, emboss=False)
        row.label(text="Chunk Path")
        if self.showChunkPath:
            box = layout.box()
            row = box.row()
            # 解包路径部分
            # layout.label(text="Chunk Path List")
            row.scale_y = 1.1
            row.prop(self, "saveChunkPaths")
            row = box.row()
            row.template_list("MOD3_UL_ChunkPathList", "", self, "chunkPathList_items", self, "chunkPathList_index", rows=3)
            row = box.row()
            row.scale_y = 1.1
            row.operator("mhw_mod3.chunk_path_list_add_item")
            row.operator("mhw_mod3.chunk_path_list_remove_item")

            # 排序按钮
            row = box.row()
            row.scale_y = 1.1
            row.operator("mhw_mod3.chunk_path_list_reorder_item", text="Move Up").direction = 'UP'
            row.operator("mhw_mod3.chunk_path_list_reorder_item", text="Move Down").direction = 'DOWN'

        row = layout.row()
        icon = "DOWNARROW_HLT" if self.showAutoUpdate else "RIGHTARROW"
        row.prop(self, "showAutoUpdate", icon=icon, icon_only=True, emboss=False)
        row.label(text="Auto Update")
        if self.showAutoUpdate:
            addon_updater_ops.update_settings_ui(self, context)