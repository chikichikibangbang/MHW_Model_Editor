import os
import bpy
from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       CollectionProperty,
                       IntVectorProperty
                       )

from ..common.general_function import string_reformat

'''用于获取能够控制材质节点参数的mrl3材质参数，以便在property list中添加扳手图标'''
def getUsableProps(propFileList):
    propSet = set()
    path = os.path.split(__file__)[0]
    # path = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]), "mrl3")
    for file in propFileList:
        # print(os.path.join(path, file))
        f = open(os.path.join(path, file), "r")
        for line in f.readlines():
            if "addPropertyNode(matInfo[\"mPropDict\"]" in line:
                propName = line.split("addPropertyNode(matInfo[\"mPropDict\"][\"")[1].split("\"]", 1)[0]
                propSet.add(string_reformat(propName))
        f.close()
    return propSet


try:
    editablePropsSet = getUsableProps(
        propFileList=[

            "blender_mod3_mrl3.py",
            "mrl3_nodes.py",])
except Exception as err:
    print(f"Unable to load usable properties - {str(err)}")
    editablePropsSet = set()
# print(editablePropsSet)

def update_materialName(self, context):
    parentObj = self.id_data
    try:
        #print(parentObj)
        if parentObj != None:
            split = parentObj.name.split("(",1)
            if len(split) == 2:
                parentObj.name = f"{split[0]}({self.materialName})"
            else:
                parentObj.name =f"Mrl3 Material 00 ({self.materialName})"
    except:
        pass

def filterMrl3Collection(self, collection):
    # return True if ((collection.get("~TYPE") == "MHW_MRL3_COLLECTION") or (".mrl3" in collection.name)) else False
    return True if collection.get("~TYPE") == "MHW_MRL3_COLLECTION" else False

def filterMod3Collection(self, collection):
    # return True if ((collection.get("~TYPE") == "MHW_MOD3_COLLECTION") or (".mod3" in collection.name)) else False
    return True if collection.get("~TYPE") == "MHW_MOD3_COLLECTION" else False

def linkBlenderMaterial(materialObj, materialName):
    # Check if material name is used more than once, link it if it's only used once
    matchCount = 0
    materialKey = None
    for mat in bpy.data.materials.keys():
        if materialName == mat.split(".", 1)[0]:
            materialKey = mat
            matchCount += 1
    if matchCount == 1:
        # print(f"Linked {materialObj.name} to {bpy.data.materials[materialKey]} (Fast)")
        materialObj.mhw_mrl3_material.linkedMaterial = bpy.data.materials[materialKey]
    elif matchCount > 1:
        # If there's more than one material with the same name, search for a mesh collection with the same name as the mrl3 and find the material assigned to an object
        mrl3CollectionName = None  # Get first mrl3 collection linked to material obj
        for collection in materialObj.users_collection:
            if ".mrl3" in collection.name:
                mrl3CollectionName = collection.name

        if mrl3CollectionName != None:
            mod3Collection = bpy.data.collections.get(mrl3CollectionName.replace(".mrl3", ".mod3", 1), None)

            if mod3Collection != None:
                meshObj = None  # Mesh object with mrl3 material assigned to it
                for obj in mod3Collection.all_objects:
                    if obj.type == "MESH":
                        if materialName in obj.name and "__" in obj.name:
                            if materialName == obj.name.split("__", 1)[1].split(".")[0]:
                                meshObj = obj
                                break
                if meshObj != None:
                    for material in meshObj.data.materials:
                        if material.name.split(".")[0] == materialName:
                            materialObj.mhw_mrl3_material.linkedMaterial = material
                            # print(f"Linked {materialObj.name} to {material} (Slow)")
                            break

def update_mrl3Collection(self, context):#Set mod3 collection automatically if it exists when active mrl3 is changed
    if self.mrl3Collection != None and self.mrl3Collection.name.replace(".mrl3",".mod3") in bpy.data.collections:
        self.mod3Collection = bpy.data.collections[self.mrl3Collection.name.replace(".mrl3",".mod3")]


