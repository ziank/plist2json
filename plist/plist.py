# -*- coding:utf-8 -*-
#authour:ziank
from xml.etree import ElementTree as etree
import collections

class Plist:
    jsonObj = None

    def __init__(self, content):
        self.convertToJson(content)

    def convertToJson(self, plistContent):
        plist = etree.fromstring(plistContent)
        dic = plist.getchildren()[0]
        self.jsonObj = self.getTagValue(dic)

    def convertDictTagToJson(self, dic):
        tagList = dic.getchildren()
        json = collections.OrderedDict()
        for index in range(0, len(tagList), 2):
            key = tagList[index]
            value = tagList[index + 1]
            json[key.text] = self.getTagValue(value)

        return json

    def converArrayTagToJson(self, tag):
        children = tag.getchildren()
        json = []
        for child in children:
            json.append(self.getTagValue(child))

        return json

    def getTagValue(self, tag):
        if tag.tag == "dict":
            return self.convertDictTagToJson(tag)
        elif tag.tag == "array":
            return self.converArrayTagToJson(tag)
        elif tag.tag == "true":
            return True
        elif tag.tag == "false":
            return False
        elif tag.tag == "number":
            return int(tag.text)
        else:
            return tag.text

    def getjson(self):
        return self.jsonObj
