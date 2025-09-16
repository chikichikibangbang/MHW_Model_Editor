import os
import traceback

import bpy
import glob

from ..ddsconv.texconv import Texconv, unload_texconv
from .mrl3_nodes import addImageNode, dynamicColorMixLayerNodeGroup, addTextureNode, \
    addPropertyNode, getPanoramaNodeGroup
from ..tex.tex_function import loadTex
from ...config import __addon_name__
from mathutils import Vector
from ..common.general_function import wildCardFileSearch, raiseWarning, string_reformat
from ..common.blender_utils import showErrorMessageBox

IMPORT_TRANSLUCENT = False#Disabled since it's not quite right yet

def getUsedTextureNodes(propFileList):
    propSet = set()
    path = os.path.split(__file__)[0]
    for file in propFileList:
        f = open(os.path.join(path, file),"r")
        for line in f.readlines():
            if "matInfo[\"textureNodeDict\"][\"" in line:
                propName = line.split("matInfo[\"textureNodeDict\"][\"")[1].split("\"]",1)[0]
                propSet.add(propName)
        f.close()
    return propSet
try:
    usedTextureSet = getUsedTextureNodes(
    propFileList = [
        "blender_mod3_mrl3.py",
        "mrl3_nodes.py",])
except Exception as err:
    print(f"Unable to load usable properties - {str(err)}")
    usedTextureSet = set()


def getChunkPathList():
    ADDON_PREFERENCES = bpy.context.preferences.addons[__addon_name__].preferences
    # print(gameName)
    chunkPathList = [bpy.path.abspath(item.path) for item in ADDON_PREFERENCES.chunkPathList_items]
    # print(chunkPathList)
    return chunkPathList


def addChunkPath(chunkPath):
    ADDON_PREFERENCES = bpy.context.preferences.addons[__addon_name__].preferences
    item = ADDON_PREFERENCES.chunkPathList_items.add()
    item.path = chunkPath
    print(f"Saved chunk path: {chunkPath}")


def findMrl3PathFromMod3Path(mod3Path):
    # TODO fix this to be less of a mess
    # Should use regex to do this
    split = mod3Path.split(".mod3")
    fileRoot = glob.escape(split[0])

    mrl3Path = f"{fileRoot}.mrl3"
    # if not os.path.isfile(mrl3Path):
    #     print(f"Could not find {mrl3Path}.\nTrying alternate mrl3 names...")
    #     # mrl3Path = f"{fileRoot}_Mat.mrl3"
    # if not os.path.isfile(mrl3Path):
    #     print(f"Could not find {mrl3Path}.\n Trying alternate mrl3 names...")
    #     mrl3Path = f"{fileRoot}_v00.mrl3"
    # if not os.path.isfile(mrl3Path):
    #     print(f"Could not find {mrl3Path}.\n Trying alternate mrl3 names...")
    #     mrl3Path = f"{fileRoot}_A.mrl3"
    # if not os.path.isfile(mrl3Path) and fileRoot.endswith("_f"):
    #     mrl3Path = f"{fileRoot[:-1] + 'm'}.mrl3"  # DD2 female armor uses male mdf, so replace _f with _m
    #
    # if not os.path.isfile(mrl3Path) and os.path.split(fileRoot)[1].startswith("SM_"):
    #     split = os.path.split(fileRoot)
    #     mrl3Path = f"{os.path.join(split[0], split[1][1::])}.mrl3"  # DR Stage meshes, SM_ to M_

    if not os.path.isfile(mrl3Path):
        # print(f"Could not find {mrl3Path}.")
        mrl3Path = None

    return mrl3Path



# def getTexPath(baseTexturePath, mrl3Path, chunkPathList):
#     inputPath = None
#     for chunkPath in chunkPathList:
#         search_path = os.path.join(chunkPath, baseTexturePath + ".tex")
#         print(f"searchPath: {search_path}")
#         inputPath = wildCardFileSearch(glob.escape(search_path))
#         print(f"inputPath: {inputPath}")
#         if inputPath == None:
#             if not baseTexturePath.startswith("Assets\default_tex" + os.sep): #防止在mrl3文件同路径下搜索Assets路径下的各种默认贴图
#                 search_path = os.path.join(os.path.dirname(mrl3Path), os.path.basename(baseTexturePath) + ".tex")
#                 # print(search_path)
#                 inputPath = wildCardFileSearch(glob.escape(search_path))
#                 print(f"searchPath: {search_path}")
#                 print(f"inputPath: {inputPath}")
#                 if inputPath != None:
#                     break
#         else:
#             break
#     return inputPath

'''优化后的函数'''
def getTexPath(baseTexturePath, mrl3Path, chunkPath, chunkPathList):
    inputPath = None
    # print(chunkPathList)
    if not baseTexturePath.startswith(os.path.normpath("Assets/default_tex/")): #防止在mrl3文件同路径下搜索Assets路径下的各种默认贴图
        #先在mrl3文件的根目录下寻找tex文件
        search_path = os.path.join(chunkPath, baseTexturePath)
        # print(f"searchPath: {search_path}")
        inputPath = wildCardFileSearch(glob.escape(search_path))
        # print(f"inputPath: {inputPath}")
        if inputPath != None:
            return inputPath

        #如果上一步没找到，再在mrl3文件的同目录下寻找tex文件
        search_path = os.path.join(os.path.dirname(mrl3Path), os.path.basename(baseTexturePath))
        inputPath = wildCardFileSearch(glob.escape(search_path))
        # print(f"searchPath: {search_path}")
        # print(f"inputPath: {inputPath}")
        if inputPath != None:
            return inputPath

        if chunkPathList != []:
            for path in chunkPathList:
                search_path = os.path.join(path, baseTexturePath)
                # print(f"searchPath: {search_path}")
                inputPath = wildCardFileSearch(glob.escape(search_path))
                # print(f"inputPath: {inputPath}")
                if inputPath != None:
                    return inputPath
    else:
        addonPath = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
        search_path = os.path.join(addonPath, "chunk", baseTexturePath)
        # print(f"searchPath: {search_path}")
        inputPath = wildCardFileSearch(glob.escape(search_path))
        # print(f"inputPath: {inputPath}")
        if inputPath != None:
            return inputPath

    return inputPath



# def createImageNode(game_path, nodes, filepath, position, use_loaded_tex=False, use_png_cache=False, overwrite_png_cache=False):
#     node_img = nodes.new(type='ShaderNodeTexImage')
#     node_img.location = Vector(position)
#
#     filepath = filepath.replace("\\", "/")
#     new_filepath = os.path.join(game_path, filepath + ".tex")
#     if not os.path.isfile(new_filepath):
#         logger.warning("Could not load texture, file does not exists (path=" + new_filepath + ")")
#         return node_img
#
#     try:
#         img = load_tex(new_filepath, use_loaded=use_loaded_tex, use_png_cache=use_png_cache,
#                        overwrite_png_cache=overwrite_png_cache)
#     except Exception as e:
#         if "Texture data format not supported" not in str(e):
#             logger.warning(
#                 "Could not load texture, exception during parsing (path=" + new_filepath + ", exception=" + str(
#                     e) + ")")
#         img = None
#     if img is not None:
#         node_img.image = img
#         node_img.extension = "REPEAT"
#
#     return node_img

