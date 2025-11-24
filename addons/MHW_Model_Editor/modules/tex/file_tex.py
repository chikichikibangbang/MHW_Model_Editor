# -*- coding: utf-8 -*-
import bpy
from ..common.message_functions import raiseError, raiseTexError
from ..common.rw_functions import read_ubyte,read_byte,read_short,read_ushort,read_uint,read_int,read_uint64,\
    read_int64,read_float,read_double,read_string,read_unicode_string,write_ubyte,write_byte,write_short,write_ushort,\
    write_uint,write_int,write_uint64,write_int64,write_float,write_double,write_string,write_unicode_string,\
    getPaddingAmount,getPaddedPos
from .....common.i18n.i18n import i18n

MHW_TEX_FORMAT = {
    0: "UNKNOWN",
    1:"R32G32B32A32FLOAT",
    2:"R16G16B16A16FLOAT",
    7: "R8G8B8A8UNORM",
    9: "R8G8B8A8UNORMSRGB",  # LUTs
    19: "R8G8UNORM",
    22: "BC1UNORM",
    23: "BC1UNORMSRGB",
    24: "BC4UNORM",
    26: "BC5UNORM",
    28: "BC6HUF16",
    29:"BC6HSF16",
    30: "BC7UNORM",
    31: "BC7UNORMSRGB",
}

# DXGI格式映射到标准DXGI_FORMAT值
# 键值元组中的值分别为DXGI_FORMAT_MAP，DDS_BPPS，FOURCC和TAG
DXGI_FORMAT_INFO = {
    "UNKNOWN": (0, 0, 1313558101, "UNKN_"),
    "R32G32B32A32FLOAT": (2, 128, 808540228, "FR32G32B32A32_"),
    "R16G16B16A16FLOAT": (10, 64, 808540228, "FR16G16B16A16_"),
    "R8G8B8A8UNORM": (28, 32, 808540228, "R8G8B8A8_"),
    "R8G8B8A8UNORMSRGB": (29, 32, 808540228, "SR8G8B8A8_"),
    "R8G8UNORM": (49, 16, 808540228, "R8G8_"),
    "BC1UNORM": (71, 4, 827611204, "DXT1L_"),
    "BC1UNORMSRGB": (72, 4, 808540228, "BC1S_"),
    "BC4UNORM": (80, 4, 1429488450, "BC4_"),
    "BC5UNORM": (83, 8, 1429553986, "BC5_"),
    "BC6HUF16": (95, 8, 808540228, "BC6_"),
    "BC6HSF16": (96, 8, 808540228, "BC6_"),
    "BC7UNORM": (98, 8, 808540228, "BC7L_"),
    "BC7UNORMSRGB": (99, 8, 808540228, "BC7S_")
}

class TexHeader():
    def __init__(self):
        self.magic = 5784916
        self.version = 16
        self.always0 = 0  # uint64
        self.always2 = 2  # uint

        self.mipCount = 0
        self.width = 0
        self.height = 0
        self.depth = 1
        self.format = 0

        # 用于转换的各种参数
        self.formatName = ""
        self.formatMap = 0
        self.ddsbpps = 0
        self.ddsfourcc = 0
        self.tag = ""

        # 写入文件用
        self.newDDSFlag = 0
        self.width2 = 0

    def read(self, file):
        self.magic = read_uint(file)
        if self.magic != 5784916:
            # raiseTexError("File is not a MHW Tex file.")
            raise Exception(i18n("File is not a MHW Tex file."))
        self.version = read_uint(file)
        if self.version != 16:
            # raiseTexError("File is not a MHW Tex file, maybe from other games.")
            raise Exception(i18n("File is not a MHW Tex file, maybe from other games."))

        file.seek(0x14)
        self.mipCount = read_uint(file)
        self.width = read_uint(file)
        self.height = read_uint(file)
        self.depth = read_uint(file)
        self.format = read_uint(file)
        if self.format not in MHW_TEX_FORMAT or self.format == 0:
            # raiseTexError(f"Unknown MHW Tex format {self.format}.")
            raise Exception(f"{i18n('Unknown MHW Tex format')} {self.format}.")
        else:
            self.formatName = MHW_TEX_FORMAT[self.format]
            self.formatMap, self.ddsbpps, self.ddsfourcc, self.tag = DXGI_FORMAT_INFO[self.formatName]

    def write(self, file):
        write_uint(file, self.magic)
        write_uint(file, self.version)
        write_uint64(file, self.always0)
        write_uint(file, self.always2)

        write_uint(file, self.mipCount)
        write_uint(file, self.width)
        write_uint(file, self.height)
        write_uint(file, self.depth)
        write_uint(file, self.format)

        # 写入28个未知字节
        write_uint64(file, 1)
        write_uint64(file, 0)
        write_uint64(file, 4294967295)
        write_uint(file, 0)

        # 写入新格式标记
        write_uint(file, self.newDDSFlag)
        file.write(b'\x00' * 16)
        file.write(b'\xFF' * 32)

        # 写入长宽字段
        write_uint(file, self.width)
        for i in range(3):
            write_ushort(file, self.width2)
            write_ushort(file, self.width)
            file.write(b'\x00' * 8)
        file.write(b'\x00' * 24)


class MHWTex():
    def __init__(self):
        self.header = TexHeader()
        # self.mipdataList = []
        self.mipOffsetList = []
        self.mipBuffer = bytearray()

    def read(self, file):
        self.header.read(file)

        file.seek(0xB8)
        for i in range(self.header.mipCount):
            self.mipOffsetList.append(read_uint64(file))

        # file.seek(read_uint64(file))
        file.seek(self.mipOffsetList[0])

        if self.header.format not in {1, 2}:
            self.mipBuffer.extend(file.read())
        else:
            if self.header.mipCount > 1:  # 暂不确定format为1和2的tex文件是否mipCount都等于1，所以这里只取最大的mipmap读取
                self.mipBuffer.extend(file.read(self.mipOffsetList[1] - self.mipOffsetList[0]))
            else:
                self.mipBuffer.extend(file.read())

    def write(self, file):
        self.header.write(file)
        for offset in self.mipOffsetList:
            write_uint64(file, offset)
        file.write(self.mipBuffer)


class MHWTexFile:
    def __init__(self):
        self.tex = MHWTex()

    def read(self, filePath):
        lang = bpy.context.preferences.view.language
        # print("Opening " + filePath)
        try:
            file = open(filePath, "rb")
        except:
            if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                raiseError(f"打开 {filePath} 失败")
            else:
                raiseError(f"Failed to open {filePath}")
        self.tex.read(file)
        file.close()

    def write(self, filePath):
        lang = bpy.context.preferences.view.language
        print(i18n("Writing ") + filePath)
        try:
            file = open(filePath, "wb")
        except:
            if lang in {"zh_CN", "zh_HANS", "zh_TW", "zh_HANT"}:
                raiseError(f"打开 {filePath} 失败")
            else:
                raiseError(f"Failed to open {filePath}")
        self.tex.write(file)
        file.close()
