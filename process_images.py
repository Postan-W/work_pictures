#这个模块专门用gan来处理图片的，不是项目的一部分
from predict_new import*
import os
def process_through_gan(source,destination):
    dir_name = source
    for filename in os.listdir(dir_name):
        if not os.path.exists(destination + filename):
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

                img.save(destination + filename)

source = input("请输入源文件地址：")
destination = input("请输入目标地址:")
process_through_gan(source,destination)