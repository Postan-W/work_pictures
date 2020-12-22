import os
import requests
import json
import time
"""
search_dict = {'guid': 'lijing', 'token': 'C9naqdkliyoDcb4x', 'type': 'image',
               'keyword':'日历','pageNo': "1", 'pageSize':"2000",'startDate':start,"endDate": end,'field':'firstTime', "direction":""}
注：field:impression和direction：DESC的效果相当于按热度或点击率降序获取
注：field:firstTime获取最新的图片
注：同一个类型下可以用channel参数进一步筛选，比如channel=102代表腾讯广告，105代表巨量引擎
注：keyword可以是任意筛选语言，比如“手机垃圾过多”也代表清理类图片
"""
def getArgu():
    startTime = input("请输入开始时间:")
    endTime = input("请输入结束时间：")
    guid = input("请输入guid:")
    token = input("请输入token:")
    keyword = input("请输入搜索图片的关键词keyword,如天气:")
    return guid,token,keyword,startTime,endTime
guid,token,keyword,start, end = getArgu()

base_url = "http://adsoc.qknode.com/adagent/material/material?"
search_dict = {'guid': guid, 'token': token, 'type': 'image',
               'keyword':keyword,'pageNo': "1", 'pageSize':"2000",'startDate':start,"endDate": end,'field':'firstTime', "direction":""}

def concatenateURL(base_url):
    for key in search_dict:
        if key != "direction":
         base_url = base_url + key + "=" + str(search_dict[key]) + "&"
        else:
            base_url = base_url + key + "=" +str(search_dict[key]) + "DESC"
    return base_url

def getPictureMaterial(url):
    count = 0
    print("获取地址为："+url)
    print("正在获取，如果图片较多则需较长等待.................")
    json_data = requests.get(url).text
    #将请求到的json格式数据转为python字典，为了更方便处理
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
                extension_name = os.path.splitext(filename)[1][1:]
                #保存图片
                #备用名称str(time.strftime("%Y.%m.%d-%H.%M.%S"))+search_dict['keyword']
                types = ""
                directory = ""
                if keyword == "清理":
                    types = "clear"
                    directory = "./clear_tem/"
                elif keyword == "天气":
                    types = "weather"
                    directory = "./weather_tem/"
                elif keyword == "日历":
                    types = "calendar"
                    directory = "./calendar_tem/"
                elif keyword == "小说":
                    types = "fiction"
                    directory = "./fiction_tem/"
                else:
                    types = "others"
                    directory = "./others_tem/"
                with open(directory+str(time.strftime("%Y.%m.%d-%H.%M.%S"))+types+str(count+1)+"."+extension_name,"wb") as f:
                    f.write(picture.content)
                    count = count + 1
    print("----图片获取成功,"+"共%d张图片----"%count)

getPictureMaterial(concatenateURL(base_url))