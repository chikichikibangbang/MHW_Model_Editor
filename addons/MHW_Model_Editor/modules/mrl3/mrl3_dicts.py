import json
import os

_block_format_dict_cache = None
_property_dict_cache = None
_master_material_dict_cache = None
_various_hash_dict_cache = None
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

def get_master_material_dict():
    global _master_material_dict_cache
    if _master_material_dict_cache is None:
        _master_material_dict_cache = load_json_data("master_material_dict")
    return _master_material_dict_cache

def get_various_hash_dict():
    global _various_hash_dict_cache
    if _various_hash_dict_cache is None:
        _various_hash_dict_cache = load_json_data("various_hash_dict")
    return _various_hash_dict_cache


def clear_all_caches():
    global _property_dict_cache, _master_material_dict_cache, _various_hash_dict_cache, _block_format_dict_cache
    _property_dict_cache = None
    _master_material_dict_cache = None
    _various_hash_dict_cache = None
    _block_format_dict_cache = None

def clear_master_material_dict_cache():
    global _master_material_dict_cache
    _master_material_dict_cache = None

def clear_various_hash_dict_cache():
    global _various_hash_dict_cache
    _various_hash_dict_cache = None

def clear_property_dict_cache():
    global _property_dict_cache
    _property_dict_cache = None

def clear_block_format_dict_cache():
    global _block_format_dict_cache
    _block_format_dict_cache = None