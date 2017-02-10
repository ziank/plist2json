# -*- coding:utf-8 -*-
#authour:ziank
from plist.plist import Plist
from plist.bplist import BPlist
import json as JSON

def convertPlistToJson(plistContent):
    json = None
    if BPlist.isBinaryPlist(plistContent):
        bplist = BPlist(plistContent)
        json = bplist.getjson()
    else:
        plist = Plist(plistContent)
        json = plist.getjson()
    jsonStr = JSON.dumps(json, ensure_ascii=False, indent=4)
    return jsonStr

def testBPlist():
    content = open("city.plist", "rb").read()
    print(convertPlistToJson(content));

def testPlist():
    content = open("info.plist", "rb").read()
    print(convertPlistToJson(content));


if __name__ == '__main__':
    testBPlist()
    testPlist()
