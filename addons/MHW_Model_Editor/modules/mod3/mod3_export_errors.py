import bpy
import textwrap
from ..common.message_functions import textColors, printErrorInfo
from bpy.props import StringProperty, IntProperty, CollectionProperty
from bpy.types import Operator
ERROR_WINDOW_SIZE = 750
SPLIT_FACTOR = .35


class MHWMod3ErrorEntry(bpy.types.PropertyGroup):
    errorType: StringProperty(
        name="",
    )
    errorName: StringProperty(
        name="",
    )
    errorDescription: StringProperty(
        name="",
    )
    objectSetString: StringProperty(
        name="",
    )
    boneSetString: StringProperty(
        name="",
    )
    errorCount: IntProperty(
        name="",
    )


class MESH_UL_Mod3_MHWMod3ErrorList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=f"{item.errorType} ({str(item.errorCount)})")

    # Disable double-click to rename
    def invoke(self, context, event):
        return {'PASS_THROUGH'}


class WM_OT_Mod3_ShowMHWMod3ErrorWindow(Operator):
    """显示导出时的错误信息"""
    bl_idname = 'mhw_mod3.show_export_error_window'
    bl_label = 'MHW Mod3 Export Error'
    bl_options = {'REGISTER'}
    collectionName: StringProperty()
    armatureName: StringProperty()
    errorList_items: CollectionProperty(type=MHWMod3ErrorEntry)
    errorList_index: IntProperty(name="")

    def execute(self, context):
        # print("Displayed error window.")
        return {'FINISHED'}

    def invoke(self, context, event):
        # 获取当前blender屏幕的正中心位置
        window = context.window
        centerX = window.width // 2
        centerY = window.height // 2

        # currentX = event.mouse_region_X
        # currentY = event.mouse_region_Y

        window.cursor_warp(centerX, centerY)
        for entry in bpy.context.scene.mhw_mod3_error_list:
            item = self.errorList_items.add()
            for key, value in entry.items():
                item[key] = value
        return context.window_manager.invoke_props_dialog(self, width=ERROR_WINDOW_SIZE)

    def draw(self, context):
        layout = self.layout
        rowCount = 2
        uifontscale = 9 * context.preferences.view.ui_scale
        max_label_width = int((ERROR_WINDOW_SIZE * (1 - SPLIT_FACTOR) * (2 - SPLIT_FACTOR)) // uifontscale)
        layout.label(
            text=f"The mod3 meshes have {len(self.errorList_items)} {'issues' if len(self.errorList_items) > 1 else 'issue'} that must be fixed before it can be exported.",
            icon="ERROR")
        # row = layout.row()
        layout.label(text=f"Target Collection: {self.collectionName}")
        layout.label(text=f"Target Armature: {self.armatureName}")

        row = layout.row().separator()
        split = layout.split(
            factor=SPLIT_FACTOR)  # Indent list slightly to make it more clear it's a part of a sub panel
        col1 = split.column()
        col2 = split.column()

        """
        layout.prop(self,"currentError")
        row.label(text =f"Error {str(self.currentError)} / {str(len(bpy.context.scene.re_mesh_error_list))}")
        if self.currentError <= len(bpy.context.scene.re_mesh_error_list):
        """

        if len(self.errorList_items) != 0:
            item = self.errorList_items[self.errorList_index]
            # col2.label(text=f"Error Info: {item.errorType}")
            box = col2.box()
            # box2 = col2.box()

            for line in item.errorDescription.splitlines():
                line = line.strip()

                # 按行宽拆分并绘制
                for chunk in textwrap.wrap(line, width=max_label_width):
                    box.label(text=chunk)
                    rowCount += 1

            '''考虑将boneSetString按每行多个骨骼名绘制，而不是每行一个'''
            row = layout.row()
            string = item.objectSetString if item.objectSetString != "" else item.boneSetString
            if string != "":
                box2 = col2.box()
                for line in string.splitlines():
                    line = line.strip()
                    for chunk in textwrap.wrap(line, width=max_label_width):
                        box2.label(text=chunk)
                        rowCount += 1
        # col1.label(text=f"Error Count: {str(len(self.errorList_items))}")
        col1.template_list(
            listtype_name="MESH_UL_Mod3_MHWMod3ErrorList",
            list_id="",
            dataptr=self,
            propname="errorList_items",
            active_dataptr=self,
            active_propname="errorList_index",
            rows=rowCount,
            type='DEFAULT'
        )


mod3ErrorInfoDict = {
"NoTargetMod3Collection": """No Target Mod3 Collection
ERROR INFO:
Target mod3 collection was not selected when exporting.
——————————————
HOW TO FIX:
Select a target mod3 collection in the export options.""",

"NoMeshesInCollection": """No Meshes In Collection
ERROR INFO:
No meshes were found in the target mod3 collection.
Also maybe there are no selected or visible meshes.
——————————————
HOW TO FIX:
Select a target mod3 collection in the export options that contains meshes.
If you checked \"Selected Objects Only\" or \"Visible Objects Only\" in the export options, please make sure there are selected or visible meshes.""",

"MultipleSameLodCollections": """Multiple Same Lod Collections
ERROR INFO:
There are multiple child lod collections with the same lod level.
——————————————
HOW TO FIX:
Change the name of child lod collections to ensure that each lod level is unique.""",

"MoreThanOneArmature": """More Than One Armature
ERROR INFO:
More than one armature was found in the target mod3 collection. 
——————————————
HOW TO FIX:
Move the extra armature into another collection or delete it.""",

"MaxBonesExceeded": """Max Bones Exceeded
ERROR INFO:
The amount of bones on the armature exceeds the maximum limit of 255.
——————————————
HOW TO FIX:
Reduce the amount of bones on the armature.""",

"IncorrectBoneNameFormat": """Incorrect Bone Name Format
ERROR INFO:
Some bones are not named with format \"MhBone__xxx\", or the name suffix index exceeds the maximum limit of 511.
——————————————
HOW TO FIX:
Change the bone name to \"MhBone__xxx\", where xxx is suffix index, such as \"MhBone__150\".
And also make sure that the suffix index is less than 512.
""",

"NoWeightsOnMesh": """No Weights On Mesh
ERROR INFO:
A mesh has an armature, but no weights assigned to bones.
——————————————
HOW TO FIX:
Add a new vertex group and weight it to a bone on the armature in weight paint mode.
""",

"NoArmatureInCollection": """No Armature In Collection
ERROR INFO:
A mesh has weights but no armature is inside the mesh collection.
——————————————
HOW TO FIX:
Move the armature that the mesh is parented to inside the mod3 collection.
You can do this by selecting the armature in the outliner and dragging it onto the mod3 collection.
""",

"NoVerticesOnSubMesh": """No Vertices On Sub Mesh
ERROR INFO:
A mesh has no vertices. All meshes must have at least 3 vertices and 1 face.
——————————————
HOW TO FIX:
Delete the listed mesh.
""",

"NoFacesOnSubMesh": """No Faces On Sub Mesh
ERROR INFO:
A mesh has no faces. All meshes must have at least 3 vertices and 1 face.
——————————————
HOW TO FIX:
Delete the listed mesh.
""",

"NoMaterialOnSubMesh": """No Material On Sub Mesh
ERROR INFO:
A mesh has no material assigned to it. All meshes must have one material assigned to them.
——————————————
HOW TO FIX:
Specify an mrl3 material name on the end of the object name separated by two underscores.
Example Object Name: Group_0_Sub_0__Ch_Pl_Standard_Mt__2
""",

"MaxVerticesExceeded": """Max Vertices Exceeded On Sub Mesh
ERROR INFO:
A mesh exceeded the limit of 65535 vertices.
——————————————
HOW TO FIX:
Separate parts of the mesh into more sub meshes.
Or use the decimate modifier to reduce mesh quality.
""",

"MaxFacesExceeded": """Max Faces Exceeded On Sub Mesh
ERROR INFO:
A mesh exceeded the limit of 1431655 faces.
——————————————
HOW TO FIX:
Separate parts of the mesh into more sub meshes.
Or use the decimate modifier to reduce mesh quality.
""",

"NonTriangulatedFace": """Non Triangulated Faces
ERROR INFO:
A mesh has non triangulated faces. All faces must be triangulated.
——————————————
HOW TO FIX:
Select the listed mesh in edit mode, press A to select all vertices. Press Ctrl + T to triangulate faces.
""",

"NoUVMapOnSubMesh": """No UV Map On Sub Mesh
ERROR INFO:
A mesh has no UV map. All meshes require at least one uv map.
——————————————
HOW TO FIX:
Create a UV map.
""",

"MultipleUVsAssignedToVertex": """Multiple UVs Assigned To Vertex
ERROR INFO:
A mesh has multiple uvs assigned to a single vertex.
——————————————
HOW TO FIX:
Check \"Auto Solve Repeated UVs\" in the export options.
""",

"MaxWeightsPerVertexExceeded": """Max Weights Per Vertex Exceeded On Sub Mesh
ERROR INFO:
A vertex has more the maximum of 8 weights assigned to it.
——————————————
HOW TO FIX:
Limit total weights to 8 in weight paint mode and normalize all weights.
If there are not too many bones in the armature, you can also limit total weights to 4.
""",

"LooseVerticesOnSubMesh": """Loose Vertices On Sub Mesh
ERROR INFO:
A mesh has loose vertices with no faces assigned.
——————————————
HOW TO FIX:
Select the listed mesh in edit mode, press A to select all vertices. 
Then select > Mesh > Clean Up > Delete Loose in the menu bar at the top.
""",

"NoBonesOnArmature": """No Bones on Armature
ERROR INFO:
The armature in the target collection has no bones.
——————————————
HOW TO FIX:
Import a valid armature from an existing mod3 file.
""",

"TotalVerticesExceeded": """Total Vertices Exceeded Max Limit
ERROR INFO:
Total vertices count exceeds the maximum limit of 4294967295.
——————————————
HOW TO FIX:
Reconsider the life choices that led you to decide to try to export so many vertices.""",

"TotalFacesExceeded": """Total Faces Exceeded Max Limit
ERROR INFO:
Total faces count exceeds the maximum limit of 1431655.
——————————————
HOW TO FIX:
Reconsider the life choices that led you to decide to try to export so many faces.""",

"TotalMeshesExceeded": """Total Meshes Exceeded Max Limit
ERROR INFO:
Total meshes count exceeds the maximum limit of 65535.
——————————————
HOW TO FIX:
Reconsider the life choices that led you to decide to try to export so many meshes.""",

"TotalMaterialsExceeded": """Total Materials Exceeded Max Limit
ERROR INFO:
Total materials count exceeds the maximum limit of 65535.
——————————————
HOW TO FIX:
Reconsider the life choices that led you to decide to try to export so many materials.""",
}

def printMod3ErrorDict(errorDict):
    print(f"\n{textColors.FAIL}Unable to export mod3. {len(errorDict)} error(s) were found that need to be fixed.{textColors.ENDC}\n")
    printErrorInfo(errorDict, mod3ErrorInfoDict)
    print("\033[92m__________________________________\nMHW Mod3 export failed.\033[0m")

def showMHWMod3ErrorWindow(errorDict, colName="", armName=""):
    bpy.types.Scene.mhw_mod3_error_list = CollectionProperty(type=MHWMod3ErrorEntry)
    bpy.context.scene.mhw_mod3_error_list.clear()
    for index, errorType in enumerate(sorted(errorDict.keys())):
        item = bpy.context.scene.mhw_mod3_error_list.add()
        item.errorCount = errorDict[errorType]["count"]
        errorInfoSplit = mod3ErrorInfoDict[errorType].split("\n", 1)

        item.errorType = errorInfoSplit[0]
        item.errorDescription = errorInfoSplit[1]
        objectSet = errorDict[errorType].get("objectSet", {})
        boneSet = errorDict[errorType].get("boneSet", {})
        errorInfo = mod3ErrorInfoDict[errorType]
        nameListString = ""
        # if objectSet:
        #     # nameListString = f"\nObjects with this error ({str(len(objectSet))}):\n"
        #     nameListString = f"\nERROR OBJECTS:\n"
        #     for name in sorted(list(objectSet)):
        #         # nameListString += "[" + name + "]\n"
        #         nameListString += f"{name}\n"
        #     item.objectSetString = nameListString
        # elif boneSet:
        #     # nameListString = f"\nObjects with this error ({str(len(objectSet))}):\n"
        #     nameListString = f"\nERROR BONES:\n"
        #     for name in sorted(list(boneSet)):
        #         # nameListString += "[" + name + "]\n"
        #         nameListString += f"{name}\n"
        #     item.boneSetString = nameListString

        if objectSet:
            nameListString = "\nERROR OBJECTS:\n" + "\n".join(sorted(objectSet))
            item.objectSetString = nameListString
        elif boneSet:
            nameListString = "\nERROR BONES:\n" + "\n".join(sorted(boneSet))
            item.boneSetString = nameListString

    # if armatureObj != None:
    #     armatureName = armatureObj.name
    # else:
    #     armatureName = ""

    bpy.ops.mhw_mod3.show_export_error_window('INVOKE_DEFAULT', collectionName=colName, armatureName=armName)
