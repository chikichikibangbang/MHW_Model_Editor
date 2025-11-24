from .addons.MHW_Model_Editor import register as addon_register, unregister as addon_unregister
from . import addon_updater_ops

bl_info = {
    "name": 'MHW Model Editor',
    "author": '诸葛不太亮, NSACloud',
    "blender": (2, 93, 0),
    "version": (0, 10),
    "description": 'Import, edit and export MHW Model (mod3, mrl3, ctc, ccl) files.',
    "warning": '',
    "wiki_url": 'https://github.com/chikichikibangbang/MHW_Model_Editor/wiki',
    "tracker_url": 'https://github.com/chikichikibangbang/MHW_Model_Editor/issues',
    "category": 'Import-Export'
}

def register():
    addon_updater_ops.register(bl_info)
    addon_register()

def unregister():
    addon_updater_ops.unregister()
    addon_unregister()

    