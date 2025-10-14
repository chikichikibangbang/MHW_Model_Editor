#Author: NSA Cloud
import bpy

def getChainMat():
    mat = bpy.data.materials.get("CTCChainMat")
    if mat == None:
        mat = bpy.data.materials.new("CTCChainMat")
        mat.use_nodes = True
        mat.diffuse_color = bpy.context.scene.mhw_ctc_toolpanel.chainColor
        mat.node_tree.nodes[0].inputs["Base Color"].default_value = bpy.context.scene.mhw_ctc_toolpanel.chainColor
        mat.node_tree.nodes[0].inputs["Alpha"].default_value = bpy.context.scene.mhw_ctc_toolpanel.chainColor[3]
        mat.blend_method = "BLEND"
        if bpy.app.version < (4, 2, 0):
            mat.shadow_method = "NONE"
    return mat

def getConeMat():
    # 获取指定名称的材质
    mat = bpy.data.materials.get("CTCConeMat")
    # 若未获取到指定名称的材质，则新建材质
    if mat == None:
        mat = bpy.data.materials.new("CTCConeMat")
        # 使用该节点
        mat.use_nodes = True
        mat.diffuse_color = bpy.context.scene.mhw_ctc_toolpanel.coneColor
        # 设置原理化着色器的基础色和透明度为插件面板的对应设置值
        mat.node_tree.nodes[0].inputs["Base Color"].default_value = bpy.context.scene.mhw_ctc_toolpanel.coneColor
        mat.node_tree.nodes[0].inputs["Alpha"].default_value = bpy.context.scene.mhw_ctc_toolpanel.coneColor[3]
        # 材质透明模式设为Alpha混合，材质阴影模式为无
        mat.blend_method = "BLEND"
        if bpy.app.version < (4, 2, 0):
            mat.shadow_method = "NONE"
    return mat

def getConeGeoNodeTree():
    TREENAME = "CTCConeGeoNodeTreeV1"
    # 获取锥体的材质
    mat = getConeMat()
    if TREENAME not in bpy.data.node_groups:
        node_group = bpy.data.node_groups.new(type="GeometryNodeTree", name=TREENAME)
        nodes = node_group.nodes
        links = node_group.links

        currentXLoc = 0
        currentYLoc = 0
        # 在几何节点中添加一个新的输入，类型为浮点，名称为AngleLimitRadius
        if bpy.app.version < (4, 0, 0):
            node_group.inputs.new("NodeSocketFloat", "AngleLimitRadius")
        else:
            node_group.interface.new_socket(name="AngleLimitRadius",
                                            description="Do not change this value manually, set it from the chain object",
                                            in_out="INPUT", socket_type="NodeSocketFloat")
        # 添加组输入节点
        inNode = nodes.new('NodeGroupInput')
        inNode.location = (currentXLoc, currentYLoc)

        currentXLoc += 300
        # 添加锥形几何体节点
        coneNode = nodes.new('GeometryNodeMeshCone')
        coneNode.location = (currentXLoc, currentYLoc - 150)

        coneNode.inputs["Vertices"].default_value = 18
        # 将角度限制半径直接传递到底部半径，这样做不是很正确，但它足够接近正确的值，因此并不重要
        links.new(inNode.outputs["AngleLimitRadius"], coneNode.inputs["Radius Bottom"])
        currentXLoc += 300
        # 添加变换节点
        transformNode = nodes.new('GeometryNodeTransform')
        transformNode.location = (currentXLoc, currentYLoc)
        transformNode.inputs["Translation"].default_value = (10.0, 0.0, 0.0)  # 将x设置为10以使锥体尖端与骨头对齐
        transformNode.inputs["Rotation"].default_value = (0.0, -1.570796, 0.0)  # 旋转-90度以使锥体朝向正确的方向
        transformNode.inputs["Scale"].default_value = (5.0, 5.0, 5.0)
        # links.new(startObjInfoNode.outputs["Location"],instanceNode.inputs["Translation"])
        links.new(coneNode.outputs["Mesh"], transformNode.inputs["Geometry"])
        # links.new(separateScaleXYZNode.outputs["X"],transformNode.inputs["Scale"])

        currentXLoc += 300
        # 添加设置材质节点
        setMaterialNode = nodes.new('GeometryNodeSetMaterial')
        setMaterialNode.location = (currentXLoc, currentYLoc)
        # 设置材质节点中的材质为角度限制锥体的材质
        setMaterialNode.inputs["Material"].default_value = mat
        links.new(transformNode.outputs["Geometry"], setMaterialNode.inputs["Geometry"])

        currentXLoc += 300
        # 添加组输出节点
        outNode = nodes.new('NodeGroupOutput')
        outNode.location = (currentXLoc, currentYLoc)
        # if bpy.app.version < (3, 4, 0):
        #     outNode.inputs.new('NodeSocketGeometry', 'Geometry')
        if bpy.app.version < (4, 0, 0):
            node_group.outputs.new('NodeSocketGeometry', 'Geometry')
        else:
            node_group.interface.new_socket(name="Geometry", description="", in_out="OUTPUT",
                                            socket_type="NodeSocketGeometry")
        # 连接组输出节点
        links.new(setMaterialNode.outputs["Geometry"], outNode.inputs["Geometry"])
    else:
        node_group = bpy.data.node_groups[TREENAME]
    return node_group


