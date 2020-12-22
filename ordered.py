import base64
import json
import pickle
import time
import requests
import os

"""
模板：
kw = {'guid': 'lijing', 'token': 'C9naqdkliyoDcb4x', 'startDate': start_time, "endDate": end_time, "userTag": "李晶",
      'pageNo': 1, 'pageSize': 2500, 'appType': '清理产品'}
"""

# 模拟Linux版本谷歌浏览器发起请求
# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Mobile Safari/537.36"}

def getArgument():
    start_time = input("请输入开始时间：")
    end_time = input("请输入结束时间：")
    guid = input("请输入guid:")
    token = input("请输入token:")
    appType = input("请输入appType:")
    userTag = input("请输入userTag:")
    return start_time,end_time,guid,token,appType,""


def get_sorted_pictures():
    start_time, end_time, guid, token, appType, userTag = getArgument()

    # 最后有没有问号结果都一样
    url = 'http://adsoc.qknode.com/adagent/material/center/rank?'

    # 请求参数是一个字典 即wd=python
    kw = {'guid': guid, 'token': token, 'startDate': start_time, "endDate": end_time, "userTag": userTag,
          'pageNo': 1, 'pageSize': 2500, 'appType': appType}

    # 带上请求参数发起请求，获取响应
    response = requests.get(url, headers=headers, params=kw)

    res = response.content

    # 将bytes转为json字典
    jsonres = json.loads(res)
    # 取出json数据
    jsonlist = jsonres["data"]["content"]

    sorted_pictures = sorted(jsonlist, key=lambda k:k['click'], reverse=True)
    return sorted_pictures,guid,token,appType

def save_sorted_pictures(sorted_pictures,appType):
    count = 0
    pictures_name = os.listdir("./ordered_pictures/")
    entire_list = [os.path.join("./ordered_pictures/", file) for file in pictures_name]
    for file in entire_list:
        os.remove(file)

    print("正在获取文件，请等待.....")
    #获取图片数量
    pictures = len(sorted_pictures)
    number = 500 if pictures > 500 else pictures
    for pic in sorted_pictures[:number]:
        count += 1
        url = pic["url"]
        queryurl = requests.get(url)
        with open("./ordered_pictures/" + str(count) + ".jpg", "wb")as f:
            f.write(queryurl.content)





