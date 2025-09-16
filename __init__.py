from .addons.MHW_Model_Editor import register as addon_register, unregister as addon_unregister

bl_info = {
    "name": 'MHW Model Editor',
    "author": '诸葛不太亮, NSACloud',
    "blender": (2, 93, 0),
    "version": (0, 1),
    "description": 'Import, edit and export MHW Model (mod3, mrl3, ctc, ccl) files.',
    "warning": '',
    "wiki_url": '',
    "tracker_url": '',
    "category": 'Import-Export'
}

def register():
    addon_register()

def unregister():
    addon_unregister()

    