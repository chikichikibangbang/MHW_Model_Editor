import math
import bpy

from ..common.general_function import string_reformat

# color_space_dict = {
#     "AlbedoMap": "sRGB",
#     "NormalMap": "Non-Color",
#     "RMTMap": "Non-Color",
#     "EmissiveMap": "sRGB", #不确定
#     "ColorMaskMap": "Non-Color",
#     "FxMap": "Non-Color",
#     "PanoramaMap": "sRGB", #不确定
#     "AddNormalMap": "Non-Color",
#     "AddNormalMaskMap": "Non-Color",
#     "PaintKzMap": "Non-Color",
#     "PaintPbMap": "Non-Color",
#     "SnowMap": "Non-Color",
#     "FurMap": "Non-Color",
#     "FurVelocityMap": "Non-Color",
#     "AlbedoBlendMap": "Non-Color", #不确定
#     "DisplacementMap": "Non-Color",
#     "FacePaintMap": "Non-Color",
#     "MaskMap": "Non-Color", #不确定
#     "PatternMap": "sRGB",
#     "VoltexMap": "Non-Color",
#     "SphereMap": "sRGB",
#     "PartsMaskMap": "Non-Color", #不确定
#     "VertexPositionMap": "Non-Color",
#     "VertexNormalMap": "Non-Color",
#     "VertexTangentMap": "Non-Color",
#     "AlbedoOverMap": "sRGB", #不确定
#     "DetailMapA": "sRGB", #不确定
#     "DetailMapB": "sRGB", #不确定
#     "DetailMapC": "sRGB", #不确定
#     "DetailMapD": "sRGB", #不确定
#     "DetailEmissiveMap": "sRGB", #不确定
#     "DetailNormalMap": "Non-Color",
#     "NormalBlendMap": "Non-Color",
#     "RMTBlendMap": "Non-Color",
#     "NormalHeightMap": "Non-Color",
#     "CubeMap": "sRGB",
#     "TranslucencyMap": "Non-Color",
#     "SkinMap": "sRGB",
#     "FaceNormalMap": "Non-Color",
#     "FaceMayuMap": "Non-Color", #不确定
#     "ArrayMap": "Non-Color", #不确定
#     "AlbedoBlendMapR": "sRGB",
#     "NormalBlendMapR": "Non-Color",
#     "RMTBlendMapR": "Non-Color",
#     "EmissiveMapR": "sRGB", #不确定
#     "AlbedoBlendMapG": "sRGB",
#     "NormalBlendMapG": "Non-Color",
#     "RMTBlendMapG": "Non-Color",
#     "EmissiveMapG": "sRGB", #不确定
#     "AlbedoBlendMapB": "sRGB",
#     "NormalBlendMapB": "Non-Color",
#     "RMTBlendMapB": "Non-Color",
#     "EmissiveMapB": "sRGB", #不确定
#     "HeightMap": "Non-Color",
#     "VertexColorMap": "Non-Color",
#     "DetailNormalBlendMap": "Non-Color",
#     "EmissiveBlendMap": "sRGB", #不确定
#     "MaterialBlendMap": "Non-Color",
#     "FurNormalMap": "Non-Color",
#     "FurMaskMap": "Non-Color",
#     "SnowAlbedoMap": "sRGB", #不确定
#     "SnowNormalBlendMap": "Non-Color",
#     "SnowDetailNormalBlendMap": "Non-Color",
#     "SnowRMTBlendMap": "Non-Color",
#     "SnowEmissiveBlendMap": "sRGB", #不确定
#     "SnowMaterialBlendMap": "Non-Color",
#     "FlowMap": "Non-Color",
#     "AlphaMap": "Non-Color",
#     "FurBlendMap": "Non-Color",
#     "FurNormalBlendMap": "Non-Color",
#     "AlbedoUniqueMap": "Non-Color",
#     "AlbedoExtendMap": "Non-Color", #不确定
#     "RefractionMaskMap": "Non-Color",
#     "OpacityMap": "Non-Color",
#     "SplashMap": "Non-Color", #不确定
#     "OpacityBlendMap": "Non-Color",
# }

