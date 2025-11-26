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


        # addon_updater.py TODO


        # addon_updater_ops.py TODO


        # blender_functions.py 完成
        'Set mod directory to': "已设置mod目录为",
        "Failed to set mod directory, exported file path probably does not follow the chunk naming scheme.": "设置mod目录失败, 导出的文件路径可能不符合chunk目录的命名方案.",


        # general_function.py 完成


        # message_functions.py 完成
        "ERROR: ": "错误: ", 
        "WARNING: ": "警告: ",
        "Message Box": "消息框",
        "Error": "错误",


        # node_arrange.py 完成
        "No output node found.": "找不到输出节点.",


        # rw_functions.py 完成


        # blender_ccl.py 完成
        'MHW CCL import started.': "MHW CCL导入开始.",
        "Parsed ccl.": "已解析ccl.",
        'CCL imported in': "CCL导入共耗时",
        'CCL Info:': "CCL信息:",
        'Collision Count:': "碰撞数量:",
        'Matched Collision Count:': "匹配的碰撞数量:",
        'MHW CCL import finished.': "MHW CCL导入完毕.",

        'MHW CCL export started.': "MHW CCL导出开始.",
        "Converting to ccl file finished.": "转换为ccl文件完毕.",
        'CCL exported in': "CCL导出共耗时",
        'MHW CCL export finished.': "MHW CCL导出完毕.",


        # ccl_export_errors.py 完成
        ("Operator", "MHW CCL Export Error"): "MHW CCL导出错误",
        'MHW CCL export failed.': "MHW CCL导出失败.",

        ("*", "Capsule Has Multiple Heads"): "胶囊有多个头部",
        ("*", "Some capsule collisions have more than one head."): "某些胶囊体碰撞有多个头部.",
        ("*", "Delete extra head."): "删除多余的头部.",
        ("*", "Make sure each capsule collision only has one head."): "确保每个胶囊体碰撞都只有一个头部.",

        ("*", "Capsule Has Multiple Tails"): "胶囊有多个尾部",
        ("*", "Some capsule collisions have more than one tail."): "某些胶囊体碰撞有多个尾部.",
        ("*", "Delete extra tail."): "删除多余的尾部.",
        ("*", "Make sure each capsule collision only has one tail."): "确保每个胶囊体碰撞都只有一个尾部.",

        ("*", "Capsule Has No Head"): "胶囊没有头部",
        ("*", "Some capsule collisions have no head."): "某些胶囊体碰撞没有头部.",

        ("*", "Capsule Has No Tail"): "胶囊没有尾部",
        ("*", "Some capsule collisions have no tail."): "某些胶囊体碰撞没有尾部.",

        ("*", "The \"BoneName\" constraint of sphere or capsule has no target or subtarget."): "球体或胶囊体的 \"骨骼名\" 约束没有目标骨架或子目标骨骼.",
        ("*", "Make sure \"BoneName\" constraint of sphere or capsule has target armature and bone."): "确保球体或胶囊体的 \"骨骼名\" 约束存在目标骨架和子目标骨骼.",

        ("*", "Some spheres or capsules have no \"BoneName\" constraint."): "某些球体或胶囊体没有名为 \"骨骼名\" 的约束.",
        ("*", "Make sure each sphere or capsule has a \"BoneName\" constraint."): "确保每个球体或胶囊体都有一个名为 \"骨骼名\" 的约束.",


        # ccl_functions.py 完成


        # ccl_io.py 完成
        ("Operator", "Import MHW CCL"): "导入MHW CCL",
        ("*", "Import MHW CCL Files." \
              "\nThe button will only be triggered if active ctc collection exists." 
              "\nNOTE: Before importing ccl, make sure that at least one mod3 armature exists in the current scene"): "导入MHW CCL文件."
                                                                                                                      "\n仅当活动ctc集合存在时, 该按钮才能被触发."
                                                                                                                      "\n注意: 在导入ccl之前, 请确保当前场景中至少存在一个mod3骨架",
        'Multi CCL Import': "导入CCL",
        ("*", "Successfully imported MHW CCL file."): "成功导入MHW CCL文件.",
        "Failed to import MHW CCL file. Check Window > Toggle System Console for details.": "导入MHW CCL文件失败. 详细信息见窗口 > 控制台.",
        "Some MHW CCL files failed to import. Check Window > Toggle System Console for details.": "某些MHW CCL文件导入失败. 详细信息见窗口 > 控制台.",

        ("Operator", "Export MHW CCL"): "导出MHW CCL",
        ("*", "Export MHW CCL File"): "导出MHW CCL文件",
        ("*", "Successfully exported MHW CCL file."): "成功导出MHW CCL文件.",
        "Failed to export MHW CCL file. Check Window > Toggle System Console for details.": "导出MHW CCL文件失败. 详细信息见窗口 > 控制台.",


        # ccl_nodes.py 完成


        # ccl_operators.py 完成
        ("Operator", "Create Collision"): "创建碰撞",
        ("*", "Create new ccl collision objects from selected bone(s)." \
              "\nThe button will only be triggered if active ctc collection exists." \
              "\nSelect one bone to create a sphere or two bones to create a capsule"): "以选中的骨骼创建新的ccl碰撞对象."
                                                                                        "\n仅当活动ctc集合存在时, 该按钮才能被触发."
                                                                                        "\n选中一个骨骼以创建单球体碰撞, 两个骨骼以创建胶囊体碰撞",
        ("*", "Selected bone(s) must be named with format \"MhBone_xxx\"."): "所选骨骼的名称必须为 \"MhBone_xxx\" 的格式.",
        ("*", "Select one bone to create a sphere or two bones to create a capsule."): "选中一个骨骼以创建单球体碰撞, 两个骨骼以创建胶囊体碰撞.",
        ("*", "Created ccl collision from bone."): "已创建新的ccl碰撞.",

        ("Operator", "Create Full Body Collisions"): "创建全身碰撞",
        ("*", "Create collisions that covers the full body (only for player models)." \
              "\nThe button will only be triggered if active ctc collection exists"): "创建覆盖全身的碰撞体 (仅对于玩家模型)."
                                                                                      "\n仅当活动ctc集合存在时, 该按钮才能被触发",
        ("*", "Created full body collisions."): "已创建全身碰撞.",


        # ccl_panels.py 完成
        ("*", "CCL Collision Properties"): "CCL碰撞属性",
        ("*", "Show Collision Names"): "显示碰撞体名称",
        ("*", "Collision Offset"): "碰撞位置",


        # ccl_properties.py 完成
        ("*", "Set the armature to attach collision objects to."
              "\nIf uncheck, addon will try to find matching armature automatically."
              "\nNOTE: If some bones that are used by ccl file are missing, corresponding collision objects won't be imported"): "设置要连接碰撞对象的骨架."
                                                                                                                                 "\n如果留空, 插件将自动寻找匹配的骨架."
                                                                                                                                 "\n注意, 如果ccl文件使用的某些骨骼丢失, 则对应的碰撞对象不会被导入",
        ("*", "Collision Color"): "碰撞体颜色",
        ("*", "Show Collision Names"): "显示碰撞体名称",
        ("*", "Show CCL Collision Names in 3D View"): "在3D视图中显示碰撞体名称",

        ("*", "Draw Collisions Through Objects"): "在前面显示碰撞体",
        ("*",
         "Make all ccl collision objects render through any objects in front of them"): "使所有ccl碰撞显示在任意对象前面",

        ("*", "Head Offset"): "头部位置",
        ("*", "Set position of the head collision object"): "设置碰撞体头部对象的位置",

        ("*", "Tail Offset"): "尾部位置",
        ("*", "Set position of the tail collision object"): "设置碰撞体尾部对象的位置",


        # file_ccl.py 完成
        "File is not a MHW CCL file.": "文件不是MHW CCL文件.",


        # blender_ctc.py 完成
        'MHW CTC import started.': "MHW CTC导入开始.",
        "Parsed ctc.": "已解析ctc.",
        'Mismatched Bones': "不匹配的骨骼",
        'CTC imported in': "CTC导入共耗时",
        'CTC Info:': "CTC信息:",
        'Chain Count:': "链数量:",
        'Matched Chain Count:': "匹配的链数量:",
        'MHW CTC import finished.': "MHW CTC导入完毕.",

        'MHW CTC export started.': "MHW CTC导出开始.",
        "Converting to ctc file finished.": "转换为ctc文件完毕.",
        'CTC exported in': "CTC导出共耗时",
        'Node Count:': "节点数量:",
        'MHW CTC export finished.': "MHW CTC导出完毕.",


        # ctc_export_errors.py 完成
        ("Operator", "MHW CTC Export Error"): "MHW CTC导出错误",
        'MHW CTC export failed.': "MHW CTC导出失败.",

        ("*", "No Target CTC Collection"): "没有目标CTC集合",
        ("*", "Target ctc collection was not selected when exporting."): "在导出时未选择目标ctc集合.",
        ("*", "Select a target ctc collection in the export options."): "在导出选项中选择一个目标ctc集合.",

        ("*", "Header Has Parent"): "标头有父级对象",
        ("*", "CTC header cannot be a child of other objects."): "CTC标头不能是其他任何对象的子级.",
        ("*", "Make sure ctc header doesn't have parent objects."): "确保ctc标头没有父级对象.",

        ("*", "Node Has More Than One Frame"): "节点有多个框架",
        ("*", "Some nodes have more than one frame as child."): "某些节点有多个子级框架对象.",
        ("*", "Make sure each node has only one child frame."): "确保每个节点只有一个子级框架对象.",

        ("*", "Node Has No Frame"): "节点没有框架",
        ("*", "Some nodes have no frame as child."): "某些节点没有子级框架对象.",

        ("*", "Incorrect Node Parent"): "错误的节点父级",
        ("*", "Some nodes have incorrect parent object types."): "某些节点有错误类型的父级对象.",
        ("*", "Or maybe node has no parent chain or node object."): "或者可能没有作为父级的链组或节点对象.",
        ("*", "Make sure each node has a parent chain or node object."): "确保每个节点都有一个作为父级的链组或节点对象.",

        ("*", "Invalid Node Constraint"): "无效的节点约束",
        ("*", "The \"BoneName\" constraint of node has no target or subtarget."): "节点的 \"骨骼名\" 约束没有目标骨架或子目标骨骼.",
        ("*", "Make sure \"BoneName\" constraint of node has target armature and subtarget bone."): "确保节点的 \"骨骼名\" 约束存在目标骨架和子目标骨骼.",

        ("*", "Node Has No Constraint"): "节点没有约束",
        ("*", "Some nodes have no \"BoneName\" constraint."): "某些节点没有名为 \"骨骼名\" 的约束.",
        ("*", "Make sure each node has a \"BoneName\" constraint."): "确保每个节点都有一个名为 \"骨骼名\" 的约束.",

        ("*", "Incorrect Chain Parent"): "错误的链组父级",
        ("*", "Some chains have incorrect parent object types."): "某些链组有错误类型的父级对象.",
        ("*", "Or maybe chain has no parent header object."): "或者可能没有作为父级的标头对象.",
        ("*", "Make sure all chains are parented to header object."): "确保所有链组都以标头对象为父级.",

        ("*", "Chain Has Less Than Two Nodes"): "链组的节点数量小于2",
        ("*", "Some chains have less than two nodes as child."): "某些链组中的节点数量小于2.",
        ("*", "Make sure each chain has at least two nodes as its child."): "确保每个链组都有至少2个子级节点.",

        ("*", "No CTC Header"): "没有CTC标头",
        ("*", "Target ctc collection has no ctc header object."): "目标ctc集合中没有找到ctc标头对象.",
        ("*", "Make sure target ctc collection has only one ctc header object."): "确保目标ctc集合中有且仅有一个ctc标头对象.",

        ("*", "More Than One CTC Header"): "有多个CTC标头",
        ("*", "Target ctc collection has more than one ctc header object."): "目标ctc集合中有多个ctc标头对象.",

        ("*", "Incorrect Bone Name Format"): "错误的骨骼名格式",
        ("*", "Some constraint bones are not named with format \"MhBone__xxx\"."): "某些约束骨骼的名称不符合 \"MhBone__xxx\" 的格式.",
        ("*", "Or the name suffix index exceeds the maximum limit of 511."): "或骨骼名称的后缀序号超过了最大限制值511.",

        ("*", "Chain Has Branch"): "链组有分支",
        ("*", "Some chains have branching node structure."): "某些链组有分支的节点结构.",
        ("*", "Delete extra branch nodes."): "删除多余的分支节点.",
        ("*", "Make sure each chain has no branch nodes."): "确保每个链组都没有分支节点.",

        ("*", "Multiple Same Bones"): "多个相同的骨骼",
        ("*", "Multiple nodes have the same constraint bone."): "多个节点拥有相同的约束骨骼.",
        ("*", "Delete extra conflict nodes."): "删除多余的冲突节点.",
        ("*", "Make sure each node corresponds to a specific bone."): "确保每个节点都对应一个单独的骨骼.",


        # ctc_functions.py 完成
        "More than one armature was found in the scene. Select an armature before importing the ctc file.": "在场景中存在多个骨架. 请在导入ctc文件之前选择一个骨架.",
        "No armature in scene. The armature from the mod3 file must be present in order to import the ctc file.": "场景中没有骨架. 为导入ctc文件, 必须存在一个来自mod3文件的骨架.",


        # ctc_io.py 完成
        ("Operator", "Import MHW CTC"): "导入MHW CTC",
        ("*", "Import MHW CTC Files." \
              "\nNOTE: Before importing ctc, make sure that at least one mod3 armature exists in the current scene"): "导入MHW CTC文件."
                                                                                                                      "\n注意: 在导入ctc之前, 请确保当前场景中至少存在一个mod3骨架",
        ("*", "Load CCL Collision"): "加载CCL碰撞",
        ("*", "Load physical collision objects from the ccl file"): "加载来自ccl文件的碰撞体对象",
        ("*", "Merge With CTC Collection:"): "合并至CTC集合:",
        'Multi CTC Import': "导入CTC",
        "Successfully imported MHW CTC file.": "成功导入MHW CTC文件.",
        "Failed to import MHW CTC file. Check Window > Toggle System Console for details.": "导入MHW CTC文件失败. 详细信息见窗口 > 控制台.",
        "Some MHW CTC files failed to import. Check Window > Toggle System Console for details.": "某些MHW CTC文件导入失败. 详细信息见窗口 > 控制台.",

        ("Operator", "Export MHW CTC"): "导出MHW CTC",
        ("*", "Export MHW CTC File"): "导出MHW CTC文件",
        ("*", "Export CCL Collision"): "导出CCL碰撞",
        ("*", "When exporting ctc file, also export collision objects as ccl file"): "在导出ctc文件时, 一并将碰撞体对象导出为ccl文件",
        ("*", "CTC Collection:"): "CTC集合:",
        ("*", "Must select a ctc collection first !!!"): "必须先选择一个ctc集合!!!",
        "Successfully exported MHW CTC file.": "成功导出MHW CTC文件.",
        "Failed to export MHW CTC file. Check Window > Toggle System Console for details.": "导出MHW CTC文件失败. 详细信息见窗口 > 控制台.",


        # ctc_nodes.py 完成


        # ctc_operators.py 完成
        ("Operator", "Create CTC Collection"): "创建CTC集合",
        ("*", "Create a ctc collection for putting ctc & ccl objects into." \
              "\nNote that a ctc header object will also be created, and all ctc & cll objects must be parented to it"): "创建一个ctc集合用于放置ctc和ccl对象."
                                                                                                                         "\n注意, 这也将创建一个ctc标头对象, 且所有的ctc和ccl对象必须以其为父级",
        ("*", "CTC Name"): "CTC名称",
        ("*", "The name of the newly created ctc collection."
                     "\nUse the same name as the ctc file"): "新创建的ctc集合名称."
                                                             "\n使用与ctc文件相同的名称",
        "Created new ctc collection.": "已创建新的ctc集合.",
        "Invalid ctc collection name.": "无效的ctc集合名称.",

        ("Operator", "Switch To Pose Mode"): "转换至姿态模式",
        ("*", "Switch to pose mode to add new ctc chains or ccl collisions"): "转换至姿态模式, 以添加新的ctc链组或ccl碰撞",

        ("Operator", "Switch To Object Mode"): "转换至物体模式",
        ("*", "Switch to object mode to configure ctc chains or ccl collisions"): "转换至物体模式, 以配置ctc链组或ccl碰撞",

        ("Operator", "Create Chain"): "创建链组",
        ("*", "Create new ctc chain objects starting from the selected bone and ending at the last child bone." \
              "\nThe button will only be triggered if active ctc collection exists." \
              "\nBones in a chain must be named with format \"MhBone_xxx\""): "创建新的ctc链组对象, 该链组以当前选中的骨骼为链首, 以最后一个子级骨骼为链尾."
                                                                              "\n仅当活动ctc集合存在时, 该按钮才能被触发."
                                                                              "\n链中的骨骼必须以 \"MhBone_xxx\" 的格式命名",

        "Select only the chain start bone.": "请只选中链的头骨.",
        "A chain must have at least 2 bones.": "一条链必须包含至少2个骨骼.",
        "Current chain has some bones that are not named with format \"MhBone_xxx\".": "当前链中含有一些名称不符合 \"MhBone_xxx\" 格式的骨骼.",
        "Cannot have branching bones in a chain.": "一条链不能含有分支.",
        ("*", "Created ctc chain from bone."): "已创建新的ctc链组.",

        ("*", "Copy properties from a ctc object." \
              "\nThe button will only be triggered if a ctc object is activated"): "复制一个ctc对象的属性."
                                                                                   "\n仅当激活一个ctc对象时, 该按钮才能被触发",
        ("*", "Copied properties of ctc header object to clipboard."): "已将ctc标头的属性复制到剪贴板中.",
        ("*", "Copied properties of ctc chain object to clipboard."): "已将ctc链组的属性复制到剪贴板中.",
        ("*", "Copied properties of ctc node object to clipboard."): "已将ctc节点的属性复制到剪贴板中.",
        ("*", "Copied properties of angle limit orientation object to clipboard."): "已将角度限制方向属性复制到剪贴板中.",

        ("*", "Copy a specific property from a ctc node object to clipboard"): "将ctc节点对象的某个特定属性复制到剪贴板中",
        ("*", "Copied unkn flags property to clipboard."): "已复制 未知标志 属性到剪贴板.",
        ("*", "Copied angle mode property to clipboard."): "已复制 角度模式 属性到剪贴板.",
        ("*", "Copied collision shape property to clipboard."): "已复制 碰撞类型 属性到剪贴板.",
        ("*", "Copied unkn enum property to clipboard."): "已复制 未知枚举 属性到剪贴板.",
        ("*", "Copied collision radius property to clipboard."): "已复制 碰撞半径 属性到剪贴板.",
        ("*", "Copied angle radius property to clipboard."): "已复制 角度半径 属性到剪贴板.",
        ("*", "Copied width rate property to clipboard."): "已复制 宽度比率 属性到剪贴板.",
        ("*", "Copied mass property to clipboard."): "已复制 质量 属性到剪贴板.",
        ("*", "Copied elastic coef property to clipboard."): "已复制 弹性系数 属性到剪贴板.",

        ("*", "Paste properties from a ctc object to selected objects." \
              "\nSelect at least one ctc object of the same type as the clipboard content to paste"): "向选中的ctc对象粘贴之前复制的属性."
                                                                                                      "\n请选择至少一个与剪贴板内容类型相同的ctc对象进行粘贴",
        ("*", "Pasted properties of ctc header object from clipboard."): "已从剪贴板粘贴ctc标头的属性.",
        ("*", "Pasted properties of ctc chain object from clipboard."): "已从剪贴板粘贴ctc链组的属性.",
        ("*", "Pasted properties of ctc node object from clipboard."): "已从剪贴板粘贴ctc节点的属性.",
        ("*", "Pasted properties of angle limit orientation object from clipboard."): "已从剪贴板粘贴角度限制方向属性.",

        ("*", "Pasted unkn flags property from clipboard."): "已从剪贴板粘贴 未知标志 属性.",
        ("*", "Pasted angle mode property from clipboard."): "已从剪贴板粘贴 角度模式 属性.",
        ("*", "Pasted collision shape property from clipboard."): "已从剪贴板粘贴 碰撞类型 属性.",
        ("*", "Pasted unkn enum property from clipboard."): "已从剪贴板粘贴 未知枚举 属性.",
        ("*", "Pasted collision radius property from clipboard."): "已从剪贴板粘贴 碰撞半径 属性.",
        ("*", "Pasted angle radius property from clipboard."): "已从剪贴板粘贴 角度半径 属性.",
        ("*", "Pasted width rate property from clipboard."): "已从剪贴板粘贴 宽度比率 属性.",
        ("*", "Pasted mass property from clipboard."): "已从剪贴板粘贴 质量 属性.",
        ("*", "Pasted elastic coef property from clipboard."): "已从剪贴板粘贴 弹性系数 属性.",

        "Select at least one ctc object of the same type as the clipboard content to paste.": "请选择至少一个与剪贴板内容类型相同的ctc对象进行粘贴.",
        "Select at least one ctc object to paste.": "请选择至少一个ctc对象进行粘贴.",

        ("Operator", "Only Show Chains"): "仅显示链组",
        ("*", "Hide other objects and only show ctc chain objects." \
              "\nPress the \"Show All Objects\" button to recover"): "隐藏其他所有对象并仅显示ctc链组对象."
                                                                     "\n按 \"显示所有对象\" 按钮以恢复",
        ("*", "Hid all non ctc chain objects."): "已隐藏所有非ctc链组的对象.",

        ("Operator", "Only Show Nodes"): "仅显示节点",
        ("*", "Hide other objects and only show ctc node objects." \
              "\nPress the \"Show All Objects\" button to recover"): "隐藏其他所有对象并仅显示ctc节点对象."
                                                                     "\n按 \"显示所有对象\" 按钮以恢复",
        ("*", "Hid all non ctc node objects."): "已隐藏所有非ctc节点的对象.",

        ("Operator", "Only Show Collisions"): "仅显示碰撞",
        ("*", "Hide other objects and only show ccl collision objects." \
              "\nPress the \"Show All Objects\" button to recover"): "隐藏其他所有对象并仅显示ccl碰撞对象."
                                                                     "\n按 \"显示所有对象\" 按钮以恢复",
        ("*", "Hid all non ccl collision objects."): "已隐藏所有非ccl碰撞的对象.",

        ("Operator", "Only Show Angle Limits"): "仅显示角度限制轴",
        ("*", "Hide other objects and only show angle limit objects." \
              "\nPress the \"Show All Objects\" button to recover"): "隐藏其他所有对象并仅显示角度限制轴."
                                                                     "\n按 \"显示所有对象\" 按钮以恢复",
        ("*", "Hid all non angle limit objects."): "已隐藏所有非角度限制轴的对象.",

        ("Operator", "Show All Objects"): "显示所有对象",
        ("*", "Unhide all objects hidden with above buttons"): "取消隐藏全部被以上按钮隐藏的对象",
        ("*", "Unhid all objects."): "已取消隐藏全部对象.",

        ("Operator", "Align Angle Limit Direction"): "校准角度限制方向",
        ("*", "Aligns angle limit direction with the next node in the chain." \
              "\nYou can select one or more ctc chain objects to align." \
              "\nNote that additional adjustments may be required for the angle limit to work properly"): "将角度限制方向校准为朝向链中的下一个节点."
                                                                                                          "\n你可以选择一个或多个ctc链组对象进行校准."
                                                                                                          "\n请注意, 可能需要进行额外调整才能使角度限制正常工作",
        ("*", "Aligned angle limit directions."): "已校准角度限制方向.",
        ("*", "No chains found in selected objects or active ctc collection."): "在所选对象或活动ctc集合中未找到链组对象.",

        ("Operator", "Apply Angle Limit Ramp"): "应用角度限制坡度",
        ("*", "Apply an increasing angle limit radius on each ctc node as it gets further away." \
              "\nYou can select one or more ctc chain objects to apply ramp"): "对链组中的每个ctc节点应用一个逐渐增加的角度限制半径."
                                                                               "\n你可以选择一个或多个ctc链组对象应用坡度",
        ("*", "Max Angle Limit"): "最大角度限制",
        ("*", "The maximum angle limit radius after the max iteration number is reached."
              "\nFor example, if the max angle limit is 60 and the max iteration is 4, the first node angle limit will be 15, the second will be 30 and so on."
              "\nOnce the max iteration is reached, all nodes after that will be the max angle limit value"): "达到最大迭代次数后的最大角度限制半径."
                                                                                                              "\n例如, 如果最大角度限制半径为60°, 最大迭代次数为4, 则第一个节点的角度限制半径将为15°, 第二个将为30°, 依此类推."
                                                                                                              "\n一旦达到最大迭代次数, 之后的所有节点都将是最大的角度限制半径值",
        ("*", "Max Iteration"): "最大迭代次数",
        ("*", "The amount of ctc nodes until the angle limit radius is at it's maximum value"): "角度限制半径达到最大值之前的ctc节点数量",
        ("*", "Applied angle limit ramp to selected ctc chains."): "已对选中的ctc链组应用角度限制坡度.",
        ("*", "Must select one or more ctc chain objects to apply ramp."): "必须选择一个或多个ctc链组对象以应用角度限制坡度.",

        ("Operator", "Rename Chain Bones"): "重命名链骨",
        ("*", "Rename all bones in a chain with format \"MhBone_xxx\"." \
              "\nIf a ctc chain has been created, all node names in the chain will also be renamed." \
              "\nCheck button on the right for detailed settings"): "将一条链中的所有骨骼重命名为 \"MhBone_xxx\" 格式."
                                                                    "\n如果已经创建了一条ctc链组, 则该链组中的所有节点名称也会被重命名."
                                                                    "\n点击右侧的按钮以查看详细设置",
        ("*", "Start Bone ID"): "头骨ID",
        ("*", "Current chain will be sorted backwards and renamed with the ID entered"): "当前链将按照输入的ID值向后排序并重新命名",
        ("*", "Select only the chain start bone."): "请只选中链的头骨.",
        ("*", "A chain must have at least 2 bones."): "一条链必须包含至少2个骨骼.",
        ("*", "Cannot have branching bones in a chain."): "一条链不能含有分支.",
        ("*", "Current start ID will result in duplicate bone names. Please select another start ID."): "当前的头骨ID将导致冲突的骨骼名称. 请选择其他的ID值.",
        ("*", "Renamed chain bones."): "已重命名链骨.",
        ("*", "Start Bone ID:"): "头骨ID:",
        'Count Of Nodes In Collection:': "当前集合内的节点数量:",
        'Count Of Unused IDs (150~200):': "未使用的ID数量 (150~200):",
        ("*", "Unused IDs (150~200):"): "未使用的ID (150~200):",

        ("Operator", "Rename Bone Settings"): "重命名链骨设置",
        ("*", "Detail settings for renaming chain bones"): "重命名链骨的细节设置项",

        ("Operator", "Set Collision Flags"): "设置碰撞标志",
        ("*", "Set flags from a list of detail values"): "从详细数值列表中设置标志值",

        ("*", "Collision Self Enable"): "与其他链发生碰撞",
        ("*", "Whether the chain is allowed to collide with other chains"): "是否允许链与其他链发生碰撞",
        ("*", "Collision Model Enable"): "与ccl发生碰撞",
        ("*", "Whether the chain is allowed to collide with ccl file"): "是否允许链与ccl文件发生碰撞",
        ("*", "Collision VGround Enable"): "与地面发生碰撞",
        ("*", "Whether the chain is allowed to collide with the ground"): "是否允许链与地面发生碰撞",
        ("*", "Set collision flags."): "已设置碰撞标志.",

        ("Operator", "Set Chain Flags"): "设置链标志",
        ("*", "Angle Limit Enable"): "启用角度限制",
        ("*", "Whether to enable angle limit."
              "\nUsually recommended to enable it, otherwise angle limit will be invalid"): "是否启用角度限制."
                                                                                            "\n通常建议启用, 否则角度限制将会无效",
        ("*", "Angle Limit Restitution Enable"): "启用角度限制恢复",
        ("*", "Whether to enable angle limit restitution"): "是否启用角度限制恢复",
        ("*", "End Rot Constraint Enable"): "启用尾节点旋转约束",
        ("*", "Whether to enable the rotation of end node (uncertain)"): "是否启用尾节点的旋转约束 (不确定)",
        ("*", "Trans Animation Enable"): "启用反动画",
        ("*", "Whether to enable trans animation."
              "\nAfter activating, the chain will stagnate in a motion stop posture, but the specific meaning is unclear"): "是否启用反动画."
                                                                                                                            "\n启用后链会停滞在运动停止的姿态, 尚不清楚具体含义",
        ("*", "Angle Free Enable"): "启用自由角度",
        ("*", "Whether to enable angle free"): "是否启用自由角度",
        ("*", "Stretch Both Enable"): "启用链骨伸缩",
        ("*", "Whether to enable stretch (uncertain)."
              "\nDepends on the mass and elasticity of the nodes"): "是否启用链骨伸缩 (不确定)."
                                                                    "\n取决于节点的质量和弹性",
        ("*", "Part Blend Enable"): "启用部分混合",
        ("*", "Whether to enable part blend."
              "\nAfter activating, the chain seems to squeeze towards the center, but the specific meaning is unclear"): "是否启用部分混合."
                                                                                                                         "\n启用后链似乎会向中心挤压, 尚不清楚具体含义",
        ("*", "Set chain flags."): "已设置链标志.",

        ("*", "Save selected ctc chain object as a preset for easy reuse and sharing." \
              "\nThe button will only be triggered if a ctc object is activated." \
              "\nPresets can be accessed using the \"Open Preset Folder\" button"): "将选中的ctc链组对象保存为预设, 以便重复使用与分享."
                                                                                    "\n仅当激活一个ctc链组对象时, 该按钮才能被触发."
                                                                                    "\n可以使用 \"打开预设文件夹\" 按钮访问预设文件",
        ("*", "Saved ctc chain preset."): "已保存ctc链组预设.",

        ("Operator", "Apply CTC Chain Preset"): "应用CTC链组预设",
        ("*", "Apply preset to selected ctc chain objects"): "将预设应用于所选的ctc链组对象",
        ("*", "There are currently no presets that can be applied."): "当前没有可以应用的预设.",
        ("*", "Applied ctc chain preset."): "已应用ctc链组预设.",
        ("*", "Must select a ctc chain object (named with \"CTC_CHAIN_XX...\") to apply preset."): "必须选择一个ctc链组对象 (以 \"CTC_CHAIN_XX...\" 命名) 以应用预设.",


        # ctc_panels.py 完成
        ("*", "CTC Header Properties"): "CTC标头属性",
        ("*", "Note: The header properties here will affect all chains."): "注意: 此处的标头属性会影响所有的链组.",
        ("*", "Global TransForce"): "整体反作用力",
        ("*", "Wind Weight"): "风力权重",

        ("*", "CTC Chain Properties"): "CTC链组属性",
        ("*", "Collider"): "碰撞器",
        ("*", "Unkn Flags"): "未知标志",

        ("*", "CTC Node Properties"): "CTC节点属性",
        ("*", "Angle Radius"): "角度半径",

        ("*", "MHW CTC & CCL Tools"): "MHW CTC & CCL 工具",
        ("Operator", "Import CTC"): "导入CTC",
        ("Operator", "Export CTC"): "导出CTC",
        ("Operator", "Import CCL"): "导入CCL",
        ("Operator", "Export CCL"): "导出CCL",
        ("*", "Active CTC Collection"): "活动CTC集合",
        ("Operator", "Align Angle Direction"): "校准角度限制方向",
        ("Operator", "Apply Angle Ramp"): "应用角度限制坡度",
        ("*", "Create new chains in Pose Mode."): "在姿态模式创建新的链组和碰撞.",
        ("*", "Configure chains in Object Mode."): "在物体模式配置链组和碰撞.",

        ("*", "Clipboard"): "剪贴板",
        'Content:': "剪贴板内容:",

        ("Operator", "Apply Chain Preset"): "应用链组预设",

        ("Operator", "Only Chains"): "仅显示链组",
        ("Operator", "Only Collisions"): "仅显示碰撞",
        ("Operator", "Only Nodes"): "仅显示节点",
        ("Operator", "Only Angles"): "仅显示角度轴",

        ("*", "Display Settings"): "显示设置",
        ("*", "Size Settings"): "尺寸设置",
        ("*", "Color Settings"): "颜色设置",

        ("*", "Header Properties"): "标头属性",
        ("*", "Chain Properties"): "链组属性",
        ("*", "Node Properties"): "节点属性",
        ("*", "Collision Properties"): "碰撞属性",


        ("*", "CTC Header"): "CTC标头",
        ("*", "CTC Chain"): "CTC链组",
        ("*", "CTC Node"): "CTC节点",
        ("*", "Angle Limit Orientation"): "角度限制方向",


        # ctc_presets.py 完成
        "Must select a ctc chain object (named with \"CTC_CHAIN_XX...\") to save preset.": "必须选择一个ctc链组对象 (以 \"CTC_CHAIN_XX...\" 命名) 以保存预设.",
        "Saved chain preset to ": "已保存链组预设到 ",
        "Applying preset to ": "正在应用预设到 ",
        "Preset is missing key ": "预设缺少键 ",
        ", cannot set value on active object.": ", 无法设置活动对象的对应属性值.",


        # ctc_properties.py 完成
        ("*", "Set the ctc collection to merge ctc objects with."
              "\nUse this when you want to merge ctc objects from different files"): "设置要合并ctc对象的ctc集合."
                                                                                     "\n当你要合并来自不同文件的ctc对象时, 可以使用此选项",
        ("*", "Set the ctc collection to be exported"): "设置要导出的ctc集合",
        ("*", "Set the armature to attach ctc objects to."
              "\nIf uncheck, addon will try to find matching armature automatically."
              "\nNOTE: If some bones that are used by ctc file are missing, corresponding ctc nodes won't be imported"): "设置要连接ctc对象的骨架."
                                                                                                                         "\n如果留空, 插件将自动寻找匹配的骨架."
                                                                                                                         "\n注意, 如果ctc文件使用的某些骨骼丢失, 则对应的ctc节点不会被导入",
        ("*", "Set the collection containing the ctc file to edit."
              "\nYou can create a new ctc collection by pressing the \"Create CTC Collection\" button."
              "\nNote that ccl collision will also be included in the ctc collection"): "设置要进行编辑的ctc集合."
                                                                                  "\n你可以按 \"创建CTC集合\" 按钮来创建一个新的ctc集合."
                                                                                  "\n注意ccl碰撞也将包含在ctc集合中",
        ("*", "Draw Chains Through Objects"): "在前面显示链组",
        ("*","Make all ctc chain objects render through any objects in front of them"): "使所有ctc链组显示在任意对象前面",
        ("*", "Show Node Names"): "显示节点名称",
        ("*", "Show Node Names in 3D View"): "在3D视图中显示节点名称",
        ("*", "Draw Nodes Through Objects"): "在前面显示节点",
        ("*", "Make all ctc node and frame objects render through any objects in front of them"): "使所有ctc节点和框架对象显示在任意对象前面",
        ("*", "Show Cones"): "显示锥体",
        ("*", "Show Angle Limit Cones in 3D View"): "在3D视图中显示角度限制锥体",
        ("*", "Draw Cones Through Objects"): "在前面显示锥体",
        ("*", "Make all angle limit cones render through any objects in front of them"): "使所有角度限制锥体显示在任意对象前面",
        ("*", "Angle Limit Size"): "角度限制轴尺寸",
        ("*", "Set the display size of node angle limits"): "设置角度限制坐标轴的显示尺寸",
        ("*", "Cone Size"): "锥体尺寸",
        ("*", "Set the display size of node angle limit cones"): "设置角度限制锥体的显示尺寸",
        ("*", "Chain Size"): "链组尺寸",
        ("*", "Set the thickness of chain lines"): "设置链组的显示尺寸",
        ("*", "Chain Color"): "链组颜色",
        ("*", "Angle Limit Color"): "锥体颜色",
        ("*", "Show Relation Lines"): "显示关系线",
        ("*", "Show dotted lines indicating object parents."
              "\nNote that this affects all objects, not just ctc objects"): "显示指示对象父级结构的虚线."
                                                                             "\n注意这会影响所有的对象, 而不仅仅是ctc对象",
        ("*", "Hide Last Node Cone"): "隐藏尾节点的锥体",
        ("*", "Hide the last ctc node's angle limit cone."
              "\nThis is because the last node is typically unused and has a dummy rotation value"): "隐藏最后一个ctc节点的角度限制锥体."
                                                                                                     "\n这是因为最后一个节点通常未使用且具有默认的矩阵值",
        ("*", "Align Bone Direction"): "校正骨骼方向",
        ("*", "Align bones in a vertical and upward direction."
              "\nNote this operation will apply all transformations of the current armature"): "将骨骼校正为竖直向上的方向."
                                                                                               "\n注意此操作会强制应用当前骨架的全部变换",
        ("*", "Reserve Mesh Objects"): "保留网格对象",
        ("*", "Reserve mesh objects when hiding other objects"): "当隐藏其他对象时, 保留网格对象",

        ("*", "Attribute Flags"): "属性标志",
        ("*", "Determine certain movement properties of the chain."
              "\nIt is actually a binary, and the maximum bit may be 8 bits from testing."
              "\nThe most common value is 64 (mostly seen on armor), followed by 80 (mostly seen on pendants)."
              "\n80 seems to make the chain move more violently than 64, you can refer to the fluttering pendant."
              "\nThe main difference lies in the fifth and seventh bits of binary, and it is unclear what these bits mean"): "决定物理链的某些运动属性."
                                                                                                                             "\n实际为二进制, 经测试最大位可能为8位."
                                                                                                                             "\n最常见的是64 (多在防具上看到), 其次是80 (多在吊坠上看到)."
                                                                                                                             "\n80相比64似乎会使链的运动更为剧烈, 可以参考会飘动的吊坠."
                                                                                                                             "\n主要区别在于二进制的第5位和第7位, 尚不清楚这些位具体表示的含义",
        ("*", "Step Time"): "时间步长",
        ("*", "The time interval between each update of the simulation by the physics engine."
              "\nSetting the step time to 0.16666 seconds means that the physics engine updates 60 times per second, which matches a frame rate of 60FPS."
              "\nPlease don't change this value"): "物理引擎每次更新模拟之间的时间间隔."
                                                   "\n将时间步长设置为1/60秒, 意味着物理引擎每秒会进行60次更新, 这与60FPS的帧率相匹配."
                                                   "\n请不要修改此值",
        ("*", "Gravity Scaling"): "重力比例",
        ("*", "Multiple of the gravity applied to the chain, Usually 1."
              "\nWhen the value is negative, the direction of gravity reverses."
              "\nWhen the value is 0, there is no gravity"): "链受到重力的倍数, 通常为1."
                                                             "\n当值为负数时, 重力方向会反转."
                                                             "\n当值为0时, 则无重力",
        ("*", "Global Damping"): "整体阻尼",
        ("*",
         "The greater the damping, the greater the resistance, and the slower and more difficult the movement of the chain."
         "\nThe smaller the damping, the smaller the resistance, and the faster and more flexible the movement of the chain."
         "\nNormally the damping is 0 or 0.1, shouldn't be set to too high."
         "\nA negative value will cause the chain to gain additional energy and move automatically"): "阻尼越大, 阻力越大, 链的运动越缓慢和困难."
                                                                                                      "\n阻尼越小, 阻力越小, 链的运动越迅速和灵活."
                                                                                                      "\n阻尼通常为0或0.1, 不应设为过高的值."
                                                                                                      "\n值为负时, 会使链获取额外的能量, 从而自动运动",
        ("*", "Global TransForce Coef"): "整体反作用力系数",
        ("*", "When the value is 1, the trans force is equal to the acting force. This is the usual value."
              "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
              "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
              "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward"): "当值为1时, 反作用力等于作用力. 这是通常设定的数值."
                                                                                                                                                                     "\n当值大于1时, 反作用力会大于作用力. 并且数值越大, 链的运动幅度越剧烈."
                                                                                                                                                                     "\n当值小于1时, 反作用力会小于作用力. 并且数值越小, 链的运动幅度越微弱."
                                                                                                                                                                     "\n当值为负时, 反作用力和作用力会反向, 会导致原本向后运动的链变为向前运动",
        ("*", "Spring Scaling"): "弹性比例",
        ("*", "Multiple of chain elasticity, Usually 1."
              "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior"): "链弹性的倍数, 通常为1."
                                                                                                                          "\n不建议设为负数, 会导致一些不稳定的物理行为",
        ("*", "Wind Scale"): "风力范围平均值",
        ("*", "Wind Scale Min"): "风力范围最小值",
        ("*", "Wind Scale Max"): "风力范围最大值",
        ("*",
         "The magnitude of the wind force exposed to the chain is divided into average (median), minimum and maximum."
         "\nThe sizes of these three parameters should be determined by default according to the rule of \"WindScaleMax>=WindScale>=WindScaleMin\"."
         "\nJudging from the traversed CTC files, it seems that there is a relationship of \"WindScale=(WindScaleMin+WindScaleMax)/2\", which may be simply an average value"): "风力范围, 分为平均值 (中间值), 最小值和最大值."
                                                                                                                                                                                "\n这三个参数的大小应默认按照 \"最大值>=平均值>=最小值\" 的规则来取值."
                                                                                                                                                                                "\n从遍历过的CTC文件来看, 似乎有着 \"平均值=(最小值+最大值)/2\" 的固定关系, 可能单纯是平均值",
        ("*", "Wind Scale Weight"): "风力范围权重",
        ("*", "Represents the wind weight (proportion) of each wind section, and the sum of the three values equals 1"): "表示各段风力权重 (占比), 三者总和等于1",

        ("*", "Collision Flags"): "碰撞标志",
        ("*", "Various attribute flags that define how chain collides"): "定义链的碰撞方式的各种属性标志",
        ("*", "Chain Flags"): "链组标志",
        ("*", "Various attribute flags that define how chain moves"): "定义链的运动方式的各种属性标志",

        ("*", "Unkn Flag1"): "未知标志1",
        ("*", "Actually binary. Common values are 0, 1, 17, 32. More testing is needed."
              "\nTaking 1 for the 1 bits seems to make the chain harder (or recovers faster) than taking 0."
              "\nTaking 1 for the 2 bits will force the chain to stretch, like a spring"): "未知标志, 实际为二进制. 常见取值有0, 1, 17, 32. 还需更多测试."
                                                                                           "\n第一位取1相比取0, 链似乎会更硬一些 (或者说恢复原状更快)."
                                                                                           "\n第二位取1相比取0, 链会被强制拉伸, 像一根弹簧一样",
        ("*", "Unkn Flag2"): "未知标志2",
        ("*", "Actually binary, Usually the value is 0, rarely the value is 1"): "未知标志, 实际为二进制, 通常取值为0, 很少为1",

        ("*", "Collider Attribute"): "碰撞属性",
        ("*", "Usually the value is -1"): "值通常为-1",
        ("*", "Collider Group"): "碰撞组",
        ("*", "Usually the value is 1"): "值通常为1",
        ("*", "Collider Type"): "碰撞类型",

        ("*", "Gravity"): "重力",
        ("*", "Usually only need to change the Y axis gravity."
              "\nWhen the value is negative, the direction of gravity reverses. When the value is 0, there is no gravity."
              "\n\"Gravity Scaling\" with the header part can be viewed as a multiplier, so when both values are negative, the actual direction of gravity is still downward"): "通常只需要调整y轴方向的重力即可."
                                                                                                                                                                                "\n当值为负数时, 重力方向会反转. 当值为0时, 则无重力."
                                                                                                                                                                                "\n与标头部分的 \"重力比例\" 可以看做乘积关系, 所以当二者值都为负时, 实际的重力方向仍然是向下的",
        ("*", "Damping"): "阻尼",
        ("*", "TransForce Coef"): "反作用力系数",
        ("*", "If \"Global TransForce\" is 1, it usually should be set to a value less than 1 here."
              "\nWhen the value is 1, the trans force is equal to the acting force. This is the usual value."
              "\nWhen the value is greater than 1, the trans force will be greater than the acting force. And the higher the value, the more intense the chain moves."
              "\nWhen the value is less than 1, the trans force will be less than the acting force. And the smaller the value, the weaker the chain moves."
              "\nWhen the value is negative, the trans force and acting force will reverse, causing the chain that was originally moving backward to move forward"): "若 \"整体反作用力\" 为1, 则此处通常应设为小于1的数值."
                                                                                                                                                                     "\n当值为1时, 反作用力等于作用力. 这是通常设定的数值."
                                                                                                                                                                     "\n当值大于1时, 反作用力会大于作用力. 并且数值越大, 链的运动幅度越剧烈."
                                                                                                                                                                     "\n当值小于1时, 反作用力会小于作用力. 并且数值越小, 链的运动幅度越微弱."
                                                                                                                                                                     "\n当值为负时, 反作用力和作用力会反向, 会导致原本向后运动的链变为向前运动",
        ("*", "Spring Coef"): "弹性系数",
        ("*", "If \"Spring Scaling\" is 1, it usually should be set to a value less than 1 here, even less than 0.1."
              "\nThe greater the value, the harder the chain and the less the deformation."
              "\nThe smaller the value, the softer the chain and the greater the deformation."
              "\nSetting it to a negative value is not recommended, which will lead to some unstable physical behavior"): "若 \"弹性比例\" 为1, 则此处通常应设为小于1的数值, 甚至小于0.1."
                                                                                                                          "\n值越大, 则链越硬, 相应的形变越小."
                                                                                                                          "\n值越小, 则链越软, 相应的形变越大."
                                                                                                                          "\n不建议设为负数, 会导致一些不稳定的物理行为",
        ("*", "Limit Force"): "限制力",
        ("*", "Usually the value is 1.0"): "值通常为1.0",
        ("*", "Friction Coef"): "摩擦系数",
        ("*", "Usually the value is 0"): "值通常为0",
        ("*", "Reflect Coef"): "反弹系数",
        ("*", "Usually the value is 0.1"): "值通常为0.1",
        ("*", "Wind Rate"): "风力比例",
        ("*", "Wind Limit"): "风力极限",
        ("*", "There is a hidden variable in memory called \"UseWindLimit\"."
              "\nWhen the value here is a negative integer, UseWindLimit = 50."
              "\nWhen the value here is a positive integer, UseWindLimit = WindLimit."
              "\nOnly seen taking 10 in a few ctc files, so you can just default to -1"): "在内存中有一个隐藏变量为 \"UseWindLimit\"."
                                                                                          "\n当此处数值为负整数时, UseWindLimit值恒为50."
                                                                                          "\n当此处数值为正整数时, UseWindLimit=风力极限."
                                                                                          "\n只在零星几个CTC文件中看到过取10, 总之平时默认-1即可",
        ("*", "Maybe actually binary, default to 0"): "未知标志, 实际可能为二进制."
                                                      "\n取0以外值的CTC文件可能没有, 所以基本上不用管, 默认0即可",
        ("*", "Maybe actually binary or boolean."
              "\nTaking 1 may make the node more compact than taking 0 (uncertain)."
              "\nThe default is 0"): "未知标志, 实际可能为二进制或布尔值."
                                     "\n取1相比取0可能会让节点更紧致一些 (不确定)."
                                     "\n默认0即可",

        ("*", "Angle Mode"): "角度模式",
        ("*", "Free"): "自由",
        ("*", "Node will rotate in any direction"): "节点将向任意方向旋转",
        ("*", "Cone"): "锥形",
        ("*", "Rotation of node will be limited to a cone"): "节点的旋转将被限制在一个圆锥体内",
        ("*", "Hinge"): "铰链",
        ("*", "Rotation of node will be limited to rotation only along the z-axis"): "节点的旋转将被限制为只绕Z轴旋转",
        ("*", "Oval"): "椭圆",
        ("*", "Rotation of node will be limited to an oval cone"): "节点的旋转将被限制在一个椭圆锥体内",

        ("*", "Collision Shape"): "碰撞类型",
        ("*", "No Collision"): "无碰撞体",
        ("*", "The shape of collision is a sphere"): "碰撞体形状为球体",
        ("*", "The shape of collision is a capsule"): "碰撞体形状为胶囊",

        ("*", "Unkn Enum"): "未知枚举",
        ("*", "Unknown enumeration, usually 1, but rarely used 0 and 2."
              "\nNormally, you can default to 1"): "未知枚举值, 通常为1, 很少会用到0和2, 平时默认1即可.\n",

        ("*", "Collision Radius"): "碰撞半径",

        ("*", "Angle Limit Radius"): "角度限制半径",
        ("*", "The amount the node is allowed to rotate from it's angle limit direction."
              "\nIt is actually in radian, representing the top angle of a cone."
              "\nThe bottom radius of the cone is used here to represent the top angle, which is incorrect but sufficient to represent the actual size"): "允许节点在其角度限制方向上旋转的量."
                                                                                                                                                          "\n实际为弧度制, 表示圆锥体的顶角."
                                                                                                                                                          "\n此处使用圆锥体的底面半径代为表示顶角, 虽然不正确但足够表示实际的大小",

        ("*", "Width Rate"): "宽度比率",
        ("*", "Rate of width to length of oval at the bottom of cone."
              "\nEffective only when Angle Mode is \"Oval\"."
              "\nWhen the value is 0, \"Oval\" has the same effect as \"Hinge\"",): "角度限制圆锥体底部椭圆的宽度相较于长度的比例."
                                                                                    "\n只在角度模式为 \"椭圆\" 时才生效."
                                                                                    "\n当值为0时, \"椭圆\" 的效果几乎和 \"铰链\" 相同",
        ("*", "Mass"): "质量",
        ("*",
         "Most ctc files default to 1, a few will have values greater than 1 or even around 10, and some will have values less than 1."
         "\nIt is not clear how this parameter works"): "节点质量, 大部分ctc文件都是默认1."
                                                        "\n少部分取值会大于1甚至到10左右, 还有一部分取值会小于1."
                                                        "\n目前不是很清楚该参数如何作用",

        ("*", "Elastic Coef"): "弹性系数",
        ("*", "Note that the elastic coef here is different from the spring coef of chain."
              "\nThe smaller the elastic coef, the easier the node is to be stretched."
              "\nThe larger the elastic coef, the more likely the node will be to maintain its original length."
              "\nChanging this value is not recommended，usually 1, which means that the node always maintains its original length"): "注意此处的弹性系数与链设置中的弹性系数不一样."
                                                                                                                                     "\n弹性系数越小, 节点越容易被拉长."
                                                                                                                                     "\n弹性系数越大, 节点越倾向于保持原本的长度."
                                                                                                                                     "\n不建议修改此值, 通常为1, 即节点总是保持原本的长度",


        # file_ctc.py 完成
        "File is not a MHW CTC file.": "文件不是MHW CTC文件.",


        # dds.py TODO


        # texconv.py TODO


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
        'Target Collection: None': "目标集合: 无",
        'Target Armature:': "目标骨架:", 
        'Target Armature: None': "目标骨架: 无", 
        'Collection:': "集合:",
        'Collection: None': "集合: 无",
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
        ("*", "Armature Type"): "骨架类型",
        ("*", "Bone Size"): "骨骼尺寸",
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
        ("*", "Load Chains & Collisions"): "加载链和碰撞",
        ("*", "Load physical chain and collision objects from the ctc & ccl file"): "从ctc与ccl文件中加载物理链和碰撞对象", 

        ("*", "Show Mod3 Options"): "显示Mod3选项", 
        ("*", "Show Mrl3 Options"): "显示Mrl3选项", 
        ("*", "Show CTC & CCL Options"): "显示CTC & CCL选项", 

        ("*", "Mod3 Options"): "Mod3选项", 
        ("*", "Armature Display Type:"): "骨架显示类型:", 
        ("*", "Bones Display Size:"): "骨骼显示尺寸:", 
        ("*", "Mrl3 Options"): "Mrl3选项", 
        ("*", "Manual Mrl3 Path:"): "手动选择Mrl3路径:",
        # ("*", "Manual Mrl3 Path:"): "手动Mrl3路径:",
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
        ("*", "Set the mod3 collection to be exported"): "设置要导出的mod3集合",


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
        "Invalid preset file name.": "无效的预设文件名.",

        "Failed to read json file.": "读取json文件失败.",
        "Preset type is not supported.": "预设类型不支持.",
        "Preset is missing material header info, cannot add preset material.": "预设丢失了材质标头信息, 无法添加预设材质.",
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
        ("*", "Set the mrl3 collection to be exported"): "设置要导出的mrl3集合",
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
                                                                                                                             "\n如果你正在使用Blender 4.1+版本, 可以将.tex或.dds文件拖放到3D视图中进行转换",
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

        ("Operator", "Copy Converted Tex Files"): "复制转换的贴图",
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


        # AddonPreferences.py 完成
        ("Operator", "Add Chunk Path"): "添加Chunk路径",
        ("*", "Add path to the extracted chunk folder.\n" + r"Example: D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC"): "添加提取的chunk文件夹路径.\n" + r"示例: D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC",
        ("Operator", "Remove Selected Path"): "移除所选路径",
        ("*", "Remove chunk path from the list"): "从列表中移除所选的chunk路径",
        ("Operator", "Reorder Item"): "排序项目",
        ("*", "Change the order in which files will be searched"): "更改检索文件的顺序",
        ("Operator", "Move Up"): "上移",
        ("Operator", "Move Down"): "下移",
        ("Operator", "Open Cache Folder"): "打开缓存文件夹",
        ("*", "Opens the texture cache folder in File Explorer"): "在文件资源管理器中打开缓存文件夹",
        ("Operator", "Check Cache Size"): "检查缓存大小",
        ("*", "Shows the current size of the texture cache folder"): "显示贴图缓存文件夹的当前大小",
        ("Operator", "Clear Cache Folder"): "清空缓存文件夹",
        ("*", "Deletes all cached converted textures."
              "\nNote that any saved blend files will lose their textures if the cache is cleared"): "删除所有缓存的转换贴图."
                                                                                                     "\n请注意, 如果清空缓存, 任何已保存的blend文件都将丢失对应的贴图",
        ("*", "Are you sure you want to delete all cached textures?"): "你确定要删除所有的缓存贴图吗?",
        ("*", "Directory:"): "目录:",
        "Cleared texture cache.": "已清空贴图缓存.",
        ("*", "Set the path to the nativePC or Chunk folder inside the extracted chunk files."
              "\nThis determines where textures will be imported from."
              "\n"+r"Example: D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC"): "设置提取的chunk文件中的nativePC或Chunk文件夹路径."
                                                                                 "\n这将决定贴图从何处导入."
                                                                                 "\n"+r"示例: D:\MHW_EXTRACT\chunk or D:\MHW_EXTRACT\nativePC",
        ("*", "Show External Links"): "显示外部链接选项",
        ("*", "Show Advanced Options"): "显示高级选项",
        ("*", "Show Mod3 Import Options"): "显示Mod3导入选项",
        ("*", "Show Mod3 Export Options"): "显示Mod3导出选项",
        ("*", "Show CTC Visibility Options"): "显示CTC可见性选项",
        ("*", "Show Texture Cache"): "显示贴图缓存选项",
        ("*", "Show Chunk Path"): "显示Chunk路径选项",
        ("*", "Show Auto Update"): "显示自动更新选项",

        ("*", "Show Drag and Drop Import Options (Blender 4.1+)"): "显示拖放导入选项 (Blender 4.1+)",
        ("*", "Show import options when dragging files into the 3D View."
              "\nIf this is disabled, the default import options will be used."
              "\nDrag and drop importing is only supported on Blender 4.1+"): "将文件拖放到3D视图中时, 显示导入选项."
                                                                              "\n如果禁用此选项, 将使用默认的导入选项."
                                                                              "\n拖放导入仅支持Blender 4.1+版本",
        ("*", "Show Console During Import / Export"): "导入或导出时显示控制台",
        ("*", "When importing or exporting a file, the console will be opened so that progress can be viewed."
              "\nNote that if the console is already opened before import or export, it will be closed instead."
              "\n This is a limitation of Blender, there's no way to get the active state of the console window"): "导入或导出文件时, 会打开控制台以便查看进度."
                                                                                                                   "\n请注意, 如果控制台在导入或导出之前已经打开, 则会被关闭."
                                                                                                                   "\n这属于Blender的限制, 无法获取控制台窗口的活动状态",
        ("*", "Use DDS Textures (Blender 4.2+)"): "使用DDS贴图 (Blender 4.2+)",
        ("*", "Use DDS textures instead of converting to other formats."
              "\nThis greatly improves material import speed but is only usable on Blender 4.2+."
              "\nIf the Blender version is less than 4.2, this option will do nothing"): "使用DDS贴图, 而不再转换为其他格式."
                                                                                         "\n这将大大提高材质的导入速度, 但仅适用于Blender 4.2+版本."
                                                                                         "\n若Blender的版本低于4.2, 此选项将无任何作用",
        ("*", "Show CTC & CCL Properties In Sub Panel"): "在子面板中显示 CTC 和 CCL 属性",
        ("*", "Synchronously show ctc & ccl properties in \"MHW Chain\" panel."
              "\nIf checked, when activating a ctc & ccl object, the properties will also be shown in the \"Properties\" sub-panel"): "在 \"MHW Chain\" 面板中同步显示ctc和ccl属性."
                                                                                                                                      "\n如果勾选此选项, 当激活ctc或ccl对象时, 属性会同步显示在 \"属性\" 子面板中",
        ("*", "Texture Cache Path"): "贴图缓存路径",
        ("*", "Location to save converted textures"): "保存转换贴图的位置",
        ("*", "Save Chunk Paths Automatically"): "自动保存Chunk路径",
        ("*", "If a chunk path is detected when a mod3 is imported, add it to the chunk path list automatically"): "若在导入mod3文件时检测到了chunk路径, 则自动将其添加到列表中",

        ("*", "Auto-check for Update"): "自动检查更新",
        ("*", "If enabled, auto-check for updates using an interval"): "如果启用, 则按照固定的时间间隔自动检查更新",
        ("*", "Months"): "月",
        ("*", "Number of months between checking for updates"): "检查更新时间隔的月数",
        ("*", "Days"): "日",
        ("*", "Number of days between checking for updates"): "检查更新时间隔的日数",
        ("*", "Hours"): "时",
        ("*", "Number of hours between checking for updates"): "检查更新时间隔的时数",
        ("*", "Minutes"): "分",
        ("*", "Number of minutes between checking for updates"): "检查更新时间隔的分数",

        ("*", "External Links"): "外部链接",
        ("*", "Advanced Options"): "高级选项",
        ("*", "Mod3 Import Options"): "Mod3导入选项",
        ("*", "Mod3 Export Options"): "Mod3导出选项",
        ("*", "Texture Cache"): "贴图缓存",
        ("*", "Texture cache path is very long."): "贴图缓存路径太长.",
        ("*", "File paths may exceed the max length of 255 characters and fail to convert."): "文件路径可能超过255个字符的最大长度, 并且无法转换.",
        ("*", "Consider changing this to a shorter path such as D:\MHWMod\TextureCache."): "考虑改为更短的路径, 比如: D:\MHWMod\TextureCache.",
        'Cache Size:': "缓存大小:",
        'Last Checked:': "上次检查时间:",
        ("*", "Chunk Path"): "缓存路径",


        # link.py 完成
        ("*", "Bilibili"): "B站",
        ("*", "QQGroup"): "QQ群",
        ("*", "Caimogu"): "踩蘑菇mod论坛",
        ("*", "Ifdian"): "爱发电",


        # __init__.py 完成
        ("*", "Import, edit and export MHW Model (mod3, mrl3, ctc, ccl) files."): "导入, 编辑并导出MHW模型 (mod3, mrl3, ctc, ccl) 文件.",
        ("*", "File handler for MHW MOD3 importing"): "MHW MOD3文件导入处理程序",
        ("*", "File handler for MHW MRL3 importing"): "MHW MRL3文件导入处理程序",
        ("*", "File handler for MHW CTC importing"): "MHW CTC文件导入处理程序",
        ("*", "File handler for MHW CCL importing"): "MHW CCL文件导入处理程序",
        ("*", "File handler for MHW Tex Conversion"): "MHW 贴图转换处理程序",

        ("Operator", "MHW MOD3 (.mod3) (Model)"): "MHW MOD3 (.mod3) (模型)",
        ("Operator", "MHW MRL3 (.mrl3) (Material)"): "MHW MRL3 (.mrl3) (材质)",
        ("Operator", "MHW CTC (.ctc) (Physic)"): "MHW CTC (.ctc) (物理链)",
        ("Operator", "MHW CCL (.ccl) (Collision)"): "MHW CCL (.ccl) (碰撞)",
    }
}

dictionary = preprocess_dictionary(dictionary)

dictionary["zh_TW"] = dictionary["zh_CN"]
dictionary["zh_HANS"] = dictionary["zh_CN"]
dictionary["zh_HANT"] = dictionary["zh_CN"]