def importMHWMrl3(mrl3File,mod3MaterialDict,loadUnusedTextures,loadUnusedProps,useBackfaceCulling,reloadCachedTextures,chunkPath,mrl3Path,arrangeNodes = False):
    TEXTURE_CACHE_DIR = bpy.context.preferences.addons[__addon_name__].preferences.textureCachePath
    USE_DDS = bpy.context.preferences.addons[__addon_name__].preferences.useDDS == True and bpy.app.version >= (4, 2, 0)
    # node_groups_blend_file = os.path.join(os.path.dirname(__file__), "mrl3_node_groups.blend")

    inErrorState = False

    loadedImageDict = dict()
    errorFileSet = set()

    mrl3MaterialDict = mrl3File.getMaterialDict()

    # if chunkPath != "":
    # chunkPathList = [chunkPath]
    # chunkPathList.extend(getChunkPathList())
    chunkPathList = getChunkPathList()

    # '''应该考虑路径的大小写问题'''
    # if bpy.context.preferences.addons[__addon_name__].preferences.saveChunkPaths == True:
    #     if ("chunk" in chunkPath or "nativepc" in chunkPath) and not (len(chunkPathList) > 1 and chunkPath in chunkPathList[1::]):
    #         addChunkPath(chunkPath)
    if bpy.context.preferences.addons[__addon_name__].preferences.saveChunkPaths:
        # chunk_path_lower = chunkPath.lower()
        # #检查路径是否包含目标文件夹（不区分大小写）
        # has_chunk_folder = any(folder in chunk_path_lower for folder in CHUNK_FOLDERS)

        #检查是否要添加路径（不在列表中或是第一个）
        # should_add = ("nativepc" not in chunkPath.lower()) and not (len(chunkPathList) > 1 and chunkPath in chunkPathList[1:])
        should_add = ("nativepc" not in chunkPath.lower()) and (chunkPath not in chunkPathList)
        if should_add:
            addChunkPath(chunkPath)

    '''不再使用链接外部文件来导入节点组'''
    # '''导入材质节点组'''
    # por = set()  #改用集合存储，自动去重且查询效率更高
    # node_group_dict = get_node_group_dict() #获取节点组字典
    # installed = [ng.name for ng in bpy.data.node_groups] #获取当前blend文件的节点组名称列表
    #
    # if "WorldShader" not in installed: #如果WorldShader节点组不在当前blend文件的节点组列表中，则将其添加进待导入集合中
    #     por.add("WorldShader")
    # if "VM_geonode" not in installed: #如果VM_geonode节点组不在当前blend文件的节点组列表中，则将其添加进待导入集合中
    #     por.add("VM_geonode")
    #
    # # for matEntry in mrl3MaterialDict.values(): #遍历导入的mrl3文件的每个材质结构
    # for matName in mod3MaterialDict.keys(): #遍历mod3材质字典中的每个材质名
    #     if matName in mrl3MaterialDict: #如果当前mod3材质名存在于mrl3材质字典中，则导入主材质的节点组
    #         matEntry = mrl3MaterialDict[matName]
    #         #提前检查mastermaterialType是否存在，避免嵌套过深
    #         if matEntry.mastermaterialType not in node_group_dict:
    #             continue
    #         #直接遍历目标节点组名称列表
    #         for name in node_group_dict[matEntry.mastermaterialType]: #遍历当前主材质名称对应的外部节点组名称（如PL_post，PL_pre）
    #             if name not in installed: #如果外部节点组名称不在当前blend文件的节点组列表中，则将其添加进待导入集合中
    #                 por.add(name) #集合自动去重
    #
    # if por: #如果待导入集合不为空，则链接外部blend文件，导入节点组
    #     with bpy.data.libraries.load(node_groups_blend_file, link=False) as (data_from, data_to):
    #         data_to.node_groups = list(por)
    #     # 如果Combiner节点组存在于当前导入新节点组之前的当前blend文件的节点组列表中，且Combiner.001节点组存在于导入后的当前blend文件的节点组列表中，则进行遍历去重流程
    #     if "Combiner" in installed and "Combiner.001" in bpy.data.node_groups:
    #         target_combiner = bpy.data.node_groups["Combiner"]
    #         for name in list(por): #遍历新添加的节点组
    #             new_ng = bpy.data.node_groups[name]
    #             for node in new_ng.nodes: #遍历新添加的节点组的表层各个节点
    #                 #如果某节点组内存在Group类型节点组，且其有节点树，且节点树指向Combiner.001节点组，则将该指向强制改为Combiner节点组
    #                 if (node.bl_idname == 'ShaderNodeGroup' and node.node_tree and node.node_tree.name == "Combiner.001"):
    #                     node.node_tree = target_combiner
    #                     # print(name)
    #         bpy.data.node_groups.remove(bpy.data.node_groups["Combiner.001"]) #遍历去重完成后，删除冗余的Combiner.001节点组

    texConv = Texconv()
    chunkPathList = getChunkPathList()
    if chunkPath in chunkPathList:
        chunkPathList.remove(chunkPath)

    for materialName, blenderMaterial in mod3MaterialDict.items():
        # print(materialName)
        # blenderMaterial = mod3MaterialDict[materialName]
        blenderMaterial.use_nodes = True
        blenderMaterial.blend_method = "HASHED"  # Blender 4.2 removed clip and opaque blend options, so everything has to be hash or blend
        if bpy.app.version < (4, 2, 0):
            blenderMaterial.shadow_method = "HASHED"
        blenderMaterial.node_tree.nodes.clear()

        mrl3Material = mrl3MaterialDict.get(materialName, None)
        if mrl3Material == None:
            print("Material \"" + materialName + "\" is not in the mrl3 file, cannot import")
            continue

        textureNodeInfoList = []
        hasAlpha = bool(mrl3Material.alpha_bytes[0] < 255)
        hasVertexColor = False

        if 2 not in mrl3Material.resourceDict:
            continue

        for resourceEntry in mrl3Material.resourceDict[2]:
            # if resourceEntry.resourceType & 0xF != 2:
            #     continue

            textureType = resourceEntry.resourceName
            texture = resourceEntry.resourcePath

            autoDetectedAlbedo = False

            if not loadUnusedTextures and textureType not in usedTextureSet:
                continue

            # imageList = [None]
            # if loadUnusedTextures or textureType in usedTextureSet or autoDetectedAlbedo:

            if texture == "" or texture in errorFileSet:
                # 纹理路径为空或之前加载失败，记录空纹理信息
                textureType = string_reformat(textureType)
                textureNodeInfoList.append((textureType, [None], None))
                continue

            # if texture != "" and (texture not in errorFileSet):
            # baseTexturePath = texture.replace(".tex", "").replace('/', os.sep)
            baseTexturePath = os.path.normpath(texture) + ".tex"
            outputPath = os.path.join(TEXTURE_CACHE_DIR, baseTexturePath.replace(".tex", ".tif"))
            if baseTexturePath in loadedImageDict:
                textureType = string_reformat(textureType)
                textureNodeInfoList.append((textureType, loadedImageDict[baseTexturePath], outputPath))
                continue
            texPath = getTexPath(baseTexturePath, mrl3Path, chunkPath, chunkPathList)
            imageList = [None]
            if texPath != None:
                # if baseTexturePath not in loadedImageDict:
                try:
                    if texPath not in errorFileSet:
                        imageList = loadTex(texPath, outputPath, texConv, reloadCachedTextures, USE_DDS)
                        loadedImageDict[baseTexturePath] = imageList
                    # print(imageList)
                except Exception as err:
                    # imageList = [None]
                    loadedImageDict[baseTexturePath] = imageList
                    errorFileSet.add(texPath)
                    raiseWarning(f"An error occurred while attempting to convert {texPath} - {str(err)}")
                # else:
                #     imageList = loadedImageDict[baseTexturePath]
            else:
                if texture not in errorFileSet:
                    raiseWarning("Could not find texture: " + texture + ", skipping...")
                    errorFileSet.add(texture)
                    # imageList = [None]

            textureType = string_reformat(textureType)
            textureNodeInfoList.append((textureType, imageList, outputPath))

        print(textureNodeInfoList)
        # print(loadedImageDict)

        nodes = blenderMaterial.node_tree.nodes
        links = blenderMaterial.node_tree.links
        nodeTree = blenderMaterial.node_tree

        nodeMaterialOutput = nodes.new('ShaderNodeOutputMaterial')
        nodeMaterialOutput.location = (800, 0)

        nodeBSDF = nodes.new('ShaderNodeBsdfPrincipled')
        nodeBSDF.location = (400, 0)
        links.new(nodeBSDF.outputs[0], nodeMaterialOutput.inputs[0])

        currentYPos = 800
        currentXPos = -1900
        currentPropPos = [-2200, 2000]
        if arrangeNodes:
            currentPropPos = [-3000, 2000]
            currentXPos = -2000

        matInfo = {
            "mmtrName": mrl3Material.mastermaterialType,
            # "flags": mdfMaterial.flags.flagValues,
            "textureNodeDict": {},
            "mPropDict": mrl3Material.getPropertyDict(),
            "currentPropPos": currentPropPos,
            "blenderMaterial": blenderMaterial,
            "albedoNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "normalNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "roughnessNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "metallicNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "emissionColorNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "emissionStrengthNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "cavityNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "aoNodeLayerGroup": dynamicColorMixLayerNodeGroup(nodeTree),
            "alphaSocket": None,
            # "specularSocket": None,
            "translucentSocket": None,
            "subsurfaceSocket": None,

            "filmSocket": None,
            "panoramaSocket": None,
            "waveEmissiveSocket": None,

            "sheenSocket": None,
            "detailColorSocket": None,
            "detailNormalSocket": None,
            "detailRoughnessSocket": None,
            "detailMetallicSocket": None,
            # "isDielectric": False,
            "disableAO": False,
            "disableShadowCast": False,
            # "isMaskAlphaMMTR": os.path.split(mdfMaterial.mmtrPath)[1].lower() in maskAlphaMMTRSet,
            "isAlphaBlend": False,
            # "shaderType": mrl3Material.shaderType,
            "currentShaderOutput": nodeBSDF.outputs["BSDF"],
        }

        UVMap1Node = nodes.new("ShaderNodeUVMap")
        UVMap1Node.name = "UVMap1Node"
        UVMap1Node.location = (-800, 900)
        UVMap1Node.uv_map = "UVMap0"

        UVMap2Node = nodes.new("ShaderNodeUVMap")
        UVMap2Node.name = "UVMap2Node"
        UVMap2Node.location = (-800, 600)
        UVMap2Node.uv_map = "UVMap1"

        # #背面剔除
        # blenderMaterial.use_backface_culling = useBackfaceCulling and not (matInfo["flags"].BaseTwoSideEnable == 1 or matInfo["flags"].TwoSideEnable == 1)

        # if matInfo["shaderType"] in alphaBlendShaderTypes:
        #     matInfo["isAlphaBlend"] = True
        #     if bpy.app.version < (4, 2, 0):
        #         blenderMaterial.shadow_method = "NONE"
        # elif matInfo["mmtrName"] == "env_decal.mmtr":
        #     matInfo["isAlphaBlend"] = True

        for (textureType, imageList, texturePath) in textureNodeInfoList:
            try:
                newNode = addImageNode(nodeTree, textureType, imageList, texturePath, (currentXPos, currentYPos))
                currentYPos += 350
                matInfo["textureNodeDict"][textureType] = newNode

            except Exception as err:
                raiseWarning(f"Failed to create {textureType} node on {materialName}: {str(err)}")

        try:
            for (textureType, _, _) in textureNodeInfoList:
                # Loop through node list again once all image nodes are added

                # if textureType in nodes:
                addTextureNode(nodeTree, textureType, matInfo)
        except Exception as err:
            raiseWarning(
                f"Material Importing Failed ({str(materialName)}). Error During Node Texture Node Assignment.\nIf you're on the latest version of MHW Mod3 Editor, please report this error.")
            traceback.print_exception(type(err), err, err.__traceback__)
            inErrorState = True

        try:
            #Base layer overrides
            # if "fRoughness__uiUNorm" in matInfo["mPropDict"]:
            #     roughnessNode = addPropertyNode(matInfo["mPropDict"]["fRoughness__uiUNorm"], "fRoughness__uiUNorm", matInfo["currentPropPos"], nodeTree)
            #     # matInfo["roughnessNodeLayerGroup"].addMixLayer(roughnessNode.outputs["Value"], factorOutSocket=None, mixType="MULTIPLY", mixFactor=1.0)
            #     multNode = nodes.new("ShaderNodeMath")
            #     multNode.location = matInfo["roughnessNodeLayerGroup"].nodeLoc + Vector((300, 0))
            #     multNode.operation = "MULTIPLY"
            #
            #     links.new(matInfo["roughnessNodeLayerGroup"].currentOutSocket, multNode.inputs[0])
            #     links.new(roughnessNode.outputs["Value"], multNode.inputs[1])

            #DetailNormalMap
            if "DetailNormalMap" in matInfo["textureNodeDict"]:
                detailNormalMapNode = matInfo["textureNodeDict"]["DetailNormalMap"]
                currentPos = [detailNormalMapNode.location[0] + 300, detailNormalMapNode.location[1]]

                # if "MaskMap" in matInfo["textureNodeDict"]:
                #     MaskMapNode = matInfo["textureNodeDict"]["MaskMap"]
                #     MaskMapSeparateNode = nodes.new("ShaderNodeSeparateRGB")
                #     MaskMapSeparateNode.location = (MaskMapNode.location[0] + 300, MaskMapNode.location[1])
                #     links.new(MaskMapNode.outputs["Color"], MaskMapSeparateNode.inputs["Image"])
                # elif "DetailMaskMap" in matInfo["textureNodeDict"]:
                #     MaskMapNode = matInfo["textureNodeDict"]["DetailMaskMap"]
                #     MaskMapSeparateNode = nodes.new("ShaderNodeSeparateRGB")
                #     MaskMapSeparateNode.location = (MaskMapNode.location[0] + 300, MaskMapNode.location[1])
                #     links.new(MaskMapNode.outputs["Color"], MaskMapSeparateNode.inputs["Image"])
                # elif "OcclusionCavityTranslucentDetailMap" in matInfo["textureNodeDict"]:
                #     MaskMapNode = matInfo["textureNodeDict"]["OcclusionCavityTranslucentDetailMap"]
                #     MaskMapSeparateNode = nodes.new("ShaderNodeSeparateRGB")
                #     MaskMapSeparateNode.location = (MaskMapNode.location[0] + 300, MaskMapNode.location[1])
                #     links.new(MaskMapNode.outputs["Alpha"], MaskMapSeparateNode.inputs["Image"])
                # if "DetailMap_Level" in matInfo["mPropDict"] and "ARRAY_DetailMap_SELECTOR" in nodes:
                #     detailMapLevelNode = addPropertyNode(matInfo["mPropDict"]["DetailMap_Level"],
                #                                          matInfo["currentPropPos"], nodeTree)
                #     subtractNode = nodes.new("ShaderNodeMath")
                #     subtractNode.location = currentPos
                #     subtractNode.operation = "SUBTRACT"
                #     links.new(detailMapLevelNode.outputs["Value"], subtractNode.inputs[0])
                #     subtractNode.inputs[1].default_value = 1.0
                #     links.new(subtractNode.outputs["Value"], nodes["ARRAY_DetailMap_SELECTOR"].inputs["Value"])

                detailNormalMappingNode = nodes.new("ShaderNodeMapping")
                # detailNormalMappingNode.location = (detailNormalMapNode.location[0]-300,detailNormalMapNode.location[1])
                detailNormalMappingNode.location = (currentPos[0] - 600, currentPos[1])
                links.new(UVMap1Node.outputs["UV"], detailNormalMappingNode.inputs["Vector"])
                links.new(detailNormalMappingNode.outputs["Vector"], detailNormalMapNode.inputs["Vector"])
                # currentPos[0] += 300

                if "fUVTransformDetailNormal" in matInfo["mPropDict"]:
                    detailNormalUVTransNode = addPropertyNode(matInfo["mPropDict"]["fUVTransformDetailNormal"], "fUVTransformDetailNormal", matInfo["currentPropPos"], nodeTree)
                    locationXYZNode = nodes.new("ShaderNodeCombineXYZ")
                    locationXYZNode.label = "Location"
                    locationXYZNode.location = (detailNormalUVTransNode.location[0] + 300, detailNormalUVTransNode.location[1])
                    links.new(detailNormalUVTransNode.outputs[0], locationXYZNode.inputs["X"])
                    links.new(detailNormalUVTransNode.outputs[1], locationXYZNode.inputs["Y"])
                    links.new(locationXYZNode.outputs["Vector"], detailNormalMappingNode.inputs["Location"])

                    scaleXYZNode = nodes.new("ShaderNodeCombineXYZ")
                    scaleXYZNode.label = "Scale"
                    scaleXYZNode.location = (detailNormalUVTransNode.location[0] + 300, detailNormalUVTransNode.location[1] - 120)
                    links.new(detailNormalUVTransNode.outputs[2], scaleXYZNode.inputs["X"])
                    links.new(detailNormalUVTransNode.outputs[3], scaleXYZNode.inputs["Y"])
                    links.new(scaleXYZNode.outputs["Vector"], detailNormalMappingNode.inputs["Scale"])



                # separateRGBNode = nodes.new("ShaderNodeSeparateRGB")
                # separateRGBNode.location = currentPos
                # currentPos[0] += 300

                # if matInfo["gameName"] not in legacyDetailMapGames:
                #
                #     nodeGroupNode = getBentNormalNodeGroup(nodeTree)
                #     nodeGroupNode.location = currentPos
                #     nodeTree.links.new(separateRGBNode.outputs["G"], nodeGroupNode.inputs["Color"])
                #     nodeTree.links.new(separateRGBNode.outputs["R"], nodeGroupNode.inputs["Alpha"])
                #
                # else:
                #     nodeGroupNode = detailMapNode

                # links.new(detailNormalMapNode.outputs["Color"], separateRGBNode.inputs["Image"])
                # currentPos[0] += 300
                # normalInfluenceNode = nodes.new("ShaderNodeMath")
                # normalInfluenceNode.location = currentPos
                # normalInfluenceNode.operation = "MULTIPLY"
                # normalInfluenceNode.inputs[0].default_value = 1.0
                # currentPos[0] += 300

                invertBlueChannelNode = nodes.new("ShaderNodeRGBCurve")
                invertBlueChannelNode.location = currentPos
                invertBlueChannelNode_B = invertBlueChannelNode.mapping.curves[2]
                invertBlueChannelNode_B.points[0].location = (0.0, 1.0)
                links.new(detailNormalMapNode.outputs["Color"],invertBlueChannelNode.inputs["Color"])
                currentPos[0] += 300

                detailNormalNode = nodes.new("ShaderNodeNormalMap")
                detailNormalNode.location = currentPos

                if "fDetailNormalBlend__uiUNorm" in matInfo["mPropDict"]:
                    detailNormalBlendNode = addPropertyNode(matInfo["mPropDict"]["fDetailNormalBlend__uiUNorm"], "fDetailNormalBlend__uiUNorm", matInfo["currentPropPos"], nodeTree)
                    links.new(detailNormalBlendNode.outputs["Value"], detailNormalNode.inputs["Strength"])
                    currentPos[0] += 300

                # if MaskMapSeparateNode != None:
                #     multiplyNormalBlendNode = nodes.new("ShaderNodeMath")
                #     multiplyNormalBlendNode.location = currentPos
                #     multiplyNormalBlendNode.operation = "MULTIPLY"
                #     links.new(MaskMapSeparateNode.outputs["R"], multiplyNormalBlendNode.inputs[0])
                #     links.new(multiplyNormalBlendNode.outputs["Value"], normalInfluenceNode.inputs[0])
                #     multiplyNormalBlendNode.inputs[1].default_value = 1.0
                #     normalInfluenceNode.inputs[1].default_value = 1.0
                #     if "Detail_NormalBlend" in matInfo["mPropDict"]:
                #         detailNormalBlendNode = addPropertyNode(matInfo["mPropDict"]["Detail_NormalBlend"],
                #                                                 matInfo["currentPropPos"], nodeTree)
                #         links.new(detailNormalBlendNode.outputs["Value"], multiplyNormalBlendNode.inputs[1])
                #     elif "Detail_Normal_Intensity" in matInfo["mPropDict"]:
                #         detailNormalBlendNode = addPropertyNode(matInfo["mPropDict"]["Detail_Normal_Intensity"],
                #                                                 matInfo["currentPropPos"], nodeTree)
                #         links.new(detailNormalBlendNode.outputs["Value"], multiplyNormalBlendNode.inputs[1])
                #     currentPos[0] += 300
                #
                #     if "Detail_RoughnessBlend" in matInfo["mPropDict"]:
                #         currentPos[1] -= 300
                #         detailRoughnessBlendNode = addPropertyNode(matInfo["mPropDict"]["Detail_RoughnessBlend"],
                #                                                    matInfo["currentPropPos"], nodeTree)
                #
                #         multiplyRoughnessBlendNode = nodes.new("ShaderNodeMath")
                #         multiplyRoughnessBlendNode.location = currentPos
                #         multiplyRoughnessBlendNode.operation = "MULTIPLY"
                #         links.new(detailRoughnessBlendNode.outputs["Value"], multiplyRoughnessBlendNode.inputs[0])
                #         links.new(MaskMapSeparateNode.outputs["R"], multiplyRoughnessBlendNode.inputs[1])
                #         currentPos[0] += 300
                #
                #         roughnessDistanceMulitplyNode = nodes.new("ShaderNodeMath")
                #         roughnessDistanceMulitplyNode.location = currentPos
                #         roughnessDistanceMulitplyNode.operation = "MULTIPLY"
                #         links.new(multiplyRoughnessBlendNode.outputs["Value"], roughnessDistanceMulitplyNode.inputs[0])
                #         roughnessDistanceMulitplyNode.inputs[1].default_value = 1.0
                #         currentPos[0] += 300
                #
                #         roughnessCorrectionNode = nodes.new(
                #             "ShaderNodeMath")  # Can't seem to get roughness values to match in game, so an approximation is used here
                #         roughnessCorrectionNode.location = currentPos
                #         roughnessCorrectionNode.operation = "ADD"
                #         roughnessCorrectionNode.use_clamp = True
                #         links.new(detailMapNode.outputs["Alpha"], roughnessCorrectionNode.inputs[0])
                #         roughnessCorrectionNode.inputs[1].default_value = 0.4
                #         currentPos[0] += 300
                #         matInfo["roughnessNodeLayerGroup"].addMixLayer(roughnessCorrectionNode.outputs["Value"],
                #                                                        factorOutSocket=
                #                                                        roughnessDistanceMulitplyNode.outputs["Value"],
                #                                                        mixType="MULTIPLY", mixFactor=1.0)
                #     if "Detail_Cavity" in matInfo["mPropDict"]:
                #         currentPos[1] -= 300
                #         detailCavityNode = addPropertyNode(matInfo["mPropDict"]["Detail_Cavity"],
                #                                            matInfo["currentPropPos"], nodeTree)
                #
                #         multiplyCavityNode = nodes.new("ShaderNodeMath")
                #         multiplyCavityNode.location = currentPos
                #         multiplyCavityNode.operation = "MULTIPLY"
                #         links.new(detailCavityNode.outputs["Value"], multiplyCavityNode.inputs[0])
                #         links.new(MaskMapSeparateNode.outputs["R"], multiplyCavityNode.inputs[1])
                #
                #         currentPos[0] += 300
                #
                #         cavityDistanceMulitplyNode = nodes.new("ShaderNodeMath")
                #         cavityDistanceMulitplyNode.location = currentPos
                #         cavityDistanceMulitplyNode.operation = "MULTIPLY"
                #         links.new(multiplyCavityNode.outputs["Value"], cavityDistanceMulitplyNode.inputs[0])
                #         cavityDistanceMulitplyNode.inputs[1].default_value = 1.0
                #         currentPos[0] += 300
                #
                #         matInfo["cavityNodeLayerGroup"].addMixLayer(MaskMapSeparateNode.outputs["B"],
                #                                                     factorOutSocket=cavityDistanceMulitplyNode.outputs[
                #                                                         "Value"], mixType="MULTIPLY", mixFactor=1.0)

                # links.new(normalInfluenceNode.outputs["Value"], detailNormalNode.inputs["Strength"])
                links.new(invertBlueChannelNode.outputs["Color"], detailNormalNode.inputs["Color"])
                matInfo["detailNormalSocket"] = detailNormalNode.outputs["Normal"]

            if "fBaseMapFactor__uiColor" in matInfo["mPropDict"]:
                baseColorNode = addPropertyNode(matInfo["mPropDict"]["fBaseMapFactor__uiColor"], "fBaseMapFactor__uiColor", matInfo["currentPropPos"], nodeTree)
                matInfo["albedoNodeLayerGroup"].addMixLayer(baseColorNode.outputs["Color"], factorOutSocket=None, mixType="MULTIPLY", mixFactor=1.0)

                if matInfo["alphaSocket"] != None:
                    alphaMultNode = nodes.new("ShaderNodeMath")
                    alphaMultNode.location = baseColorNode.location + Vector((300, 0))
                    alphaMultNode.operation = "MULTIPLY"

                    links.new(matInfo["alphaSocket"], alphaMultNode.inputs[0])
                    links.new(baseColorNode.outputs["Alpha"], alphaMultNode.inputs[1])
                    matInfo["alphaSocket"] = alphaMultNode.outputs["Value"]



            normalNode = None
            if matInfo["normalNodeLayerGroup"].currentOutSocket != None:
                # normalMapNode = matInfo["textureNodeDict"]["NormalMap"]
                # currentPos = [normalMapNode.location[0] + 300, normalMapNode.location[1]]

                invertBlueChannelNode = nodes.new("ShaderNodeRGBCurve")
                invertBlueChannelNode.location = (matInfo["normalNodeLayerGroup"].currentOutSocket.node.location[0] + 300,
                                       matInfo["normalNodeLayerGroup"].currentOutSocket.node.location[1])
                invertBlueChannelNode_B = invertBlueChannelNode.mapping.curves[2]
                invertBlueChannelNode_B.points[0].location = (0.0, 1.0)
                links.new(matInfo["normalNodeLayerGroup"].currentOutSocket, invertBlueChannelNode.inputs["Color"])

                normalNode = nodes.new("ShaderNodeNormalMap")
                normalNode.location = (matInfo["normalNodeLayerGroup"].currentOutSocket.node.location[0] + 600,
                                       matInfo["normalNodeLayerGroup"].currentOutSocket.node.location[1])
                normalNode.inputs["Strength"].default_value = 2.0
                links.new(invertBlueChannelNode.outputs["Color"], normalNode.inputs["Color"])

                if matInfo["detailNormalSocket"] == None:
                    links.new(normalNode.outputs["Normal"], nodeBSDF.inputs["Normal"])
                else:
                    detailNormalNodeLoc = matInfo["detailNormalSocket"].node.location
                    mixNormalNode = nodeTree.nodes.new("ShaderNodeVectorMath")
                    mixNormalNode.location = (detailNormalNodeLoc[0] + 300, detailNormalNodeLoc[1])
                    mixNormalNode.operation = "ADD"
                    links.new(matInfo["detailNormalSocket"], mixNormalNode.inputs[0])
                    links.new(normalNode.outputs["Normal"], mixNormalNode.inputs[1])

                    normalizeNormalNode = nodeTree.nodes.new("ShaderNodeVectorMath")
                    normalizeNormalNode.location = (detailNormalNodeLoc[0] + 600, detailNormalNodeLoc[1])
                    normalizeNormalNode.operation = "NORMALIZE"
                    links.new(mixNormalNode.outputs["Vector"], normalizeNormalNode.inputs["Vector"])
                    links.new(normalizeNormalNode.outputs["Vector"], nodeBSDF.inputs["Normal"])
                    #转换法向空间
                    # if "textureCoordinateNode" in nodeTree.nodes:
                    #     textureCoordinateNode = nodeTree.nodes["textureCoordinateNode"]
                    # else:
                    #     textureCoordinateNode = nodeTree.nodes.new("ShaderNodeTexCoord")
                    #     textureCoordinateNode.name = "textureCoordinateNode"
                    #     textureCoordinateNode.location = (-800, 400)
                    # crossProductNode = nodeTree.nodes.new("ShaderNodeVectorMath")
                    # crossProductNode.location = (detailNormalNodeLoc[0] + 300, detailNormalNodeLoc[1] + 300)
                    # crossProductNode.operation = "CROSS_PRODUCT"
                    # links.new(matInfo["detailNormalSocket"], crossProductNode.inputs[0])
                    # links.new(textureCoordinateNode.outputs["Normal"], crossProductNode.inputs[1])
                    #
                    # dotProductNode = nodeTree.nodes.new("ShaderNodeVectorMath")
                    # dotProductNode.location = (detailNormalNodeLoc[0] + 300, detailNormalNodeLoc[1])
                    # dotProductNode.operation = "DOT_PRODUCT"
                    # links.new(matInfo["detailNormalSocket"], dotProductNode.inputs[0])
                    # links.new(textureCoordinateNode.outputs["Normal"], dotProductNode.inputs[1])
                    #
                    # arcCosineNode = nodeTree.nodes.new("ShaderNodeMath")
                    # arcCosineNode.location = (detailNormalNodeLoc[0] + 600, detailNormalNodeLoc[1])
                    # arcCosineNode.operation = "ARCCOSINE"
                    # links.new(dotProductNode.outputs["Value"], arcCosineNode.inputs[0])
                    #
                    # normalVectorRotateNode = nodeTree.nodes.new("ShaderNodeVectorRotate")
                    # normalVectorRotateNode.location = (detailNormalNodeLoc[0] + 900, detailNormalNodeLoc[1])
                    #
                    # links.new(normalNode.outputs["Normal"], normalVectorRotateNode.inputs["Vector"])
                    # links.new(crossProductNode.outputs["Vector"], normalVectorRotateNode.inputs["Axis"])
                    # links.new(arcCosineNode.outputs["Value"], normalVectorRotateNode.inputs["Angle"])
                    #
                    # links.new(normalVectorRotateNode.outputs["Vector"], nodeBSDF.inputs["Normal"])

            if "PanoramaMap" in matInfo["textureNodeDict"]:
                node = matInfo["textureNodeDict"]["PanoramaMap"]
                nodeGroupNode = getPanoramaNodeGroup(nodeTree)
                nodeGroupNode.location = node.location + Vector((-300, 0))
                links.new(nodeGroupNode.outputs["PanoramaVector"], node.inputs["Vector"])

                if "fPanoramaTile" in matInfo["mPropDict"]:
                    panoramaTileNode = addPropertyNode(matInfo["mPropDict"]["fPanoramaTile"], "fPanoramaTile", matInfo["currentPropPos"], nodeTree)
                    links.new(panoramaTileNode.outputs["Value"], nodeGroupNode.inputs["PanoramaTile"])

                multNode = None
                if matInfo["panoramaSocket"] != None:
                    multNode = nodes.new("ShaderNodeMath")
                    multNode.location = matInfo["panoramaSocket"].node.location + Vector((300, 0))
                    multNode.operation = "MULTIPLY"
                    multNode.inputs[0].default_value = 0.0
                    multNode.inputs[1].default_value = 0.0
                    links.new(matInfo["panoramaSocket"], multNode.inputs[0])

                    if "fRefractBlend__uiUNorm" in matInfo["mPropDict"]:
                        refractBlendNode = addPropertyNode(matInfo["mPropDict"]["fRefractBlend__uiUNorm"],
                                                           "fRefractBlend__uiUNorm", matInfo["currentPropPos"], nodeTree)
                        links.new(refractBlendNode.outputs["Value"], multNode.inputs[1])

                if multNode != None:
                    matInfo["albedoNodeLayerGroup"].addMixLayer(node.outputs["Color"], multNode.outputs["Value"], mixType="MULTIPLY", mixFactor=0.0)
                else:
                    matInfo["albedoNodeLayerGroup"].addMixLayer(node.outputs["Color"], mixType="MULTIPLY", mixFactor=0.0)

            if matInfo["albedoNodeLayerGroup"].currentOutSocket != None:
                links.new(matInfo["albedoNodeLayerGroup"].currentOutSocket, nodeBSDF.inputs["Base Color"])

            #粗糙度
            if matInfo["roughnessNodeLayerGroup"].currentOutSocket != None:
                clampNode = nodes.new("ShaderNodeClamp")
                clampNode.location = (matInfo["roughnessNodeLayerGroup"].currentOutSocket.node.location[0] + 600,
                                      matInfo["roughnessNodeLayerGroup"].currentOutSocket.node.location[1])
                links.new(matInfo["roughnessNodeLayerGroup"].currentOutSocket, clampNode.inputs["Value"])
                links.new(clampNode.outputs["Result"], nodeBSDF.inputs["Roughness"])

                if "fRoughness__uiUNorm" in matInfo["mPropDict"]:
                    roughnessNode = addPropertyNode(matInfo["mPropDict"]["fRoughness__uiUNorm"],
                                                    "fRoughness__uiUNorm", matInfo["currentPropPos"], nodeTree)
                    multNode = nodes.new("ShaderNodeMath")
                    multNode.location = matInfo["roughnessNodeLayerGroup"].nodeLoc + Vector((300, 0))
                    multNode.operation = "MULTIPLY"

                    links.new(matInfo["roughnessNodeLayerGroup"].currentOutSocket, multNode.inputs[0])
                    links.new(roughnessNode.outputs["Value"], multNode.inputs[1])
                    links.new(multNode.outputs["Value"], clampNode.inputs["Value"])
                else:
                    links.new(matInfo["roughnessNodeLayerGroup"].currentOutSocket, clampNode.inputs["Value"])

            #金属度
            if matInfo["metallicNodeLayerGroup"].currentOutSocket != None:
                clampNode = nodes.new("ShaderNodeClamp")
                clampNode.location = (matInfo["metallicNodeLayerGroup"].currentOutSocket.node.location[0] + 600,
                                      matInfo["metallicNodeLayerGroup"].currentOutSocket.node.location[1] - 150)

                links.new(clampNode.outputs["Result"], nodeBSDF.inputs["Metallic"])

                if "fMetalic__uiUNorm" in matInfo["mPropDict"]:
                    metallicNode = addPropertyNode(matInfo["mPropDict"]["fMetalic__uiUNorm"], "fMetalic__uiUNorm", matInfo["currentPropPos"], nodeTree)

                    multNode = nodes.new("ShaderNodeMath")
                    multNode.location = matInfo["metallicNodeLayerGroup"].nodeLoc + Vector((300, -150))
                    multNode.operation = "MULTIPLY"

                    links.new(matInfo["metallicNodeLayerGroup"].currentOutSocket, multNode.inputs[0])
                    links.new(metallicNode.outputs["Value"], multNode.inputs[1])
                    links.new(multNode.outputs["Value"], clampNode.inputs["Value"])
                else:
                    links.new(matInfo["metallicNodeLayerGroup"].currentOutSocket, clampNode.inputs["Value"])

            #高光
            if "fSpecular__uiUNorm" in matInfo["mPropDict"]:
                specularNode = addPropertyNode(matInfo["mPropDict"]["fSpecular__uiUNorm"], "fSpecular__uiUNorm", matInfo["currentPropPos"], nodeTree)
                #高光为1.0的话感觉反射太明显了，这里乘以0.5来进行缩放
                multNode = nodeTree.nodes.new('ShaderNodeMath')
                multNode.location = [specularNode.location[0] + 300, specularNode.location[1]]
                multNode.operation = "MULTIPLY"
                multNode.inputs[1].default_value = 0.5
                links.new(specularNode.outputs["Value"], multNode.inputs[0])

                clampNode = nodes.new("ShaderNodeClamp")
                clampNode.location = (specularNode.location[0] + 600, specularNode.location[1])
                clampNode.inputs["Max"].default_value = 0.5
                links.new(multNode.outputs["Value"], clampNode.inputs["Value"])
                links.new(clampNode.outputs["Result"], nodeBSDF.inputs["Specular"])

            if matInfo["emissionColorNodeLayerGroup"].currentOutSocket != None:
                if "bBaseColorEmissive" in matInfo["mPropDict"]:
                    baseColorEMINode = addPropertyNode(matInfo["mPropDict"]["bBaseColorEmissive"], "bBaseColorEmissive", matInfo["currentPropPos"], nodeTree)
                    if matInfo["albedoNodeLayerGroup"].currentOutSocket != None:
                        matInfo["emissionColorNodeLayerGroup"].addMixLayer(matInfo["albedoNodeLayerGroup"].currentOutSocket, baseColorEMINode.outputs["Value"], mixType="MULTIPLY", mixFactor=1.0)

                if bpy.app.version < (4, 0, 0):
                    links.new(matInfo["emissionColorNodeLayerGroup"].currentOutSocket, nodeBSDF.inputs["Emission"])
                else:  # I swear Blender changes things just to break addon compatibility
                    # I had to dig through the source code just to find the actual name of this socket since it's not listed anywhere and Blender only gives you it's index :/
                    links.new(matInfo["emissionColorNodeLayerGroup"].currentOutSocket, nodeBSDF.inputs["Emission Color"])

            if matInfo["emissionStrengthNodeLayerGroup"].currentOutSocket != None:
                emissionClampNode = nodes.new("ShaderNodeClamp")  # Prevent negative emission values
                emissionClampNode.location = (matInfo["emissionStrengthNodeLayerGroup"].nodeLoc[0] + 300, matInfo["emissionStrengthNodeLayerGroup"].nodeLoc[1])
                emissionClampNode.inputs["Max"].default_value = 9999
                links.new(matInfo["emissionStrengthNodeLayerGroup"].currentOutSocket, emissionClampNode.inputs["Value"])
                links.new(emissionClampNode.outputs["Result"], nodeBSDF.inputs["Emission Strength"])

            alphaClippingNode = None
            if matInfo["alphaSocket"] != None:
                links.new(matInfo["alphaSocket"], nodeBSDF.inputs["Alpha"])

            # if arrangeNodes:
            #     # TODO Force blender to update node dimensions so that a large margin doesn't need to be used as a workaround
            #     arrangeNodeTree(nodeTree, margin_x=300, margin_y=300, centerNodes=True)

        except Exception as err:
            raiseWarning(f"Material Importing Failed ({str(materialName)}). Error During Node Detection. \nIf you're on the latest version of MHW Mod3 Editor, please report this error.")
            traceback.print_exception(type(err), err, err.__traceback__)
            inErrorState = True


        # general_frame_x = -1650.0
        # general_frame_y = 500.0
        # property_frame_x = -1400.0
        # property_frame_y = 500.0
        # texture_frame_x = -1000.0
        # texture_frame_y = 500.0
        #
        # general_frame = nodes.new(type='NodeFrame')
        # general_frame.label = "General"
        # # property_frame = nodes.new(type='NodeFrame')
        # # property_frame.label = "Properties"
        # texture_frame = nodes.new(type='NodeFrame')
        # texture_frame.label = "Maps"
        # texture_frame.label_size = 12
        #
        # mhw_shader_node = nodes.new(type='ShaderNodeGroup')
        # mhw_shader_node.location = Vector((-500.0, 500.0))
        # mhw_shader_node.node_tree = bpy.data.node_groups["WorldShader"]
        # mhw_shader_node.label = "WorldShader"
        #
        # material_output = nodes.new("ShaderNodeOutputMaterial")
        # material_output.name = "Material Output"
        # material_output.location = (300.0, 300.0)
        #
        # links.new(mhw_shader_node.outputs[0], material_output.inputs[0])
        # links.new(mhw_shader_node.outputs[1], material_output.inputs[2])
        #
        # if "damage" in materialName:
        #     mhw_shader_node.inputs["Damage"].default_value = 1.0
        #     blenderMaterial.cycles.displacement_method = "BOTH"
        #
        # node_UVMap0 = nodes.new(type='ShaderNodeUVMap')
        # node_UVMap0.location = Vector((general_frame_x, general_frame_y - 0.0))
        # node_UVMap0.uv_map = "UVMap0"
        # node_UVMap0.parent = general_frame
        # node_UVMap1 = nodes.new(type='ShaderNodeUVMap')
        # node_UVMap1.location = Vector((general_frame_x, general_frame_y - 100.0))
        # node_UVMap1.uv_map = "UVMap1"
        # node_UVMap1.parent = general_frame
        # node_UVMap2 = nodes.new(type='ShaderNodeUVMap')
        # node_UVMap2.location = Vector((general_frame_x, general_frame_y - 200.0))
        # node_UVMap2.uv_map = "UVMap2"
        # node_UVMap2.parent = general_frame
        # node_UVMap3 = nodes.new(type='ShaderNodeUVMap')
        # node_UVMap3.location = Vector((general_frame_x, general_frame_y - 300.0))
        # node_UVMap3.uv_map = "UVMap4"
        # node_UVMap3.parent = general_frame
        # node_VertexColor = nodes.new(type='ShaderNodeVertexColor')
        # node_VertexColor.location = Vector((general_frame_x, general_frame_y - 400.0))
        # node_VertexColor.layer_name = "Color"
        # node_VertexColor.parent = general_frame
        # node_geometry = nodes.new(type='ShaderNodeNewGeometry')
        # node_geometry.location = Vector((general_frame_x, general_frame_y - 500.0))
        # node_geometry.parent = general_frame
        # node_object_info = nodes.new(type='ShaderNodeObjectInfo')
        # node_object_info.location = Vector((general_frame_x, general_frame_y - 700.0))
        # node_object_info.parent = general_frame
        #
        # if mrl3Material.mastermaterialType not in node_group_dict:
        #     continue
        #
        # ng_name_list = node_group_dict[mrl3Material.mastermaterialType]
        # mmtr_post = nodes.new(type='ShaderNodeGroup')
        # mmtr_post.location = Vector((-700.0, 500.0))
        # mmtr_post.node_tree = bpy.data.node_groups[ng_name_list[0]]
        # mmtr_post.label = mrl3Material.mastermaterialType
        #
        # mmtr_pre = nodes.new(type='ShaderNodeGroup')
        # mmtr_pre.location = Vector((-1200.0, 500.0))
        # mmtr_pre.node_tree = bpy.data.node_groups[ng_name_list[1]]
        # mmtr_pre.label = mrl3Material.mastermaterialType
        #
        # for (mapNodeName, textureType, imageList, texturePath) in textureNodeInfoList:
        #     try:
        #         newNode = addImageNode(blenderMaterial.node_tree, mapNodeName, textureType, imageList, texturePath,
        #                                (texture_frame_x, texture_frame_y))
        #         texture_frame_y -= 300.0
        #         newNode.parent = texture_frame
        # #         # print(newNode)
        # #         matInfo["textureNodeDict"][textureType] = newNode
        #
        #         try:
        #             if newNode.image: #暂时不支持CubeMap和ArrayMap
        #                 links.new(mmtr_pre.outputs["vector_" + mapNodeName], newNode.inputs["Vector"])
        #                 links.new(newNode.outputs["Color"], mmtr_post.inputs[mapNodeName + "_RGB"])
        #                 links.new(newNode.outputs["Alpha"], mmtr_post.inputs[mapNodeName + "_A"])
        #         except:
        #             pass
        #
        #     except Exception as err:
        #         raiseWarning(f"Failed to create {mapNodeName} node on {materialName}: {str(err)}")
        #
        # #导入property
        # for resourceEntry in mrl3Material.resourceDict[0]:
        # #     if resourceEntry.resourceType & 0xF != 0:
        # #         continue
        #
        #     propBlockType = resourceEntry.resourceName
        #     propDict = resourceEntry.propertyDict
        #
        #     propBlockName = string_reformat(propBlockType)
        #     property_frame = nodes.new(type='NodeFrame')
        #     property_frame.label = propBlockName
        #
        #     for propType, propValue in propDict.items():
        #         try:
        #             if propType.startswith("align"):
        #                 continue
        #             if propType.endswith("uiColor"):
        #                 node_RGB = nodes.new(type='ShaderNodeRGB')
        #                 node_RGB.location = Vector((property_frame_x, property_frame_y))
        #                 property_frame_y -= 150.0
        #                 node_RGB.parent = property_frame
        #                 node_floatvalue = nodes.new(type='ShaderNodeValue')
        #                 node_floatvalue.location = Vector((property_frame_x, property_frame_y))
        #                 property_frame_y -= 100.0
        #                 node_floatvalue.parent = property_frame
        #                 if len(propValue[1]) == 3:
        #                     node_RGB.outputs["Color"].default_value = Vector(propValue[1] + [1.0])
        #                     node_floatvalue.outputs["Value"].default_value = 1.0
        #                 else:
        #                     node_RGB.outputs["Color"].default_value = Vector(propValue[1])
        #                     node_floatvalue.outputs["Value"].default_value = propValue[1][3]
        #
        #
        #                 node_RGB.label = string_reformat(propType) + "_RGB"
        #                 node_floatvalue.label = string_reformat(propType) + "_A"
        #
        #
        #                 links.new(node_RGB.outputs["Color"], mmtr_pre.inputs[node_RGB.label])
        #                 links.new(node_RGB.outputs["Color"], mmtr_post.inputs[node_RGB.label])
        #                 links.new(node_floatvalue.outputs["Value"], mmtr_pre.inputs[node_floatvalue.label])
        #                 links.new(node_floatvalue.outputs["Value"], mmtr_post.inputs[node_floatvalue.label])
        #
        #             else:
        #                 if propValue[0] not in {'int', 'uint', 'byte', 'ubyte', 'float', 'bbool'}:
        #                     for property_i, property_value in enumerate(propValue[1]):
        #                         node_floatvalue = nodes.new(type='ShaderNodeValue')
        #                         node_floatvalue.location = Vector((property_frame_x, property_frame_y))
        #                         property_frame_y -= 20.0
        #
        #                         node_floatvalue.label = string_reformat(propType) + "_" + str(property_i)
        #
        #                         node_floatvalue.parent = property_frame
        #                         node_floatvalue.outputs["Value"].default_value = float(property_value)
        #                         links.new(node_floatvalue.outputs["Value"], mmtr_pre.inputs[node_floatvalue.label])
        #                         links.new(node_floatvalue.outputs["Value"], mmtr_post.inputs[node_floatvalue.label])
        #                 else:
        #                     node_floatvalue = nodes.new(type='ShaderNodeValue')
        #                     node_floatvalue.location = Vector((property_frame_x, property_frame_y))
        #                     property_frame_y -= 20.0
        #
        #                     node_floatvalue.label = string_reformat(propType)
        #
        #                     node_floatvalue.parent = property_frame
        #                     node_floatvalue.outputs["Value"].default_value = float(propValue[1])
        #                     links.new(node_floatvalue.outputs["Value"], mmtr_pre.inputs[node_floatvalue.label])
        #                     links.new(node_floatvalue.outputs["Value"], mmtr_post.inputs[node_floatvalue.label])
        #                 property_frame_y -= 80.0
        #
        #         except Exception as err:
        #             raiseWarning(f"Failed to connect prop {propType}: {str(err)}")
        #
        # links.new(node_UVMap0.outputs["UV"], mmtr_pre.inputs["TexCoord1"])
        # links.new(node_UVMap1.outputs["UV"], mmtr_pre.inputs["TexCoord2"])
        # links.new(node_UVMap2.outputs["UV"], mmtr_pre.inputs["TexCoord3"])
        # links.new(node_UVMap3.outputs["UV"], mmtr_pre.inputs["TexCoord4"])
        # links.new(node_VertexColor.outputs["Color"], mmtr_pre.inputs["VertexColor"])
        # links.new(node_VertexColor.outputs["Color"], mmtr_post.inputs["VertexColor"])
        #
        # for mmtr_output_key in mmtr_post.outputs.keys():
        #     try:
        #         if mmtr_output_key in ["Emission", "Emission Strength"]:
        #             has_emissive = True
        #             if has_emissive:
        #                 links.new(mmtr_post.outputs[mmtr_output_key], mhw_shader_node.inputs[mmtr_output_key])
        #         else:
        #             links.new(mmtr_post.outputs[mmtr_output_key], mhw_shader_node.inputs[mmtr_output_key])
        #     except:
        #         pass
        #
        # for mmtr_output_key in mmtr_post.outputs.keys():
        #     try:
        #         links.new(mmtr_post.outputs[mmtr_output_key], material_output.inputs[mmtr_output_key])
        #     except:
        #         pass


        # matInfo = {
        #     "mmtrName": os.path.split(mrl3Material.mmtrPath.lower())[1],
        #     "flags": mrl3Material.flags.flagValues,
        #     "textureNodeDict": {},
        #     "mPropDict": mrl3Material.getPropertyDict(),
        #     "currentPropPos": currentPropPos,
        #     "blenderMaterial": blenderMaterial,
        #     "albedoNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "normalNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "roughnessNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "metallicNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "emissionColorNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "emissionStrengthNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "cavityNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "aoNodeLayerGroup": dynamicColorMixLayerNodeGroup(blenderMaterial.node_tree),
        #     "alphaSocket": None,
        #     "translucentSocket": None,
        #     "subsurfaceSocket": None,
        #     "sheenSocket": None,
        #     "detailColorSocket": None,
        #     "detailNormalSocket": None,
        #     "detailRoughnessSocket": None,
        #     "detailMetallicSocket": None,
        #     "isDielectric": False,
        #     "isNRRT": False,
        #     "disableAO": False,
        #     "disableShadowCast": False,
        #     "isMaskAlphaMMTR": os.path.split(mdfMaterial.mmtrPath)[1].lower() in maskAlphaMMTRSet,
        #     "isAlphaBlend": False,
        #     "shaderType": mdfMaterial.shaderType,
        #     "currentShaderOutput": nodeBSDF.outputs["BSDF"],
        #     "gameName": gameName,
        # }












    errorFileSet.clear()
    loadedImageDict.clear()
    unload_texconv()
    if inErrorState:
        showErrorMessageBox(
            "An error occurred while loading materials. See the Window > Toggle System Console for details.")
    else:
        print("Finished loading materials.")