# default_tex_dict = {
#     "AlbedoMap": "Assets\\default_tex\\null_white",
#     "NormalMap": "Assets\\default_tex\\null_NM",
#     "RMTMap": "Assets\\default_tex\\null_RMT",
#     "EmissiveMap": "Assets\\default_tex\\null_black",
#     "ColorMaskMap": "Assets\\default_tex\\null_black",
#     "FxMap": "Assets\\default_tex\\null_black",
#     "PanoramaMap": "Assets\\default_tex\\null_gray_LIN",
#     "AddNormalMap": "Assets\\default_tex\\null_NM",
#     "AddNormalMaskMap": "Assets\\default_tex\\null_black",
#     "PaintKzMap": "Assets\\default_tex\\kizu_CMM",
#     "PaintPbMap": "Assets\\default_tex\\paint_CMM",
#     "SnowMap": "Assets\\default_tex\\snow_Col_CMM",
#     "FurMap": "Assets\\default_tex\\noise_LIN",
#     "FurVelocityMap": "Assets\\default_tex\\null_black",
#     "AlbedoBlendMap": "Assets\\default_tex\\null_black",
#     "DisplacementMap": "Assets\\default_tex\\null_black",
#     "FacePaintMap": "Assets\\default_tex\\null_NM",
#     "MaskMap": "Assets\\default_tex\\null_black",
#     "PatternMap": "Assets\\default_tex\\null_black",
#     "VoltexMap": "Assets\\default_tex\\turbulance_000_CMM",
#     "SphereMap": "Assets\\default_tex\\fake_env_BML",
#     "PartsMaskMap": "Assets\\default_tex\\null_black",
#     "VertexPositionMap": "Assets\\default_tex\\null_black",
#     "VertexNormalMap": "Assets\\default_tex\\null_black",
#     "VertexTangentMap": "Assets\\default_tex\\null_black",
#     "AlbedoOverMap": "Assets\\default_tex\\null_gray_LIN",
#     "DetailMapA": "Assets\\default_tex\\null_black",
#     "DetailMapB": "Assets\\default_tex\\null_black",
#     "DetailMapC": "Assets\\default_tex\\null_black",
#     "DetailMapD": "Assets\\default_tex\\null_black",
#     "DetailEmissiveMap": "Assets\\default_tex\\null_black",
#     "DetailNormalMap": "Assets\\default_tex\\null_NM",
#     "NormalBlendMap": "Assets\\default_tex\\null_NM",
#     "RMTBlendMap": "Assets\\default_tex\\null_RMT",
#     "NormalHeightMap": "Assets\\default_tex\\ice_FR_A_CMM",
#     # "CubeMap": "Assets\\default_tex\\CM\\arborium[1]_CM-00",
#     "TranslucencyMap": "Assets\\default_tex\\null_white",
#     "SkinMap": "Assets\\default_tex\\skin_BM",
#     "FaceNormalMap": "Assets\\default_tex\\null_NM",
#     "FaceMayuMap": "Assets\\default_tex\\null_black",
#     # "ArrayMap": "",
#     "AlbedoBlendMapR": "Assets\\default_tex\\null_gray_BM",
#     "NormalBlendMapR": "Assets\\default_tex\\null_NM",
#     "RMTBlendMapR": "Assets\\default_tex\\null_RMT",
#     "EmissiveMapR": "Assets\\default_tex\\null_black",
#     "AlbedoBlendMapG": "Assets\\default_tex\\null_gray_BM",
#     "NormalBlendMapG": "Assets\\default_tex\\null_NM",
#     "RMTBlendMapG": "Assets\\default_tex\\null_RMT",
#     "EmissiveMapG": "Assets\\default_tex\\null_black",
#     "AlbedoBlendMapB": "Assets\\default_tex\\null_gray_BM",
#     "NormalBlendMapB": "Assets\\default_tex\\null_NM",
#     "RMTBlendMapB": "Assets\\default_tex\\null_RMT",
#     "EmissiveMapB": "Assets\\default_tex\\null_black",
#     "HeightMap": "Assets\\default_tex\\null_gray_MM",
#     "VertexColorMap": "Assets\\default_tex\\null_CMML",
#     "DetailNormalBlendMap": "Assets\\default_tex\\null_NM",
#     "EmissiveBlendMap": "Assets\\default_tex\\null_black",
#     "MaterialBlendMap": "Assets\\default_tex\\null_black",
#     "FurNormalMap": "Assets\\default_tex\\null_NM",
#     "FurMaskMap": "Assets\\default_tex\\null_black",
#     "SnowAlbedoMap": "Assets\\default_tex\\null_white",
#     "SnowNormalBlendMap": "Assets\\default_tex\\null_NM",
#     "SnowDetailNormalBlendMap": "Assets\\default_tex\\null_NM",
#     "SnowRMTBlendMap": "Assets\\default_tex\\null_RMT",
#     "SnowEmissiveBlendMap": "Assets\\default_tex\\null_black",
#     "SnowMaterialBlendMap": "Assets\\default_tex\\null_white",
#     "FlowMap": "Assets\\default_tex\\null_NM",
#     "AlphaMap": "Assets\\default_tex\\null_white",
#     "FurBlendMap": "Assets\\default_tex\\noise_LIN",
#     "FurNormalBlendMap": "Assets\\default_tex\\sand_CMML",
#     "AlbedoUniqueMap": "Assets\\default_tex\\null_black",
#     "AlbedoExtendMap": "Assets\\default_tex\\null_black",
#     "RefractionMaskMap": "Assets\\default_tex\\null_white",
#     "OpacityMap": "Assets\\default_tex\\null_white",
#     "SplashMap": "Assets\\default_tex\\null_white",
#     "OpacityBlendMap": "Assets\\default_tex\\null_black",
# }

