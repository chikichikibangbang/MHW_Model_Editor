import bpy
import os

import numpy as np

from ..common.general_function import raiseWarning
from .file_tex import MHWTexFile
from .file_dds import DDS, DX10_Header, DDSFile

DELETE_DDS = True


def TexToDDS(tex):
    """ Generates a DDS file from the 'imageIndex'th image in the tex file"""
    dds = DDS()
    dds.header.dwSize = 124
    # DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT | DDSD_MIPMAPCOUNT | DDSD_LINEARSIZE
    dds.header.dwFlags = 0x00000001 | 0x00000002 | 0x00000004 | 0x00001000 | 0x00020000 | 0x00080000
    dds.header.dwHeight = tex.header.height
    dds.header.dwWidth = tex.header.width
    # bpps = ddsBpps[texenum.texFormatToDXGIStringDict[tex.header.format]]
    bpps = tex.header.ddsbpps
    dds.header.dwPitchOrLinearSize = (
        dds.header.dwWidth * dds.header.dwHeight * bpps) // 8
    dds.header.dwDepth = tex.header.depth
    dds.header.dwMipMapCount = tex.header.mipCount
    dds.header.ddpfPixelFormat.dwSize = 32
    dds.header.ddpfPixelFormat.dwFlags = 0x4  # DDPF_FOURCC
    # dds.header.ddpfPixelFormat.dwFourCC = 808540228  # DX10
    dds.header.ddpfPixelFormat.dwFourCC = tex.header.ddsfourcc
    dds.header.ddpfPixelFormat.dwRGBBitCount = 0
    dds.header.ddpfPixelFormat.dwRBitMask = 0
    dds.header.ddpfPixelFormat.dwGBitMask = 0
    dds.header.ddpfPixelFormat.dwBBitMask = 0
    dds.header.ddpfPixelFormat.dwABitMask = 0
    dds.header.ddsCaps1 = 0x00000008 | 0x00001000 | 0x00400000  # DDSCAPS_COMPLEX | DDSCAPS_TEXTURE | DDSCAPS_MIPMAP
    # if tex.header.cubemapMarker != 0:
    #     dds.header.ddsCaps1 = dds.header.ddsCaps1 | 0x00000008  # DDSCAPS_COMPLEX
    #     # DDSCAPS2_CUBEMAP | DDSCAPS2_CUBEMAP_POSITIVEX | DDSCAPS2_CUBEMAP_NEGATIVEX | DDSCAPS2_CUBEMAP_POSITIVEY | DDSCAPS2_CUBEMAP_NEGATIVEY | DDSCAPS2_CUBEMAP_POSITIVEZ | DDSCAPS2_CUBEMAP_NEGATIVEZ
    #     dds.header.ddsCaps2 = 0x00000200 | 0x00000400 | 0x00000800 | 0x00001000 | 0x00002000 | 0x00004000 | 0x00008000
    # else:
    #     dds.header.ddsCaps2 = 0
    dds.header.ddsCaps2 = 0
    dds.header.ddsCaps3 = 0
    dds.header.ddsCaps4 = 0
    dds.header.dwReserved2 = 0

    if tex.header.ddsfourcc == 808540228:
        dds.header.dx10Header = DX10_Header()
        dds.header.dx10Header.dxgiFormat = tex.header.formatMap
        # D3D10_RESOURCE_DIMENSION_TEXTURE2D
        dds.header.dx10Header.resourceDimension = 3
        dds.header.dx10Header.miscFlags = 0
        dds.header.dx10Header.arraySize = 1
        dds.header.dx10Header.miscFlags2 = 0
    dds.data = bytes(tex.mipBuffer)
    return dds

# def convertTexFileToDDS(texPath, outputPath):
#     texFile = MHWTexFile()
#     texFile.read(texPath)
#
#     ddsFile = DDSFile()
#     ddsFile.dds = TexToDDS(texFile.tex)
#
#     ddsFile.write(outputPath)

def convertTexFileToDDS(tex, outputPath):
    ddsFile = DDSFile()
    ddsFile.dds = TexToDDS(tex)

    ddsFile.write(outputPath)

def convertFloatTexFile(tex, exrPath):
    if tex.header.format == 1:
        tex_array = np.frombuffer(tex.mipBuffer, dtype=np.float32)
    else:
        tex_array = np.frombuffer(tex.mipBuffer, dtype=np.float16)

    tex_array = tex_array.reshape([tex.header.height, tex.header.width, 4])
    tex_name = os.path.basename(exrPath)
    img = bpy.data.images.new(tex_name, height=tex_array.shape[0], width=tex_array.shape[1], alpha=True, float_buffer=True, is_data=True)
    img.pixels = (np.flip(tex_array, 0)).ravel()
    img.alpha_mode = "CHANNEL_PACKED"

    img.filepath_raw = exrPath
    img.file_format = 'OPEN_EXR'
    # 确保目录存在
    os.makedirs(os.path.dirname(exrPath), exist_ok=True)
    print("Writing " + exrPath)
    img.save() #将图像保存为exr文件

    if tex_name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[tex_name]) #删除新建的图像，避免后续每次新建图像时出现重复的图像（如test.exr，test.exr.001）



