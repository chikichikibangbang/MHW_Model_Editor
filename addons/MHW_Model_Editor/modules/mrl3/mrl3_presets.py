import json
import os
import re
import bpy
from ..common.message_functions import showErrorMessageBox, textColors
from ..common.blender_functions import checkNameUsage, createEmpty
mrl3PresetList = []


def saveAsPreset(activeObj, presetName):
	# if len(selection) == 1:
	# 	activeObj = selection[0]
	if activeObj != None:
		mrl3ObjType = activeObj.get("~TYPE", None)
		if not re.search(r'^[\w,\s-]+\.[A-Za-z]{3}$',
						 presetName) and not ".." in presetName:  # 检查预设名称是否包含非法字符
			presetDict = {}
			folderPath = None

			if mrl3ObjType == "MHW_MRL3_MATERIAL":
				folderPath = "MaterialPresets"
				mhw_mrl3_material = activeObj.mhw_mrl3_material
				presetDict["presetType"] = "MHW_MRL3_MATERIAL"

				presetDict["Material Header"] = {
					"materialName": mhw_mrl3_material.materialName,
					"materialNameHash": mhw_mrl3_material.materialNameHash,
					"mmtrHash": mhw_mrl3_material.mmtrHash,
					"mmtrName": mhw_mrl3_material.mmtrName,
					"shaderHash": mhw_mrl3_material.shaderHash,
					"surfaceCoef": list(mhw_mrl3_material.surfaceCoef),
					"alphaCoef": list(mhw_mrl3_material.alphaCoef),
					}

				if mhw_mrl3_material.mapList_items:
					presetDict["Map List"] = []
					for mapItem in mhw_mrl3_material.mapList_items:
						mapDict = {"name": mapItem.name, "value": mapItem.value, "code": mapItem.code}
						presetDict["Map List"].append(mapDict)

				if mhw_mrl3_material.samplerList_items:
					presetDict["Sampler List"] = []
					for samplerItem in mhw_mrl3_material.samplerList_items:
						samplerDict = {"name": samplerItem.name, "value": samplerItem.value, "code": samplerItem.code}
						presetDict["Sampler List"].append(samplerDict)

				if mhw_mrl3_material.propertyBlock_items:
					presetDict["Property List"] = []
					for propBlockItem in mhw_mrl3_material.propertyBlock_items:
						propBlockDict = {"blockName": propBlockItem.blockName, "code": propBlockItem.code, "props": []}
						for prop in propBlockItem.propertyList_items:
							if prop.data_type == "INT":
								value = prop.int_value
							elif prop.data_type == "UINT":
								value = prop.uint_value
							elif prop.data_type == "BOOL":
								value = 1 if prop.bool_value else 0
							elif prop.data_type == "FLOAT[2]":
								value = list(prop.float2_value)
							elif prop.data_type == "FLOAT[3]":
								value = list(prop.float3_value)
							elif prop.data_type == "FLOAT[4]":
								value = list(prop.float4_value)
							elif prop.data_type == "COLOR":
								value = list(prop.color_value)
							else:  # float
								value = prop.float_value

							# if value.__class__.__name__ == "IDPropertyArray":
							# 	value = value.to_list()

							propDict = {"prop_name": prop.prop_name, "ori_name": prop.ori_name, "data_type": prop.data_type, "value": value}
							propBlockDict["props"].append(propDict)

						presetDict["Property List"].append(propBlockDict)
			else:
				showErrorMessageBox("Must select a mrl3 material object (named with \"Mrl3 Material 00...\") to save preset.")

			if presetDict != {}:
				jsonPath = os.path.join(os.path.dirname(__file__), folderPath, presetName + ".json")
				try:
					os.makedirs(os.path.split(jsonPath)[0])
				except:
					pass
				with open(jsonPath, 'w', encoding='utf-8') as f:
					json.dump(presetDict, f, ensure_ascii=False, indent=4)
					print(textColors.OKGREEN + "Saved material preset to " + str(jsonPath) + textColors.ENDC)
					return True
		else:
			showErrorMessageBox("Invalid preset file name.")
	else:
		showErrorMessageBox("Must select a mrl3 material object (named with \"Mrl3 Material 00...\") to save preset.")


