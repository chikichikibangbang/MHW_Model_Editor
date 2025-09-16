# -*- coding: utf-8 -*-
from ..common.general_function import raiseError, read_uint, read_uint64, raiseTexError

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
DXGI_FORMAT_MAP = {
    "UNKNOWN": 0,
    "R32G32B32A32FLOAT": 2,
    "R16G16B16A16FLOAT": 10,
    "R8G8B8A8UNORM": 28,
    "R8G8B8A8UNORMSRGB": 29,
    "R8G8UNORM": 49,
    "BC1UNORM": 71,
    "BC1UNORMSRGB": 72,
    "BC4UNORM": 80,
    "BC5UNORM": 83,
    "BC6HUF16": 95,
    "BC6HSF16": 96,
    "BC7UNORM": 98,
    "BC7UNORMSRGB": 99
}

DDS_BPPS = {
    "UNKNOWN": 0,
    "R32G32B32A32FLOAT": 128,
    "R16G16B16A16FLOAT": 64,
    "R8G8B8A8UNORM": 32,
    "R8G8B8A8UNORMSRGB": 32,
    "R8G8UNORM": 16,
    "BC1UNORM": 4,
    "BC1UNORMSRGB": 4,
    "BC4UNORM": 4,
    "BC5UNORM": 8,
    "BC6HUF16": 8,
    "BC6HSF16": 8,
    "BC7UNORM": 8,
    "BC7UNORMSRGB": 8,
}

FORMAT_TO_FOURCC = {
    "UNKNOWN": 1313558101, #UNKNS
    "R32G32B32A32FLOAT": 808540228, #DX10
    "R16G16B16A16FLOAT": 808540228, #DX10
    "R8G8B8A8UNORM": 808540228, #DX10
    "R8G8B8A8UNORMSRGB": 808540228, #DX10
    "R8G8UNORM": 808540228, #DX10
    "BC1UNORM": 827611204, #DXT1
    "BC1UNORMSRGB": 808540228, #DX10
    "BC4UNORM": 1429488450, #BC4U
    "BC5UNORM": 1429553986, #BC5U
    "BC6HUF16": 808540228, #DX10
    "BC6HSF16": 808540228, #DX10
    "BC7UNORM": 808540228, #DX10
    "BC7UNORMSRGB": 808540228 #DX10
}

FORMAT_TO_TAG = {
    "UNKNOWN": "UNKN_",
    "R32G32B32A32FLOAT": "FR32G32B32A32_",
    "R16G16B16A16FLOAT": "FR16G16B16A16_",
    "R8G8B8A8UNORM": "R8G8B8A8_",
    "R8G8B8A8UNORMSRGB": "SR8G8B8A8_",
    "R8G8UNORM": "R8G8_",
    "BC1UNORM": "DXT1L_",
    "BC1UNORMSRGB": "BC1S_",
    "BC4UNORM": "BC4_",
    "BC5UNORM": "BC5_",
    "BC6HUF16": "BC6_",
    "BC6HSF16": "BC6_",
    "BC7UNORM": "BC7L_",
    "BC7UNORMSRGB": "BC7S_"
}

class TexHeader():
    def __init__(self):
        self.magic = 5784916
        self.version = 16
        self.always0 = 0 #uint64
        self.always2 = 2 #uint

        self.mipCount = 0
        self.width = 0
        self.height = 0
        self.depth = 0
        self.format = 0

        #用于转换的各种参数
        self.formatName = ""
        self.formatMap = 0
        self.ddsbpps = 0
        self.ddsfourcc = 0
        self.tag = ""

        self.packetSizeData = None  # Internal, for reading texture data with cursed pitch

    def read(self, file):
        self.magic = read_uint(file)
        if self.magic != 5784916:
            raiseTexError("File is not a MHW Tex file.")
        self.version = read_uint(file)
        if self.version != 16:
            raiseTexError("File is not a MHW Tex file, maybe from other games.")

        file.seek(0x14)
        self.mipCount = read_uint(file)
        self.width = read_uint(file)
        self.height = read_uint(file)
        self.depth = read_uint(file)
        self.format = read_uint(file)
        if self.format not in MHW_TEX_FORMAT or self.format == 0:
            raiseTexError(f"Unknown MHW Tex format {self.format}.")
        else:
            self.formatName = MHW_TEX_FORMAT[self.format]
            self.formatMap = DXGI_FORMAT_MAP[self.formatName]
            self.ddsbpps = DDS_BPPS[self.formatName]
            self.ddsfourcc = FORMAT_TO_FOURCC[self.formatName]
            self.tag = FORMAT_TO_TAG[self.formatName]



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
            if self.header.mipCount > 1: #暂不确定format为1和2的tex文件是否mipCount都等于1，所以这里只取最大的mipmap读取
                self.mipBuffer.extend(file.read(self.mipOffsetList[1] - self.mipOffsetList[0]))
            else:
                self.mipBuffer.extend(file.read())



        # print(self.mipBuffer)

        # data_offsets = []
        # data_sizes = []


class MHWTexFile:
    def __init__(self):
        self.tex = MHWTex()

    def read(self, filePath):
        #print("Opening " + filePath)
        try:
            file = open(filePath, "rb")
        except:
            raiseError("Failed to open " + filePath)
        self.tex.read(file)
        file.close()

    def write(self, filePath):
        print("Writing " + filePath)
        try:
            file = open(filePath, "wb")
        except:
            raiseError("Failed to open " + filePath)
        self.tex.write(file)
        file.close()