def update_materialNodes(self, context):
    obj = self.id_data
    if self.prop_name in editablePropsSet:
        # matName = obj.mhw_mrl3_material.materialName
        if obj.mhw_mrl3_material.linkedMaterial == None:
            linkBlenderMaterial(obj, obj.mhw_mrl3_material.materialName)

        # TODO filter by collection
        if obj.mhw_mrl3_material.linkedMaterial != None:
            node = obj.mhw_mrl3_material.linkedMaterial.node_tree.nodes.get(self.prop_name, None)
            if node != None:
                # print(self.data_type)
                # print(node.name)
                if self.data_type == "FLOAT":
                    value = self.float_value
                    node.outputs["Value"].default_value = value
                elif self.data_type == "INT":
                    value = self.int_value
                    node.outputs["Value"].default_value = value
                elif self.data_type == "UINT":
                    value = self.uint_value
                    node.outputs["Value"].default_value = value
                elif self.data_type == "BOOL":
                    value = 1.0 if self.bool_value else 0.0
                    node.outputs["Value"].default_value = value
                elif self.data_type == "FLOAT[2]":
                    value = list(self.float2_value)
                    node.inputs[0].default_value = value[0]
                    node.inputs[1].default_value = value[1]
                    node.inputs[2].default_value = 0.0
                    node.inputs[3].default_value = 0.0
                elif self.data_type == "FLOAT[3]":
                    value = list(self.float3_value)
                    node.inputs[0].default_value = value[0]
                    node.inputs[1].default_value = value[1]
                    node.inputs[2].default_value = value[2]
                    node.inputs[3].default_value = 0.0
                elif self.data_type == "FLOAT[4]":
                    value = list(self.float4_value)
                    node.inputs[0].default_value = value[0]
                    node.inputs[1].default_value = value[1]
                    node.inputs[2].default_value = value[2]
                    node.inputs[3].default_value = value[3]
                elif self.data_type == "COLOR":
                    value = list(self.color_value)
                    node.inputs["Color"].default_value = value
                else:
                    value = 0.0
                    node.outputs["Value"].default_value = value


def update_modDirectoryRelPathToAbs(self, context):
    try:

        if "//" in self.modDirectory:
            # print("updated path")
            self.modDirectory = os.path.realpath(bpy.path.abspath(self.modDirectory))
    except:
        pass


def update_textureDirectoryRelPathToAbs(self, context):
    try:
        if "//" in self.textureDirectory:
            # print("updated path")
            self.textureDirectory = os.path.realpath(bpy.path.abspath(self.textureDirectory))
    except:
        pass

def update_listFilter(self, context):
    context.area.tag_redraw()

'''移除sampler，考虑建一个独立的samplerPG'''
class Mrl3MapPG(bpy.types.PropertyGroup):
    # resourceIndex: IntProperty(name="")
    # resourceType: IntProperty(
    #     name="",
    # )
    mapType: StringProperty(
        name="",
    )
    mapPath: StringProperty(
        name="",
    )
    # resourceBytes: IntVectorProperty(
    #     name="",
    #     size=3,
    # )
    resourceHash: StringProperty(name="")


class Mrl3SamplerPG(bpy.types.PropertyGroup):
    # resourceIndex: IntProperty(name="")
    samplerType: StringProperty(
        name="",
    )
    samplerIndex:IntProperty(
        name="",
        min=0,
    )
    # resourceBytes: IntVectorProperty(
    #     name="",
    #     size=3,
    # )
    resourceHash: StringProperty(name="")


