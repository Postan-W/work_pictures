import base64
import os
import requests
def converted_to_base64_and_post():
    name_list = os.listdir('./converted/')
    print("开始推送处理后的图片，每推出一张就会返回一个响应信息.......")
    # 带路径的列表
    entire_list = [os.path.join("./converted/", file) for file in name_list]
    k = 5 if 5 < len(entire_list) else len(entire_list)
    m = len(entire_list)
    for i in range(m):
        with open(entire_list[i], "rb") as f:
            base64_body = str(base64.b64encode(f.read()), encoding='utf-8')
            name = os.path.basename(entire_list[i])
            extension_name = os.path.splitext(name)[1][1:]
            base64_head = "data:image/%s;base64," % extension_name
            base64_entire = base64_head + base64_body
            dict_post = {"guid": "lijing", "token": "C9naqdkliyoDcb4x", "tag": "M_gen", "userTag": "李晶",
                         "picList": base64_entire,
                         "appType": "清理产品"}
            post = requests.post("http://adsoc.qknode.com/adagent/material/center/push", data=dict_post).text
            print("推送结果:"+post)
    print("------推送完成------")

converted_to_base64_and_post()