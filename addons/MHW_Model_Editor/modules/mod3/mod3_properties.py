import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, \
                    FloatVectorProperty, EnumProperty, PointerProperty
from ..common.blender_functions import findTempSpace

def filterMod3Collection(self, collection):
    return True if collection.get("~TYPE") == "MHW_MOD3_COLLECTION" else False
def updateExportMod3Collection(self, context):
    browserSpace = findTempSpace("FileSelectParams")
    if browserSpace and self.exportMod3Collection:
        colName = self.exportMod3Collection.name
        if ".mod3" in colName:
            browserSpace.params.filename = colName.split(".mod3")[0] + ".mod3"

class Mod3ToolPanelPG(bpy.types.PropertyGroup):
    importSettingsLoaded: BoolProperty(default=False)
    exportSettingsLoaded: BoolProperty(default=False)

    lastImportCollection: StringProperty(default="")
    lastExportCollection: StringProperty(default="")

    exportMod3Collection: PointerProperty(
        name="",
        description="Set the mod3 collection to be exported",
        type=bpy.types.Collection,
        poll=filterMod3Collection,
        update=updateExportMod3Collection,
    )
