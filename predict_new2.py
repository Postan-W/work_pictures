import warnings
warnings.filterwarnings("ignore")
import os
# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = "3"
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)
import cv2
import cyclegan
from PIL import Image
import numpy as np
import time

gan = cyclegan.CycleGAN()


class picGAN:
    def __init__(self):
        print("------------------loading gan weight------------------")
        self.graph = tf.get_default_graph()
        self.modelA = gan.build_generator()
        self.modelA.load_weights("./g_AB_epoch1270.h5")
        self.modelB = gan.build_generator()
        self.modelB.load_weights("./g_BA_epoch1270.h5")
        print("------------------loading gan done--------------------")


    def change_1280_720(self,yuan_path):
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
        img_list = []
        for n in range(len(moban)):
            img = np.array(moban[n].resize([128, 128])) / 127.5 - 1
            img_list.append(np.expand_dims(img, axis=0))
        fakeA = []
        fakeB = []
        for i in range(len(img_list)):
            fakeA.append((self.modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)
            fakeB.append((self.modelB.predict(img_list[i]) * 0.5 + 0.5) * 255)

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

    def get_1280_720(self,yuan_img):
        print("----------------get 1280 720 ----------------")
        width = 1280
        higth = 720
        col = 64
        row = 36
        cel_width = int(width/col)
        cel_higth = int(higth/row)
        moban = []
        yuan_img = yuan_img.resize((1280,720),Image.ANTIALIAS)
        with self.graph.as_default():
            for j in range(row):
                for i in range(col):
                    tmp = yuan_img.crop((i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
                    moban.append(tmp)
            #print(len(moban))

            img_list = []
            for n in range(len(moban)):
                img = np.array(moban[n].resize([128, 128])) / 127.5 - 1
                img_list.append(np.expand_dims(img, axis=0))
            fakeA = []
            fakeB = []
            for i in range(len(img_list)):
                fakeA.append((self.modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)
                fakeB.append((self.modelB.predict(img_list[i]) * 0.5 + 0.5) * 255)

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
            print('ok')
        return yuan_img


    def get_720_1280(self,yuan_img):
        print("---------------get 720 1280------------------")
        width = 720
        higth = 1280
        col = 36
        row = 64
        cel_width = int(width/col)
        cel_higth = int(higth/row)
        yuan_img = yuan_img.resize((720,1280),Image.ANTIALIAS)
        moban = []
        with self.graph.as_default():

            for j in range(row):
                for i in range(col):
                    tmp = yuan_img.crop((i*cel_width, j*cel_higth, (i+1)*cel_width, (j+1)*cel_higth))
                    moban.append(tmp)


            img_list = []
            for n in range(len(moban)):
                img = np.array(moban[n].resize([128, 128])) / 127.5 - 1
                img_list.append(np.expand_dims(img, axis=0))

            fakeA = []
            fakeB = []
            for i in range(len(img_list)):
                fakeA.append((self.modelA.predict(img_list[i]) * 0.5 + 0.5) * 255)
                fakeB.append((self.modelB.predict(img_list[i]) * 0.5 + 0.5) * 255)

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
    #目录不要带汉字
    #get_1280_720("F:\\Keras-GAN-master\\pix2pix\\datasets\\toolspic\\testA\\9.jpg")
    #dir_name = 'F:\\ad\\test'
    #dir_name = 'F:\\ad\\src1128'
    G = picGAN()
    dir_name = "/workspace/nologopics/20201218"
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
                img = G.get_1280_720(img1)
                #print(type(img))
            else:
                img = G.get_720_1280(img1)
            #####显示图片#######
            #img.show()

            #####################

            #####保存图片#########
            #img.save("F:/ad/w20201128/" + str(n) + "width.jpg")
            #img.save("F:/ad/20201128/" + str(n) + "kk.jpg")

    time_end=time.time()
    print('--------------totally cost-------------------',time_end-time_start)