def readPresetJSON(filepath):
	mrl3Collection = bpy.context.scene.mhw_mrl3_toolpanel.mrl3Collection
	try:
		with open(filepath) as jsonFile:
			jsonDict = json.load(jsonFile)
	except Exception as err:
		showErrorMessageBox("Failed to read json file. \n" + str(err))
		return False

	if jsonDict["presetType"] != "MHW_MRL3_MATERIAL":
		showErrorMessageBox("Preset type is not supported.")
		return False

	if not jsonDict.get("Material Header"):
		showErrorMessageBox("Preset is missing material header info, cannot add preset material.")
		return False
	else:
		matHeader = jsonDict["Material Header"]
		if not matHeader.get("materialName") or not matHeader.get("mmtrHash") or not matHeader.get("mmtrName") \
				or not matHeader.get("shaderHash") or not matHeader.get("surfaceCoef") or not matHeader.get("alphaCoef"):
			showErrorMessageBox("Preset is missing material header info, cannot add preset material.")
			return False

	print("Adding preset material " + jsonDict["Material Header"]["materialName"])

	# 检查前缀名是否已被使用
	currentIndex = 0
	subName = "Mrl3 Material " + str(currentIndex).zfill(2)
	while (checkNameUsage(subName, checkSubString=True, objList=mrl3Collection.all_objects)):
		currentIndex += 1
		subName = "Mrl3 Material " + str(currentIndex).zfill(2)

	name = subName + " (" + jsonDict["Material Header"]["materialName"] + ")"
	matObj = createEmpty(name, [("~TYPE", "MHW_MRL3_MATERIAL")], None, mrl3Collection)
	mhw_mrl3_material = matObj.mhw_mrl3_material

	mhw_mrl3_material.materialName = jsonDict["Material Header"]["materialName"]
	mhw_mrl3_material.materialNameHash = jsonDict["Material Header"]["materialNameHash"]
	mhw_mrl3_material.mmtrHash = jsonDict["Material Header"]["mmtrHash"]
	mhw_mrl3_material.mmtrName = jsonDict["Material Header"]["mmtrName"]
	mhw_mrl3_material.shaderHash = jsonDict["Material Header"]["shaderHash"]
	mhw_mrl3_material.surfaceCoef = jsonDict["Material Header"]["surfaceCoef"]
	mhw_mrl3_material.alphaCoef = jsonDict["Material Header"]["alphaCoef"]

	if jsonDict.get("Map List"):
		for mapEntry in jsonDict["Map List"]:
			newListItem = mhw_mrl3_material.mapList_items.add()
			newListItem.name = mapEntry["name"]
			newListItem.value = mapEntry["value"]
			newListItem.code = mapEntry["code"]

	if jsonDict.get("Sampler List"):
		for samplerEntry in jsonDict["Sampler List"]:
			newListItem = mhw_mrl3_material.samplerList_items.add()
			newListItem.name = samplerEntry["name"]
			newListItem.value = samplerEntry["value"]
			newListItem.code = samplerEntry["code"]

	if jsonDict.get("Property List"):
		for propBlockEntry in jsonDict["Property List"]:
			propertyBlock_item = mhw_mrl3_material.propertyBlock_items.add()
			propertyBlock_item.blockName = propBlockEntry["blockName"]
			propertyBlock_item.code = propBlockEntry["code"]
			propertyBlock_item.propertyList_items.clear()  # 清空现有属性

			for propEntry in propBlockEntry["props"]:
				newListItem = propertyBlock_item.propertyList_items.add()
				newListItem.prop_name = propEntry["prop_name"]
				newListItem.ori_name = propEntry["ori_name"]
				newListItem.data_type = propEntry["data_type"]

				if propEntry["data_type"] == "FLOAT":
					newListItem.float_value = propEntry["value"]
				if propEntry["data_type"] == "INT":
					newListItem.int_value = propEntry["value"]
				elif propEntry["data_type"] == "UINT":
					newListItem.uint_value = propEntry["value"]
				elif propEntry["data_type"] == "BOOL":
					newListItem.bool_value = bool(propEntry["value"])
				elif propEntry["data_type"] == "FLOAT[2]":
					newListItem.float2_value = propEntry["value"]
				elif propEntry["data_type"] == "FLOAT[3]":
					newListItem.float3_value = propEntry["value"]
				elif propEntry["data_type"] == "FLOAT[4]":
					newListItem.float4_value = propEntry["value"]
				elif propEntry["data_type"] == "COLOR":
					newListItem.color_value = propEntry["value"]

	bpy.context.view_layer.objects.active = matObj
	return True


def reloadPresets(folderPath):
	global mrl3PresetList
	mrl3PresetList.clear()
	presetsPath = os.path.join(os.path.dirname(__file__), folderPath)
	# presetList = []
	identifier = 0
	# relPathStart = os.path.join(presetsPath, folderPath)
	relPathStart = presetsPath
	if os.path.exists(relPathStart):
		for entry in os.scandir(relPathStart):
			if entry.name.endswith(".json") and entry.is_file():
				# print(os.path.splitext(entry.name)[0].encode('utf-8'))
				mrl3PresetList.append((os.path.relpath(os.path.join(relPathStart, entry), start=presetsPath),
								   os.path.splitext(entry.name)[0], ""))

				# presetList.append((str(identifier), os.path.splitext(entry.name)[0], ""))
				identifier += 1

	#print("Loading " + folderPath + " presets...")
	#print("DEBUG:" + str(presetList)+"\n")#debug
	# print(presetList)
	return mrl3PresetList