class Mrl3PropPG(bpy.types.PropertyGroup):
    prop_name: StringProperty(
        name="",
    )
    data_type: EnumProperty(
        items=[
            ('FLOAT', 'Float', 'Float'),
            ('INT', 'Int', 'Int'),
            ('UINT', 'Uint', 'Uint'),
            ('BOOL', 'Bool', 'Bool'),
            ('FLOAT[2]', 'Float[2]', 'Float[2]'),
            ('FLOAT[3]', 'Float[3]', 'Float[3]'),
            ('FLOAT[4]', 'Float[4]', 'Float[4]'),
            ('COLOR', 'Color', 'Color'),
        ],
        name="Data Type",
    )
    float_value: FloatProperty(
        name="",
        update=update_materialNodes
    )
    int_value: IntProperty(
        name="",
        update=update_materialNodes
    )
    uint_value: IntProperty(
        name="",
        min=0,
        update=update_materialNodes
    )
    bool_value: BoolProperty(
        name="",
        default=False,
        update=update_materialNodes
    )
    float2_value: FloatVectorProperty(
        name="",
        size=2,
        update=update_materialNodes
    )
    float3_value: FloatVectorProperty(
        name="",
        size=3,
        update=update_materialNodes
    )
    float4_value: FloatVectorProperty(
        name="",
        size=4,
        update=update_materialNodes
    )
    color_value: FloatVectorProperty(
        name="",
        subtype='COLOR',
        size=4,
        min=0.0,
        soft_max=1.0,
        update=update_materialNodes
    )
    # resourceBytes: IntVectorProperty(
    #     name="",
    #     size=3,
    # )
    # padding: IntProperty(#Not exposed in editor, used for SF6's weird mmtrs padding
    #     name="",
    #     default=0
    # )

'''要考虑导出时resource的排序问题（应该完全按照原本的顺序）'''
# 新增资源属性组
class Mrl3PropBlockPG(bpy.types.PropertyGroup):
    # resource_id: StringProperty(name="Resource ID")  # 资源标识
    propertyList_items: CollectionProperty(type=Mrl3PropPG)  # 资源属性列表
    propertyList_index: IntProperty(name="")  # 属性索引
    # is_expanded: BoolProperty(name="", default=True)  # 控制面板折叠
    # resourceIndex: IntProperty(name="")
    propertyBlockType: StringProperty(name="")
    # resourceBytes: IntVectorProperty(
    #     name="",
    #     size=3,
    # )
    # blockOffset: IntProperty(name="")
    resourceHash: StringProperty(name="")

class Mrl3MaterialPG(bpy.types.PropertyGroup):
    # headID: StringProperty(
    #     name="Head ID",
    #     description="Do not change this unless you know what you're doing",
    #     default="1159129003",
    # )
    materialName: StringProperty(
        name="Material Name",
        description="The name of the current mrl3 material.\nThe material name must match on the mod3 and mrl3 file.",
        update=update_materialName
    )
    shaderHash1: StringProperty(
        name="Shader Hash1",
        description="Do not change this unless you know what you're doing",
    )
    shaderHash2: StringProperty(
        name="Shader Hash2",
        description="Do not change this unless you know what you're doing",
    )
    mastermaterialType: StringProperty(
        name="Master Material Type",
        description="The type of the current mrl3 material.\nDo not change this unless you know what you're doing.",
        # update=update_materialName
    )
    # materialBlockSize: IntProperty(name="")
    surfaceDirection: StringProperty(
        name="Surface Direction",
        description="",
        # default="1100",
    )
    # resourceCount: IntProperty(name="")
    alphaCoef: IntVectorProperty(
        name="Alpha Coef",
        description="",
        default=(0, 0, 0, 0),
        size=4,
        min=0,
        max=255,
        # subtype="XYZ"
    )
    # shaderType: EnumProperty(
    #     name="Material Shader Type",
    #     description="Set shader type",
    #     items=[("0", "Standard", ""),
    #            ("1", "Decal", ""),
    #            ("2", "DecalWithMetallic", ""),
    #            ("3", "DecalNRMR", ""),
    #            ("4", "Transparent", ""),
    #            ("5", "Distortion", ""),
    #            ("6", "PrimitiveMesh", ""),
    #            ("7", "PrimitiveSolidMesh", ""),
    #            ("8", "Water", ""),
    #            ("9", "SpeedTree", ""),
    #            ("10", "GUI", ""),
    #            ("11", "GUIMesh", ""),
    #            ("12", "GUIMeshTransparent", ""),
    #            ("13", "ExpensiveTransparent", ""),
    #            ("14", "Forward", ""),
    #            ("15", "RenderTarget", ""),
    #            ("16", "PostProcess", ""),
    #            ("17", "PrimitiveMaterial", ""),
    #            ("18", "PrimitiveSolidMaterial", ""),
    #            ("19", "SpineMaterial", ""),
    #            ("20", "Max", ""),
    #
    #            ]
    # )
    linkedMaterial: PointerProperty(
    	name="Linked Material",
    	description="The blender material that corresponds to this mrl3 material. Any changes made to supported mrl3 properties will reflect on the blender material.\nIf a linked material is not set, it will be set automatically once an mrl3 property is changed",
    	type=bpy.types.Material,
    )
    mapList_items: CollectionProperty(type=Mrl3MapPG)
    mapList_index: IntProperty(name="")

    samplerList_items: CollectionProperty(type=Mrl3SamplerPG)
    samplerList_index: IntProperty(name="")

    # flags: PointerProperty(type=MDFFlagsPropertyGroup)

    # propertyList_items: CollectionProperty(type=Mrl3PropPG)
    # propertyList_index: IntProperty(name="")

    propertyBlock_items: CollectionProperty(type=Mrl3PropBlockPG)  # 新增资源集合
    propertyBlock_index: IntProperty(name="")  # 资源索引