def checkColorSpace(img, filepath):
    filename = os.path.basename(filepath)

    if filename.lower().endswith(".tif"): #如果文件是tif格式，检查文件是否以"end='w'?>"字符串结尾
        target_bytes = b"end='w'?>"
        target_hex = b'\x65\x6E\x64\x3D\x27\x77\x27\x3F\x3E'  #等同于b"end='w'?>"

        with open(filepath, 'rb') as f:
            #跳转到文件末尾前9个字节
            f.seek(-len(target_bytes), 2)  #2表示从文件末尾计算
            last_bytes = f.read(len(target_bytes))
            #如果文件以"end='w'?>"字符串结尾，则颜色空间为Non-Color，否则为sRGB
            img.colorspace_settings.name = "Non-Color" if last_bytes == target_bytes else "sRGB"

    elif filename.lower().endswith(".exr"):  #如果文件是exr格式，颜色空间固定设为Non-Color
        img.colorspace_settings.name = "Non-Color"

    elif filename.lower().endswith(".dds"): #如果文件是dds格式，待做
        pass

    else:
        pass


def loadTex(texPath,outputPath,texConv,reloadCachedTextures,useDDS):
    ddsPath = os.path.splitext(outputPath)[0] + ".dds"
    # print(ddsPath)
    if useDDS: #若使用dds（仅在blender4.2版本以上有效），则输出文件扩展名为dds，否则为tif
        outputPath = ddsPath

    blenderImageList = None
    if not reloadCachedTextures and os.path.isfile(outputPath): #若不重载缓存贴图，且确实存在该dds或tif文件路径，则将该文件直接加载到blender中
        img = bpy.data.images.load(outputPath, check_existing=True)
        blenderImageList = [img]

        checkColorSpace(img, outputPath) #设置颜色空间
        return blenderImageList

    # if blenderImageList == None: #若重载缓存贴图，或该dds或tif文件路径不存在，则读取tex文件
    texFile = MHWTexFile()
    texFile.read(texPath)
    tex = texFile.tex

    if tex.header.format not in {1, 2}: #若tex文件format不为1或2，则将其转换为dds
        convertTexFileToDDS(tex, ddsPath)
        if not useDDS: #若不使用dds，则进一步将dds转换为tif
            texConv.convert_to_tif(ddsPath, out=os.path.dirname(outputPath), verbose=False)
    else: #若tex文件format为1或2，则考虑exr文件路径，不再转换为dds和tif
        exrPath = os.path.splitext(outputPath)[0] + ".exr"
        if not reloadCachedTextures and os.path.isfile(exrPath): #若不重载缓存贴图，且确实存在该exr文件路径，则将该文件直接加载到blender中
            img = bpy.data.images.load(exrPath, check_existing=True)
            blenderImageList = [img]
            img.colorspace_settings.name = "Non-Color"
            return blenderImageList #直接返回，避免后续继续向blender中加载文件
        else: #若重载缓存贴图，或该exr文件路径不存在，则将tex文件转换为exr
            convertFloatTexFile(tex, exrPath)
            outputPath = exrPath #输出文件路径改为exr文件的路径

    if os.path.isfile(outputPath): #若最后的输出文件路径确实存在，则将该文件直接加载到blender中
        img = bpy.data.images.load(outputPath, check_existing=not reloadCachedTextures)
        blenderImageList = [img]

        checkColorSpace(img, outputPath) #设置颜色空间


    if not useDDS and os.path.isfile(ddsPath): #若不使用dds，且确实存在该dds文件路径，则尝试直接删除该dds文件，否则抛出警告无法删除临时dds文件
        try:
            os.remove(ddsPath)
        except:
            raiseWarning(f"Could not delete temporary dds file: {ddsPath}")

    return blenderImageList

supportedImageExtensions = {".png", ".tga", ".tif"}  #Not implemented yet

# from addons.MHW_Model_Editor.ddsconv.texconv import Texconv
def convertTexDDSList(fileNameList, inDir, outDir):
    ddsConversionList = []
    texConversionList = []

    conversionCount = 0
    failCount = 0

    for fileName in fileNameList:
        fullPath = os.path.join(inDir, fileName)
        if os.path.isfile(fullPath):
            if fileName.lower().endswith(".dds"):
                path = os.path.join(inDir, fileName)
                ddsConversionList.append(path)
                print(str(path))
            elif fileName.lower().endswith(".tex"):
                path = os.path.join(inDir, fileName)
                texConversionList.append(path)
        elif os.path.splitext(fileName)[1] in supportedImageExtensions:
            pass  # TODO

    if ddsConversionList != []:
        os.makedirs(outDir, exist_ok=True)

        # # Single Texture Conversion
        # for ddsPath in ddsConversionList:
        #     texPath = os.path.join(outDir, os.path.splitext(os.path.split(ddsPath)[1])[0]) + f".tex"
        #     print(str(texPath))
        #     DDSToTex([ddsPath], texVersion, texPath, streamingFlag=False)  # TODO Streaming
        #     conversionCount += 1

    if texConversionList != []:
        # texconvert = Texconv()
        os.makedirs(outDir, exist_ok=True)
        for texPath in texConversionList:
            try:
                texFile = MHWTexFile()
                texFile.read(texPath)
                convertTexFileToDDS(texFile.tex, texPath.split(".tex")[0] + ".dds")
                # texconvert.convert_to_tif(texPath.split(".tex")[0] + ".dds", out=os.path.join(os.path.dirname(texPath), "tif"), verbose=False) #进一步转换成tif，测试用
                conversionCount += 1
            except Exception as err:
                print(f"Failed to convert {texPath} - {str(err)}")
                failCount += 1
    return (conversionCount, failCount)
























