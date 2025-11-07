import bpy
from .config import __addon_name__
from .i18n.dictionary import dictionary
from .modules.mod3.mod3_io import ImportMHWMod3, ExportMHWMod3
from .modules.mod3.mod3_properties import Mod3ToolPanelPG
from .modules.mrl3.mrl3_io import ExportMHWMrl3, ImportMHWMrl3
from .modules.mrl3.mrl3_properties import Mrl3MaterialPG, Mrl3ToolPanelPG
from .modules.ctc.ctc_io import ImportMHWCTC, ExportMHWCTC
from .modules.ctc.ctc_properties import CTCToolPanelPG, CTCHeaderPG, CTCChainPG, CTCNodePG, CTCClipboardPG
from .modules.ccl.ccl_properties import CCLToolPanelPG, CCLCollisionPG
from .modules.ccl.ccl_io import ImportMHWCCL, ExportMHWCCL
from ...common.class_loader import auto_load
from ...common.class_loader.auto_load import add_properties, remove_properties
from ...common.i18n.dictionary import common_dictionary
from ...common.i18n.i18n import load_dictionary
from bpy.props import PointerProperty
# Add-on info
bl_info = {
    "name": "MHW Model Editor",
    "author": "诸葛不太亮, NSACloud",
    "blender": (2, 93, 0),
    "version": (0, 7),
    "description": "Import, edit and export MHW Model (mod3, mrl3, ctc, ccl) files.",
    "warning": "",
    "wiki_url": "https://github.com/chikichikibangbang/MHW_Model_Editor/wiki",
    "tracker_url": "https://github.com/chikichikibangbang/MHW_Model_Editor/issues",
    "category": "Import-Export"
}

_addon_properties = {}


# You may declare properties like following, framework will automatically add and remove them.
# Do not define your own property group class in the __init__.py file. Define it in a separate file and import it here.
# 注意不要在__init__.py文件中自定义PropertyGroup类。请在单独的文件中定义它们并在此处导入。
# _addon_properties = {
#     bpy.types.Scene: {
#         "property_name": bpy.props.StringProperty(name="property_name"),
#     },
# }


if bpy.app.version >= (4, 1, 0):
    class MHW_MOD3_FH_drag_import(bpy.types.FileHandler):
        bl_idname = "MHW_MOD3_FH_drag_import"
        bl_label = "File handler for MHW MOD3 importing"
        bl_import_operator = "mhw_mod3.import_mhw_mod3"
        bl_file_extensions = ".mod3"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

    class MHW_MRL3_FH_drag_import(bpy.types.FileHandler):
        bl_idname = "MHW_MRL3_FH_drag_import"
        bl_label = "File handler for MHW MRL3 importing"
        bl_import_operator = "mhw_mrl3.import_mhw_mrl3"
        bl_file_extensions = ".mrl3"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

    class MHW_CTC_FH_drag_import(bpy.types.FileHandler):
        bl_idname = "MHW_CTC_FH_drag_import"
        bl_label = "File handler for MHW CTC importing"
        bl_import_operator = "mhw_ctc.import_mhw_ctc"
        bl_file_extensions = ".ctc"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')

    class MHW_CCL_FH_drag_import(bpy.types.FileHandler):
        bl_idname = "MHW_CCL_FH_drag_import"
        bl_label = "File handler for MHW CCL importing"
        bl_import_operator = "mhw_ccl.import_mhw_ccl"
        bl_file_extensions = ".ccl"

        @classmethod
        def poll_drop(cls, context):
            return (context.area and context.area.type == 'VIEW_3D')


class IMPORT_MT_mhw_model_editor(bpy.types.Menu):
    bl_label = "MHW Model Editor"
    bl_idname = "IMPORT_MT_mhw_model_editor"

    def draw(self, context):
        layout = self.layout
        layout.operator(ImportMHWMod3.bl_idname, text="MHW MOD3 (.mod3) (Model)", icon="MESH_DATA")
        layout.operator(ImportMHWMrl3.bl_idname, text="MHW MRL3 (.mrl3) (Material)", icon="MATERIAL")
        layout.operator(ImportMHWCTC.bl_idname, text="MHW CTC (.ctc) (Physic)", icon="LINK_BLEND")
        layout.operator(ImportMHWCCL.bl_idname, text="MHW CCL (.ccl) (Collision)", icon="SPHERE")

def mhw_model_editor_import(self, context):
    self.layout.menu("IMPORT_MT_mhw_model_editor", icon="MOD_LINEART")


