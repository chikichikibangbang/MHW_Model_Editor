import json
import os

_block_format_dict_cache = None
_property_dict_cache = None
_shader_dict_cache = None
_texture_dict_cache = None
_master_material_dict_cache = None
_ibhash_to_material_dict_cache = None
_node_group_dict_cache = None
def load_json_data(json_name):
    json_path = os.path.join(os.path.dirname(__file__), "dict", f"{json_name}.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load {json_name}.json: {e}")
        return {}  # 返回空字典避免后续报错

def get_block_format_dict():
    global _block_format_dict_cache
    if _block_format_dict_cache is None:
        _block_format_dict_cache = load_json_data("block_format_dict")
    return _block_format_dict_cache

def get_property_dict():
    global _property_dict_cache
    if _property_dict_cache is None:
        _property_dict_cache = load_json_data("property_dict")
    return _property_dict_cache

def get_shader_dict():
    global _shader_dict_cache
    if _shader_dict_cache is None:
        _shader_dict_cache = load_json_data("shader_dict")
    return _shader_dict_cache

def get_texture_dict():
    global _texture_dict_cache
    if _texture_dict_cache is None:
        _texture_dict_cache = load_json_data("texture_dict")
    return _texture_dict_cache

def get_master_material_dict():
    global _master_material_dict_cache
    if _master_material_dict_cache is None:
        _master_material_dict_cache = load_json_data("master_material_dict")
    return _master_material_dict_cache

def get_ibhash_to_material_dict():
    global _ibhash_to_material_dict_cache
    if _ibhash_to_material_dict_cache is None:
        _ibhash_to_material_dict_cache = load_json_data("IBHashToMaterial")
    return _ibhash_to_material_dict_cache

def get_node_group_dict():
    global _node_group_dict_cache
    if _node_group_dict_cache is None:
        _node_group_dict_cache = load_json_data("node_group_dict")
    return _node_group_dict_cache

def clear_all_caches():
    global _property_dict_cache, _shader_dict_cache, _texture_dict_cache, _master_material_dict_cache, _ibhash_to_material_dict_cache
    _property_dict_cache = None
    _shader_dict_cache = None
    _texture_dict_cache = None
    _master_material_dict_cache = None
    _ibhash_to_material_dict_cache = None
    _node_group_dict_cache = None

def clear_master_material_dict_cache():
    global _master_material_dict_cache
    _master_material_dict_cache = None

def clear_ibhash_to_material_dict_cache():
    global _ibhash_to_material_dict_cache
    _ibhash_to_material_dict_cache = None

def clear_node_group_dict_cache():
    global _node_group_dict_cache
    _node_group_dict_cache = None

def clear_block_format_dict_cache():
    global _block_format_dict_cache
    _block_format_dict_cache = None