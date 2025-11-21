# -*- coding: utf-8 -*-
import bpy
import os
import numpy as np
from ..common.message_functions import raiseWarning
from ..ddsconv.util import is_windows
from ..ddsconv.dds import DDSHeader
from .file_tex import MHWTexFile, DXGI_FORMAT_INFO
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
    img.save()  # 将图像保存为exr文件

    if tex_name in bpy.data.images:
        bpy.data.images.remove(bpy.data.images[tex_name])  # 删除新建的图像，避免后续每次新建图像时出现重复的图像（如test.exr，test.exr.001）



def checkColorSpace(img, filepath):
    filename = os.path.basename(filepath).lower()

    if filename.endswith(".tif"):  # 如果文件是tif格式，检查文件是否以"end='w'?>"字符串结尾
        target_bytes = b"end='w'?>"
        target_hex = b'\x65\x6E\x64\x3D\x27\x77\x27\x3F\x3E'  # 等同于b"end='w'?>"

        with open(filepath, 'rb') as f:
            # 跳转到文件末尾前9个字节
            f.seek(-len(target_bytes), 2)  # 2表示从文件末尾计算
            last_bytes = f.read(len(target_bytes))
            # 如果文件以"end='w'?>"字符串结尾，则颜色空间为Non-Color，否则为sRGB
            img.colorspace_settings.name = "Non-Color" if last_bytes == target_bytes else "sRGB"

    elif filename.endswith(".tga"):  # 如果文件是tga格式
        pass

    elif filename.endswith(".exr"):  # 如果文件是exr格式，颜色空间固定设为Non-Color
        img.colorspace_settings.name = "Non-Color"

    elif filename.endswith(".dds"):  # 如果文件是dds格式，检查文件的dxgiFormat是否包含SRGB字符串
        dds_header = DDSHeader.read_from_file(filepath)
        img.colorspace_settings.name = "sRGB" if "SRGB" in dds_header.get_format_as_str() else "Non-Color"
    else:
        pass


def loadTex(texPath,outputPath,texConv,reloadCachedTextures,useDDS):
    ddsPath = os.path.splitext(outputPath)[0] + ".dds"
    convertDDSFormat = None
    # print(ddsPath)

    if useDDS:  # 若使用dds（仅在blender4.2版本以上有效），则输出文件扩展名为dds，否则转换为其他格式
        outputPath = ddsPath
    else:
        if is_windows():  # 如果是windows平台，则转换为tif，否则转换为tga
            outputPath = os.path.splitext(outputPath)[0] + ".tif"
            convertDDSFormat = texConv.convert_to_tif
        else:
            outputPath = os.path.splitext(outputPath)[0] + ".tga"
            convertDDSFormat = texConv.convert_to_tga

    blenderImageList = None
    if not reloadCachedTextures and os.path.isfile(outputPath):  # 若不重载缓存贴图，且确实存在该dds或其他格式文件路径，则将该文件直接加载到blender中
        img = bpy.data.images.load(outputPath, check_existing=True)
        blenderImageList = [img]

        checkColorSpace(img, outputPath)  # 设置颜色空间
        return blenderImageList

    # if blenderImageList == None:  # 若重载缓存贴图，或该dds或其他格式文件路径不存在，则读取tex文件
    texFile = MHWTexFile()
    texFile.read(texPath)
    tex = texFile.tex

    if tex.header.format not in {1, 2}:  # 若tex文件format不为1或2，则将其转换为dds
        convertTexFileToDDS(tex, ddsPath)
        if not useDDS:  # 若不使用dds，则进一步将dds转换为其他格式
            convertDDSFormat(ddsPath, out=os.path.dirname(outputPath), invert_normals=False, verbose=False)
            # texConv.convert_to_tif(ddsPath, out=os.path.dirname(outputPath), invert_normals=False, verbose=False)

            # 考虑到在linux平台上，texconv不支持转换为tif格式，所以改为更加通用的tga格式
            # texConv.convert_to_tga(ddsPath, out=os.path.dirname(outputPath), verbose=False)

    else:  # 若tex文件format为1或2，则考虑exr文件路径，不再转换为dds和tif
        exrPath = os.path.splitext(outputPath)[0] + ".exr"
        if not reloadCachedTextures and os.path.isfile(exrPath):  # 若不重载缓存贴图，且确实存在该exr文件路径，则将该文件直接加载到blender中
            img = bpy.data.images.load(exrPath, check_existing=True)
            blenderImageList = [img]
            img.colorspace_settings.name = "Non-Color"
            return blenderImageList  # 直接返回，避免后续继续向blender中加载文件
        else:  # 若重载缓存贴图，或该exr文件路径不存在，则将tex文件转换为exr
            convertFloatTexFile(tex, exrPath)
            outputPath = exrPath  # 输出文件路径改为exr文件的路径

    if os.path.isfile(outputPath):  # 若最后的输出文件路径确实存在，则将该文件直接加载到blender中
        img = bpy.data.images.load(outputPath, check_existing=not reloadCachedTextures)
        blenderImageList = [img]

        checkColorSpace(img, outputPath)  # 设置颜色空间


    if not useDDS and os.path.isfile(ddsPath):  # 若不使用dds，且确实存在该dds文件路径，则尝试直接删除该dds文件，否则抛出警告无法删除临时dds文件
        try:
            os.remove(ddsPath)
        except:
            raiseWarning(f"Could not delete temporary dds file: {ddsPath}")

    return blenderImageList


