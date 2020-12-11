# import base64
# import os
# import requests
# #文件名列表
# name_list = os.listdir('./pictures/')
# #带路径的列表
# entire_list = [os.path.join("./pictures/",file) for file in name_list]
# entire_list.sort()
# r = []
# k = 5 if 5 < len(entire_list) else len(entire_list)
# m = len(entire_list)
# # #post请求链接http://adsoc.qknode.com/adagent/material/center/push
# # #字段字典
#
#
# for i in range(m):
#     with open(entire_list[i],"rb") as f:
#         base64_body = str(base64.b64encode(f.read()), encoding='utf-8')
#         name= os.path.basename(entire_list[i])
#         extension_name = os.path.splitext(name)[1][1:]
#         base64_head = "data:image/%s;base64,"%extension_name
#         base64_entire = base64_head + base64_body
#         dict_post = {"guid": "lijing", "token": "C9naqdkliyoDcb4x", "tag": "test", "userTag": "李晶", "picList": base64_entire,
#                      "appType": "清理产品"}
#         post = requests.post("http://adsoc.qknode.com/adagent/material/center/push", data=dict_post).text
#         print(post)





#测试向后端post这些base64图片

# base64_array = []
# for picture in entire_list:
#     with open(picture,"rb") as f:
#         base64_body = str(base64.b64encode(f.read()), encoding='utf-8')
#         name = os.path.basename(picture)
#         extension_name = os.path.splitext(name)[1][1:]
#         base64_head = "data:image/%s;base64," % extension_name
#         base64_entire = base64_head + base64_body
#         base64_array.append(base64_entire)

# #         base64_array.append(base64_entire)
# r = []
# with open(entire_list[4],'rb') as f:
#     base64_body = str(base64.b64encode(f.read()), encoding='utf-8')
#     name = os.path.basename(entire_list[0])
#     extension_name = os.path.splitext(name)[1][1:]
#     base64_head = "data:image/%s;base64," % extension_name
#     base64_entire = base64_head + base64_body
#     r.append(base64_entire)
#     print(r)
from pandas import Series
import numpy as np
import keras
import tensorflow as tf
x1 = Series(data=[1,2,3,4],index=['a','b','c','d'])
x2 = np.array([1,2,3,4,5,6,7,8,9,0])
print(x1)
print(x2)
print(keras.__version__)
print(tf.__version__)