default_color_dict = {
    "AlbedoMap": ("sRGB", (1.0, 1.0, 1.0, 1.0)),
    "NormalMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "RMTMap": ("Non-Color", (1.0, 0.0, 1.0, 1.0)),
    "EmissiveMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "ColorMaskMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "FxMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "PanoramaMap": ("Non-Color", (0.502, 0.502, 0.502, 1.0)),
    "AddNormalMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "AddNormalMaskMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "PaintKzMap": ("Non-Color", (0.502, 0.502, 1.0, 1.0)),
    "PaintPbMap": ("Non-Color", (0.502, 0.502, 1.0, 1.0)),
    "SnowMap": ("Non-Color", (0.502, 0.502, 1.0, 1.0)),
    "FurMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "FurVelocityMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "AlbedoBlendMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "DisplacementMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "FacePaintMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "MaskMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "PatternMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "VoltexMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "SphereMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "PartsMaskMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "VertexPositionMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "VertexNormalMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "VertexTangentMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "AlbedoOverMap": ("Non-Color", (0.502, 0.502, 0.502, 1.0)),
    "DetailMapA": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "DetailMapB": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "DetailMapC": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "DetailMapD": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "DetailEmissiveMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "DetailNormalMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "NormalBlendMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "RMTBlendMap": ("Non-Color", (1.0, 0.0, 1.0, 1.0)),
    "NormalHeightMap": ("Non-Color", (0.502, 0.502, 1.0, 1.0)),
    # "CubeMap": "Assets\\default_tex\\CM\\arborium[1]_CM-00",
    "TranslucencyMap": ("sRGB", (1.0, 1.0, 1.0, 1.0)),
    "SkinMap": ("sRGB", (0.741, 0.573, 0.518, 1.0)),
    "FaceNormalMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "FaceMayuMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    # "ArrayMap": "",
    "AlbedoBlendMapR": ("sRGB", (0.502, 0.502, 0.502, 1.0)),
    "NormalBlendMapR": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "RMTBlendMapR": ("Non-Color", (1.0, 0.0, 1.0, 1.0)),
    "EmissiveMapR": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "AlbedoBlendMapG": ("sRGB", (0.502, 0.502, 0.502, 1.0)),
    "NormalBlendMapG": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "RMTBlendMapG": ("Non-Color", (1.0, 0.0, 1.0, 1.0)),
    "EmissiveMapG": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "AlbedoBlendMapB": ("sRGB", (0.502, 0.502, 0.502, 1.0)),
    "NormalBlendMapB": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "RMTBlendMapB": ("Non-Color", (1.0, 0.0, 1.0, 1.0)),
    "EmissiveMapB": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "HeightMap": ("Non-Color", (0.502, 0.502, 0.502, 1.0)),
    "VertexColorMap": ("Non-Color", (0.502, 0.502, 0.502, 1.0)),
    "DetailNormalBlendMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "EmissiveBlendMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "MaterialBlendMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "FurNormalMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "FurMaskMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "SnowAlbedoMap": ("sRGB", (1.0, 1.0, 1.0, 1.0)),
    "SnowNormalBlendMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "SnowDetailNormalBlendMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "SnowRMTBlendMap": ("Non-Color", (1.0, 0.0, 1.0, 1.0)),
    "SnowEmissiveBlendMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "SnowMaterialBlendMap": ("Non-Color", (1.0, 1.0, 1.0, 1.0)),
    "FlowMap": ("Non-Color", (0.502, 0.502, 0.0, 1.0)),
    "AlphaMap": ("sRGB", (1.0, 1.0, 1.0, 1.0)),
    "FurBlendMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
    "FurNormalBlendMap": ("Non-Color", (0.502, 0.502, 1.0, 1.0)),
    "AlbedoUniqueMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "AlbedoExtendMap": ("sRGB", (0.0, 0.0, 0.0, 1.0)),
    "RefractionMaskMap": ("Non-Color", (1.0, 1.0, 1.0, 1.0)),
    "OpacityMap": ("Non-Color", (1.0, 1.0, 1.0, 1.0)),
    "SplashMap": ("Non-Color", (1.0, 1.0, 1.0, 1.0)),
    "OpacityBlendMap": ("Non-Color", (0.0, 0.0, 0.0, 1.0)),
}


def getColorNodeGroup(nodeTree):  # No RGBA node in shader editor so a custom group is needed
    if "ColorNodeGroup" in bpy.data.node_groups:
        nodeGroup = bpy.data.node_groups["ColorNodeGroup"]
    else:
        nodeGroup = bpy.data.node_groups.new(type="ShaderNodeTree", name="ColorNodeGroup")

        if bpy.app.version < (4, 0, 0):
            nodeGroup.inputs.new("NodeSocketColor", "Color")
            nodeGroup.inputs.new("NodeSocketFloat", "Alpha")
        else:
            nodeGroup.interface.new_socket(name="Color", description="", in_out="INPUT", socket_type="NodeSocketColor")
            nodeGroup.interface.new_socket(name="Alpha", description="", in_out="INPUT", socket_type="NodeSocketFloat")

        inNode = nodeGroup.nodes.new('NodeGroupInput')

        outNode = nodeGroup.nodes.new('NodeGroupOutput')
        if bpy.app.version < (4, 0, 0):
            nodeGroup.outputs.new('NodeSocketColor', 'Color')
            nodeGroup.outputs.new('NodeSocketFloat', 'Alpha')
        else:
            nodeGroup.interface.new_socket(name="Color", description="", in_out="OUTPUT", socket_type="NodeSocketColor")
            nodeGroup.interface.new_socket(name="Alpha", description="", in_out="OUTPUT", socket_type="NodeSocketFloat")
        nodeGroup.links.new(inNode.outputs["Color"], outNode.inputs["Color"])
        nodeGroup.links.new(inNode.outputs["Alpha"], outNode.inputs["Alpha"])

    nodeGroupNode = nodeTree.nodes.new("ShaderNodeGroup")
    nodeGroupNode.node_tree = nodeGroup

    return nodeGroupNode


