import bpy
import bmesh
from .general_function import splitNativesPath
from mathutils import Matrix, Vector, Quaternion

def checkNameUsage(baseName,checkSubString=True,objList=None):
    """
    在指定对象列表中查找指定名称的对象

    baseName: 指定名称
    checkSubString: 是否将指定名称作为子字符串进行检查
    objList: 对象列表
    """
    # 若未提供对象列表，则获取当前场景中的所有对象
    if objList == None:
        objList = bpy.data.objects

    # checkSubString为True，则检查baseName是否作为子字符串出现在对象列表中
    # checkSubString为False，则检查baseName是否精确匹配对象列表中某个对象的名称
    if checkSubString:
        return any(baseName in name for name in [obj.name for obj in objList])
    else:
        return baseName in [obj.name for obj in objList]

def findTempSpace(typeName):
    """
    查找指定名称的屏幕空间

    name: 屏幕空间的类型名，如 "FileSelectParams" 为文件浏览器空间
    """
    temp = bpy.data.screens.get("temp")
    browserSpace = None
    if temp != None:
        for area in temp.areas:
            for space in area.spaces:
                try:
                    if type(space.params).__name__ == typeName:
                        browserSpace = space
                        break
                except:
                    pass

    return browserSpace

def setModDirectoryFromFilePath(filePath):
    """
    将插件面板的 modDirectory 属性设为导出文件的根目录，如 D:\MHW_EXTRACT\nativePC

    filePath: 导出的文件路径
    """
    split = splitNativesPath(filePath)
    if split:
        bpy.context.scene.mhw_mrl3_toolpanel.modDirectory = split[0]
        print(f"Set mod directory to {bpy.context.scene.mhw_mrl3_toolpanel.modDirectory}.")
    else:
        print("Failed to set mod directory, exported file path probably does not follow the chunk naming scheme.")

def clearScene():
    """
    清空当前场景中的所有对象，属性等等
    """
    for collection in bpy.data.collections:
        for obj in collection.objects:
            collection.objects.unlink(obj)
        bpy.data.collections.remove(collection)
    for bpy_data_iter in (bpy.data.objects, bpy.data.meshes, bpy.data.lights, bpy.data.cameras):
        for id_data in bpy_data_iter:
            bpy_data_iter.remove(id_data)
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    for amt in bpy.data.armatures:
        bpy.data.armatures.remove(amt)
    for obj in bpy.data.objects:
        bpy.data.objects.remove(obj)
        obj.user_clear()
    for nodeGroup in bpy.data.node_groups:
        bpy.data.node_groups.remove(nodeGroup)
    for img in bpy.data.images:
        if not img.users:
            bpy.data.images.remove(img)

def createCollection(name,color,type,parentCollection=None):
    """
    创建一个新集合

    name: 集合名称
    color: 集合颜色，如 "COLOR_01"，注意 "NONE" 是默认的白色
    type: 集合的自定义属性，如 "MHW_MOD3_COLLECTION"
    parentCollection: 父级集合

    return 新创建的集合
    """
    collection = bpy.data.collections.new(name)
    collection.color_tag = color
    collection["~TYPE"] = type
    if parentCollection != None:
        parentCollection.children.link(collection)
    else:
        bpy.context.scene.collection.children.link(collection)
    return collection

def getCollection(name,parentCollection=None,makeNew=False):
    """
    获取指定名称的集合

    name: 集合名称
    parentCollection: 父级集合
    makeNew: 指定是否创建新集合

    return 获取或新创建的集合
    """
    if makeNew or not bpy.data.collections.get(name):
        collection = bpy.data.collections.new(name)
        # collectionName = collection.name
        if parentCollection != None:
            parentCollection.children.link(collection)
        else:
            bpy.context.scene.collection.children.link(collection)

        return collection
    else:
        return bpy.data.collections[name]

def createEmpty(name,propertyList,parentObj=None,parentCollection=None):
    """
    创建一个新的空物体对象

    name: 对象名称
    propertyList: 自定义属性的二元元组列表，结构如 [("~TYPE", "MHW_CTC_HEADER")]
    parentObj: 父级对象
    parentCollection: 父级集合

    return 新创建的空物体对象
    """
    obj = bpy.data.objects.new(name, None)
    obj.empty_display_size = .10
    obj.empty_display_type = 'PLAIN_AXES'  # 显示类型为“纯轴”
    obj.parent = parentObj

    for prop in propertyList:
        obj[prop[0]] = prop[1]

    if parentCollection == None:
        parentCollection = bpy.context.scene.collection
    parentCollection.objects.link(obj)

    return obj

