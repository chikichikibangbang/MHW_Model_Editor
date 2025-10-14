import bpy
import textwrap
from ..common.message_functions import textColors, printErrorInfo
from bpy.props import StringProperty, IntProperty, CollectionProperty
from bpy.types import Operator
ERROR_WINDOW_SIZE = 750
SPLIT_FACTOR = .35


class MHWCCLErrorEntry(bpy.types.PropertyGroup):
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


class MESH_UL_CCL_MHWCCLErrorList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(text=f"{item.errorType} ({str(item.errorCount)})")

    # Disable double-click to rename
    def invoke(self, context, event):
        return {'PASS_THROUGH'}


class WM_OT_CCL_ShowMHWCCLErrorWindow(Operator):
    """显示导出时的错误信息"""
    bl_idname = 'mhw_ccl.show_export_error_window'
    bl_label = 'MHW CCL Export Error'
    bl_options = {'REGISTER'}
    collectionName: StringProperty()
    armatureName: StringProperty()
    errorList_items: CollectionProperty(type=MHWCCLErrorEntry)
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
        for entry in bpy.context.scene.mhw_ccl_error_list:
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
            text=f"The ccl objects have {len(self.errorList_items)} {'issues' if len(self.errorList_items) > 1 else 'issue'} that must be fixed before it can be exported.",
            icon="ERROR")
        # row = layout.row()
        layout.label(text=f"Target Collection: {self.collectionName}")
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
            listtype_name="MESH_UL_CCL_MHWCCLErrorList",
            list_id="",
            dataptr=self,
            propname="errorList_items",
            active_dataptr=self,
            active_propname="errorList_index",
            rows=rowCount,
            type='DEFAULT'
        )
        

cclErrorInfoDict = {
"NoTargetCTCCollection": """No Target CTC Collection
ERROR INFO:
Target ctc collection was not selected when exporting.
——————————————
HOW TO FIX:
Select a target ctc collection in the export options.""",

"CapsuleHasMultipleHeads": """Capsule Has Multiple Heads
ERROR INFO:
Some capsule collisions have more than one head.
——————————————
HOW TO FIX:
Delete extra head.
Make sure each capsule collision only has one head.
""",

"CapsuleHasMultipleTails": """Capsule Has Multiple Tails
ERROR INFO:
Some capsule collisions have more than one tail.
——————————————
HOW TO FIX:
Delete extra tail.
Make sure each capsule collision only has one tail.
""",

"CapsuleHasNoHead": """Capsule Has No Head
ERROR INFO:
Some capsule collisions have no head.
——————————————
HOW TO FIX:
Make sure each capsule collision only has one head.
""",

"CapsuleHasNoTail": """Capsule Has No Tail
ERROR INFO:
Some capsule collisions have no tail.
——————————————
HOW TO FIX:
Delete extra tail.
Make sure each capsule collision only has one tail.
""",

"InvalidNodeConstraint": """Invalid Node Constraint
ERROR INFO:
The \"BoneName\" constraint of sphere or capsule head & tail has no target or subtarget.
——————————————
HOW TO FIX:
Make sure \"BoneName\" constraint of sphere or capsule head & tail has target armature and subtarget bone.
""",

"NodeHasNoConstraint": """Node Has No Constraint
ERROR INFO:
Some spheres or capsule heads & tails have no \"BoneName\" constraint.
——————————————
HOW TO FIX:
Make sure each sphere or capsule head & tail has a \"BoneName\" constraint.
""",

"IncorrectBoneNameFormat": """Incorrect Bone Name Format
ERROR INFO:
Some constraint bones are not named with format \"MhBone__xxx\", or the name suffix index exceeds the maximum limit of 511.
——————————————
HOW TO FIX:
Change the bone name to \"MhBone__xxx\", where xxx is suffix index, such as \"MhBone__150\".
And also make sure that the suffix index is less than 512.
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

def printCCLErrorDict(errorDict, isNested=False):
    front = "" if isNested else "\n"
    print(f"{front}{textColors.FAIL}Unable to export ccl. {len(errorDict)} error(s) were found that need to be fixed.{textColors.ENDC}\n")
    printErrorInfo(errorDict, cclErrorInfoDict)
    if not isNested:
        print("\033[92m__________________________________\nMHW CCL export failed.\033[0m")

def showMHWCCLErrorWindow(errorDict, colName="", armName=""):
    bpy.types.Scene.mhw_ccl_error_list = CollectionProperty(type=MHWCCLErrorEntry)
    bpy.context.scene.mhw_ccl_error_list.clear()
    for index, errorType in enumerate(sorted(errorDict.keys())):
        item = bpy.context.scene.mhw_ccl_error_list.add()
        item.errorCount = errorDict[errorType]["count"]
        errorInfoSplit = cclErrorInfoDict[errorType].split("\n", 1)

        item.errorType = errorInfoSplit[0]
        item.errorDescription = errorInfoSplit[1]
        objectSet = errorDict[errorType].get("objectSet", {})
        boneSet = errorDict[errorType].get("boneSet", {})
        errorInfo = cclErrorInfoDict[errorType]
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

    bpy.ops.mhw_ccl.show_export_error_window('INVOKE_DEFAULT', collectionName=colName, armatureName=armName)