def getVec4NodeGroup(nodeTree):
    if "Vec4NodeGroup" in bpy.data.node_groups:
        nodeGroup = bpy.data.node_groups["Vec4NodeGroup"]
    else:
        nodeGroup = bpy.data.node_groups.new(type="ShaderNodeTree", name="Vec4NodeGroup")

        if bpy.app.version < (4, 0, 0):
            nodeGroup.inputs.new("NodeSocketFloat", "X")
            nodeGroup.inputs.new("NodeSocketFloat", "Y")
            nodeGroup.inputs.new("NodeSocketFloat", "Z")
            nodeGroup.inputs.new("NodeSocketFloat", "W")
        else:
            nodeGroup.interface.new_socket(name="X", description="", in_out="INPUT", socket_type="NodeSocketFloat")
            nodeGroup.interface.new_socket(name="Y", description="", in_out="INPUT", socket_type="NodeSocketFloat")
            nodeGroup.interface.new_socket(name="Z", description="", in_out="INPUT", socket_type="NodeSocketFloat")
            nodeGroup.interface.new_socket(name="W", description="", in_out="INPUT", socket_type="NodeSocketFloat")
        inNode = nodeGroup.nodes.new('NodeGroupInput')

        outNode = nodeGroup.nodes.new('NodeGroupOutput')
        if bpy.app.version < (4, 0, 0):
            nodeGroup.outputs.new('NodeSocketFloat', "X")
            nodeGroup.outputs.new('NodeSocketFloat', "Y")
            nodeGroup.outputs.new('NodeSocketFloat', "Z")
            nodeGroup.outputs.new('NodeSocketFloat', "W")
        else:
            nodeGroup.interface.new_socket(name="X", description="", in_out="OUTPUT", socket_type="NodeSocketFloat")
            nodeGroup.interface.new_socket(name="Y", description="", in_out="OUTPUT", socket_type="NodeSocketFloat")
            nodeGroup.interface.new_socket(name="Z", description="", in_out="OUTPUT", socket_type="NodeSocketFloat")
            nodeGroup.interface.new_socket(name="W", description="", in_out="OUTPUT", socket_type="NodeSocketFloat")

        nodeGroup.links.new(inNode.outputs["X"], outNode.inputs["X"])
        nodeGroup.links.new(inNode.outputs["Y"], outNode.inputs["Y"])
        nodeGroup.links.new(inNode.outputs["Z"], outNode.inputs["Z"])
        nodeGroup.links.new(inNode.outputs["W"], outNode.inputs["W"])

    nodeGroupNode = nodeTree.nodes.new("ShaderNodeGroup")
    nodeGroupNode.node_tree = nodeGroup

    return nodeGroupNode

def getPanoramaNodeGroup(nodeTree):
    if "PanoramaNodeGroup" in bpy.data.node_groups:
        nodeGroup = bpy.data.node_groups["PanoramaNodeGroup"]
    else:
        nodeGroup = bpy.data.node_groups.new(type="ShaderNodeTree", name="PanoramaNodeGroup")
        nodes = nodeGroup.nodes
        links = nodeGroup.links
        if bpy.app.version < (4, 0, 0):
            nodeGroup.inputs.new("NodeSocketFloat", "PanoramaTile")
        else:
            nodeGroup.interface.new_socket(name="PanoramaTile", description="", in_out="INPUT",
                                           socket_type="NodeSocketFloat")

        inNode = nodeGroup.nodes.new('NodeGroupInput')
        currentLoc = [300, 0]

        geometryNode = nodes.new("ShaderNodeNewGeometry")
        geometryNode.location = currentLoc
        currentLoc[0] += 300

        vectorMathNode_01 = nodes.new("ShaderNodeVectorMath")
        vectorMathNode_01.location = currentLoc
        currentLoc[0] += 300
        vectorMathNode_01.operation = 'MULTIPLY'
        vectorMathNode_01.inputs[1].default_value = (1.0, -1.0, -1.0)
        links.new(geometryNode.outputs["Incoming"], vectorMathNode_01.inputs[0])

        separateXYZNode = nodes.new("ShaderNodeSeparateXYZ")
        separateXYZNode.location = currentLoc
        currentLoc[0] += 300
        links.new(vectorMathNode_01.outputs["Vector"], separateXYZNode.inputs["Vector"])

        arctan2Node = nodes.new("ShaderNodeMath")
        arctan2Node.location = currentLoc
        arctan2Node.operation = "ARCTAN2"
        links.new(separateXYZNode.outputs["X"], arctan2Node.inputs[1])
        links.new(separateXYZNode.outputs["Y"], arctan2Node.inputs[0])

        arcsineNode = nodes.new("ShaderNodeMath")
        arcsineNode.location = (currentLoc[0], currentLoc[1] - 300)
        currentLoc[0] += 300
        arcsineNode.operation = "ARCSINE"
        links.new(separateXYZNode.outputs["Z"], arcsineNode.inputs[0])

        divideNode_01 = nodes.new("ShaderNodeMath")
        divideNode_01.location = currentLoc
        divideNode_01.operation = "DIVIDE"
        links.new(arctan2Node.outputs["Value"], divideNode_01.inputs[0])
        divideNode_01.inputs[1].default_value = 2 * math.pi

        divideNode_02 = nodes.new("ShaderNodeMath")
        divideNode_02.location = (currentLoc[0], currentLoc[1] - 300)
        currentLoc[0] += 300
        divideNode_02.operation = "DIVIDE"
        links.new(arcsineNode.outputs["Value"], divideNode_02.inputs[0])
        divideNode_02.inputs[1].default_value = math.pi

        addNode_01 = nodes.new("ShaderNodeMath")
        addNode_01.location = currentLoc
        addNode_01.operation = "ADD"
        links.new(divideNode_01.outputs["Value"], addNode_01.inputs[0])
        addNode_01.inputs[1].default_value = 0.5

        addNode_02 = nodes.new("ShaderNodeMath")
        addNode_02.location = (currentLoc[0], currentLoc[1] - 300)
        currentLoc[0] += 300
        addNode_02.operation = "ADD"
        links.new(divideNode_02.outputs["Value"], addNode_02.inputs[0])
        addNode_02.inputs[1].default_value = 0.5

        combineXYZNode = nodes.new("ShaderNodeCombineXYZ")
        combineXYZNode.location = currentLoc
        currentLoc[0] += 300
        links.new(addNode_01.outputs["Value"], combineXYZNode.inputs["X"])
        links.new(addNode_02.outputs["Value"], combineXYZNode.inputs["Y"])

        vectorMathNode_02 = nodes.new("ShaderNodeVectorMath")
        vectorMathNode_02.location = currentLoc
        currentLoc[0] += 300
        vectorMathNode_02.operation = 'SCALE'
        links.new(combineXYZNode.outputs["Vector"], vectorMathNode_02.inputs["Vector"])
        links.new(inNode.outputs["PanoramaTile"], vectorMathNode_02.inputs["Scale"])

        vectorMathNode_03 = nodes.new("ShaderNodeVectorMath")
        vectorMathNode_03.location = currentLoc
        currentLoc[0] += 300
        vectorMathNode_03.operation = 'ADD'
        links.new(vectorMathNode_02.outputs["Vector"], vectorMathNode_03.inputs[0])

        outNode = nodeGroup.nodes.new('NodeGroupOutput')
        outNode.location = currentLoc
        if bpy.app.version < (4, 0, 0):
            nodeGroup.outputs.new('NodeSocketVector', "PanoramaVector")
        else:
            nodeGroup.interface.new_socket(name="PanoramaVector", description="", in_out="OUTPUT", socket_type="NodeSocketVector")
        links.new(vectorMathNode_03.outputs["Vector"], outNode.inputs["PanoramaVector"])

    nodeGroupNode = nodeTree.nodes.new("ShaderNodeGroup")
    nodeGroupNode.node_tree = nodeGroup

    return nodeGroupNode

