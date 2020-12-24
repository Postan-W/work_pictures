import requests
import time
import json
import os
from predict_new import*
import sys
"""
请求参数模板：
search_dict = {'guid': 'lijing', 'token': 'C9naqdkliyoDcb4x', 'type': 'image',
               'keyword':'天气','pageNo': "1", 'pageSize':
        "100",'startDate':start,"endDate": end,'field':'firstTime', "direction":""}
注：field:impression和direction：DESC的效果相当于按热度或点击率降序获取
注：field:firstTime获取最新的图片        
"""

#这个模块获取用户输入的参数
def getArgument():
    startTime = input("请输入开始时间：")
    endTime = input("请输入结束时间:")
    guid = input("请输入guid:")
    token = input("请输入token:")
    keyword = input("请输入搜索图片的关键词keyword,如天气:")
    return guid,token,keyword,startTime,endTime

#这个函数拼接url
def concatenateURL(base_url,search_dict):
    for key in search_dict:
        if key != "direction":
         base_url = base_url + key + "=" + str(search_dict[key]) + "&"
        else:
            base_url = base_url + key + "=" +str(search_dict[key]) + "DESC"
    return base_url

#下面这个函数向文件夹里存储新的获取的图片
def getPictureMaterial(url):
    # 接收开始时间和结束时间
    # 注意要清空当前文件夹的所有内容,不然重复获取相同的内容
    # 文件名列表
    name_list = os.listdir('./pictures/')
    # 带路径的列表
    entire_list = [os.path.join("./pictures/", file) for file in name_list]
    for file in entire_list:
        os.remove(file)

    count = 0
    print("获取地址为："+url)
    print("正在获取，如果图片较多则需较长等待.................")
    json_data = requests.get(url).text
    #json是字符串，将其转为对应的python数据结构需要loads,比如这里loads的结果就是字典
    response_dict = json.loads(json_data)
    #注意，获取到的图片素材链接前面没有http协议，故要加上
    #注意，content的值是个数组，materials的值也是个数组
    for element in response_dict['data']['content']:
        for dict in element["materials"]:
            url = dict["url"]
            if not url.startswith("http:"):
                url = "http:" + dict["url"]
            if url.startswith("http://"):
                picture = requests.get(url)
                #获取图片名称
                filename = os.path.basename(url)
                #保存图片
                with open("./pictures/"+filename,"wb") as f:
                    f.write(picture.content)
                    count = count + 1
    print("----图片获取成功,"+"共%d张图片----"%count)