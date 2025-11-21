![MHWModelEditorTitle](https://github.com/user-attachments/assets/825df30a-81e9-4943-83f1-e4e2c7185bfd)

**[Download MHW Model Editor](https://github.com/chikichikibangbang/MHW_Model_Editor/archive/refs/heads/main.zip)**

**V0.9 (11/22/2025) (BETA RELEASE, THERE MAY BE BUGS) | [Change Log](https://github.com/chikichikibangbang/MHW_Model_Editor?tab=readme-ov-file#change-log)**

**This addon allows for importing, editing and exporting MHW Model (mod3, mrl3, ctc, ccl) files in Blender**.

<img width="2560" height="1400" alt="MHWModelEditorPreview" src="https://github.com/user-attachments/assets/8e667cbb-7abc-449a-8467-620ece43c71e" />

## Features (特色功能)
><details>
>  <summary>中文翻译</summary>
>
>正在着手编写wiki。  
插件的功能与NSACloud的RE Mesh Editor以及RE Chain Editor插件基本相同。
> 
>以下是一些特色功能：
>* 你可以在侧边栏中找到“MHW Mesh”和“MHW Chain”两个插件面板。
>* 你可以直接通过侧边栏的插件面板导入和导出文件。
>* 在 **Blender4.1+** 版本，你可以将文件拖放到3D视图中以导入它们。
>* 导入导出文件的速度非常快（取决于你的io选项）。
>* 导入的文件会被放入对应的集合中。
>* 你可以导入和导出所有lod级别的网格，每个lod级别的网格将被分组并放入对应的集合中。
>* 导入的mod3网格摆脱了所谓“负权重”问题，旧插件导入的某些混乱权重（比如但丁腰，霜牙腰，霜牙头发，黑龙，以及头模）将被正确解析。  
这意味着你可以按照8wt的权重总限值直接导出模型，也可以通过权重传递绑定整个面部模型。
>* 插件会自动处理一些未知属性（比如blocklabel、shadowflag、weightdynamics等），基本上不必在意它们。
>* 导出模型时，插件会自动计算网格的边界球、AABB边界盒和OBB边界盒。
>* 导出文件时有非常完整且详细的报错信息，可以帮助你解决各种问题。
>* 可以在Blender中修改mrl3文件的参数来实时改变材质效果。  
注意，只支持部分参数，还有很多参数需要解析。
>* 可以在Blender中实时编辑物理链和碰撞体，“MHW Chain”面板中有很多有用的功能。
>* 导入mod3文件时，插件会自动检查非法的网格，并确保只导入完全合法的网格。  
这意味着你可以导入某些“加密”的mod3文件。
>* 导入mrl3文件时，插件会自动检查非法的材质，并确保只导入完全合法的材质。  
这意味着你可以导入某些“加密”的mrl3文件。
>* 后续更新会增加中文翻译。
>* 链预设和材质预设的名称支持中文。
>* 网格的材质名以及mrl3材质的材质名也都支持中文。  
也就是说材质名不必再局限于类似“Ch_Pl_Standard_Mt__0”的命名格式。  
你可以按照任意格式命名，比如“body”或“皮肤”，只要确保mod3和mrl3中的材质名互相对应即可。
>
>注意：部分功能尚未开放，部分材质节点显示仍存在问题。这些都会在后续的更新中逐步完善。
> 
></details>

Working on writing a wiki.  
The functions are basically the same as NSACloud's RE Mesh Editor and RE Chain Editor.

Here are some features:
* The addon panels "MHW Mesh" and "MHW Chain" can be found in the sidebar.
* You can import and export files directly through the sidebar now.
* You can drag and drop files into the 3D View to import them on Blender 4.1+.
* Importing and exporting files is fast (depending on your io options).
* The imported files will be placed into the corresponding collections.
* You can import and export meshes of all lod levels.  
The meshes of each lod level will be grouped and placed into the corresponding collection.
* The imported mod3 meshes eliminates the problem of "negative weight", and certain "confusing" weights (such as Dante Waist) will be correctly parsed.  
It means you can directly export model according to the total limit of 8wt, and you can also bind the entire facial model through weight transfer.
* The plugin automatically handles some unknown attributes (such as blocklabel, shadowflag, weightdynamics), so basically you don't have to care about them.
* When exporting the model, the plugin will automatically calculate the bounding spheres, AABBs and OBBs.
* There are very complete and detailed error messages when exporting files to help you solve various problems.
* You can modify the parameters of mrl3 files to change the material effect in real time.  
Note that only some parameters are supported, there are still many parameters that need to be parsed.
* You can edit chains and collisions in real time, and there are many useful functions in the "MHW Chain" panel.
* When importing mod3 files, the plugin will automatically check for illegal meshes and ensure that only fully legal meshes are imported.  
This means that you can import certain "encrypted" mod3 files.
* When importing mrl3 files, the plugin will automatically check for illegal materials and ensure that only fully legal materials are imported.  
This means that you can import certain "encrypted" mrl3 files.
* Chinese translation will be added in the future.
* The names of chain preset and material preset support Chinese.
* The material names of the meshes and the mrl3 material both support Chinese.

NOTE: Some functions have not yet been opened, and there are problems with the display of some material nodes. These will be gradually improved in subsequent updates.

## Installation (安装)
><details>
>  <summary>中文翻译</summary>
>
>首先，请确保已安装 **[Blender 2.93或更高版本](https://www.blender.org/download/)**。  
然后从顶部的“Download MHW Model Editor”链接下载插件，或者点击右上角的Code > Download Zip。  
在Blender中，转到编辑 > 偏好设置 > 插件，然后点击右上角的“安装”按钮。  
注意，如果你使用的是Blender 4.2或更高版本，则可以点击插件菜单右上角的箭头来找到安装按钮。  
找到你下载的插件压缩包，然后点击“安装插件”。之后就可以使用插件了。      
要更新此插件，请转到偏好设置 > 插件 > MHW Model Editor，并点击“检查更新”按钮。 
>
></details>

First, please make sure you have installed **[Blender 2.93 or higher version](https://www.blender.org/download/)**.   
Then download the addon from the "Download MHW Model Editor" link at the top or click Code > Download Zip.  
In Blender, go to Edit > Preferences > Addons, then click "Install" in the top right.  
NOTE: If you are on Blender 4.2 or above, the "Install" button is found by clicking the arrow in the top right of the addon menu.

![image](https://github.com/user-attachments/assets/49dd95c1-9a20-49d8-af55-7160d54836df)

Navigate to the downloaded zip file for this addon and click "Install Addon". The addon should then be usable.  
To update this addon, navigate to Preferences > Add-ons > MHW Model Editor and press the "Check for update" button.

## Change Log
### V0.9 - 11/22/2025
><details>
>  <summary>中文翻译</summary>
>
>* 修复若mod3文件中某个父级骨骼索引不在重映射表中，导入该文件会报错的问题。 
>* 添加“Mod目录”属性，用于设定mod的nativePC目录。导出文件时会自动设定该目录。  
该目录应该如“D:\SteamLibrary\steamapps\common\Monster Hunter World\nativePC”。
>* 添加“MHW贴图工具”子面板，该子面板中的按钮可以快速且批量地转换.tex或.dds贴图文件。  
>* “MHW贴图转换”按钮会打开文件视图，以选择需要转换的贴图文件。   
点击右侧的设置按钮可以选择不同的选项。  
“添加转换文件夹”选项将在选定的目录下创建一个新的文件夹，用于存放转换后的文件。  
”添加DXGI格式前缀“选项将在转换后的.dds文件名前面加上格式字符，比如.tex文件名为“body_BML.tex”，则转换后的.dds文件名将为“BC7S_body_BML.dds”。  
如果你不确定该以何种格式保存.dds文件，可以参考此前缀。
>* “转换目录为Tex”按钮可以让你将选中目录中的所有.dds文件转换为.tex文件。
>* “复制转换的Tex”按钮可以让你将上一步转换得到的.tex文件复制到指定的mod目录中。  
复制的文件将被放置在当前激活的mrl3集合中所设置的路径下。
>* 在 **Blender4.1+** 版本，你可以将.tex或.dds贴图文件拖放到3D视图中以转换它们。
>
></details>

* Fixed an issue where if a parent bone index is not in the remap table, importing this mod3 file would cause an error.
* Added "Mod Directory" property to set the "nativePC" directory for your mod. It will be set automatically when a file is exported.    
This directory should be like "D:\SteamLibrary\steamapps\common\Monster Hunter World\nativePC".
* Added "MHW Tex Tools" sub-panel, where buttons allow you to quickly convert .tex or .dds files.  
* The "MHW Tex Conversion" button will open a window to select textures to convert.  
Click the settings button on the right to choose different options.  
The "Add Conversion Folder" option will create a new folder in the selected directory to store the converted files.  
The "Add DXGI Format Prefix" option will add dxgi format prefix to file name. 
For example, if the name of .tex is "body_BML.tex", the name of the converted .dds will be "BC7S_body_BML.dds".  
If you are not sure which format to save .dds files in, you can refer to this prefix.  
* The "Convert Directory to Tex" button allows you to convert all .dds files in the chosen directory to .tex.
* The "Copy Converted Tex Files" button allows tou to copy .tex files in conversion folder into the specified mod directory.  
Copied files will be placed at the paths set in the active mrl3 collection.
* You can drag and drop .tex or .dds files into the 3D View to convert them on **Blender 4.1+**.

### V0.8 - 11/20/2025
><details>
>  <summary>中文翻译</summary>
>
>* 添加对 **Blender5.0** 版本的支持。
>* 在“MHW网格工具”子面板中添加“创建Mod3集合”按钮。  
注意，如果你正在制作防具模型，可以使用此按钮创建新集合。**否则，强烈建议从外部导入mod3文件来继承集合的自定义属性。**
>* 在“MHW网格工具”子面板中添加“创建嵌套集合组”按钮，该按钮可以创建包含mod3，mrl3和ctc集合的嵌套集合组。  
嵌套集合组可以让集合的层级结构更为清晰。
>* 在“MHW网格工具”子面板中添加“设置网格组ID”按钮，该按钮可以让你快速修改所有选中网格的网格组ID。  
比如，你选择了某些名称中含有“Group_0”的网格，并输入序号2，则这些网格名称中的“Group_0”都会被修改为“Group_2”。  
注意，如果从某个网格的名称中无法解析到网格组ID（也就是Group_x），则会跳过此网格。
>* 在“MHW网格工具”子面板中添加“烘焙法向到顶点色”按钮，该按钮可以将世界空间的法向烘焙为顶点色。  
烘焙出来的顶点色会被保存在名为“World Space Normal”的顶点色通道中。
>* 在“CTC节点属性”面板的每个属性右侧添加一个小的复制按钮，该按钮可以让你单独复制一个属性到剪贴板，粘贴时也只会粘贴该属性。  
当你想同时修改多个CTC节点的某个属性而不影响其他属性时，使用该按钮进行复制和粘贴尤为方便。
>* 在“Mrl3材质属性”面板的贴图列表中添加“替换字符串”按钮，该按钮可以让你快速替换贴图路径中的指定字符串。
>* 修复点击“创建碰撞”按钮时，有时会向错误的ccl集合添加新碰撞体的问题。
>
></details>

* Added support for **Blender 5.0**.
* Added "Create Mod3 Collection" button in "MHW Mesh Tools" sub-panel.  
Note that if you are making armor models, you can use this button to create a new collection.   
**Otherwise, it is highly recommended to import a mod3 file to inherit the custom properties of the collection.**
* Added "Create Nested Collections" button in "MHW Mesh Tools" sub-panel, which allows you to create nested collections containing mod3, mrl3 and ctc collections.  
Nested Collections will make the collection structure look clearer.
* Added "Set Mesh Group ID" button in "MHW Mesh Tools" sub-panel, which allows you to quickly change the group ID of all selected meshes.  
For example, if you select some meshes with "Group_0" and enter ID 2, All "Group_0" in their names will be changed to "Group_2".  
Note that if some meshes cannot be parsed group ID (Group_x), they will be skipped.
* Added "Bake Normal To Vertex Color" button in "MHW Mesh Tools" sub-panel, which allows you to bake world space normal to vertex color.  
Baked vertex color will be saved in the channel called "World Space Normal".
* Added a small button to the right of each property in the "CTC Node Properties" panel, which allows you to copy a specific property to clipboard.  
When you want to change only one specific property of multiple nodes at the same time, it is especially convenient to use this button.
* Added "Replace String" button in "Mrl3 Material Properties" panel, which allows you to quickly replace specified string in the texture path.
* Fixed an issue where new collision objects were sometimes added to the wrong ccl collection when clicking the "Create Collision" button.

### V0.7 - 11/8/2025
><details>
>  <summary>中文翻译</summary>
>
>* 在“MHW网格工具”子面板中添加“删除松散元素”按钮。
>* 增加用于判定骨骼对称性的距离容错量（从1e-6改为5e-4）。  
这可以避免某些x轴坐标非常接近0的骨骼被误判为没有对称骨骼。
>* 针对非Windows平台，由于Texconv不支持转换为TIF格式，所以改为TGA格式。
>* 在插件偏好设置面板中添加“使用DDS贴图”选项。  
如果启用此选项，插件将缓存贴图为DDS格式，而不再转换为其他格式。  
这将大大提高材质的导入速度，但仅适用于 **Blender 4.2+** 版本。（大约快6倍）
>* 调整部分材质节点：   
适当增加发光强度。   
修复“Standard_Mt”主材质发光太亮的问题。  
在 **Blender 3.3+** 版本上，“分离RGB”与“合并RGB”节点将会被替换为新的“分离颜色”与“合并颜色”节点。   
>* 现在导入材质时，插件会调整Blender的色彩管理以改善渲染效果。   
以“标准”视图变换以及中高对比度进行渲染，可以更好地呈现色彩。
>
></details>

* Added "Delete Loose Geometry" button in "MHW Mesh Tools" sub-panel.
* Increased distance tolerance for determining bone symmetry (1e-6 --> 5e-4).  
This prevents some bones with x-axis coordinates very close to 0 from being mistakenly determined to have no symmetrical bone.
* For non-Windows platforms, since Texconv does not support conversion to TIF, it will be changed to TGA format.
* Added "Use DDS Textures" option in preference setting panel.  
If this option is enabled, the plugin will cache textures as DDS files instead of converting to other formats.  
This greatly improves material import speed but is only usable on **Blender 4.2+**. (Approximately 6x faster)
* Adjusted some material nodes:  
Appropriately increased the emission strength.  
Fixed an issue where the emission values of "Standard_Mt" material were much too bright.  
The "Separate RGB" and "Combine RGB" nodes will be replaced with new "Separate Color" and "Combine Color" nodes on **Blender 3.3+**.  
* Now when importing materials, the plugin will adjust Blender's Color Management to improve rendering effects.  
With the "Standard" view transform and medium high contrast, color can be better presented.
![image](https://github.com/user-attachments/assets/b7a863b5-99e0-43fe-938e-166666a98c49)

### V0.6 - 11/4/2025
><details>
>  <summary>中文翻译</summary>
>
>* 修复若mod3文件中含有重复的骨骼，导入该文件会报错的问题。  
>* 修复若某些网格没有三角化，则在导出模型时其法向可能变得不正确的问题。  
>* 修复在Linux平台上无法安装插件的问题。
>
></details>

* Fixed an issue where if there are duplicate bones in the mod3 file, importing it would cause an error.
* Fixed an issue where if some meshes are not triangulated, their normals could become incorrect when exporting models.
* Fixed an issue where addon could not be successfully installed on the linux platform.

### V0.5 - 10/22/2025
><details>
>  <summary>中文翻译</summary>
>
>* 修复点击“打开预设文件夹”或“打开缓存文件夹”按钮时，会报错找不到文件的问题。  
>* 修复当点击“重命名链骨”按钮并同时勾选了“校准骨骼方向”选项时，骨骼扭转不会归零的问题。  
>* 在mod3导出窗口中添加“隐藏衣装Mod修复”选项。  
**[隐藏衣装Mod](https://www.nexusmods.com/monsterhunterworld/mods/4191)** 有一个bug，即当穿上转身衣装后，人物身体部位模型的第一个材质的发光效果将被强制关闭。  
如果启用此选项，插件将添加一个无用材质作为第一个材质，来避免此问题。因此，强烈建议启用此选项。
>
></details>
* Fixed an issue where an error would occur that the file could not be found when clicking the "Open Preset Folder" or "Open Cache Folder" button.
* Fixed an issue where if "Align Bone Direction" is checked, the bone roll would not be reset when clicking "Rename Chain Bones" button.
* Added "Invisible Mantles Mod Fix" option in the mod3 export window.  
The **[Invisible Mantles Mod](https://www.nexusmods.com/monsterhunterworld/mods/4191)** has a bug where the glowing effects of the first material on the body part would be turned off when wearing the temporal mantle.  
If this option is enabled, the plugin will add an unused material as the first material to avoid this issue. So leaving this option enabled is highly recommended.

### V0.4 - 10/17/2025
><details>
>  <summary>中文翻译</summary>
>
>* 添加拖放导入选项。  
在 **Blender4.1+** 版本，你可以将文件拖放到3D视图中以导入它们。
>
></details>

* Added drag and drop import options.  
Now you can drag and drop files into the 3D View to import them on **Blender 4.1+**.


https://github.com/user-attachments/assets/3420eb16-37f2-49d2-9e6d-bfc5e66f6bc3

### V0.3 - 10/17/2025
><details>
>  <summary>中文翻译</summary>
>
>* 修复导出模型时，超过4wt限制的权重会变得混乱的问题。
>
></details>

* Fixed an issue where weights exceeding 4wt would become confusing when exporting models.

### V0.2 - 10/15/2025
* Beta initial release.

## Usage Guide (使用指南)
><details>
>  <summary>中文翻译</summary>
>
>正在着手编写wiki。  
插件的使用方法与NSACloud的RE Mesh Editor以及RE Chain Editor插件基本相同。如果你曾经制作过其他RE引擎游戏的mod，可以快速上手。  
注意，如果你当前正在使用 **[MHW CTC&CCL Editor](https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor)** 插件，你可以点击“打开预设文件夹”按钮来复制旧的链预设文件，然后将它们粘贴到该插件的预设文件夹中。之后就可以卸载旧的链插件了。  
如果需要额外的帮助，你可以加入 **[Monster Hunter Modding Discord](https://discord.gg/gJwMdhK)** ，然后向任何人提问，或者@chikichikibangbang来找到我。
>
></details>

Working on writing a wiki.  
The usage method is basically the same as NSACloud's RE Mesh Editor and RE Chain Editor. If you have made mods for other RE Engine games, you can get started quickly.  
NOTE: If you are currently using **[MHW CTC&CCL Editor](https://github.com/chikichikibangbang/MHW_CTC_CCL_Editor)**, you can copy old chain preset files by pressing "Open Preset Folder" button in addon panel, and paste them into new path. Then you can uninstall it!  
For additional help, you can join **[Monster Hunter Modding Discord](https://discord.gg/gJwMdhK)**, then ask anyone or @chikichikibangbang to find me.

 
## Credits (鸣谢)
><details>
>  <summary>中文翻译</summary>
>
>- [NSACloud](https://github.com/NSACloud) - 出色的RE Mesh Editor以及RE Chain Editor插件！
>- [xzhuah](https://github.com/xzhuah) - 出色的Blender插件打包工具！
>- [AsteriskAmpersand](https://github.com/AsteriskAmpersand) - 来自他mrl3编辑器中的哈希字典，以及他对于mod3网格数据格式的研究。
>- [CG Cookie](https://github.com/CGCookie) - 插件更新模块。
>- [matyalatte](https://github.com/matyalatte/Texconv-Custom-DLL) - DirectX Texconv动态链接库。
>- [PhilippSeifried](https://github.com/Philipp-Seifried/Blender-Normals-To-Vertex-Color) - 将法向烘焙到顶点色的解决方案。
>- Torvosaure - 帮我在Linux平台上进行测试。
>
></details>

- [NSACloud](https://github.com/NSACloud) - Excellent RE Mesh Editor and RE Chain Editor!
- [xzhuah](https://github.com/xzhuah) - Excellent Blender Addon Package Tool!
- [AsteriskAmpersand](https://github.com/AsteriskAmpersand) - Hash dictionary from his Mrl3 Editor, and mod3 mesh format research.
- [CG Cookie](https://github.com/CGCookie) - Addon updater module.
- [matyalatte](https://github.com/matyalatte/Texconv-Custom-DLL) - DirectX Texconv DLL library.
- [PhilippSeifried](https://github.com/Philipp-Seifried/Blender-Normals-To-Vertex-Color) - Normal to vertex color solution.
- [JodoZT](https://github.com/JodoZT/MHWTexConvertor) - MHW Tex file format from his converter.
- Torvosaure - Help me test on the linux platform.

## 一些中文内容
* B站：[不太亮的诸葛亮](https://space.bilibili.com/84161516?spm_id_from=333.1007.0.0)
* 怪猎mod作者交流群：[640945651](https://qm.qq.com/q/iABxIIl3gs)
* 踩蘑菇：[诸葛不太亮](https://www.caimogu.cc/user/183747.html)
* 爱发电：[诸葛不太亮](http://www.ifdian.net/a/korone_suki)