def addPropertyNode(propValue, propName, currentPos, node_tree):
    propNodeName = string_reformat(propName)
    if propNodeName in node_tree.nodes:
        propNode = node_tree.nodes[propNodeName]
    else:
        if propName.endswith("__uiColor"):
            # RGBA Color
            nodeGroup = getColorNodeGroup(node_tree)
            if propValue[0] == "float[3]":
                nodeGroup.inputs["Color"].default_value = propValue[1] + [1.0]
                nodeGroup.inputs["Alpha"].default_value = 1.0
            else:
                nodeGroup.inputs["Color"].default_value = propValue[1]
                nodeGroup.inputs["Alpha"].default_value = propValue[1][3]
            propNode = nodeGroup
        elif propValue[0] == "float[2]":
            # Vec2
            nodeGroup = getVec4NodeGroup(node_tree)
            nodeGroup.inputs[0].default_value = propValue[1][0]
            nodeGroup.inputs[1].default_value = propValue[1][1]
            nodeGroup.inputs[2].default_value = 0.0
            nodeGroup.inputs[3].default_value = 0.0
            propNode = nodeGroup
        elif propValue[0] == "float[3]":
            # Vec3
            nodeGroup = getVec4NodeGroup(node_tree)
            nodeGroup.inputs[0].default_value = propValue[1][0]
            nodeGroup.inputs[1].default_value = propValue[1][1]
            nodeGroup.inputs[2].default_value = propValue[1][2]
            nodeGroup.inputs[3].default_value = 0.0
            propNode = nodeGroup
        elif propValue[0] == "float[4]":
            # Vec4
            nodeGroup = getVec4NodeGroup(node_tree)
            nodeGroup.inputs[0].default_value = propValue[1][0]
            nodeGroup.inputs[1].default_value = propValue[1][1]
            nodeGroup.inputs[2].default_value = propValue[1][2]
            nodeGroup.inputs[3].default_value = propValue[1][3]
            propNode = nodeGroup
        else:
            propNode = node_tree.nodes.new("ShaderNodeValue")
            propNode.outputs["Value"].default_value = float(propValue[1])

        propNode.name = propNodeName
        propNode.label = propNodeName
        propNode.location = currentPos
        currentPos[1] -= int(propNode.height * 2.5)
    return propNode


class dynamicColorMixLayerNodeGroup():
    def __init__(self, nodeTree):
        self._currentOutSocket = None
        self.nodeLoc = (0, 0)
        self.node_tree = nodeTree

    @property
    def currentOutSocket(self):
        return self._currentOutSocket

    @currentOutSocket.setter
    def currentOutSocket(self, value):
        self._currentOutSocket = value
        if value != None:
            self.nodeLoc = value.node.location

    def addMixLayer(self, colorOutSocket, factorOutSocket=None, mixType="MIX", mixFactor=0.5, swapInputs=False):

        if self.currentOutSocket == None:  # For the first layer added, just store the out socket since it's not being mixed with anything
            self.currentOutSocket = colorOutSocket
        else:
            mixNode = self.node_tree.nodes.new('ShaderNodeMixRGB')
            mixNode.location = (self.nodeLoc[0] + (self.currentOutSocket.node.width + 100), self.nodeLoc[1])
            mixNode.blend_type = mixType
            mixNode.inputs["Fac"].default_value = mixFactor

            if swapInputs:
                self.node_tree.links.new(self.currentOutSocket, mixNode.inputs["Color2"])
                self.node_tree.links.new(colorOutSocket, mixNode.inputs["Color1"])
            else:
                self.node_tree.links.new(self.currentOutSocket, mixNode.inputs["Color1"])
                self.node_tree.links.new(colorOutSocket, mixNode.inputs["Color2"])
            if factorOutSocket != None:
                self.node_tree.links.new(factorOutSocket, mixNode.inputs["Fac"])
            self.currentOutSocket = mixNode.outputs["Color"]