class MESH_UL_Mrl3MapList(bpy.types.UIList):
    filterString: StringProperty(
        name="Filter",
        description="Search the list for items that contain this string.\nPress enter to search",
        default='',
        update=update_listFilter)

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display the properties of each item in the UIList
        # col1.label(text=item.name)
        layout.ui_units_y = 1.4
        split = layout.split(factor=0.35)
        col1 = split.column()
        col2 = split.column()
        row = col2.row()
        col2.alignment = 'RIGHT'
        col1.label(text=item.mapType)
        row.prop(item, "mapPath")

    # Disable double-click to rename
    def invoke(self, context, event):
        return {'PASS_THROUGH'}

    def draw_filter(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, 'filterString', text='', icon='VIEWZOOM')

    def filter_items(self, context, data, propname):
        """Filter and order items in the list."""
        filtered = []
        ordered = []
        items = getattr(data, propname)

        # Initialize with all items visible
        if self.filterString:
            filtered = [self.bitflag_filter_item] * len(items)
            for i, item in enumerate(items):
                if self.filterString.lower() not in item.mapType.lower():
                    filtered[i] &= ~self.bitflag_filter_item
        return filtered, ordered


class MESH_UL_Mrl3PropertyList(bpy.types.UIList):
    filterString: StringProperty(
        name="Filter",
        description="Search the list for items that contain this string.\nPress enter to search",
        default='',
        update=update_listFilter)

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display the properties of each item in the UIList
        # col1.label(text=item.name)
        layout.ui_units_y = 1.4
        split = layout.split(factor=0.48)
        col1 = split.column()
        col2 = split.column()
        row = col2.row()
        col2.alignment = 'RIGHT'
        col1.label(text=item.prop_name, icon="MODIFIER" if item.prop_name in editablePropsSet else "NONE")
        # col1.label(text=item.prop_name, icon="MODIFIER")

        if item.data_type == 'FLOAT':
            row.prop(item, "float_value")
        elif item.data_type == 'INT':
            row.prop(item, "int_value")
        elif item.data_type == 'UINT':
            row.prop(item, "uint_value")
        elif item.data_type == 'BOOL':
            row.prop(item, "bool_value")
        elif item.data_type == 'FLOAT[2]':
            row.prop(item, "float2_value")
        elif item.data_type == 'FLOAT[3]':
            row.prop(item, "float3_value")
        elif item.data_type == 'FLOAT[4]':
            row.prop(item, "float4_value")
        elif item.data_type == 'COLOR':
            row.prop(item, "color_value")

    # Disable double-click to rename
    def invoke(self, context, event):
        return {'PASS_THROUGH'}

    def draw_filter(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, 'filterString', text='', icon='VIEWZOOM')

    def filter_items(self, context, data, propname):
        """Filter and order items in the list."""
        filtered = []
        ordered = []
        items = getattr(data, propname)

        # Initialize with all items visible
        if self.filterString:
            filtered = [self.bitflag_filter_item] * len(items)
            for i, item in enumerate(items):
                if self.filterString.lower() not in item.prop_name.lower():
                    filtered[i] &= ~self.bitflag_filter_item
        return filtered, ordered

