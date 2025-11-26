#Author: NSA Cloud
import os
import re
import json
from ..common.message_functions import textColors, raiseWarning, showErrorMessageBox
from .....common.i18n.i18n import i18n
presetList = []

def saveAsPreset(activeObj, presetName):
	# if len(selection) == 1:
	# 	activeObj = selection[0]
	if activeObj != None:
		ctcObjType = activeObj.get("~TYPE", None)
		if not re.search(r'^[\w,\s-]+\.[A-Za-z]{3}$',
						 presetName) and not ".." in presetName:  # 检查预设名称是否包含非法字符
			presetDict = {}
			folderPath = None
			variableList = []

			if ctcObjType == "MHW_CTC_CHAIN":
				folderPath = "ChainPresets"
				presetDict["presetType"] = "CTC_CHAIN"  # 兼容旧版插件的预设文件
				variableList = activeObj.mhw_ctc_chain.items()
			else:
				showErrorMessageBox(i18n("Must select a ctc chain object (named with \"CTC_CHAIN_XX...\") to save preset."))

			if variableList != []:
				for key, value in variableList:
					if type(value).__name__ == "IDPropertyArray":
						value_list = value.to_list()
						if key == "Gravity":  # 兼容旧版插件的预设文件
							value_list = [100 * value_list[0], 100 * value_list[1], 100 * value_list[2]]
						presetDict[key] = value_list
					else:
						if key == "LimitForce":  # 兼容旧版插件的预设文件
							value = 100 * value
						presetDict[key] = value

				# jsonPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]), "presets",
				# 						folderPath, presetName + ".json")
				jsonPath = os.path.join(os.path.dirname(__file__), folderPath, presetName + ".json")

				# print(presetDict)  # debug
				try:
					os.makedirs(os.path.split(jsonPath)[0])
				except:
					pass
				with open(jsonPath, 'w', encoding='utf-8') as f:
					json.dump(presetDict, f, ensure_ascii=False, indent=4)
					print(textColors.OKGREEN + i18n("Saved chain preset to ") + str(jsonPath) + textColors.ENDC)
					return True
		else:
			showErrorMessageBox(i18n("Invalid preset file name."))
	else:
		showErrorMessageBox(i18n("Must select a ctc chain object (named with \"CTC_CHAIN_XX...\") to save preset."))

def readPresetJSON(filepath, activeObj):
	try:
		with open(filepath) as jsonFile:
			jsonDict = json.load(jsonFile)

	except Exception as err:
		showErrorMessageBox(i18n("Failed to read json file.") + " \n" + i18n(str(err)))
		return False

	if jsonDict["presetType"] != "CTC_CHAIN":
		showErrorMessageBox(i18n("Preset type is not supported."))
		return False

	if activeObj.get("~TYPE", None) != "MHW_CTC_CHAIN":
		showErrorMessageBox(i18n("Must select a ctc chain object (named with \"CTC_CHAIN_XX...\") to apply preset."))
		return False
	# propertyGroup = {}
	propertyGroup = activeObj.mhw_ctc_chain
	# if jsonDict["presetType"] == "CTC_CHAIN":
	# 	propertyGroup = activeObj.ctc_settings
	# else:
	# 	showErrorMessageBox("Preset type is not supported.")
	# 	return False
	print(i18n("Applying preset to ") + activeObj.name)

	for key in propertyGroup.keys():
		try:
			if key == "Gravity":  # 兼容旧版插件的预设文件
				propertyGroup[key] = [0.01 * jsonDict[key][0], 0.01 * jsonDict[key][1], 0.01 * jsonDict[key][2]]
			elif key == "LimitForce":  # 兼容旧版插件的预设文件
				propertyGroup[key] = 0.01 * jsonDict[key]
			else:
				propertyGroup[key] = jsonDict[key]
		except:
			raiseWarning(i18n("Preset is missing key ") + str(key) + i18n(", cannot set value on active object."))
	return True


def reloadPresets(folderPath):
	# presetsPath = os.path.join(os.path.dirname(os.path.split(os.path.abspath(__file__))[0]),"presets")
	# global presetList  # 支持中文预设名
	global presetList
	presetList.clear()
	presetsPath = os.path.join(os.path.dirname(__file__), folderPath)
	# presetList = []
	identifier = 0
	# relPathStart = os.path.join(presetsPath, folderPath)
	relPathStart = presetsPath
	if os.path.exists(relPathStart):
		for entry in os.scandir(relPathStart):
			if entry.name.endswith(".json") and entry.is_file():
				# print(os.path.splitext(entry.name)[0].encode('utf-8'))
				presetList.append((os.path.relpath(os.path.join(relPathStart, entry), start=presetsPath),
								   os.path.splitext(entry.name)[0], ""))

				# presetList.append((str(identifier), os.path.splitext(entry.name)[0], ""))
				identifier += 1

	#print("Loading " + folderPath + " presets...")
	#print("DEBUG:" + str(presetList)+"\n")#debug
	# print(presetList)
	return presetList