DXGI_FORMAT_TO_MHW_FORMAT = {
    0: ("UNKNOWN", 0),
    2: ("R32G32B32A32FLOAT", 1),
    10: ("R16G16B16A16FLOAT", 2),
    28: ("R8G8B8A8UNORM", 7),
    29: ("R8G8B8A8UNORMSRGB", 9),
    49: ("R8G8UNORM", 19),
    71: ("BC1UNORM", 22),
    72: ("BC1UNORMSRGB", 23),
    80: ("BC4UNORM", 24),
    83: ("BC5UNORM", 26),
    95: ("BC6HUF16", 28),
    96: ("BC6HSF16", 29),
    98: ("BC7UNORM", 30),
    99: ("BC7UNORMSRGB", 31),
}

# From https://github.com/JodoZT/MHWTexConvertor的导出部分代码
def DDSToTex(ddsList):
    ddsHeader = ddsList[0].header

    newTexFile = MHWTexFile()
    texHeader = newTexFile.tex.header

    isRaw = (ddsHeader.dwFlags & 0x8 == 0x8)
    texHeader.mipCount = ddsHeader.dwMipMapCount
    texHeader.width = ddsHeader.dwWidth
    texHeader.height = ddsHeader.dwHeight
    # texHeader.depth = ddsHeader.dwDepth
    texHeader.depth = 1  # 暂时固定为1
    texHeader.ddsfourcc = ddsHeader.ddpfPixelFormat.dwFourCC

    # if texHeader.ddsfourcc == 808540228:  # DX10
    if ddsHeader.dx10Header:  # DX10
        texHeader.formatName, texHeader.format = DXGI_FORMAT_TO_MHW_FORMAT.get(ddsHeader.dx10Header.dxgiFormat, ("", 0))
    elif texHeader.ddsfourcc == 827611204:  # DXT1
        texHeader.format = 22
        texHeader.formatName = "BC1UNORM"
    elif texHeader.ddsfourcc == 1429488450:  # BC4U
        texHeader.format = 24
        texHeader.formatName = "BC4UNORM"
    elif texHeader.ddsfourcc in {1429553986, 843666497}:  # BC5U或ATI2
        texHeader.format = 26
        texHeader.formatName = "BC5UNORM"
    elif texHeader.ddsfourcc == 0 and isRaw:
        texHeader.format = 7
        texHeader.formatName = "R8G8B8A8UNORM"

    # if texHeader.formatName == "":
    if texHeader.format == 0:
        raise Exception(f"Unsupported DDS format.")

    _, texHeader.ddsbpps, _, _ = DXGI_FORMAT_INFO.get(texHeader.formatName)

    if texHeader.formatName in {"BC6HUF16", "BC7UNORM", "BC7UNORMSRGB"}:
        texHeader.newDDSFlag = 1

    texHeader.width2 = texHeader.width // 2
    if isRaw or texHeader.formatName == "R8G8UNORM":
        texHeader.width2 = texHeader.width

    curWidth = texHeader.width
    curHeight = texHeader.height
    mipOffset = 0xB8 + texHeader.mipCount * 8
    maxWidth = 2 if isRaw else 4

    if texHeader.ddsbpps == 4:
        multi = 1
    elif texHeader.ddsbpps == 16:
        multi = 2
    elif isRaw:
        multi = 4
    else:
        multi = 1

    for i in range(texHeader.mipCount):
        newTexFile.tex.mipOffsetList.append(mipOffset)

        if texHeader.ddsbpps == 4:
            mipOffset += curWidth * curHeight // 2
        else:
            mipOffset += curWidth * curHeight * multi

        curWidth = max(curWidth // 2, maxWidth)
        curHeight = max(curHeight // 2, maxWidth)

    newTexFile.tex.mipBuffer = bytearray(ddsList[0].data)

    # texHeader.imageCount = imageCount
    # texHeader.mipCount = ddsHeader.dwMipMapCount  # For DMC5/RE2
    # texHeader.imageMipHeaderSize = ddsHeader.dwMipMapCount << 4
    # #texHeader.imageCount = (ddsHeader.dwMipMapCount << 12) | imageCount
    # #print(f"imageCount {imageCount}")
    # #print(f"dwMipMapCount {ddsHeader.dwMipMapCount}")
    # #print(f"tex image count {texHeader.imageCount}")
    # texHeader.formatString = format_ops.buildFormatString(ddsHeader)
    # texHeader.format = texenum.formatStringToTexFormatDict[texHeader.formatString]
    # cubemap = (ddsHeader.ddsCaps2 & 0x00000200 != 0)*1  # DDSCAPS2_CUBEMAP
    # texHeader.cubemapMarker = cubemap * 4
    return newTexFile


def convertDDSFileToTex(ddsPathList, outPath):
    if len(ddsPathList) == 1:
        ddsFile = DDSFile()
        ddsFile.read(ddsPathList[0])
        # ddsHeader = [ddsFile.dds][0].header

        # texFile = getTexFileFromDDS([ddsFile.dds])
        # texFile = DDSToTex(ddsHeader, len([ddsFile.dds]))
        texFile = DDSToTex([ddsFile.dds])
        # texFile.tex.mipBuffer = bytearray([ddsFile.dds][0].data)

        texFile.write(outPath)
    else:
        pass
    # else:  # Array texture
    #     baseHeader = getDDSHeader(ddsPathList[0])
    #     # Preparse dds files to make sure they have the same height,width,format and mip count as the first
    #     valid = True
    #     fixDDSMipList = []  # Force mip counts to match first dds in array
    #     for ddsPath in ddsPathList:
    #
    #         currentHeader = getDDSHeader(ddsPath)
    #         if currentHeader.dwWidth != baseHeader.dwWidth:
    #             raiseWarning(
    #                 f"{os.path.split(ddsPath)[1]} - Width does not match first array texture.")
    #             valid = False
    #         if currentHeader.dwHeight != baseHeader.dwHeight:
    #             raiseWarning(
    #                 f"{os.path.split(ddsPath)[1]} - Height does not match first array texture.")
    #             valid = False
    #         if currentHeader.dwMipMapCount != baseHeader.dwMipMapCount:
    #             raiseWarning(
    #                 f"{os.path.split(ddsPath)[1]} - Mipmap count does not match first array texture.")
    #             fixDDSMipList.append(ddsPath)
    #             #valid = False
    #         if currentHeader.dx10Header == None:
    #             raiseWarning(
    #                 f"{os.path.split(ddsPath)[1]} - DX10 header is missing, save the DDS file using Photoshop with the Intel DDS plugin.")
    #             valid = False
    #         else:
    #             if baseHeader.dx10Header != None:
    #                 if currentHeader.dx10Header.dxgiFormat != baseHeader.dx10Header.dxgiFormat:
    #                     raiseWarning(
    #                         f"{os.path.split(ddsPath)[1]} - DDS format ({dxgienum.DXGIToFormatStringDict.get(currentHeader.dx10Header.dxgiFormat)}) does not match first array texture ({dxgienum.DXGIToFormatStringDict.get(baseHeader.dx10Header.dxgiFormat)}).")
    #                     valid = False
    #
    #     if valid:
    #         if fixDDSMipList != []:
    #             texConv = Texconv()
    #             for fixPath in fixDDSMipList:
    #                 print(f"Fixing mip count on {os.path.split(fixPath)[1]}")
    #                 texConv.fix_mip_count(fixPath, os.path.split(
    #                     fixPath)[0], baseHeader.dwMipMapCount)
    #             unload_texconv()
    #
    #         ddsList = []
    #         for ddsPath in ddsPathList:
    #             ddsFile = DDSFile()
    #             ddsFile.read(ddsPath)
    #             ddsList.append(ddsFile.dds)
    #
    #         texFile = getTexFileFromDDS(ddsList, texVersion, streamingFlag)
    #         texFile.write(outPath)


supportedImageExtensions = {".png", ".tga", ".tif"}  # Not implemented yet
def convertTexDDSList(fileNameList, inDir, outDir, addFolder=False, addPrefix=False):
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
                # print(str(path))
            elif fileName.lower().endswith(".tex"):
                path = os.path.join(inDir, fileName)
                texConversionList.append(path)
        elif os.path.splitext(fileName)[1] in supportedImageExtensions:
            pass  # TODO

    if ddsConversionList != []:
        if addFolder:  # 如果勾选添加转换文件夹，则额外创建一个新的文件夹用于统一存放文件
            outDir = os.path.join(outDir, "Converted_MHW_Tex")
        os.makedirs(outDir, exist_ok=True)

        # Single Texture Conversion
        for ddsPath in ddsConversionList:
            try:
                convertedPath = os.path.join(outDir, os.path.splitext(os.path.split(ddsPath)[1])[0]) + ".tex"
                # print(str(convertedPath))

                convertDDSFileToTex([ddsPath], convertedPath)  # TODO Streaming
                conversionCount += 1
            except Exception as err:
                print(f"Failed to convert {ddsPath} - {str(err)}")
                failCount += 1

    if texConversionList != []:
        if addFolder:  # 如果勾选添加转换文件夹，则额外创建一个新的文件夹用于统一存放文件
            outDir = os.path.join(outDir, "Converted_MHW_DDS")
        os.makedirs(outDir, exist_ok=True)

        for texPath in texConversionList:
            try:
                texFile = MHWTexFile()
                texFile.read(texPath)

                fileName = os.path.splitext(os.path.split(texPath)[1])[0] + ".dds"
                if addPrefix:  # 如果勾选添加格式前缀，则在转换后的dds文件的文件名前面添加dxgiformat前缀
                    fileName = texFile.tex.header.tag + fileName

                convertedPath = os.path.join(outDir, fileName)
                # convertTexFileToDDS(texFile.tex, texPath.split(".tex")[0] + ".dds")
                convertTexFileToDDS(texFile.tex, convertedPath)

                conversionCount += 1
            except Exception as err:
                print(f"Failed to convert {texPath} - {str(err)}")
                failCount += 1
    return conversionCount, failCount
























