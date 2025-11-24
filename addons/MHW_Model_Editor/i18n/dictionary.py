from ....common.i18n.dictionary import preprocess_dictionary

dictionary = {
    "zh_CN": {
        # ("*", "Example Addon Side Bar Panel"): "示例插件面板", 
        # ("*", "Example Functions"): "示例功能", 
        # ("*", "ExampleAddon"): "示例插件", 
        # ("*", "Resource Folder"): "资源文件夹", 
        # ("*", "Int Config"): "整数参数", 
        # # This is not a standard way to define a translation, but it is still supported with preprocess_dictionary.
        # "Boolean Config": "布尔参数", 
        # "Second Panel": "第二面板", 
        # ("*", "Add-on Preferences View"): "插件设置面板", 
        # ("Operator", "ExampleOperator"): "示例操作", 

        # message_functions.py 完成
        "ERROR: ": "错误: ", 
        "WARNING: ": "警告: ",

        # blender_mod3.py 完成
        "Parsed mrl3.": "已解析mrl3.", 
        "Loading mrl3 data...": "正在加载mrl3数据...", 
        "Loading mod3 materials from mrl3...": "正在从mrl3中加载mod3材质...", 
        'Materials loading took': "材质加载耗时", 

        'MHW Mod3 import started.': "MHW Mod3导入开始.", 
        "Parsed mod3.": "已解析mod3.", 
        'Mod3 parsing took': "Mod3解析耗时", 
        'Mod3 imported in': "Mod3导入共耗时", 
        'Mod3 Info:': "Mod3信息:", 
        'Mod3 TimeStamp:': "Mod3时间戳:", 
        'Mesh Count:': "网格数量:", 
        'Valid Mesh Count:': "合法的网格数量:", 
        'Imported Mesh Count:': "导入的网格数量:", 
        'MHW Mod3 import finished.': "MHW Mod3导入完毕.", 

        'MHW Mod3 export started.': "MHW Mod3导出开始.", 
        'Target Collection:': "目标集合:", 
        'Target Armature:': "目标骨架:", 
        'Target Armature: None': "目标骨架: 无", 
        'Collection:': "集合:", 
        'Failed to solve repeated UVs.': "处理重叠UV失败.", 
        'Failed to split sharp edges.': "分离锐边失败.", 
        'Triangulated': "三角化", 
        'Gathering mesh data took': "收集网格数据耗时", 
        'Converting to mod3 file took': "转换为mod3文件耗时", 
        'Mod3 exported in': "Mod3导出共耗时", 
        'Vertex Count:': "顶点数量:", 
        'Face Count:': "三角面数量:", 
        'Armature Bone Count:': "骨骼数量:", 
        'MHW Mod3 export finished.': "MHW Mod3导出完毕.", 


        # file_mod3.py 完成
        "File is not a MHW MOD3 file.": "文件不是MHW MOD3文件.", 
        "Opening ": "正在打开 ", 
        "Writing to ": "正在写入 ",


        # mod3_export_errors.py 完成
        ("Operator", "MHW Mod3 Export Error"): "MHW Mod3导出错误",

        ("*", "ERROR INFO:"): "错误信息:",
        ("*", "HOW TO FIX:"): "如何修复:",
        ("*", "ERROR OBJECTS:"): "错误对象:",
        ("*", "ERROR BONES:"): "错误骨骼:",

        ("*", "No Target Mod3 Collection"): "没有目标Mod3集合",
        ("*", "Target mod3 collection was not selected when exporting."): "在导出时未选择目标mod3集合.",
        ("*", "Select a target mod3 collection in the export options."): "在导出选项中选择一个目标mod3集合.",

        ("*", "No Meshes In Collection"): "集合中没有网格",
        ("*", "No meshes were found in the target mod3 collection."): "在目标mod3集合中没有找到网格.",
        ("*", "Also maybe there are no selected or visible meshes."): "也可能是没有选中的或可见的网格.",
        ("*", "Select a target mod3 collection in the export options that contains meshes."): "在导出选项中选择一个包含网格的目标mod3集合.",
        ("*", "If you checked \"Only Selected Meshes\" or \"Only Visible Meshes\" in the export options,"): "如果你在导出选项中勾选了 \"仅选中网格\" 或 \"仅可见网格\",",
        ("*", "please make sure there are selected or visible meshes."): "请确保有选中的或可见的网格.",

        ("*", "Multiple Same Lod Collections"): "有多个相同的Lod集合",
        ("*", "There are multiple child lod collections with the same lod level."): "存在多个相同lod层级的子lod集合.",
        ("*", "Change the name of child lod collections to ensure that each lod level is unique."): "修改子lod集合的名称, 确保每个lod层级都是唯一的.",

        ("*", "More Than One Armature"): "有多个骨架",
        ("*", "More than one armature was found in the target mod3 collection."): "目标mod3集合中有多个骨架.",
        ("*", "Move the extra armature into another collection or delete it."): "将多余的骨架移到其他集合中, 或者删除它.",

        ("*", "Max Bones Exceeded"): "骨骼数量超过限制",
        ("*", "The amount of bones on the armature exceeds the maximum limit of 255."): "骨骼数量超过了最大限制255.",
        ("*", "Reduce the amount of bones on the armature."): "减少骨架中的骨骼数量.",

        ("*", "Incorrect Bone Name Format"): "错误的骨骼名称格式",
        ("*", "Some bones are not named with format \"MhBone__xxx\"."): "某些骨骼名称不符合 \"MhBone__xxx\" 的格式.",
        ("*", "Or the name suffix index exceeds the maximum limit of 511."): "或者后缀序号超过了最大限制511.",
        ("*", "Change the bone name to \"MhBone__xxx\", where xxx is suffix index, such as \"MhBone__150\"."): "将骨骼名称修改为 \"MhBone__xxx\" 的格式, 其中xxx是后缀序号, 例如 \"MhBone__150\".",
        ("*", "And also make sure that the suffix index is less than 512."): "并且也要确保后缀序号小于512.",

        ("*", "No Weights On Mesh"): "网格没有权重",
        ("*", "A mesh has an armature, but no weights assigned to bones."): "某个网格没有对应骨骼的权重.",
        ("*", "Add a new vertex group and weight it to a bone on the armature in weight paint mode."): "添加一个新的顶点组, 将其绑定至对应骨骼.",

        ("*", "No Vertices On Sub Mesh"): "子网格中没有顶点",
        ("*", "A mesh has no vertices. All meshes must have at least 3 vertices and 1 face."): "某个网格没有顶点. 所有网格必须有至少3个顶点和1个面.",
        ("*", "Delete the listed mesh objects."): "删除下面列出的网格对象.",

        ("*", "No Faces On Sub Mesh"): "子网格中没有面",
        ("*", "A mesh has no faces. All meshes must have at least 3 vertices and 1 face."): "某个网格没有面. 所有网格必须有至少3个顶点和1个面.",

        ("*", "No Material On Sub Mesh"): "子网格没有材质",
        ("*", "A mesh has no material assigned to it."): "某个网格没有分配材质.",
        ("*", "All meshes must have one material assigned to them."): "所有网格必须至少有1个材质.",
        ("*", "Specify an mrl3 material name on the end of the object name separated by two underscores."): "在网格名称的末尾指定材质名, 用两个下划线分隔.",
        ("*", "Example Object Name: Group_0_Sub_0__body"): "示例网格名称: Group_0_Sub_0__body",

        ("*", "Max Vertices Exceeded On Sub Mesh"): "子网格顶点数量超过限制",
        ("*", "A mesh exceeded the limit of 65535 vertices."): "某个网格的顶点数量超过了最大限制65535.",
        ("*", "Separate parts of the mesh into more sub meshes."): "将网格分离为更多的子网格.",
        ("*", "Or use the decimate modifier to reduce mesh quality."): "或者使用精简修改器来减少网格的顶点数量.",

        ("*", "Max Faces Exceeded On Sub Mesh"): "子网格面数量超过限制",
        ("*", "A mesh exceeded the limit of 1431655 faces."): "某个网格的面数量超过了最大限制1431655.",

        ("*", "No UV Map On Sub Mesh"): "子网格没有UV通道",
        ("*", "A mesh has no UV map. All meshes require at least one uv map."): "某个网格没有UV通道. 所有网格必须有至少1个UV通道.",
        ("*", "Create a UV map."): "创建一个UV通道.",

        ("*", "Multiple UVs Assigned To Vertex"): "顶点有多个UV",
        ("*", "A mesh has multiple uvs assigned to a single vertex."): "某个网格中的某个顶点有多个UV.",
        ("*", "Check \"Auto Solve Repeated UVs\" in the export options."): "在导出选项中勾选 \"自动处理重叠UV\".",

        ("*", "Max Weights Per Vertex Exceeded On Sub Mesh"): "子网格权重总限值超过限制",
        ("*", "A vertex has more the maximum of 8 weights assigned to it."): "某个顶点的绑定顶点组数量超过了最大限制8.",
        ("*", "Limit total weights to 8 in weight paint mode and normalize all weights."): "在权重模式下将总限值设为8, 并规格化所有权重.",
        ("*", "Or click \"Limit Total and Normalize All\" button in \"MHW Mesh Tools\" to solve this."): "或者点击 \"MHW 网格工具\" 面板中的 \"限制总限值并归一化\" 按钮来解决.",
        ("*", "If there are not too many bones in the armature, you can also limit total weights to 4."): "如果骨架中的骨骼数量不是很多, 你也可以将总限值设为4.",

        ("*", "Loose Vertices On Sub Mesh"): "子网格有松散顶点",
        ("*", "A mesh has loose vertices with no faces assigned."): "某个网格有松散顶点.",
        ("*", "Select the listed mesh objects in edit mode, press A to select all vertices."): "选中下面列出的网格对象, 进入编辑模式, 按A键全选所有的顶点.",
        ("*", "Then select Mesh > Clean Up > Delete Loose in the menu bar at the top."): "然后选择顶部菜单栏中的 网格 > 清理 > 删除松散元素.",
        ("*", "Or click \"Delete Loose Geometry\" button in \"MHW Mesh Tools\" to solve this."): "或者点击 \"MHW 网格工具\" 面板中的 \"删除松散元素\" 按钮来解决.",

        ("*", "No Bones on Armature"): "骨架中没有骨骼",
        ("*", "The armature in the target collection has no bones."): "目标集合中的骨架中没有任何骨骼.",
        ("*", "Import a valid armature from an existing mod3 file."): "从外部mod3文件中导入一个有效的骨架.",

        ("*", "Total Vertices Exceeded Max Limit"): "总顶点数量超过限制",
        ("*", "Total vertices count exceeds the maximum limit of 4294967295."): "总顶点数量超过了最大限制值4294967295.",
        ("*", "Reconsider your life choices."): "重新考虑您的人生.",
        ("*", "Why decide to try to export so many vertices?"): "为什么要导出这么多顶点?",

        ("*", "Total Faces Exceeded Max Limit"): "总面数量超过限制",
        ("*", "Total faces count exceeds the maximum limit of 1431655."): "总面数量超过了最大限制值1431655.",
        ("*", "Why decide to try to export so many faces?"): "为什么要导出这么多面?",

        ("*", "Total Meshes Exceeded Max Limit"): "总网格数量超过限制",
        ("*", "Total meshes count exceeds the maximum limit of 65535."): "总网格数量超过了最大限制值65535.",
        ("*", "Why decide to try to export so many meshes?"): "为什么要导出这么多网格?",

        ("*", "Total Materials Exceeded Max Limit"): "总材质数量超过限制",
        ("*", "Total materials count exceeds the maximum limit of 65535."): "总材质数量超过了最大限制值65535.",
        ("*", "Why decide to try to export so many materials?"): "为什么要导出这么多材质?",

        'MHW Mod3 export failed.': "MHW Mod3导出失败.",


        # mod3_functions.py 完成


        # mod3_io.py 完成
        ("Operator", "Import MHW MOD3"): "导入MHW MOD3", 
        ("*", "Import MHW MOD3 Files"): "导入MHW MOD3文件",

        ("*", "Clear Scene"): "清理场景", 
        ("*", "Clear all objects before importing the mod3 file"): "在导入mod3文件之前清理所有的对象", 
        ("*", "Add Nested Collections"): "添加嵌套集合", 
        ("*", "Add a general parent collection to place other collections of various imported files."
              "\nThis will make the collection structure look clearer."
              "\nLeaving this option enabled is highly recommended"): "添加一个总的父级集合, 用于放置其他各种导入文件的集合."
                                                               "\n这会使集合的层级结构看起来更为清晰."
                                                               "\n强烈建议启用此选项", 
        ("*", "Only Import Armature"): "仅导入骨架", 
        ("*", "Only import the armature of the mod3 file"): "仅导入mod3文件的骨架", 
        ("*", "Import All LODs"): "导入全部LOD层级", 
        ("*", "Import all LOD (level of detail) meshes in mod3 file."
              "\nIf unchecked, only the highest LOD meshes will be imported"): "导入mod3文件中的全部LOD层级网格."
                                                                               "\n如果未勾选, 则只会导入最高LOD层级的网格", 
        ("*", "Armature Display Type"): "骨架显示类型", 
        ("*", "Set the display size of the bones to be imported"): "设置导入骨骼的显示尺寸", 
        ("*", "Load Material Data"): "加载材质数据", 
        ("*", "Imports the mrl3 materials as objects inside a collection in the outliner."
              "\nYou can make changes to material data by selecting the mrl3 material objects in the outliner."
              "\nUnder the Object Data Properties tab (green axis), there's a panel called \"Mrl3 Material Properties\"."
              "\nMake any changes to mrl3 materials there"): "将mrl3材质导入为对象, 并放入大纲视图的集合中."
                                                             "\n你可以在大纲视图中选择mrl3材质对象来更改材质数据."
                                                             "\n在物体数据属性栏 (绿色轴) 下, 有一个名为 \"Mrl3材质属性\" 的面板, 你可以在那儿修改材质数据",
        ("*", "Load Mesh Materials"): "加载网格材质", 
        ("*", "Load materials from the mrl3 file. This may increase the time the model takes to import"): "从mrl3文件中加载材质."
                                                                                                          "\n这可能会增加导入模型所需的时间", 
        ("*", "Load Unused Textures"): "加载未使用的贴图", 
        ("*", "Loads textures that have no function assigned to them in the material shader graph."
              "\nLeaving this disabled will make materials load faster."
              "\nOnly enable this if you plan on editing the material shader graph", ): "在材质节点中加载未指定功能的贴图."
                                                                                       "\n禁用此选项将加快导入材质的速度."
                                                                                       "\n仅当你计划编辑材质节点时才启用此选项", 
        ("*", "Load Unused Properties"): "加载未使用的属性", 
        ("*", "Loads material properties that have no function assigned to them in the material shader graph."
              "\nLeaving this disabled will make materials load faster."
              "\nOnly enable this if you plan on editing the material shader graph"): "在材质节点中加载未指定功能的属性."
                                                                                       "\n禁用此选项将加快导入材质的速度."
                                                                                       "\n仅当你计划编辑材质节点时才启用此选项", 
        ("*", "Use Backface Culling"): "使用背面剔除", 
        ("*", "Enables backface culling on materials. May improve Blender's performance on high poly meshes."
              "\nBackface culling will only be enabled on materials without the two sided flag"): "在材质上启用背面剔除."
                                                                                                  "\n对于高多边形的网格, 可能会提高Blender的性能."
                                                                                                  "\n背面剔除仅会在未设置双面标志的材质上启用", 
        ("*", "Reload Cached Textures"): "重载缓存贴图", 
        ("*", "Convert all textures again instead of reading from already converted textures."
              "\nUse this if you make changes to textures and need to reload them"): "重新转换所有的贴图, 而不是读取已经转换的贴图."
                                                                                     "\n如果你修改了贴图并需要重载贴图, 可以使用此选项", 
        ("*", "Manually set the path of the mrl3 file."
              "\nThe mrl3 file is found automatically if this is left blank."
              "\nTip: Hold shift and right click the mrl3 file and click \"Copy as path\", then paste into this field"): "手动设置mrl3文件的路径."
                                                                                                                         "\n如果留空, 插件会自动寻找mrl3文件."
                                                                                                                         "\n提示: 按住shift并右键单击mrl3文件, 然后点击 \"复制为路径\", 并粘贴于此",
        ("*", "Load Chains & Collisions"): "加载物理链和碰撞", 
        ("*", "Load physical chain and collision objects from the ctc & ccl file"): "从ctc与ccl文件中加载物理链和碰撞对象", 

        ("*", "Show Mod3 Options"): "显示Mod3选项", 
        ("*", "Show Mrl3 Options"): "显示Mrl3选项", 
        ("*", "Show CTC & CCL Options"): "显示CTC & CCL选项", 

        ("*", "Mod3 Options"): "Mod3选项", 
        ("*", "Armature Display Type:"): "骨架显示类型:", 
        ("*", "Bones Display Size:"): "骨骼显示尺寸:", 
        ("*", "Mrl3 Options"): "Mrl3选项", 
        ("*", "Manual Mrl3 Path:"): "手动选择Mrl3路径:", 
        ("*", "CTC & CCL Options"): "CTC & CCL选项", 

        'Blender Version': "Blender版本", 
        'Multi MOD3 Import': "导入MOD3", 
        'Path does not exist, cannot import file.': "路径不存在, 无法导入文件.", 
        'If you are importing multiple files at once, they must all be in the same directory.': "如果一次导入多个文件, 它们必须都在同一目录中.", 
        'Invalid Path:': "无效路径:", 
        "Successfully imported MHW MOD3 file.": "成功导入MHW MOD3文件.", 
        "Failed to import MHW MOD3 file. Check Window > Toggle System Console for details.": "导入MHW MOD3文件失败. 详细信息见窗口 > 控制台.", 
        "Some MHW MOD3 files failed to import. Check Window > Toggle System Console for details.": "某些MHW MOD3文件导入失败. 详细信息见窗口 > 控制台.", 

        ("Operator", "Export MHW MOD3"): "导出MHW MOD3", 
        ("*", "Export MHW MOD3 File"): "导出MHW MOD3文件",

        ("*", "Only Selected Meshes"): "仅选中网格", 
        ("*", "Only export selected meshes"): "仅导出选中的网格", 
        ("*", "Only Visible Meshes"): "仅可见网格", 
        ("*", "Only export visible meshes"): "仅导出可见的网格", 
        ("*", "Auto Solve Repeated UVs"): "自动处理重叠UV", 
        ("*", "Splits connected UV islands if present. The mesh format does not allow for multiple uvs assigned to a vertex."
              "\nNOTE: This will modify the exported mesh. If auto smooth is disabled on the mesh, the normals may change"): "分离相连的UV孤岛."
                                                                                                                             "\n网格格式不允许一个顶点有多个UV."
                                                                                                                             "\n注意: 这会修改导出的网格. 如果未启用网格的自动光滑, 则法向可能会变", 
        ("*", "Split Sharp Edges"): "分离锐边", 
        ("*", "Edge splits all edges marked as sharp to preserve them on the exported mesh."
              "\nNOTE: This will modify the exported mesh"): "分离所有锐边, 以在导出的网格上保留锐边."
                                                             "\n注意: 这会修改导出的网格", 
        ("*", "Use Blender Material Names"): "使用Blender材质名", 
        ("*", "If left unchecked, the exporter will get the material names to be used from the end of each object name."
              "\nFor example, if a mesh is named Group_0_Sub_0__Shirts_Mat, the material name is Shirts_Mat."
              "\nIf this option is enabled, the material name will instead be taken from the first material assigned to the object"): "如果不勾选, 导出时会从每个网格的名称中获取材质名."
                                                                                                                                      "\n例如, 如果网格名称为Group_0_Sub_0__Shirts_Mat, 则材质名称为Shirts_Mat."
                                                                                                                                      "\n如果勾选, 则材质名称将取自分配给网格的第一个材质", 
        ("*", "Invisible Mantles Mod Fix"): "隐藏衣装Mod修复", 
        ("*", "The \"Invisible Mantles Mod\" has a bug where the glowing effects of the first material on the body part would be turned off when wearing the temporal mantle."
              "\nIf this option is enabled, the plugin will add an unused material as the first material to avoid this issue."
              "\nLeaving this option enabled is highly recommended"): "隐藏衣装Mod有一个bug, 即当穿上转身衣装后, 人物身体部位模型的第一个材质的发光效果将被强制关闭."
                                                                      "\n如果启用此选项, 插件将添加一个无用材质作为第一个材质, 来避免此问题."
                                                                      "\n强烈建议启用此选项",
        ("*", "Mod3 Collection:"): "Mod3集合:", 
        ("*", "Must select a mod3 collection first !!!"): "必须先选择一个mod3集合!!!", 

        "Successfully exported MHW MOD3 file.": "成功导出MHW MOD3文件.", 
        "Failed to export MHW MOD3 file. Check Window > Toggle System Console for details.": "导出MHW MOD3文件失败. 详细信息见窗口 > 控制台.",


        # mod3_operators.py 完成
        ("Operator", "Create Mod3 Collection"): "创建Mod3集合",
        ("*", "Create a mod3 collection for putting armature and meshes into." \
              "\nIf you are making armor models, you can use this button." \
              "\nOtherwise, it is highly recommended to import a mod3 file to inherit the custom properties of the collection"): "创建一个mod3集合用于放置骨架和网格."
                                                                                                                                 "\n如果你正在制作防具模型, 可以使用此按钮创建新集合."
                                                                                                                                 "\n否则, 强烈建议从外部导入mod3文件来继承集合的自定义属性",
        ("*", "Mod3 Name"): "Mod3名称",
        ("*", "The name of the newly created mod3 collection."
              "\nUse the same name as the mod3 file"): "新创建的mod3集合名称."
                                                       "\n使用与mod3文件相同的名称",
        "Created new mod3 collection.": "已创建新的mod3集合.",
        "Invalid mod3 collection name.": "无效的mod3集合名称.",

        ("Operator", "Create Nested Collections"): "创建嵌套集合",
        ("*", "Create nested collections containing mod3, mrl3 and ctc collections." \
              "\nThis will make the collection structure look clearer"): "创建包含mod3, mrl3和ctc集合的嵌套集合组."
                                                                         "\n这会使集合的层级结构看起来更为清晰",
        ("*", "Collection Name"): "集合名称",
        ("*", "The name of the newly created nested collections"): "新创建的嵌套集合名称",
        "Created new nested collections.": "已创建新的嵌套集合.",
        "Invalid collection name.": "无效的集合名称.",

        ("Operator", "Rename Meshes"): "重命名网格",
        ("*", "Renames selected meshes to mod3 mesh naming scheme (Example: Group_0_Sub_0__Ch_Pl_Standard_Mt__1)"): "将选中的网格重命名为mod3网格的命名格式 (例如: Group_0_Sub_0__Ch_Pl_Standard_Mt__1)",
        "There are no meshes in selected objects.": "选中的对象中没有网格对象.",

        ("Operator", "Set Mesh Group ID"): "设置网格组ID",
        ("*", "Quickly set mesh group ID on selected meshes"): "快速设置选中网格的网格组ID",
        ("*", "Group ID"): "网格组ID",
        "There are no meshes that can be parsed group ID.": "没有能被解析网格组ID的网格对象.",

        ("Operator", "Delete Loose Geometry"): "删除松散元素",
        ("*", "Deletes loose vertices and edges with no faces on selected meshes"): "删除选中网格上不成面的松散顶点和边",

        ("Operator", "Remove Empty Vertex Groups"): "清除空顶点组",
        ("*", "Remove all vertex groups that have no weight assigned to them"): "清除所有未分配权重的顶点组",

        ("Operator", "Limit Total and Normalize All"): "限制总限值并归一化",
        ("*", "Limits the amount of bones influences per vertex to 8 and normalizes the weights of all vertex groups for all selected meshes"): "将每个顶点的骨骼影响数量限制为8, 并对选中网格的所有顶点组的权重进行归一化",

        ("Operator", "Bake Normal To Vertex Color"): "烘焙法向到顶点色",
        ("*", "Bakes the world normal to vertex color on selected meshes." \
              "\nBaked vertex color will be saved in the channel called \"World Space Normal\"." \
              "\nIf you select too many meshes, this operation may consume a lot of time"): "将世界空间的法向烘焙到选中网格的顶点色."
                                                                                            "\n烘焙出来的顶点色会被保存在名为 \"World Space Normal\" 的顶点色通道中."
                                                                                            "\n如果选中了过多网格, 该操作可能会消耗较长时间",


        # mod3_panels.py 完成
        ("*", "MHW Mesh Tools"): "MHW 网格工具",


        # mod3_parser.py 完成
        "Non normalized weights detected on sub mesh! Weights may not behave as expected in game!": "在子网格上检测到未归一化的权重! 权重在游戏中的表现可能与预期不符!",


        # mod3_properties.py 完成


        # blender_mod3_mrl3.py 完成
        "Finished loading materials.": "加载材质完毕.",
        "An error occurred while loading materials. See the Window > Toggle System Console for details.": "加载材质时发生错误. 详细信息见窗口 > 控制台.",
        'Saved chunk path:': "已保存chunk路径:",


        # blender_mrl3.py 完成
        'MHW Mrl3 import started.': "MHW Mrl3导入开始.",
        'Mismatched Material Hashes': "不匹配的材质哈希值",
        'Mrl3 data imported in': "Mrl3数据导入共耗时",
        'Mrl3 Info:': "Mrl3信息:",
        'Mrl3 TimeStamp:': "Mrl3时间戳:",
        'Material Count:': "材质数量:",
        'Matched Material Count:': "匹配的材质数量:",
        'Imported Material Count:': "导入的材质数量:",
        'MHW Mrl3 import finished.': "MHW Mrl3导入完毕.",

        'MHW Mrl3 export started.': "MHW Mrl3导出开始.",
        "Converting to mrl3 file finished.": "转换为mrl3文件完毕.",
        'Mrl3 exported in': "Mrl3导出共耗时",
        'Texture Count:': "贴图数量:",

        'MHW Mrl3 export finished.': "MHW Mrl3导出完毕.",


        # file_mrl3.py 完成
        "File is not a MHW MRL3 file.": "文件不是MHW MRL3文件.",
        'Unknown property type:': "未知属性类型:",
        'Unknown Hash': "未知哈希值:",


        # mrl3_dicts.py 完成


        # mrl3_export_errors.py 完成
        ("Operator", "MHW Mrl3 Export Error"): "MHW Mrl3导出错误",
        'MHW Mrl3 export failed.': "MHW Mrl3导出失败.",

        ("*", "No Target Mrl3 Collection"): "没有目标Mrl3集合",
        ("*", "Target mrl3 collection was not selected when exporting."): "在导出时未选择目标mrl3集合.",
        ("*", "Select a target mrl3 collection in the export options."): "在导出选项中选择一个目标mrl3集合.",

        ("*", "Multiple Same Materials"): "存在多个相同材质",
        ("*", "Multiple mrl3 objects have the same material name."): "存在包含相同材质名称的mrl3材质对象.",
        ("*", "Delete extra conflict objects, or set the material name to a different name."): "删除多余的冲突对象, 或者将材质名改为不同的名称.",
        ("*", "Make sure each mrl3 object has its unique material name."): "确保每个mrl3材质对象都有唯一的材质名.",


        # mrl3_functions.py 完成


        # mrl3_io.py 完成
        ("Operator", "Import MHW MRL3"): "导入MHW MRL3",
        ("*", "Import MHW MRL3 Files"): "导入MHW MRL3文件",
        'Multi MRL3 Import': "导入MRL3",
        "Successfully imported MHW MRL3 file.": "成功导入MHW MRL3文件.",
        "Failed to import MHW MRL3 file. Check Window > Toggle System Console for details.": "导入MHW MRL3文件失败. 详细信息见窗口 > 控制台.",
        "Some MHW MRL3 files failed to import. Check Window > Toggle System Console for details.": "某些MHW MRL3文件导入失败. 详细信息见窗口 > 控制台.",

        ("Operator", "Export MHW MRL3"): "导出MHW MRL3",
        ("*", "Export MHW MRL3 File"): "导出MHW MRL3文件",
        ("*", "Mrl3 Collection:"): "Mrl3集合:",
        ("*", "Must select a mrl3 collection first !!!"): "必须先选择一个mrl3集合!!!",
        "Successfully exported MHW Mrl3 file.": "成功导出MHW MRL3文件.",
        "Failed to export MHW Mrl3 file. Check Window > Toggle System Console for details.": "导出MHW MRL3文件失败. 详细信息见窗口 > 控制台.",


        # mrl3_nodes.py 完成


        # mrl3_operators.py 完成
        ("Operator", "Create Mrl3 Collection"): "创建Mrl3集合",
        ("*", "Create a mrl3 collection for putting mrl3 material objects into"): "创建一个mrl3集合, 用于放置mrl3材质对象",
        ("*", "Mrl3 Name"): "Mrl3名称",
        ("*", "The name of the newly created mrl3 collection."
              "\nUse the same name as the mrl3 file"): "新创建的mrl3集合名称."
                                                       "\n使用与mrl3文件相同的名称",
        ("*", "Created new mrl3 collection."): "已创建新的mrl3集合.",
        ("*", "Invalid mrl3 collection name."): "无效的mrl3集合名称.",

        ("Operator", "Reindex Mrl3 Materials"): "排序Mrl3材质",
        ("*", "Reorders the mrl3 material objects and sets their names to the name set in the custom properties."
              "\nThe button will only be triggered if active mrl3 collection exists"): "重新排序mrl3材质对象, 并将其名称设置为当前属性中的材质名称."
                                                                                       "\n仅当活动mrl3集合存在时, 该按钮才能被触发",
        ("*", "Reindexed mrl3 material objects."): "已重新排序mrl3材质对象.",

        ("Operator", "Add Preset Material"): "添加预设材质",
        ("*", "Add a new mrl3 material object with current material preset."
              "\nThe button will only be triggered if active mrl3 collection exists"): "添加一个具有当前预设属性的mrl3材质对象."
                                                                                       "\n仅当活动mrl3集合存在时, 该按钮才能被触发",
        "Reading Preset: ": "正在读取预设: ",
        "There are currently no presets that can be added.": "当前没有可以添加的预设.",
        "Added preset material.": "已添加预设材质.",

        ("Operator", "Save Selected As Preset"): "保存为预设",
        ("*", "Save selected mrl3 material object as a preset for easy reuse and sharing." 
              "\nThe button will only be triggered if a mrl3 material object is activated." 
              "\nPresets can be accessed using the \"Open Preset Folder\" button"): "将选中的mrl3材质对象保存为预设, 以便重复使用与分享."
                                                                                    "\n仅当激活一个mrl3材质对象时, 该按钮才能被触发."
                                                                                    "\n可以使用 \"打开预设文件夹\" 按钮访问预设文件",
        "Saved mrl3 material preset.": "已保存mrl3材质预设.",

        ("Operator", "Open Preset Folder"): "打开预设文件夹",
        ("*", "Open the preset folder in File Explorer"): "在文件资源管理器中打开预设文件夹",

        ("Operator", "Replace String"): "替换字符串",
        ("*", "Replace certain specific string in the texture path"): "替换贴图路径中的指定字符串",

        ("*", "Original String"): "原始字符串",
        ("*", "The original string that needs to be replaced"): "需要被替换的原始字符串",
        ("*", "Replaced String"): "替换字符串",
        ("*", "The string after being replaced"): "替换后的字符串",


        # mrl3_panels.py 完成
        ("*", "MHW Mrl3 Tools"): "MHW Mrl3工具",
        ("Operator", "Import Mod3"): "导入Mod3",
        ("Operator", "Export Mod3"): "导出Mod3",
        ("Operator", "Import Mrl3"): "导入Mrl3",
        ("Operator", "Export Mrl3"): "导出Mrl3",
        ("*", "Active Mrl3 Collection"): "活动Mrl3集合",
        ("*", "Mod Directory"): "Mod目录",

        ("*", "Presets"): "预设",
        ("Operator", "Save Preset"): "保存预设",

        ("*", "Mrl3 Material Properties"): "Mrl3材质属性",
        ("*", "Master Material Type:"): "主材质类型:",
        ("*", "Master Material Type: Unknown"): "主材质类型: 未知",
        ("*", "Surface Coef"): "表面系数",
        ("*", "Alpha Coef"): "透明系数",

        ("*", "Map List"): "贴图列表",
        ("*", "Property List"): "属性列表",
        ("*", "Property Count:"): "属性数量:",
        ("*", "Sampler List"): "采样列表",
        ("*", "Sampler Count:"): "采样数量:",


        # mrl3_presets.py 完成
        'Must select a mrl3 material object (named with \"Mrl3 Material 00...\") to save preset.': "必须选择一个mrl3材质对象 (以 \"Mrl3 Material 00...\" 命名) 以保存预设.",
        "Saved material preset to ": "已保存材质预设到 ",
        "Invalid preset file name.": "无效的材质文件名.",

        "Failed to read json file.": "读取json文件失败.",
        "Preset type is not supported.": "预设类型不支持.",
        "Preset is missing material header info, cannot add preset material.": "预设丢失了材质头信息, 无法添加预设材质.",
        "Adding preset material ": "正在添加预设材质 ",


        # mrl3_properties.py 完成
        'Unable to load usable properties': "无法加载可用的属性",

        ("*", "Material Name"): "材质名称",
        ("*", "The name of the current mrl3 material."
              "\nThe material name must match on the mod3 and mrl3 file"): "当前mrl3材质的名称."
                                                                           "\nmod3与mrl3文件的材质名必须互相匹配",
        ("*", "Material Name Hash"): "材质名哈希值",
        ("*", "Do not change this unless you know what you're doing"): "除非你知道自己在做什么, 否则不要改动该属性",
        ("*", "MMTR Hash"): "主材质哈希值",
        ("*", "MMTR Name"): "主材质名称",
        ("*", "The type of the current mrl3 material."
              "\nDo not change this unless you know what you're doing"): "当前mrl3材质的类型."
                                                                         "\n除非你知道自己在做什么, 否则不要改动该属性",
        ("*", "Shader Hash"): "着色器哈希值",
        ("*", "Linked Material"): "链接材质",
        ("*", "The blender material that corresponds to this mrl3 material object."
              "\nAny changes made to supported mrl3 properties (with spanner icon) will reflect on the blender material."
              "\nIf a linked material is not set, it will be set automatically once an mrl3 property is changed"): "链接到此mrl3材质对象的blender材质."
                                                                                                                   "\n修改任意支持的mrl3属性 (带扳手图标的) 都会直接影响blender材质的效果."
                                                                                                                   "\n如果未设置链接材质, 则当某个mrl3属性被修改时, 它会被自动设置",
        ("*", "Search the list for items that contain this string.\nPress enter to search"): "在列表中搜索包含此字符串的项目."
                                                                                             "\n按 enter 键进行检索",
        ("*", "Set the blue collection containing the mrl3 file to edit."
              "\nYou can create a new mrl3 collection by pressing the \"Create Mrl3 Collection\" button"): "设置要进行编辑的mrl3集合."
                                                                                                           "\n你可以按 \"创建Mrl3集合\" 按钮来创建一个新的mrl3集合",
        # ("*", "Set the red mod3 collection to apply the active mrl3 collection to"): "设置",
        ("*", "Set the nativePC directory of your mod."
              "\nThis is used by \"Apply Active Mrl3\" and \"Copy Converted Tex\" button."
              "\nThis will be set automatically when a file is exported."
              "\nExample:\n" + r"D:\SteamLibrary\steamapps\common\Monster Hunter World\nativePC"): "设置mod的nativePC目录."
                                                                                                   "\n该目录会在使用 \"应用活动Mrl3\" 和 \"复制转换的贴图\" 按钮时调用."
                                                                                                   "\n导出文件时会自动设置该目录."
                                                                                                   "\n示例: " + r"D:\SteamLibrary\steamapps\common\Monster Hunter World\nativePC",
        ("*", "Add Conversion Folder"): "添加转换文件夹",
        ("*", "When converting textures files, add a folder called \"Converted_MHW_DDS\" or \"Converted_MHW_Tex\" to put converted texture files into"): "当转换贴图文件时, 添加一个名为 \"Converted_MHW_DDS\" 或 \"Converted_MHW_Tex\" 的文件夹, 用于放置转换后的贴图文件",
        ("*", "Add DXGI Format Prefix"): "添加DXGI格式前缀",
        ("*", "When converting .tex to .dds, add dxgi format prefix to file name."
              "\nFor example, if the name of .tex is \"body_BML.tex\", the name of the converted .dds will be \"BC7S_body_BML.dds\""): "在转换.tex为.dds时, 在文件名前面添加格式字符."
                                                                                                                                       "\n比如.tex文件名为 \"body_BML.tex\", 则转换后的.dds文件名将为 \"BC7S_body_BML.dds\"",
        ("*", "Set the directory containing textures to be converted to .tex files"): "设置包含需要被转换为.tex文件的贴图的目录",


        # file_dds.py 完成
        "File is not a valid DDS file.": "文件不是有效的DDS文件.",
        "Writing ": "正在写入 ",


        # file_tex.py 完成
        "File is not a MHW Tex file.": "文件不是MHW Tex文件.",
        "File is not a MHW Tex file, maybe from other games.": "文件不是MHW Tex文件, 可能来自其他游戏.",
        'Unknown MHW Tex format': "未知MHW Tex格式",


        # tex_function.py 完成
        'Could not delete temporary dds file:': "无法删除临时dds文件:",
        'Unsupported DDS format': "不支持的DDS格式",


        # tex_operators.py 完成
        ("Operator", "MHW Tex Conversion"): "MHW贴图转换",
        ("*", "Opens a window to select textures to convert." 
              "\nSelected .dds files will be converted to .tex, and .tex files will be converted to .dds." 
              "\nIf you are using Blender 4.1 or higher, you can drag .tex or .dds files into the 3D view to convert them"): "打开一个窗口, 以选择需要转换的贴图."
                                                                                                                             "\n选中的.dds将被转换为.tex, 而.tex将被转换为.dds."
                                                                                                                             "\n如果你正在使用 Blender 4.1+ 版本, 可以将.tex或.dds文件拖放到3D视图中进行转换",
        'MHW Tex convert started.': "MHW贴图转换开始.",
        'Tex converted in': "贴图转换共耗时",
        'Conversion Info:': "转换信息:",
        'Success Count:': "成功数量:",
        'Failure Count:': "失败数量:",
        'MHW Tex convert finished.': "MHW贴图转换完毕.",

        ("Operator", "Convert Settings"): "转换设置",
        ("*", "Detail settings for converting texture files"): "转换贴图文件的细节设置项",

        ("Operator", "Convert Directory to Tex"): "转换目录为Tex",
        ("*", "Converts all .dds files in the chosen directory to .tex." 
              "\nConverted files will be saved inside a folder called \"Converted_MHW_Tex\"." 
              "\nSave .dds with BC7 sRGB for color type textures, BC5 Linear for normal and BC7 Linear for anything else"): "将所选目录中的所有.dds转换为.tex."
                                                                                                                            "\n转换后的文件将被保存在名为 \"Converted_MHW_Tex\" 的文件夹中."
                                                                                                                            "\n将颜色类型的贴图保存为BC7 sRGB格式, 法线贴图保存为BC5线性格式, 其他类型的贴图保存为BC7线性格式",
        "There are no .dds files in provided directory.": "提供的目录中没有.dds文件.",
        "Provided texture directory is not a directory or does not exist.": "提供的贴图目录不是一个目录, 或者目录不存在.",

        ("Operator", "Open Conversion Folder"): "打开转换文件夹",
        ("*", "Open the folder containing the converted texture files in File Explorer"): "在文件资源管理器中打开包含转换贴图文件的文件夹",

        ("Operator", "Copy Converted Tex Files"): "复制转换的贴图文件",
        ("*", "Copies .tex files in conversion folder into the specified mod \"nativePC\" directory." 
              "\nCopied files will be placed at the paths set in the active mrl3 collection"): "将转换得到的.tex文件复制到指定的mod目录中."
                                                                                               "\n复制的文件将被放置在当前的活动mrl3集合中所设置的路径下",
        "Please set texture and mod directory first.": "请先选择贴图目录以及mod目录.",
        "Please set active mrl3 collection first.": "请先选择活动mrl3集合.",
        "Provided mod directory is not a directory or does not exist.": "提供的mod目录不是一个目录, 或者目录不存在.",
        'MHW Tex copy started.': "MHW贴图复制开始.",
        'MHW Tex copy finished.': "MHW贴图复制完毕.",


        # tex_panels.py 完成
        ("*", "MHW Tex Tools"): "MHW 贴图工具",
        ("*", "Texture Directory"): "贴图目录",







    }
}

dictionary = preprocess_dictionary(dictionary)

dictionary["zh_TW"] = dictionary["zh_CN"]
dictionary["zh_HANS"] = dictionary["zh_CN"]
dictionary["zh_HANT"] = dictionary["zh_CN"]
