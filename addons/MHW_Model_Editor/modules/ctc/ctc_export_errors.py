import bpy
import textwrap
from .....common.i18n.i18n import i18n
from ..common.message_functions import textColors, printErrorInfo
from bpy.props import StringProperty, IntProperty, CollectionProperty
from bpy.types import Operator
ERROR_WINDOW_SIZE = 750
SPLIT_FACTOR = .35


class MHWCTCErrorEntry(bpy.types.PropertyGroup):
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


class MESH_UL_CTC_MHWCTCErrorList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=f"{i18n(item.errorType)} ({str(item.errorCount)})")

    # Disable double-click to rename
    def invoke(self, context, event):
        return {'PASS_THROUGH'}


class WM_OT_CTC_ShowMHWCTCErrorWindow(Operator):
    """显示导出时的错误信息"""
    bl_idname = 'mhw_ctc.show_export_error_window'
    bl_label = 'MHW CTC Export Error'
    bl_options = {'REGISTER'}
    collectionName: StringProperty()
    armatureName: StringProperty()
    errorList_items: CollectionProperty(type=MHWCTCErrorEntry)
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
        for entry in bpy.context.scene.mhw_ctc_error_list:
            item = self.errorList_items.add()
            for key, value in entry.items():
                item[key] = value
        return context.window_manager.invoke_props_dialog(self, width=ERROR_WINDOW_SIZE)

    def draw(self, context):
        lang = bpy.context.preferences.view.language
        layout = self.layout
        rowCount = 2
        uifontscale = 9 * context.preferences.view.ui_scale
        max_label_width = int((ERROR_WINDOW_SIZE * (1 - SPLIT_FACTOR) * (2 - SPLIT_FACTOR)) // uifontscale)
        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            layout.label(
                text=f"CTC对象有 {len(self.errorList_items)} 个需要被修复的问题.", icon="ERROR")
        else:
            layout.label(
                text=f"The ctc objects have {len(self.errorList_items)} {'issues' if len(self.errorList_items) > 1 else 'issue'} that must be fixed before it can be exported.",
                icon="ERROR")
        # row = layout.row()
        layout.label(text=f"{i18n('Target Collection:')} {self.collectionName}")
        # layout.label(text=f"Target Armature: {self.armatureName}")

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
            listtype_name="MESH_UL_CTC_MHWCTCErrorList",
            list_id="",
            dataptr=self,
            propname="errorList_items",
            active_dataptr=self,
            active_propname="errorList_index",
            rows=rowCount,
            type='DEFAULT'
        )
        

ctcErrorInfoDict = {
"NoTargetCTCCollection": """No Target CTC Collection
ERROR INFO:
Target ctc collection was not selected when exporting.
——————————————
HOW TO FIX:
Select a target ctc collection in the export options.""",

"HeaderHasParent": """Header Has Parent
ERROR INFO:
CTC header cannot be a child of other objects.
——————————————
HOW TO FIX:
Make sure ctc header doesn't have parent objects.
""",

"NodeHasMoreThanOneFrame": """Node Has More Than One Frame
ERROR INFO:
Some nodes have more than one frame as child.
——————————————
HOW TO FIX:
Make sure each node has only one child frame.
""",

"NodeHasNoFrame": """Node Has No Frame
ERROR INFO:
Some nodes have no frame as child.
——————————————
HOW TO FIX:
Make sure each node has only one child frame.
""",

"IncorrectNodeParent": """Incorrect Node Parent
ERROR INFO:
Some nodes have incorrect parent object types.
Or maybe node has no parent chain or node object.
——————————————
HOW TO FIX:
Make sure each node has a parent chain or node object.
""",

"InvalidNodeConstraint": """Invalid Node Constraint
ERROR INFO:
The \"BoneName\" constraint of node has no target or subtarget.
——————————————
HOW TO FIX:
Make sure \"BoneName\" constraint of node has target armature and subtarget bone.
""",

"NodeHasNoConstraint": """Node Has No Constraint
ERROR INFO:
Some nodes have no \"BoneName\" constraint.
——————————————
HOW TO FIX:
Make sure each node has a \"BoneName\" constraint.
""",

"IncorrectChainParent": """Incorrect Chain Parent
ERROR INFO:
Some chains have incorrect parent object types.
Or maybe chain has no parent header object.
——————————————
HOW TO FIX:
Make sure all chains are parented to header object.
""",

"ChainHasLessThanTwoNodes": """Chain Has Less Than Two Nodes
ERROR INFO:
Some chains have less than two nodes as child.
——————————————
HOW TO FIX:
Make sure each chain has at least two nodes as its child.
""",

"NoCTCHeader": """No CTC Header
ERROR INFO:
Target ctc collection has no ctc header object.
——————————————
HOW TO FIX:
Make sure target ctc collection has only one ctc header object.""",

"MoreThanOneCTCHeader": """More Than One CTC Header
ERROR INFO:
Target ctc collection has more than one ctc header object.
——————————————
HOW TO FIX:
Make sure target ctc collection has only one ctc header object.""",

"IncorrectBoneNameFormat": """Incorrect Bone Name Format
ERROR INFO:
Some constraint bones are not named with format \"MhBone__xxx\".
Or the name suffix index exceeds the maximum limit of 511.
——————————————
HOW TO FIX:
Change the bone name to \"MhBone__xxx\", where xxx is suffix index, such as \"MhBone__150\".
And also make sure that the suffix index is less than 512.
""",

"ChainHasBranch": """Chain Has Branch
ERROR INFO:
Some chains have branching node structure.
——————————————
HOW TO FIX:
Delete extra branch nodes.
Make sure each chain has no branch nodes.
""",

"MultipleSameBones": """Multiple Same Bones
ERROR INFO:
Multiple nodes have the same constraint bone.
——————————————
HOW TO FIX:
Delete extra conflict nodes.
Make sure each node corresponds to a specific bone.
""",
}

def printCTCErrorDict(errorDict):
    lang = bpy.context.preferences.view.language
    if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
        print(f"\n{textColors.FAIL}无法导出ctc. 发现了 {len(errorDict)} 个需要被修复的问题.{textColors.ENDC}\n")
    else:
        print(f"\n{textColors.FAIL}Unable to export ctc. {len(errorDict)} error(s) were found that need to be fixed.{textColors.ENDC}\n")
    printErrorInfo(errorDict, ctcErrorInfoDict)
    print(f"\033[92m__________________________________\n{i18n('MHW CTC export failed.')}\033[0m")

def showMHWCTCErrorWindow(errorDict, colName="", armName=""):
    bpy.types.Scene.mhw_ctc_error_list = CollectionProperty(type=MHWCTCErrorEntry)
    bpy.context.scene.mhw_ctc_error_list.clear()
    for index, errorType in enumerate(sorted(errorDict.keys())):
        item = bpy.context.scene.mhw_ctc_error_list.add()
        item.errorCount = errorDict[errorType]["count"]
        errorInfoSplit = ctcErrorInfoDict[errorType].split("\n", 1)

        item.errorType = errorInfoSplit[0]
        item.errorDescription = errorInfoSplit[1]
        objectSet = errorDict[errorType].get("objectSet", {})
        boneSet = errorDict[errorType].get("boneSet", {})
        errorInfo = ctcErrorInfoDict[errorType]
        nameListString = ""
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

    bpy.ops.mhw_ctc.show_export_error_window('INVOKE_DEFAULT', collectionName=colName, armatureName=armName)
