"""
启动模块。
2020-12-1
汪明珠
注：总的调用语句写在该模块文件的最下面
"""
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
"""

#图片处理
def image_process(source,destination):
    #处理之前也要把目标文件夹清空，这是为了避免处理以及后面推送重复图片
    # 文件列表
    name_list = os.listdir(destination)
    # 带完整路径的列表
    entire_list     = [os.path.join(destination, file) for file in name_list]

    for file in entire_list:
        os.remove(file)
    n = 0
    time_start = time.time()
    dir_name = source
    print("正在处理图片，此过程可能较长........")
    for filename in os.listdir(dir_name):
        n = n + 1
        print(filename)
        bool = filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png")
        if bool:
            # img = cv2.imread(dir_name + "/" + filename)
            img_path = dir_name + "/" + filename
            img1 = Image.open(img_path)
            print(img1.size)
            a = img1.size[0]
            b = img1.size[1]
            print(a, b)
            if a > b:
                img = get_1280_720(img_path)
                # print(type(img))
            else:
                img = get_720_1280(img_path)

            img.save(destination + str(n) + ".jpg")
    time_end = time.time()
    print("--------------处理完成----------------")
    print('--------------totally cost-------------------', time_end - time_start,"秒")

#将处理后的图片转为base64
#base64固定的头data:image/~;base64,
import base64
import os
def converted_to_base64_and_post(source,guid,token,appType):
    name_list = os.listdir(source)
    print("开始推送处理后的图片，每推出一张就会返回一个响应信息.......")
    # 带路径的列表
    entire_list = [os.path.join(source, file) for file in name_list]
    k = 5 if 5 < len(entire_list) else len(entire_list)
    m = len(entire_list)
    userTag = input("请输入userTag，即推送人：")
    for i in range(m):
        with open(entire_list[i], "rb") as f:
            base64_body = str(base64.b64encode(f.read()), encoding='utf-8')
            name = os.path.basename(entire_list[i])
            extension_name = os.path.splitext(name)[1][1:]
            base64_head = "data:image/%s;base64," % extension_name
            base64_entire = base64_head + base64_body
            dict_post = {"guid": guid, "token": token, "tag": "M_gen", "userTag": userTag,
                         "picList": base64_entire,
                         "appType":appType}
            post = requests.post("http://adsoc.qknode.com/adagent/material/center/push", data=dict_post).text
            print("推送结果:"+post)
    print("------推送完成------")




def start(taskType):
    if taskType == "1":
        import normal
        guid, token, keyword, start, end = normal.getArgument()

        base_url = "http://adsoc.qknode.com/adagent/material/material?"
        search_dict = {'guid': guid, 'token': token, 'type': 'image',
                       'keyword': keyword, 'pageNo': "1", 'pageSize':
                           "2000", 'startDate': start, "endDate": end, 'field': 'firstTime', "direction": ""}
        url = normal.concatenateURL(base_url,search_dict)
        normal.getPictureMaterial(url)
        image_process("./pictures/","./converted/")
        input("图片处理完成，按enter键开始推送........")
        converted_to_base64_and_post("./converted/",guid,token,keyword)

    elif taskType == "2":
        import ordered

        sorted_pictures, guid,token,appType = ordered.get_sorted_pictures()
        ordered.save_sorted_pictures(sorted_pictures, appType)
        if appType == "清理产品":
            image_process("./ordered_pictures/clear/", "./sorted_pictures_converted/clear/")
            input("图片处理已完成，请去查看图片质量，确定推送请按enter键！！！")
            converted_to_base64_and_post("./sorted_pictures_converted/clear/",guid,token, appType)
        elif appType == "日历产品":
            image_process("./ordered_pictures/calendar/", "./sorted_pictures_converted/calendar/")
            input("图片处理已完成，请去查看图片质量，确定推送请按enter键！！！")
            converted_to_base64_and_post("./sorted_pictures_converted/calendar/", guid,token,appType)
        elif appType == "天气产品":
            image_process("./ordered_pictures/weather/", "./sorted_pictures_converted/weather/")
            input("图片处理已完成，请去查看图片质量，确定推送请按enter键！！！")
            converted_to_base64_and_post("./sorted_pictures_converted/weather/",guid,token, appType)

#开始
taskType = input("输入任务类型，1代表处理非经排序获取的图片，2代表处理排序过的:")
start(taskType)






