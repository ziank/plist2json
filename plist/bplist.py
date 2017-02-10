# -*- coding:utf-8 -*-
#authour:ziank
import struct
import array
import json

class Index:
    index = -1
    def __init__(self, index):
        self.index = index

class BPlist:
    data = ""
    offsetTable = ()
    objectList = []
    offsetLen = 0

    @staticmethod
    def isBinaryPlist(data):
        if len(data) < 8:
            return False
        if data[:8] == b"bplist00":
            return True
        else:
            return False

    def __init__(self, data):
        if BPlist.isBinaryPlist(data=data):
            self.data = data
            self.parseData()

    def parseData(self):
        tail = self.data[-32:]
        (blank, L, M, N, T, K) = struct.unpack("!6s2c3Q", tail)
        L, M = (ord(L), ord(M))
        offsetData = self.data[K:K + L * N]
        offsetData = array.array("B", offsetData)
        self.offsetTable = [self.getNumber(x, L, offsetData) for x in range(0, len(offsetData), L)]

        i = 0
        while i < len(self.offsetTable):
            subStr = ""
            if i != len(self.offsetTable) - 1:
                subStr = self.data[self.offsetTable[i]:self.offsetTable[i + 1]]
            else:
                subStr = self.data[self.offsetTable[i]:K]
            self.objectList.append(self.parseObj(subStr))
            i += 1

        for obj in self.objectList:
            if type(obj) == list:
                index = 0
                while index < len(obj):
                    item = obj[index]
                    if type(item) == Index:
                        obj.remove(item)
                        obj.insert(index, self.objectList[item.index])
                    index += 1
            if type(obj) == dict:
                for key, val in obj.items():
                    if type(key) == Index:
                        obj.pop(key)
                        obj[self.objectList[key.index]] = self.objectList[val.index]

    def parseObj(self, str):
        typechar = str[0] // 16
        X = str[0] % 16
        headLen = 1
        if typechar == 0:
            if X == 8:
                return False
            elif X == 9:
                return True
            else:
                return None
        elif typechar == 1:
            intLen = pow(2, X)
            return self.getNumber(1, intLen, str)
        elif typechar == 2:
            intLen = pow(2, X)
            if intLen <= 4:
                return struct.unpack("!f", b'\x00' * (4 - intLen) + str)
            else:
                return struct.unpack("!d", b'\x00' * (8 - intLen) + str)
        elif typechar == 3:
            return struct.unpack("!d", str)
        elif typechar == 4:
            return struct.unpack("!%ds" % X, str)
        elif typechar == 5:
            strLen = 0
            strStart = 0
            if X == 0x0F:
                intLen = pow(2, str[1] % 16)
                strLen = self.parseObj(str[1:intLen + 2])
                strStart = intLen + 2
            else:
                strLen = X
                strStart = 1
            return struct.unpack("%ds" % strLen, str[strStart:])[0].decode()

        elif typechar == 6:
            strLen = 0
            strStart = 0
            if X == 0x0F:
                intLen = pow(2, str[1] % 16)
                strLen = self.parseObj(str[1:intLen + 2])
                strStart = intLen + 2
            else:
                strLen = X
                strStart = 1
            strList = struct.unpack("!%dH" % strLen, str[strStart:])
            strList = [chr(x) for x in strList]
            return "".join(strList)

        elif typechar == 8:
            return struct.unpack("%ds" % (X+1), str)

        elif typechar == 10 or typechar == 12:
            arrayLen = 0
            arrayStartPos = 0
            if X == 0x0F:
                intLen = pow(2, str[1] % 16)
                arrayLen = self.parseObj(str[1:intLen + 2])
                arrayStartPos = intLen + 2
            else:
                arrayLen = X
                arrayStartPos = 1

            if self.offsetLen == 0:
                self.offsetLen = (len(str) - arrayStartPos) // arrayLen
            arrayData = array.array("B", str[arrayStartPos:])
            return [self.getIndex(x, self.offsetLen, arrayData) for x in range(0, arrayLen * self.offsetLen, self.offsetLen)]

        elif typechar == 13:
            dictLen = 0
            dictStartPos = 0
            if X == 0x0F:
                intLen = pow(2, str[1] % 16)
                dictLen = self.parseObj(str[1:intLen + 2])
                dictStartPos = intLen + 2
            else:
                dictLen = X
                dictStartPos = 1

            if self.offsetLen == 0:
                self.offsetLen = (len(str) - dictStartPos) // dictLen // 2
            dictData = array.array("B", str[dictStartPos:])
            keyValues = [self.getIndex(x, self.offsetLen, dictData) for x in range(0, dictLen * 2 * self.offsetLen, self.offsetLen)]
            result = {}
            for i in range(0, dictLen):
                result[keyValues[i]] = keyValues[i + dictLen]
            return  result

    def getjson(self):
        return self.objectList[0]

    def getIndex(self, x, L, offset):
        return Index(self.getNumber(x, L, offset))

    def getNumber(self, x, L, offset):
        num = L - 1
        result = 0
        while num >= 0:
            result += offset[x] * pow(256, num)
            num -= 1
            x += 1
        return result


if __name__ == '__main__':
    data = open("city.plist", "rb").read()
    bplist = BPlist(data)
    print(json.dumps(bplist.getjson(), indent=4))
