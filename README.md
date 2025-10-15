![MHWModelEditorTitle](https://github.com/user-attachments/assets/825df30a-81e9-4943-83f1-e4e2c7185bfd)

**[Download MHW Model Editor](https://github.com/chikichikibangbang/MHW_Model_Editor/archive/refs/heads/main.zip)**

**V0.2 (10/15/2025) (BETA RELEASE, THERE MAY BE BUGS) | [Change Log](https://github.com/chikichikibangbang/MHW_Model_Editor?tab=readme-ov-file#change-log)**

**This addon allows for importing, editing and exporting MHW Model (mod3, mrl3, ctc, ccl) files in Blender**.

<img width="2560" height="1400" alt="MHWModelEditorPreview" src="https://github.com/user-attachments/assets/8e667cbb-7abc-449a-8467-620ece43c71e" />

## Features.
Working on writing a wiki.

The functions are basically the same as NSACloud's RE Mesh Editor and RE Chain Editor.

Here are some features:
* The addon sub-panels "MHW Mesh" and "MHW Chain" can be found in the sidebar.
* You can import and export files directly through the sidebar now.
* The imported files will be placed into the corresponding collections.
* You can import and export meshes of all lod levels. The meshes of each lod level will be grouped and placed into the corresponding collection.
* The imported mod3 meshes eliminates the problem of "negative weight", and certain "confusing" weights (such as Dante Waist) will be correctly parsed.
It means you can directly export model according to the total limit of 8wt, and also means that you can bind the entire facial model through weight transfer.
* The plugin automatically handles some unknown attributes (such as blocklabel, shadowflag, weightdynamics), so basically you don't have to care about them.
* There are very complete and detailed error messages when exporting files to help you solve various problems.
* You can modify the parameters of mrl3 files to change the material effect in real time. Note that only some parameters are supported, there are still many parameters that need to be parsed.
* You can edit chains and collisions in real time, and there are many useful functions in the "MHW Chain" panel.
* Importing and exporting files is fast (depending on your io options).
* When importing mod3 files, the plugin will automatically check for illegal meshes and ensure that only fully legal meshes are imported. This means that you can import certain "encrypted" mod3 files.
* When importing mrl3 files, the plugin will automatically check for illegal materials and ensure that only fully legal materials are imported. This means that you can import certain "encrypted" mrl3 files.
* Chinese translation will be added in the future.
* When exporting the model, the plugin will automatically calculate the bounding spheres, AABBs and OBBs.
* The names of chain preset and material preset support Chinese.
* The material names of the meshes and the mrr3 material both support Chinese.

NOTE: Some functions have not yet been opened, and there are problems with the display of some material nodes. These will be gradually improved in subsequent updates.

## Installation
First, please make sure you have installed **[Blender 2.93 or higher version](https://www.blender.org/download/)**.

Then download the addon from the "Download MHW Model Editor" link at the top or click Code > Download Zip.

In Blender, go to Edit > Preferences > Addons, then click "Install" in the top right.

NOTE: If you are on Blender 4.2 or above, the install button is found by clicking the arrow in the top right of the addon menu.

![image](https://github.com/user-attachments/assets/49dd95c1-9a20-49d8-af55-7160d54836df)

Navigate to the downloaded zip file for this addon and click "Install Addon". The addon should then be usable.

To update this addon, navigate to Preferences > Add-ons > MHW Model Editor and press the "Check for update" button.

## Change Log
### V0.2 - 10/15/2025
* Beta initial release.

## Usage Guide
Working on writing a wiki.

The usage method is basically the same as NSACloud's RE Mesh Editor and RE Chain Editor. If you have made mods for other RE Engine games, you can get started quickly.

NOTE: If you are currently using [MHW CTC&CCL Editor](https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor), you can copy old chain preset files by pressing "Open Preset Folder" button in addon panel, and paste them into new path. Then you can uninstall it!

For additional help, you can join [Monster Hunter Modding Discord](https://discord.gg/gJwMdhK), then ask anyone or @chikichikibangbang to find me.

 
## Credits
- [NSACloud](https://github.com/NSACloud) - Excellent RE Mesh Editor and RE Chain Editor!
- [xzhuah](https://github.com/xzhuah) - Excellent Blender Addon Package Tool!
- [AsteriskAmpersand](https://github.com/AsteriskAmpersand) - Hash dictionary from his mrl3 editor, and mod3 mesh format research.
- [CG Cookie](https://github.com/CGCookie) - Addon updater module.
- [matyalatte](https://github.com/matyalatte/Texconv-Custom-DLL) - DirectX Texconv DLL library.

 ## 一些中文内容
 * B站：[不太亮的诸葛亮](https://space.bilibili.com/84161516?spm_id_from=333.1007.0.0)
 * 怪猎mod作者交流群：[640945651](https://qm.qq.com/q/iABxIIl3gs)
 * 踩蘑菇：[诸葛不太亮](https://www.caimogu.cc/user/183747.html)
 * 爱发电：[诸葛不太亮](http://www.ifdian.net/a/korone_suki)
