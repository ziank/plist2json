### 使用Python转换plist到json

同时支持binary和xml两种格式的plist转换成json，对于xml格式，使用系统自动ET库进行解析；对于binary格式的plist文件，使用struct库进行处理，把plist文件格式的数据转换为JSON格式。

具体使用方式可以参考示例代码。

**需要注意的是，如果要做大量转换的话，转换时一定要先判断是否为binary格式。**

```python
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
```

