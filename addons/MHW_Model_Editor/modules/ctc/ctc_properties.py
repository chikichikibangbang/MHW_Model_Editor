import bpy
from bpy.props import StringProperty, BoolProperty, IntProperty, FloatProperty, \
                    FloatVectorProperty, EnumProperty, PointerProperty
import math

def filterCTCCollection(self, collection):
    return True if collection.get("~TYPE") == "MHW_CTC_COLLECTION" else False
def filterArmature(self, object):
    return True if object.type == "ARMATURE" else False
class CTCToolPanelPG(bpy.types.PropertyGroup):
    importCTCCollection: PointerProperty(
        name="",
        description="Set the ctc collection to merge ctc objects with",
        type=bpy.types.Collection,
        poll=filterCTCCollection,
        # update=updateCTCCollection,
    )
    exportCTCCollection: PointerProperty(
        name="",
        description="Set the ctc collection to be exported",
        type=bpy.types.Collection,
        poll=filterCTCCollection,
        # update=updateCTCCollection,
    )
    importCTCArmature: PointerProperty(
        name="",
        description="Set the armature to attach ctc objects to.\n"
                    "NOTE: If some bones that are used by ctc file are missing on the armature, corresponding ctc nodes using those bones won't be imported",
        type=bpy.types.Object,
        poll=filterArmature,
        # update=updateCTCCollection,
    )
