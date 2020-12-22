#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Liuxiaozhe on 2020/9/16
import queue
import cv2
import glob
import numpy as np
from moviepy.editor import VideoFileClip
from predict_new2 import picGAN
from PIL import Image
import time
g = picGAN()
q = queue.Queue()

def processedGAN(img):
    a = img.shape[1]
    b = img.shape[0]
    input = Image.fromarray(img)
    if a > b:
        img = g.get_1280_720(input)
    else:
        img = g.get_720_1280(input)
    res = np.array(img)
    return res

def conver(in_filename:str,out_filename:str,num:int):
    videoreader = cv2.VideoCapture(in_filename)
    # 获取视频宽度
    width = int(videoreader.get(cv2.CAP_PROP_FRAME_WIDTH))
    # 获取视频高度
    height = int(videoreader.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # 获取视频fps
    fps = videoreader.get(cv2.CAP_PROP_FPS)
    print("视频fps为:"+str(fps))
    print("--------------------------------")
    print("视频宽度width为:"+str(width))
    print("--------------------------------")
    print("视频高度height为:"+str(height))
    #videowriter = cv2.VideoWriter(out_filename, 0x00000002, fps,(width,height)) #0x00000002-->flv
    videowriter = cv2.VideoWriter(out_filename, 0x7634706d, fps,(720,1280))

    count = 0
    while True:
        success, frame = videoreader.read()
        if success:
            count += 1
            output = processedGAN(frame)
            q.put(output)
            print("视频总帧数为：%d"%videoreader.get(7))
            print("no.{} frame success!".format(str(count)))

        else:
            print('ending...')
            break
    while not q.empty():
        videowriter.write(q.get())
    videowriter.release()
    videoreader.release()
    time.sleep(2)

    # 读取2个视频文件
    videoclip_1 = VideoFileClip(in_filename)
    videoclip_2 = VideoFileClip(out_filename)

    # 提取第一个视频文件的音频部分
    audio_1 = videoclip_1.audio

    # 将提取的音频和第二个视频文件进行合成
    videoclip_3 = videoclip_2.set_audio(audio_1)

    # 输出新的视频文件
    videoclip_3.write_videofile("./video_destination/new_{}.mp4".format(str(num)))







# if __name__ == '__main__':
#     for i in range(8, 9):
#         conver("./video_origin/%d.mp4"%i,"./video_destination/%d.mp4"%i,i)

conver("./video_origin/55.mp4","./video_destination/55.mp4",55)