def createCurveEmpty(name,propertyList,parentObj=None,parentCollection=None,makeNew=False):
    """
    创建一个新的空曲线对象

    name: 对象名称
    propertyList: 自定义属性的二元元组列表，结构如 [("~TYPE", "MHW_CTC_HEADER")]
    parentObj: 父级对象
    parentCollection: 父级集合
    makeNew: 是否强制创建新的空曲线对象

    return 新创建的空曲线对象
    """
    if makeNew:
        curveData = bpy.data.curves.new(name, 'CURVE')
        curveData.use_path = False
    else:
        CURVE_DATA_NAME = "emptyCurve"
        # 检查blender数据中是否已经存在名为"emptyCurve"的曲线数据
        if CURVE_DATA_NAME in bpy.data.curves:  # 如果存在，则将其赋值给curveData
            curveData = bpy.data.curves[CURVE_DATA_NAME]
        else:  # 如果不存在，则创建新的曲线数据
            curveData = bpy.data.curves.new(CURVE_DATA_NAME, 'CURVE')
            # 曲线不作为路径使用
            curveData.use_path = False

    obj = bpy.data.objects.new(name, curveData)
    obj.parent = parentObj
    for prop in propertyList:
        obj[prop[0]] = prop[1]

    if parentCollection == None:
        parentCollection = bpy.context.scene.collection
    parentCollection.objects.link(obj)

    return obj

splinePointList = [([(-1.1, 0.0, 0.0), (0.0, 1.1, 0.0), (1.1, 0.0, 0.0), (0.0, -1.1, 0.0)],
                    [(-1.1, -0.6073, 0.0), (-0.6073, 1.1, 0.0), (1.1, 0.6073, 0.0), (0.6073, -1.1, 0.0)],
                    [(-1.1, 0.6073, 0.0), (0.6073, 1.1, 0.0), (1.1, -0.6073, 0.0), (-0.6073, -1.1, 0.0)]), (
                   [(-1.1, 0.0, 0.0), (0.0, -0.0, -1.1), (1.1, 0.0, 0.0), (0.0, 0.0, 1.1)],
                   [(-1.1, 0.0, 0.6073), (-0.6073, -0.0, -1.1), (1.1, -0.0, -0.6073), (0.6073, 0.0, 1.1)],
                   [(-1.1, -0.0, -0.6073), (0.6073, -0.0, -1.1), (1.1, 0.0, 0.6073), (-0.6073, 0.0, 1.1)]), (
                   [(0.0, 0.0, 1.1), (0.0, 1.1, -0.0), (-0.0, -0.0, -1.1), (-0.0, -1.1, 0.0)],
                   [(0.0, -0.6073, 1.1), (0.0, 1.1, 0.6073), (-0.0, 0.6073, -1.1), (-0.0, -1.1, -0.6073)],
                   [(0.0, 0.6073, 1.1), (0.0, 1.1, -0.6073), (-0.0, -0.6073, -1.1), (-0.0, -1.1, 0.6073)])]

def createFakeEmptySphere(name,propertyList,parentObj=None,parentCollection=None):
    """
    创建一个新的球形空曲线对象

    name: 对象名称
    propertyList: 自定义属性的二元元组列表，结构如 [("~TYPE", "MHW_CTC_HEADER")]
    parentObj: 父级对象
    parentCollection: 父级集合

    return 新创建的空曲线对象
    """
    CURVE_DATA_NAME = "fakeEmptySphere"
    if CURVE_DATA_NAME in bpy.data.curves:
        curveData = bpy.data.curves[CURVE_DATA_NAME]
    else:
        curveData = bpy.data.curves.new(CURVE_DATA_NAME, 'CURVE')
        curveData.use_path = False
        for pointSet in splinePointList:
            coordList = pointSet[0]
            leftList = pointSet[1]
            rightList = pointSet[2]
            spline = curveData.splines.new(type='BEZIER')
            spline.use_cyclic_u = True
            spline.bezier_points.add(3)
            for index, point in enumerate(spline.bezier_points):
                point.co = coordList[index]
                point.handle_left = leftList[index]
                point.handle_right = rightList[index]

    obj = bpy.data.objects.new(name, curveData)
    obj.parent = parentObj
    for prop in propertyList:
        obj[prop[0]] = prop[1]
    if parentCollection == None:
        parentCollection = bpy.context.scene.collection
    parentCollection.objects.link(obj)
    return obj