def addImageNode(nodeTree, textureType, imageList, texturePath, currentPos):
    imageNode = None
    if len(imageList) == 1:

        imageNode = nodeTree.nodes.new('ShaderNodeTexImage')
        imageNode.name = textureType
        imageNode.label = textureType
        imageNode.location = currentPos

        if imageList[0] != None:
            imageNode.image = imageList[0]
            # print(f"image node {textureType} path:{imageList[0].filepath}")

        #创建1x1默认图像
        else:
            if f"Missing {textureType}" in bpy.data.images:
                imageNode.image = bpy.data.images[f"Missing {textureType}"]
            else:
                if textureType in default_color_dict:
                    imageNode.image = bpy.data.images.new(
                        name=f"Missing {textureType}",
                        width=1,
                        height=1,
                    )
                    imageNode.image.colorspace_settings.name, imageNode.image.generated_color = default_color_dict[textureType]
                    imageNode.image.update()
                else:
                    pass #CubeMap和ArrayMap
                # print(f"Created \"Missing {textureType}\" texture.")

            #不再考虑直接读取Assets\default_tex\路径下的tex文件来创建默认图像
            # imageName = os.path.basename(texturePath)
            # if imageName in bpy.data.images:
            #     imageNode.image = bpy.data.images[imageName]
            # else:
            #     if mapNodeName in default_tex_dict:
            #
            #         baseTexturePath = os.path.normpath(default_tex_dict[mapNodeName] + ".tex")
            #         addonPath = os.path.dirname(os.path.split(os.path.abspath(__file__))[0])
            #         defaultTexPath = os.path.join(addonPath, baseTexturePath)
            #         outputPath = os.path.join(TEXTURE_CACHE_DIR, default_tex_dict[mapNodeName] + os.path.splitext(texturePath)[1])
            #         imageList = loadTex(defaultTexPath, outputPath, texConv, reloadCachedTextures, USE_DDS)
            #         imageNode.image = imageList[0]
        if imageNode.image:
            imageNode.image.alpha_mode = "CHANNEL_PACKED"

        '''不再在此处设置颜色空间'''
        # colorSpace = color_space_dict[mapNodeName] if mapNodeName in color_space_dict else "Non-Color"
        # imageNode.image.colorspace_settings.name = colorSpace

    return imageNode


def newAlbedoMapNode(nodeTree, textureType, matInfo):
    imageNode = nodeTree.nodes[textureType]
    currentPos = [imageNode.location[0] + 300, imageNode.location[1]]

    matInfo["albedoNodeLayerGroup"].addMixLayer(imageNode.outputs["Color"])
    matInfo["alphaSocket"] = imageNode.outputs["Alpha"]

    return imageNode

def newNormalMapNode(nodeTree, textureType, matInfo):
    imageNode = nodeTree.nodes[textureType]
    currentPos = [imageNode.location[0] + 300, imageNode.location[1]]

    matInfo["normalNodeLayerGroup"].addMixLayer(imageNode.outputs["Color"])
    return imageNode


def newRMTMapNode(nodeTree, textureType, matInfo):
    imageNode = nodeTree.nodes[textureType]
    currentPos = [imageNode.location[0] + 300, imageNode.location[1]]

    separateNode = nodeTree.nodes.new('ShaderNodeSeparateRGB')
    separateNode.location = currentPos

    matInfo["roughnessNodeLayerGroup"].addMixLayer(separateNode.outputs["R"])
    matInfo["metallicNodeLayerGroup"].addMixLayer(separateNode.outputs["G"])
    matInfo["translucentSocket"] = separateNode.outputs["B"]

    currentPos[0] += 300
    nodeTree.links.new(imageNode.outputs["Color"], separateNode.inputs["Image"])
    return imageNode

def newColorMaskMapNode (nodeTree,textureType,matInfo):
    imageNode = nodeTree.nodes[textureType]
    currentPos = [imageNode.location[0]+300,imageNode.location[1]]

    mixNode = None
    if "bUseCMM" in matInfo["mPropDict"]:
        useCMMNode = addPropertyNode(matInfo["mPropDict"]["bUseCMM"], "bUseCMM", matInfo["currentPropPos"], nodeTree)

        mixNode = nodeTree.nodes.new("ShaderNodeMixRGB")
        mixNode.location = currentPos
        mixNode.blend_type = "MULTIPLY"
        mixNode.inputs["Fac"].default_value = 1.0
        nodeTree.links.new(imageNode.outputs["Color"], mixNode.inputs[1])
        nodeTree.links.new(useCMMNode.outputs["Value"], mixNode.inputs[2])
        currentPos[0] += 300

    if "CMMSepNode" in nodeTree.nodes:
        CMMSeparateNode = nodeTree.nodes["CMMSepNode"]
    else:
        CMMSeparateNode = nodeTree.nodes.new('ShaderNodeSeparateRGB')
        CMMSeparateNode.location = currentPos
        CMMSeparateNode.name = "CMMSepNode"

    #这里之后再看看，优化一下逻辑
    if "bUseCMM" in matInfo["mPropDict"]:
        nodeTree.links.new(mixNode.outputs["Color"], CMMSeparateNode.inputs["Image"])
    else:
        nodeTree.links.new(imageNode.outputs["Color"], CMMSeparateNode.inputs["Image"])
    # nodeTree.links.new(imageNode.outputs["Color"], CMMSeparateNode.inputs["Image"])

    #调试用
    RColorNode = addPropertyNode(["float[4]",[1.0,1.0,1.0,1.0]], "S_col_R__uiColor", matInfo["currentPropPos"], nodeTree)
    GColorNode = addPropertyNode(["float[4]",[1.0,1.0,1.0,1.0]], "S_col_G__uiColor", matInfo["currentPropPos"], nodeTree)
    if matInfo["albedoNodeLayerGroup"] != None:
        matInfo["albedoNodeLayerGroup"].addMixLayer(RColorNode.outputs["Color"], CMMSeparateNode.outputs["R"],
                                                    mixType="MULTIPLY")
        matInfo["albedoNodeLayerGroup"].addMixLayer(GColorNode.outputs["Color"], CMMSeparateNode.outputs["G"],
                                                    mixType="MULTIPLY")

    return imageNode


