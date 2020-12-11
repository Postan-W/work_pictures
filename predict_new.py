import os
import cv2
import cyclegan
from PIL import Image
import numpy as np
import time
gan = cyclegan.CycleGAN()
modelA = gan.build_generator()

modelA.load_weights("./g_AB_epoch1270.h5")

print(modelA)

def get_1280_720(yuan_path):
    width = 1280
    higth = 720
    col = 64
    row = 36
    cel_width = int(width/col)
    cel_higth = int(higth/row)
    yuan_img = cv2.imread(yuan_path)
    img1 = cv2.resize(yuan_img, (1280, 720))
    yuan_img = Image.fromarray(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    moban = []

    for j in range(row):
        for i in range(col):
            tmp = yuan_img.crop((i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
            moban.append(tmp)
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
        fakeB.append((modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)

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

def get_720_1280(yuan_path):
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
        fakeB.append((modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)

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

if __name__=='__main__':

    dir_name = './pictures'
    n = 0
    time_start = time.time()
    for filename in os.listdir(dir_name):
        n = n + 1
        print(filename)
        bool = filename.endswith(".jpg") or filename.endswith(".jepg") or filename.endswith("png")
        if bool:
            #img = cv2.imread(dir_name + "/" + filename)
            img_path = dir_name + "/" + filename
            img1 = Image.open(img_path)
            print(img1.size)
            a = img1.size[0]
            b = img1.size[1]
            print(a,b)
            if a > b:
                img = get_1280_720(img_path)
                #print(type(img))
            else:
                img = get_720_1280(img_path)

            img.save("./converted/" + str(n) + ".jpg")
    time_end=time.time()
    print('--------------totally cost-------------------',time_end-time_start)