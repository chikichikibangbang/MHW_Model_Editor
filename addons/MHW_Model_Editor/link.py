import webbrowser
from bpy.types import Operator

class WM_OT_MHW_BilibiliWebsite(Operator):
    bl_idname = "mhw_model.open_bilibili_website"
    bl_label = "Bilibili"

    def execute(self, context):
        webbrowser.open("https://space.bilibili.com/84161516?spm_id_from=333.1007.0.0")
        return {'FINISHED'}


class WM_OT_MHW_QQWebsite(Operator):
    bl_idname = "mhw_model.open_qq_website"
    bl_label = "QQGroup"

    def execute(self, context):
        webbrowser.open("https://qm.qq.com/q/iABxIIl3gs")
        return {'FINISHED'}


class WM_OT_MHW_CaimoguWebsite(Operator):
    bl_idname = "mhw_model.open_caimogu_website"
    bl_label = "Caimogu"

    def execute(self, context):
        webbrowser.open("https://www.caimogu.cc/user/183747.html")
        return {'FINISHED'}

class WM_OT_MHW_GithubWebsite(Operator):
    bl_idname = "mhw_model.open_github_website"
    bl_label = "Github"

    def execute(self, context):
        webbrowser.open("https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor")
        return {'FINISHED'}