class EXPORT_MT_mhw_model_editor(bpy.types.Menu):
    bl_label = "MHW Model Editor"
    bl_idname = "EXPORT_MT_mhw_model_editor"

    def draw(self, context):
        layout = self.layout
        layout.operator(ExportMHWMod3.bl_idname, text="MHW MOD3 (.mod3) (Model)", icon="MESH_DATA")
        layout.operator(ExportMHWMrl3.bl_idname, text="MHW MRL3 (.mrl3) (Material)", icon="MATERIAL")
        layout.operator(ExportMHWCTC.bl_idname, text="MHW CTC (.ctc) (Physic)", icon="LINK_BLEND")
        layout.operator(ExportMHWCCL.bl_idname, text="MHW CCL (.ccl) (Collision)", icon="SPHERE")

def mhw_model_editor_export(self, context):
    self.layout.menu("EXPORT_MT_mhw_model_editor", icon="MOD_LINEART")


def register():
    # Register classes
    auto_load.init()
    auto_load.register()
    add_properties(_addon_properties)

    # Internationalization
    load_dictionary(dictionary)
    bpy.app.translations.register(__addon_name__, common_dictionary)

    bpy.utils.register_class(IMPORT_MT_mhw_model_editor)
    bpy.utils.register_class(EXPORT_MT_mhw_model_editor)

    # REGISTER PROPERTY GROUP PROPERTIES
    bpy.types.Scene.mhw_mod3_toolpanel = PointerProperty(type=Mod3ToolPanelPG)

    bpy.types.Scene.mhw_mrl3_toolpanel = PointerProperty(type=Mrl3ToolPanelPG)
    bpy.types.Object.mhw_mrl3_material = PointerProperty(type=Mrl3MaterialPG)

    bpy.types.Scene.mhw_ctc_toolpanel = PointerProperty(type=CTCToolPanelPG)
    bpy.types.Object.mhw_ctc_header = PointerProperty(type=CTCHeaderPG)
    bpy.types.Object.mhw_ctc_chain = PointerProperty(type=CTCChainPG)
    bpy.types.Object.mhw_ctc_node = PointerProperty(type=CTCNodePG)

    bpy.types.Scene.mhw_ccl_toolpanel = PointerProperty(type=CCLToolPanelPG)
    bpy.types.Object.mhw_ccl_collision = PointerProperty(type=CCLCollisionPG)

    bpy.types.Scene.mhw_ctc_clipboard = PointerProperty(type=CTCClipboardPG)

    # bpy.types.TOPBAR_MT_file_import.append(mhw_mod3_import)
    # bpy.types.TOPBAR_MT_file_export.append(mhw_mod3_export)

    bpy.types.TOPBAR_MT_file_import.append(mhw_model_editor_import)
    bpy.types.TOPBAR_MT_file_export.append(mhw_model_editor_export)

    # Blender 4.1 and higher drag and drop operators
    if bpy.app.version >= (4, 1, 0):
        bpy.utils.register_class(MHW_MOD3_FH_drag_import)
        bpy.utils.register_class(MHW_MRL3_FH_drag_import)
        bpy.utils.register_class(MHW_CTC_FH_drag_import)
        bpy.utils.register_class(MHW_CCL_FH_drag_import)

    print("{} addon is installed.".format(__addon_name__))


def unregister():
    # bpy.types.TOPBAR_MT_file_import.remove(mhw_mod3_import)
    # bpy.types.TOPBAR_MT_file_export.remove(mhw_mod3_export)

    bpy.utils.unregister_class(IMPORT_MT_mhw_model_editor)
    bpy.utils.unregister_class(EXPORT_MT_mhw_model_editor)

    bpy.types.TOPBAR_MT_file_import.remove(mhw_model_editor_import)
    bpy.types.TOPBAR_MT_file_export.remove(mhw_model_editor_export)

    if bpy.app.version >= (4, 1, 0):
        bpy.utils.unregister_class(MHW_MOD3_FH_drag_import)
        bpy.utils.unregister_class(MHW_MRL3_FH_drag_import)
        bpy.utils.unregister_class(MHW_CTC_FH_drag_import)
        bpy.utils.unregister_class(MHW_CCL_FH_drag_import)

    # Internationalization
    bpy.app.translations.unregister(__addon_name__)
    # unRegister classes
    auto_load.unregister()
    remove_properties(_addon_properties)
    print("{} addon is uninstalled.".format(__addon_name__))