class MESH_UL_Mrl3SamplerList(bpy.types.UIList):
    filterString: StringProperty(
        name="Filter",
        description="Search the list for items that contain this string.\nPress enter to search",
        default='',
        update=update_listFilter)

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # Display the properties of each item in the UIList
        # col1.label(text=item.name)
        layout.ui_units_y = 1.4
        split = layout.split(factor=0.35)
        col1 = split.column()
        col2 = split.column()
        row = col2.row()
        col2.alignment = 'RIGHT'
        col1.label(text=item.samplerType)
        row.prop(item, "samplerIndex")

    # Disable double-click to rename
    def invoke(self, context, event):
        return {'PASS_THROUGH'}

    def draw_filter(self, context, layout):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, 'filterString', text='', icon='VIEWZOOM')

    def filter_items(self, context, data, propname):
        """Filter and order items in the list."""
        filtered = []
        ordered = []
        items = getattr(data, propname)

        # Initialize with all items visible
        if self.filterString:
            filtered = [self.bitflag_filter_item] * len(items)
            for i, item in enumerate(items):
                if self.filterString.lower() not in item.samplerType.lower():
                    filtered[i] &= ~self.bitflag_filter_item
        return filtered, ordered



class Mrl3ToolPanelPG(bpy.types.PropertyGroup):

    # def getMaterialPresets(self, context):
    # 	return reloadPresets(context.scene.re_mdf_toolpanel.activeGame)

    mrl3Collection: PointerProperty(
        name="",
        description="Set the blue collection containing the mrl3 file to edit.\nYou can create a new mrl3 collection by pressing the \"Create Mrl3 Collection\" button",
        type=bpy.types.Collection,
        poll=filterMrl3Collection,
        update=update_mrl3Collection
    )
    mod3Collection: PointerProperty(
        name="",
        description="Set the red mod3 collection to apply the active mrl3 collection to",
        type=bpy.types.Collection,
        poll=filterMod3Collection
    )
    modDirectory: StringProperty(
    	name="",
    	subtype="DIR_PATH",
    	description="Set the nativePC directory of your mod."
                    "\nThis is used by \"Apply Active Mrl3\" and \"Copy Converted Tex\"."
                    "\nThis will be set automatically when a mod3 or mrl3 file is exported."
                    "\nExample:\n" + r"D:\SteamLibrary\steamapps\common\Monster Hunter World\nativePC",
    	update=update_modDirectoryRelPathToAbs
    )
    textureDirectory: StringProperty(
        name="",
        subtype="DIR_PATH",
        description="Set the directory containing images to be converted to .tex files",
        update=update_textureDirectoryRelPathToAbs
    )
    openConvertedFolder: BoolProperty(
        name="Open Folder After Conversion",
        description="Opens the directory containing the converted image files after conversion",
        default=False,
    )

    # mrl3 load settings
    loadUnusedTextures: BoolProperty(
        name="Load Unused Textures",
        description="Loads textures that have no function assigned to them in the material shader graph.\nLeaving this disabled will make materials load faster.\nOnly enable this if you plan on editing the material shader graph",
        default=True)
    loadUnusedProps: BoolProperty(
        name="Load Unused Material Properties",
        description="Loads material properties that have no function assigned to them in the material shader graph.\nLeaving this disabled will make materials load faster.\nOnly enable this if you plan on editing the material shader graph",
        default=False)
    useBackfaceCulling: BoolProperty(
        name="Use Backface Culling",
        description="Enables backface culling on materials. May improve Blender's performance on high poly meshes.\nBackface culling will only be enabled on materials without the two sided flag",
        default=False)
    reloadCachedTextures: BoolProperty(
        name="Reload Cached Textures",
        description="Convert all textures again instead of reading from already converted textures.\nUse this if you make changes to textures and need to reload them",
        default=True)