EMISSION_MULTIPLIER = 0.1  # Multiply strength by this value,way too bright by default
def newEmissiveMapNode(nodeTree, textureType, matInfo):
    imageNode = nodeTree.nodes[textureType]
    currentPos = [imageNode.location[0] + 300, imageNode.location[1]]

    matInfo["emissionColorNodeLayerGroup"].addMixLayer(imageNode.outputs["Color"])

    # if "bBaseColorEmissive" in matInfo["mPropDict"]:
    #     baseColorEMINode = addPropertyNode(matInfo["mPropDict"]["bBaseColorEmissive"], "bBaseColorEmissive", matInfo["currentPropPos"], nodeTree)
    #     matInfo["emissionColorNodeLayerGroup"].addMixLayer(baseColorEMINode.outputs["Value"], mixType="MULTIPLY", mixFactor=1.0)

    if "fEmissiveMapFactor__uiColor" in matInfo["mPropDict"]:
        emiColorNode = addPropertyNode(matInfo["mPropDict"]["fEmissiveMapFactor__uiColor"], "fEmissiveMapFactor__uiColor", matInfo["currentPropPos"], nodeTree)
        matInfo["emissionColorNodeLayerGroup"].addMixLayer(emiColorNode.outputs["Color"], mixType="MULTIPLY", mixFactor=1.0)

    # elif "Emissive_Color" in matInfo["mPropDict"]:
    #     emiColorNode = addPropertyNode(matInfo["mPropDict"]["Emissive_Color"], matInfo["currentPropPos"], nodeTree)
    #     matInfo["emissionColorNodeLayerGroup"].addMixLayer(emiColorNode.outputs["Color"], mixType="MULTIPLY",
    #                                                        mixFactor=1.0)
    # elif "EmissiveColor" in matInfo["mPropDict"]:
    #     emiColorNode = addPropertyNode(matInfo["mPropDict"]["EmissiveColor"], matInfo["currentPropPos"], nodeTree)
    #     matInfo["emissionColorNodeLayerGroup"].addMixLayer(emiColorNode.outputs["Color"], mixType="MULTIPLY",
    #                                                        mixFactor=1.0)

    if "fAnimEmitMin" in matInfo["mPropDict"]:
        animEmitMinNode = addPropertyNode(matInfo["mPropDict"]["fAnimEmitMin"], "fAnimEmitMin", matInfo["currentPropPos"], nodeTree)

        reduceEMIMultNode = nodeTree.nodes.new('ShaderNodeMath')
        reduceEMIMultNode.location = [animEmitMinNode.location[0] + 300, animEmitMinNode.location[1]]
        reduceEMIMultNode.operation = "MULTIPLY"
        nodeTree.links.new(animEmitMinNode.outputs["Value"], reduceEMIMultNode.inputs[0])
        reduceEMIMultNode.inputs[1].default_value = EMISSION_MULTIPLIER

        matInfo["emissionStrengthNodeLayerGroup"].currentOutSocket = reduceEMIMultNode.outputs["Value"]
    # emiIntensityNode = None
    # if "Emissive_intensity" in matInfo["mPropDict"]:
    #     emiIntensityNode = addPropertyNode(matInfo["mPropDict"]["Emissive_intensity"], matInfo["currentPropPos"],
    #                                        nodeTree)
    # elif "Emissive_Intensity" in matInfo["mPropDict"]:  # I should have lower cased the prop dict
    #     emiIntensityNode = addPropertyNode(matInfo["mPropDict"]["Emissive_Intensity"], matInfo["currentPropPos"],
    #                                        nodeTree)
    # elif "EmissiveIntensity" in matInfo["mPropDict"]:  # I should have lower cased the prop dict
    #     emiIntensityNode = addPropertyNode(matInfo["mPropDict"]["EmissiveIntensity"], matInfo["currentPropPos"],
    #                                        nodeTree)
    # elif "Emissive_Power" in matInfo["mPropDict"]:
    #     emiIntensityNode = addPropertyNode(matInfo["mPropDict"]["Emissive_Power"], matInfo["currentPropPos"], nodeTree)
    # if emiIntensityNode != None:
    #     bwNode = nodeTree.nodes.new('ShaderNodeRGBToBW')
    #     bwNode.location = currentPos
    #     bwNode.name = "BWEMINode"
    #
    #     currentPos[0] += 300
    #
    #     reduceEMIMultNode = nodeTree.nodes.new('ShaderNodeMath')
    #     reduceEMIMultNode.location = currentPos
    #     reduceEMIMultNode.operation = "MULTIPLY"
    #     nodeTree.links.new(emiIntensityNode.outputs["Value"], reduceEMIMultNode.inputs[0])
    #     reduceEMIMultNode.inputs[1].default_value = EMISSION_MULTIPLIER
    #
    #     currentPos[0] += 300
    #     nodeTree.links.new(imageNode.outputs["Color"], bwNode.inputs[0])
    #
    #     baseEMIMultNode = nodeTree.nodes.new('ShaderNodeMath')
    #     baseEMIMultNode.location = currentPos
    #     baseEMIMultNode.operation = "MULTIPLY"
    #     nodeTree.links.new(bwNode.outputs[0], baseEMIMultNode.inputs[0])
    #     nodeTree.links.new(reduceEMIMultNode.outputs["Value"], baseEMIMultNode.inputs[1])
    #
    #     matInfo["emissionStrengthNodeLayerGroup"].addMixLayer(baseEMIMultNode.outputs["Value"], mixType="MULTIPLY",
    #                                                           mixFactor=1.0)

    # if "S_col_R" in matInfo["mPropDict"] and "S_col_G" in matInfo["mPropDict"] and "S_col_R_Emissive_intensity" in \
    #         matInfo["mPropDict"] and "S_col_G_Emissive_intensity" in matInfo["mPropDict"]:
    #     RColorNode = addPropertyNode(matInfo["mPropDict"]["S_col_R"], matInfo["currentPropPos"], nodeTree)
    #     GColorNode = addPropertyNode(matInfo["mPropDict"]["S_col_G"], matInfo["currentPropPos"], nodeTree)
    #
    #     RColorEmiIntensityNode = addPropertyNode(matInfo["mPropDict"]["S_col_R_Emissive_intensity"],
    #                                              matInfo["currentPropPos"], nodeTree)
    #     GColorEmiIntensityNode = addPropertyNode(matInfo["mPropDict"]["S_col_G_Emissive_intensity"],
    #                                              matInfo["currentPropPos"], nodeTree)
    #
    #     if "CMMSepNode" in nodeTree.nodes:
    #         CMMSeparateNode = nodeTree.nodes["CMMSepNode"]
    #     else:
    #         CMMSeparateNode = nodeTree.nodes.new('ShaderNodeSeparateRGB')
    #         CMMSeparateNode.location = currentPos
    #         CMMSeparateNode.name = "CMMSepNode"
    #
    #     RMultNode = nodeTree.nodes.new("ShaderNodeMath")
    #     RMultNode.operation = "MULTIPLY"
    #
    #     nodeTree.links.new(RColorEmiIntensityNode.outputs["Value"], RMultNode.inputs[0])
    #     nodeTree.links.new(CMMSeparateNode.outputs["R"], RMultNode.inputs[1])
    #
    #     GMultNode = nodeTree.nodes.new("ShaderNodeMath")
    #     GMultNode.operation = "MULTIPLY"
    #
    #     StrengthAddNode = nodeTree.nodes.new("ShaderNodeMath")
    #     StrengthAddNode.operation = "ADD"
    #
    #     nodeTree.links.new(RMultNode.outputs["Value"], StrengthAddNode.inputs[0])
    #     nodeTree.links.new(GMultNode.outputs["Value"], StrengthAddNode.inputs[1])
    #
    #     matInfo["emissionStrengthNodeLayerGroup"].addMixLayer(StrengthAddNode.outputs["Value"], factorOutSocket=None,
    #                                                           mixType="ADD", mixFactor=1.0)
    #
    #     nodeTree.links.new(GColorEmiIntensityNode.outputs["Value"], GMultNode.inputs[0])
    #     nodeTree.links.new(CMMSeparateNode.outputs["G"], GMultNode.inputs[1])
    #
    #     matInfo["emissionColorNodeLayerGroup"].addMixLayer(RColorNode.outputs["Color"],
    #                                                        factorOutSocket=CMMSeparateNode.outputs["R"], mixType="ADD")
    #     matInfo["emissionColorNodeLayerGroup"].addMixLayer(GColorNode.outputs["Color"],
    #                                                        factorOutSocket=CMMSeparateNode.outputs["G"], mixType="ADD")

    return imageNode



def newFxMapNode(nodeTree, textureType, matInfo):
    imageNode = nodeTree.nodes[textureType]
    currentPos = [imageNode.location[0] + 300, imageNode.location[1]]

    separateNode = nodeTree.nodes.new('ShaderNodeSeparateRGB')
    separateNode.location = currentPos
    matInfo["filmSocket"] = separateNode.outputs["R"]
    matInfo["panoramaSocket"] = separateNode.outputs["G"]
    matInfo["waveEmissiveSocket"] = separateNode.outputs["B"]

    currentPos[0] += 300
    nodeTree.links.new(imageNode.outputs["Color"], separateNode.inputs["Image"])
    return imageNode


nodeDict = {
    "AlbedoMap": newAlbedoMapNode,
    "NormalMap": newNormalMapNode,
    "RMTMap": newRMTMapNode,
    "ColorMaskMap": newColorMaskMapNode,
    "EmissiveMap": newEmissiveMapNode,
    "FxMap": newFxMapNode,
}
def addTextureNode(nodeTree, textureType, matInfo):
    # print(nodeType)
    # print(textureType)
    # print(texturePath)
    if textureType in nodeDict:
        return nodeDict[textureType](nodeTree, textureType, matInfo)
    else:
        return None
