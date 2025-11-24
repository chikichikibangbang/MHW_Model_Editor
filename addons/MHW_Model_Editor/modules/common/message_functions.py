import bpy
from .....common.i18n.i18n import i18n, i18n_split

class textColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def raiseError(error, errorCode=999):
    try:
        raise Exception()
    except Exception:
        print(textColors.FAIL + i18n("ERROR: ") + error + textColors.ENDC)

def raiseTexError(error, errorCode=999):
    print(textColors.FAIL + i18n("ERROR: ") + error + textColors.ENDC)
    raise Exception(error)

def raiseWarning(warning):
    print(textColors.WARNING + i18n("WARNING: ") + warning + textColors.ENDC)

def showMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        self.layout.label(text = message)
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def showErrorMessageBox(message):
    print(textColors.FAIL + i18n("ERROR: ") + message + textColors.ENDC)
    showMessageBox(message,title = "Error", icon = "ERROR")

def addErrorToDict(errorDict, errorType, objectName=None, boneName=None):
    if errorType in errorDict:
        errorDict[errorType]["count"] += 1
        if objectName != None:
            errorDict[errorType]["objectSet"].add(objectName)
        if boneName != None:
            errorDict[errorType]["boneSet"].add(boneName)
    else:
        if objectName != None:
            errorDict[errorType] = {"count": 1, "objectSet": {objectName}}
        elif boneName != None:
            errorDict[errorType] = {"count": 1, "boneSet": {boneName}}
        else:
            errorDict[errorType] = {"count": 1}

def printErrorInfo(errorDict, errorInfoDict):
    lang = bpy.context.preferences.view.language
    errorTypes = sorted(errorDict.keys())
    lastIndex = len(errorTypes) - 1

    for index, errorType in enumerate(errorTypes):
        count = errorDict[errorType]["count"]
        objectSet = errorDict[errorType].get("objectSet", {})
        boneSet = errorDict[errorType].get("boneSet", {})
        errorInfo = errorInfoDict[errorType]
        nameListString = ""
        # if objectSet:
        #     # nameListString = f"\nObjects with this error ({str(len(objectSet))}):\n"
        #     nameListString = f"\nERROR OBJECTS:\n"
        #     for name in sorted(list(objectSet)):
        #         # nameListString += "["+name +"]\n"
        #         nameListString += f"{name}\n"
        # elif boneSet:
        #     # nameListString = f"\nObjects with this error ({str(len(objectSet))}):\n"
        #     nameListString = f"\nERROR BONES:\n"
        #     for name in sorted(list(boneSet)):
        #         # nameListString += "["+name +"]\n"
        #         nameListString += f"{name}\n"

        if objectSet:
            nameListString = f"\n{i18n('ERROR OBJECTS:')}\n" + "\n".join(sorted(objectSet))
        elif boneSet:
            nameListString = f"\n{i18n('ERROR BONES:')}\n" + "\n".join(sorted(boneSet))

        separator = "" if index == lastIndex else "\n__________________________________"

        if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
            print(f"{textColors.FAIL}错误 ({str(index + 1)} / {len(errorDict)}): "
                  f"{str(count)}例 {i18n_split(errorInfo, specialStrings=SPECIAL_STRINGS_SET)}{nameListString}"
                  f"{separator}{textColors.ENDC}")
        else:
            print(f"{textColors.FAIL}ERROR ({str(index + 1)} / {len(errorDict)}): "
                  f"{str(count)} instance(s) of {errorInfo}{nameListString}"
                  f"{separator}{textColors.ENDC}")


SPECIAL_STRINGS_SET = {"Select a target mod3 collection in the export options.",
                       "please make sure there are selected or visible meshes.",
                       "Change the name of child lod collections to ensure that each lod level is unique.",
                       "Move the extra armature into another collection or delete it.",
                       "Reduce the amount of bones on the armature.",
                       "Why decide to try to export so many vertices?",
                       "Why decide to try to export so many faces?",
                       "Why decide to try to export so many meshes?",
                       "Why decide to try to export so many materials?",
                       "Select a target mrl3 collection in the export options.",
                       }


