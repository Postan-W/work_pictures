import os
import cv2
import cyclegan
from PIL import Image
import numpy as np
import time
gan = cyclegan.CycleGAN()
modelA = gan.build_generator()
#model.load_weights(r"F:/Keras-GAN-master/cyclegan/weights/toolspic/g_AB_epoch100.h5")
#modelB = gan.build_generator()
modelA.load_weights("./g_AB_epoch1270.h5")
print("------------------loading weight------------------")
#modelA.load_weights("F:\\Keras-GAN-master\\cyclegan\\weights\\toolspic\\g_AB_epoch1650.h5")
#modelA.load_weights("F:\\Keras-GAN-master\\cyclegan\\weights\\apple2orange\\g_AB_epoch2280.h5")
print(modelA)
print("------------------loading done--------------------")
modelB = gan.build_generator()
#model.load_weights(r"F:/Keras-GAN-master/cyclegan/weights/toolspic/g_AB_epoch100.h5")
#modelB = gan.build_generator()
modelB.load_weights("./g_BA_epoch1270.h5")
#modelB = modelB.load_weights("F:\\Keras-GAN-master\\cyclegan\\weights\\toolspic\\g_BA_epoch85.h5")
print(modelB)

def change_1280_720(yuan_path):
    print("change")
    yuan_img = cv2.imread(yuan_path)
    yuan_img = Image.fromarray(cv2.cvtColor(yuan_img, cv2.COLOR_BGR2RGB))
    moban = []

    for j in range(5):
        for i in range(10):
            tmp = yuan_img.crop((i*128, j*128, (i+1)*128, (j+1)*128))
            moban.append(tmp)
    for i in range(10):
        tmp1 = yuan_img.crop((i*128, 640, (i+1)*128, 720))
        moban.append(tmp1)
    print(len(moban))

    img_list = []
    for n in range(len(moban)):
        img = np.array(moban[n].resize([128, 128])) / 127.5 - 1
        print(type(img),img.shape)
        img_list.append(np.expand_dims(img, axis=0))
        print("===========img shape",img_list[n].shape)
        print(img_list[n].shape)
    print(len(img_list))
    fakeA = []
    fakeB = []
    for i in range(len(img_list)):
        print(img_list[i].shape)
        fakeA.append((modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)
        fakeB.append((modelB.predict(img_list[i]) * 0.5 + 0.5) * 255)

    resA = []
    resB = []
    for i in range (len(fakeA)):
        resA.append(Image.fromarray(np.uint8(fakeA[i][0])))
        resB.append(Image.fromarray(np.uint8(fakeB[i][0])))

    faceA = []
    faceB = []
    for i in range(50):
        faceA.append(resA[i].resize((128, 128)))
        faceB.append(resB[i].resize((128, 128)))
    for j in range(10):
        faceA.append(resA[50+j].resize((128, 80)))
        faceB.append(resB[50+j].resize((128, 80)))

    for j in range(5):
        for i in range(10):
            yuan_img.paste(faceA[i+10*j],(i*128, j*128, (i+1)*128, (j+1)*128))
    for i in range(10):
        yuan_img.paste(faceA[i+50],(i*128, 640, (i+1)*128, 720))

    yuan_img.save('A_00.jpg')

    for j in range(5):
        for i in range(10):
            yuan_img.paste(faceB[i+10*j],(i*128, j*128, (i+1)*128, (j+1)*128))
    for i in range(10):
        yuan_img.paste(faceB[i+50],(i*128, 640, (i+1)*128, 720))

    yuan_img.save('B_00.jpg')

def get_1280_720(yuan_path):
    print("----------------get 1280 720 ----------------")
    width = 1280
    higth = 720
    col = 64
    row = 36
    # col = 4
    # row = 4
    cel_width = int(width/col)
    cel_higth = int(higth/row)
    print(yuan_path)
    yuan_img = cv2.imread(yuan_path)
    print(type(yuan_img))
    img1 = cv2.resize(yuan_img, (1280, 720))
    yuan_img = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    moban = []

    for j in range(row):
        for i in range(col):
            tmp = yuan_img.crop((i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
            moban.append(tmp)
    #print(len(moban))

    img_list = []
    for n in range(len(moban)):
        img = np.array(moban[n].resize([128, 128])) / 127.5 - 1
        #print(type(img),img.shape)
        img_list.append(np.expand_dims(img, axis=0))
        #print("===========img shape",img_list[n].shape)
        #print(img_list[n].shape)
    #print(len(img_list))
    fakeA = []
    fakeB = []
    for i in range(len(img_list)):
        #print(img_list[i].shape)
        fakeA.append((modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)
        fakeB.append((modelB.predict(img_list[i]) * 0.5 + 0.5) * 255)

    resA = []
    resB = []
    for i in range (len(fakeA)):
        resA.append(Image.fromarray(np.uint8(fakeA[i][0])))
        resB.append(Image.fromarray(np.uint8(fakeB[i][0])))

    faceA = []
    faceB = []
    for i in range(row*col):
        faceA.append(resA[i].resize((cel_width, cel_higth)))
        faceB.append(resB[i].resize((cel_width, cel_higth)))


    for j in range(row):
        for i in range(col):
            yuan_img.paste(faceA[i+col*j],(i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
    return yuan_img
    # p =  Image.new('RGB', (1280,720))
    # for j in range(row):
    #     for i in range(col):
    #         p.paste(faceA[i+col*j],(i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
    # return p
    #yuan_img.save('A_9a.jpg')

    # for j in range(row):
    #     for i in range(col):
    #         yuan_img.paste(faceB[i+col*j],(i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
    #
    # yuan_img.save('B_9a.jpg')
    print("--------------- 1280 720 done-------------")
def get_720_1280(yuan_path):
    print("---------------get 720 1280------------------")
    width = 720
    higth = 1280
    col = 36
    row = 64
    cel_width = int(width/col)
    cel_higth = int(higth/row)
    yuan_img = cv2.imread(yuan_path)

    #print("img shape", yuan_img.shape)
    img1 = cv2.resize(yuan_img, (720, 1280))
    #print("img1 reshape", img1.shape)
    #cv2.imwrite("new33.jpg", img1)
    yuan_img = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    moban = []

    for j in range(row):
        for i in range(col):
            tmp = yuan_img.crop((i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
            moban.append(tmp)
    #print(len(moban))

    img_list = []
    for n in range(len(moban)):
        img = np.array(moban[n].resize([128, 128])) / 127.5 - 1
        #print(type(img),img.shape)
        img_list.append(np.expand_dims(img, axis=0))
        #print("===========img shape",img_list[n].shape)
        #print(img_list[n].shape)
    #print(len(img_list))
    fakeA = []
    fakeB = []
    for i in range(len(img_list)):
        print(img_list[i].shape)
        fakeA.append((modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)
        fakeB.append((modelB.predict(img_list[i]) * 0.5 + 0.5) * 255)

    resA = []
    resB = []
    for i in range (len(fakeA)):
        resA.append(Image.fromarray(np.uint8(fakeA[i][0])))
        resB.append(Image.fromarray(np.uint8(fakeB[i][0])))

    faceA = []
    faceB = []
    for i in range(row*col):
        faceA.append(resA[i].resize((cel_width, cel_higth)))
        faceB.append(resB[i].resize((cel_width, cel_higth)))


    for j in range(row):
        for i in range(col):
            yuan_img.paste(faceA[i+col*j],(i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
    return yuan_img
    print("-----------720 1280 done------------")


if __name__=='__main__':
    #目录不要带汉字
    #get_1280_720("F:\\Keras-GAN-master\\pix2pix\\datasets\\toolspic\\testA\\9.jpg")
    #dir_name = 'F:\\ad\\test'
    #dir_name = 'F:\\ad\\src1128'
    dir_name = "F:\\ad\\edu\\edupic"
    n = 0
    time_start = time.time()
    for filename in os.listdir(dir_name):
        n = n + 1
        print(filename)
        bool = filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png")
        print(bool)
        if bool:
            #img = cv2.imread(dir_name + "/" + filename)
            img_path = dir_name + "/" + filename
            img1 = Image.open(img_path)
            img1 = img1.convert('RGB')
            #print(img1.size)
            a = img1.size[0]
            b = img1.size[1]
            print(a,b)
            if a > b:
                img = get_1280_720(img_path)
                #print(type(img))
            else:
                img = get_720_1280(img_path)
            #####显示图片#######
            #img.show()

            #####################

            #####保存图片#########
            #img.save("F:/ad/w20201128/" + str(n) + "width.jpg")
            #img.save("F:/ad/20201128/" + str(n) + "kk.jpg")
            img.save("F:/ad/edu/20201215/" + str(n) + "c.jpg")
    time_end=time.time()
    print('--------------totally cost-------------------',time_end-time_start)