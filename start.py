"""
启动模块。
2020-12-1
wmingzhu
注：总的调用语句写在最下面
"""
import requests
import time
import json
import os
from predict_new import*
import sys
import glob
from client import sock_client_image
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
    entire_list = [os.path.join(destination, file) for file in name_list]

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
        #将爬取的图片传给去logo端
        f = glob.glob('./pictures/*')
        k = 0
        for i in f:
            if not i.endswith("webp"):
                k = k + 1
                print("正在传给去logo端第%d张图片"%k)
                sock_client_image(i,'1')
        print("所有带logo的图片上传完成,下面开始处理........")
        image_process("./withoutlogo/","./converted/")
        #下面需要把withoutlogo清空，以便下次使用
        withoutlog_file = os.listdir("./withoutlogo/")
        entirepath_withoutlog = [os.path.join("./withoutlogo/", file) for file in withoutlog_file]
        for file_w in entirepath_withoutlog:
            os.remove(file_w)
        print("开始回传处理过的图片..............")
        f2 = glob.glob('./converted/*')
        k2 = 0
        for i2 in f2:
            k2 = k2 + 1
            print("正在将处理过的第%d张图片回传" % k2)
            sock_client_image(i2, '2')
        #把通过质量核查的图片上传
        converted_to_base64_and_post("./qualified/",guid,token,keyword)
        #然后把qualified清空，下次继续使用
        qualified_list = os.listdir('./qualified/')
        entire_qualified_path = [os.path.join("./qualified/", file) for file in qualified_list]
        for qualified_file in entire_qualified_path:
            os.remove(qualified_file)

    elif taskType == "2":
        import ordered
        sorted_pictures, guid,token,appType = ordered.get_sorted_pictures()
        ordered.save_sorted_pictures(sorted_pictures, appType)
        image_process("./ordered_pictures/", "./sorted_pictures_converted/")
        #下面把处理过的排行图片传去质量核查
        f3 = glob.glob('./sorted_pictures_converted/*')
        k3 = 0
        for i3 in f3:
            if not i3.endswith("webp"):
                k3 = k3 + 1
                print("正在上传处理过的第%d张排行图片去核查质量......"%k3)
                sock_client_image(i3,"0")
        converted_to_base64_and_post("./sorted_qualified/",guid,token, appType)
        #下面需要把sorted_qualified清空，以便下次使用
        files = os.listdir("./sorted_qualified/")
        entirefilepath = [os.path.join("./sorted_qualified/", file) for file in files]

#开始
taskType = input("输入任务类型，1代表处理素材洞察的图片，2代表处理排行过的图片:")
start(taskType)