def lockObjTransforms(obj,lockLocation=True,lockRotation=True,lockScale=True):
    """
    给对象添加限制约束

    obj: 对象
    lockLocation: 是否锁定位置
    lockRotation: 是否锁定旋转
    lockScale: 是否锁定缩放
    """
    if lockLocation:
        constraint = obj.constraints.new(type="LIMIT_LOCATION")
        constraint.use_min_x = True
        constraint.use_min_y = True
        constraint.use_min_z = True

        constraint.use_max_x = True
        constraint.use_max_y = True
        constraint.use_max_z = True
    if lockRotation:
        constraint = obj.constraints.new(type="LIMIT_ROTATION")
        constraint.use_limit_x = True
        constraint.use_limit_y = True
        constraint.use_limit_z = True

    if lockScale:
        constraint = obj.constraints.new(type="LIMIT_SCALE")
        constraint.use_min_x = True
        constraint.use_min_y = True
        constraint.use_min_z = True

        constraint.use_max_x = True
        constraint.use_max_y = True
        constraint.use_max_z = True

        constraint.min_x = 1.0
        constraint.max_x = 1.0
        constraint.min_y = 1.0
        constraint.max_y = 1.0
        constraint.min_z = 1.0
        constraint.max_z = 1.0

def orientVectorPair(v0,v1):
    """从两个向量 v0 和 v1 计算旋转矩阵"""
    v0 = v0.normalized()
    v1 = v1.normalized()
    if v0 == v1:
        return Matrix.Identity(3)
    v = v0.cross(v1)
    #s = v.length
    c = v0.dot(v1)
    if c == -1: return Matrix([[-1,0,0],[0,-1,0],[0,0,1]])
    vx = Matrix([[0,-v[2], v[1]],[v[2],0,-v[0]],[-v[1],v[0],0]])
    return Matrix.Identity(3)+vx+(1/(1+c))*vx@vx


# 处理重叠UV和分离锐边所需要的函数集
# --------------------------------
def checkObjForUVDoubling(obj):
    """检查网格对象是否有重叠UV"""
    hasUVDoubling = False
    UVPoints = dict()
    if len(obj.data.uv_layers) > 0:
        for loop in obj.data.loops:
            currentVertIndex = loop.vertex_index
            # Vertex UV
            uv = obj.data.uv_layers[0].data[loop.index].uv

            if currentVertIndex in UVPoints and UVPoints[currentVertIndex] != uv:
                hasUVDoubling = True
                break
            # raise Exception
            else:
                UVPoints[currentVertIndex] = uv
    return hasUVDoubling

def cloneMesh(mesh):
    """克隆网格对象"""
    new_obj = mesh.copy()
    new_obj.data = mesh.data.copy()
    bpy.context.scene.collection.objects.link(new_obj)
    return new_obj

def bad_iter(blenderCrap):
    """迭代器"""
    # Blender will throw errors if you loop directly over the uv layers
    i = 0
    while (True):
        try:
            yield(blenderCrap[i])
            i+=1
        except:
            return
def selectRepeated(bm):
    bm.verts.index_update()
    bm.verts.ensure_lookup_table()
    targetVert = set()
    for uv_layer in bad_iter(bm.loops.layers.uv):
        uvMap = {}
        for face in bm.faces:
            for loop in face.loops:
                uvPoint = tuple(loop[uv_layer].uv)
                if loop.vert.index in uvMap and uvMap[loop.vert.index] != uvPoint:
                    targetVert.add(bm.verts[loop.vert.index])
                else:
                    uvMap[loop.vert.index] = uvPoint
    return targetVert
def solveRepeatedVertex(op, mesh):
    bpy.ops.mesh.select_all(action='DESELECT')
    bm = bmesh.from_edit_mesh(mesh.data)
    oldmode = bm.select_mode
    bm.select_mode = {'VERT'}
    targets = selectRepeated(bm)
    for target in targets:
        bmesh.utils.vert_separate(target, target.link_edges)
        bm.verts.ensure_lookup_table()
    bpy.ops.mesh.select_all(action='DESELECT')
    bm.select_mode = oldmode
    bm.verts.ensure_lookup_table()
    bm.verts.index_update()
    bmesh.update_edit_mesh(mesh.data)
    mesh.data.update()
    return

def transferNormals(clone, mesh):
    """传递法向数据"""
    m = mesh.modifiers.new("Normals Transfer", "DATA_TRANSFER")
    m.use_loop_data = True
    m.loop_mapping = "TOPOLOGY"  # "POLYINTERP_NEAREST"#
    m.data_types_loops = {'CUSTOM_NORMAL'}
    m.object = clone
    bpy.ops.object.modifier_move_to_index(modifier=m.name, index=0)
    bpy.ops.object.modifier_apply(modifier=m.name)


def deleteClone(clone):
    """删除克隆的网格对象"""
    objs = bpy.data.objects
    objs.remove(objs[clone.name], do_unlink=True)

