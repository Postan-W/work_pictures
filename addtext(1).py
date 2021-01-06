import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import matplotlib as pl
pl.use('TkAgg')
import matplotlib.pyplot as plt
import os
#dir_name = u"F:\\ad\\clean\\20201217"
dir_name = u"F:\\ad\\weather\\no-logo-W"
n = 0
for filename in os.listdir(dir_name):
    n = n + 1
    print(filename)
    bool = filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png")
    print(bool)
    if bool:
        # img = cv2.imread(dir_name + "/" + filename)
        img_path = dir_name + "/" + filename
        img1 = Image.open(img_path)
        img1 = img1.convert('RGB')
        # print(img1.size)
        a = img1.size[0]
        b = img1.size[1]
        if (a==1280 and b==720) or (b==1280 and a==720):
            font = ImageFont.truetype("msyh.ttf", 24, encoding="utf-8")
            draw = ImageDraw.Draw(img1)
            #draw.text((a-230, b-80),u"下载APP即可清理",(255,0,0),font=font)
            draw.text((a - 245, b - 80), u"下载APP即可查看天气", (255, 0, 0), font=font)

        # plt.imshow(img1)
        # plt.show()
        # 保存
            img1.save("F:/ad/weather/test/" + str(n) + ".jpg")
print('运行结束')