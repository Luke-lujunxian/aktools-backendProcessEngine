# aktools-backend

# 使用方法<br>
调用`detection.request(modelPath, anchorsPath, classesPath, image)`将会返回一个list<br>
调用示例：<br>
`request(
    'ObjReg.h5',
    'objDetectionAnchor.txt',
    'itemList.txt',
    image
    )
`<br>
返回示例：<br>
`[['TKT_INST_FIN', None], ['TKT_RECRUIT', 1], ........]`<br>