def solveRepeatedUVs(obj):
    """处理重叠UV"""
    context = bpy.context
    context.view_layer.objects.active = obj
    if bpy.app.version < (4, 0, 0):
        if obj.data.use_auto_smooth == False:
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = .785  # 45 degrees, try to preserve normals if auto smooth was disabled
    obj.data.polygons.foreach_set("use_smooth", [True] * len(obj.data.polygons))
    clone = cloneMesh(obj)
    bpy.ops.object.mode_set(mode='EDIT')
    obj = context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    # old seams
    old_seams = [e for e in bm.edges if e.seam]
    # unmark
    for e in old_seams:
        e.seam = False
    # mark seams from uv islands
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.seams_from_islands()
    seams = [e for e in bm.edges if e.seam]
    bmesh.ops.split_edges(bm, edges=seams)
    for e in old_seams:
        e.seam = True
    bmesh.update_edit_mesh(me)
    solveRepeatedVertex(None, obj)
    bpy.ops.object.mode_set(mode='OBJECT')
    transferNormals(clone, obj)
    if bpy.app.version < (4, 0, 0):
        obj.data.calc_normals_split()
    deleteClone(clone)

    print(f"Solved Repeated UVs on {obj.name}")


def splitSharpEdges(obj):
    """分离锐边"""
    context = bpy.context
    isHidden = obj.hide_viewport
    if isHidden:
        obj.hide_viewport = False
    context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    # old seams
    sharp = [e for e in bm.edges if not e.smooth]
    if sharp != []:
        print(f"Split Sharp Edges on {obj.name}")
    bmesh.ops.split_edges(bm, edges=sharp)
    bmesh.update_edit_mesh(me)
    bpy.ops.object.mode_set(mode='OBJECT')
    obj.hide_viewport = isHidden
# --------------------------------

# def triangulateMesh(mesh):
#     """
#     三角化网格的面
#     """
#     # BMesh triangulation screws up normals, so save them and reset them after triangulation
#     # custom_normals = None
#     # if mesh.has_custom_normals:
#     #    custom_normals = [0.0]*len(mesh.vertices)
#     #    for vertex in mesh.vertices:
#     #        custom_normals[vertex.index] = vertex.normal.copy()
#
#     bm = bmesh.new()
#     bm.from_mesh(mesh)
#     bmesh.ops.triangulate(bm, faces=bm.faces[:])
#     bm.to_mesh(mesh)
#     bm.free()
#     # if custom_normals:
#     # mesh.normals_split_custom_set_from_vertices(custom_normals)

# 之前的triangulateMesh使用bmesh进行三角化会有时破坏网格的法向，所以改为进编辑模式使用bpy.ops.mesh.quads_convert_to_tris进行三角化
def triangulateMesh(meshObj):
    """
    三角化网格的面
    """
    bpy.context.view_layer.objects.active = meshObj
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    bpy.ops.object.mode_set(mode='OBJECT')

class ContextExecuterOverride:
    def __init__(self, window, screen, area, region):
        self.window, self.screen, self.area, self.region = window, screen, area, region
        self.legacy = not hasattr(bpy.context, "temp_override")
        if self.legacy:
            self.context = bpy.context.copy()
            self.context['window'] = window
            self.context['screen'] = screen
            self.context['area'] = area
            self.context['region'] = region
        else:
            self.context = bpy.context.temp_override(window=window, screen=screen, area=area, region=region)

    def __enter__(self):
        if not self.legacy:
            self.context.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not self.legacy:
            self.context.__exit__(self, exc_type, exc_value, traceback)
        return self

class ContextScriptExecuter():

    def __init__(self, area_type, ui_type=None, script=None):
        self.area_type = area_type
        self.ui_type = ui_type if ui_type else area_type
        self.script = script

    def script_content(self, override):
        self.script(override)

    def execute_script(self):
        window = bpy.context.window
        screen = window.screen
        areas = [area for area in screen.areas if area.type == self.area_type]
        area = areas[0] if len(areas) else screen.areas[0]
        prev_ui_type = area.ui_type
        area.ui_type = self.ui_type
        regions = [region for region in area.regions if region.type == 'WINDOW']
        region = regions[0] if len(regions) else None
        with ContextExecuterOverride(window=window, screen=screen, area=area, region=region) as override:
            self.script_content(override)
        area.ui_type = prev_ui_type

def outlinerShowObject(objName):
    if objName in bpy.data.objects:
        obj = bpy.data.objects[objName]
        bpy.context.view_layer.objects.active = obj
        ContextScriptExecuter(
    area_type='OUTLINER',
    script=lambda override: (
        bpy.ops.outliner.show_active(override.context)
        if override.legacy
        else bpy.ops.outliner.show_active()
    )
).execute_script()

def operator_exists(idname):
    # from bpy.ops import op_as_string
    try:
        # op_as_string(idname)
        bpy.ops.op_as_string(idname)
        return True
    except:
        return False



