import base64
import os
import random
import re
from io import BytesIO

from PIL import Image

import darknet
from yolo import YOLO


def request(modelPath, anchorsPath, classesPath, image):
    # parser = init()
    FLAGS = {
        "model_path": modelPath,
        "anchors_path": anchorsPath,
        "classes_path": classesPath,
        "score": 0.5,
        "iou": 0.45,
        "model_image_size": (416, 416),
        "gpu_num": 0,
    }


    # detect_img(YOLO(FLAGS),image,FLAGSnum)
    print(detect_img(YOLO(FLAGS), image))


def detect_img(objReg, image):
    resultList = []
    base64_data = re.sub('^data:image/.+;base64,', '', image)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    image = Image.open(image_data)
    # image.show()
    out_boxes, out_scores, out_classes = objReg.detect_image(image)
    # print(out_boxes,out_classes,out_scores)
    # objReg.close_session()
    objReg.close_session()
    resName = open('itemList.txt').readlines()
    # print(type(out_classes))
    net = darknet.load_net(b"modelData/yolov3-tiny.cfg", b"modelData/yolov3-tiny_final.weights", 0)
    meta = darknet.load_meta(b"modelData/data2.data")
    for i in range(out_classes.tolist().__len__()):
        top, left, bottom, right = out_boxes[i]
        size = max(right - left, bottom - top)
        temp = image.crop((left, top, left + size, top + size))
        try:
            filename = str(int(random.uniform(100000, 10000000)))
            try:
                temp.save('temp/' + filename + '.jpg')
            except OSError:
                temp = temp.convert('RGB')
                temp.save('temp/' + filename + '.jpg')
            string = 'temp/' + filename + '.jpg'
            #temp.show()
            resultList.append(
                [resName[out_classes[i]].replace('\n', ''),
                 getNum(darknet.detect(net, meta, bytes(string, encoding='utf8')))])
            # temp.show()
            # print(resultList[-1])
        finally:
            os.remove('temp/' + filename + '.jpg')
    return resultList


FLAGS = None


# The code above and yolo.py are modified from original code writtened by @qqwweee
# https://github.com/qqwweee/keras-yolo3
# The Original Code is using MIT license,
# DO NOT remove this statement


def getNum(results):
    if results == []:
        #print("Failed")
        return
    #print(results)
    out_boxes = []
    out_scores = []
    out_classes = []
    for result in results:
        if result[1] < 0.7:
            pass
        out_boxes.append(result[2])
        out_scores.append(result[1])
        out_classes.append(int(result[0]))
    #print(out_classes)
    out = 0

    while out_boxes.__len__() != 0:
        num = -1
        tmp = 1919810
        maxIndex = 0
        for i in range(out_boxes.__len__()):
            if out_boxes[i][0] < tmp:
                tmp = out_boxes[i][0]
                num = out_classes[i]
                maxIndex = i
        out_boxes.pop(maxIndex)
        out_classes.pop(maxIndex)
        out = out * 10 + num
    return out


# test only
"""
request(
    'ObjRegv3.h5',
    'objDetectionAnchor.txt',
    'itemList.txt',
    ''
)
"""
