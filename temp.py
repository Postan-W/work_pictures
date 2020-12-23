from patchMatch import inpaint
from src.ssd_model import SSD300, Backbone
# from src.img_scores import CNNIQAnet
from src.img_scores import BRISQUE
# from src.IQADataset import NonOverlappingCropPatches
import transform
import collections
import torch
import json
from PIL import Image, ImageFont, ImageDraw
import os
import requests
from io import BytesIO
import time
from datetime import datetime, timedelta
from goto import with_goto
import paramiko
from scp import SCPClient
from src.predict_old import picGAN
import base64
from tornado.ioloop import IOLoop
from apscheduler.schedulers.tornado import TornadoScheduler
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler('./output.log', mode='w', encoding='utf-8')
# 第三步，定义handler的输出格式
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
# 第四步，将logger添加到handler里面
logger.addHandler(fh)

G = picGAN()


class LOGO:
    def __init__(self, device="cuda:1"):
        picfile = str(time.strftime("%Y%m%d"))
        self.todaypath = os.path.join('/workspace/nologopics', picfile)
        if not os.path.exists(self.todaypath):
            os.mkdir(self.todaypath)

        self.device = torch.device(device)
        # logo检测模型
        backbone = Backbone()
        self.ssdmodel = SSD300(backbone=backbone, num_classes=2)
        modelpath = './weights/ssd300-best.pth'
        weights_dict = torch.load(modelpath, map_location=device)
        self.ssdmodel.load_state_dict(weights_dict, strict=False)
        json_file = open('./pascal_voc_classes.json', 'r')
        class_dict = json.load(json_file)
        self.category_index = {v: k for k, v in class_dict.items()}
        self.data_transforms = transform.Compose([transform.Resize(),
                                                  transform.ToTensor(),
                                                  transform.Normalization()])

        # 水印字体
        self.font = ImageFont.truetype("./src/msyh.TTF", 24, encoding="utf-8")

        # 爬虫网址
        self.spiderurl = {
            #clear_log
            2: {'url': 'http://adsoc.qknode.com/adagent/material/material?', 'topic': ["清理", "日历", "天气"]},
            0: {'url': 'http://adsoc.qknode.com/adagent/material/center/rank?', 'topic': ["清理", "日历", "天气", "教育"]},
            # 排行榜
            1: {'url': 'http://adsoc.qknode.com/adagent/material/material?', 'topic': ["清理", "日历", "天气"]}

            # 素材洞察
        }

        # 推送地址
        self.finalurl = 'http://adsoc.qknode.com/adagent/material/center/push'

        # self.cnniqamodel = CNNIQAnet(ker_size=7, n_kers=50, n1_nodes=800, n2_nodes=800)
        # self.cnniqamodel.load_state_dict(torch.load('./weights/CNNIQA-LIVE.pth',map_location=device))
        if device != 'cpu':
            # self.cnniqamodel = self.cnniqamodel.to(self.device)
            # self.cnniqamodel.eval()
            self.ssdmodel = self.ssdmodel.to(self.device)
            self.ssdmodel.eval()

    # 添加水印
    def addText(self, img):
        img1 = img.convert('RGB')
        a = img1.size[0]
        b = img1.size[1]
        draw = ImageDraw.Draw(img1)
        draw.text((a - 230, b - 80), u"下载APP即可清理", (255, 0, 0), font=self.font)
        return img1

    # 存储图片
    def saveImg(self, image, imgname):
        dstpath = os.path.join(self.todaypath, imgname)
        image.save(dstpath)
        return dstpath

    @staticmethod
    def mkDir():
        picfile = str(time.strftime("%Y%m%d"))
        todaypath = os.path.join('/workspace/nologopics', picfile)
        if not os.path.exists(todaypath):
            print('mkDir')
            os.mkdir(todaypath)

    @staticmethod
    def uploadResult(dsthost, dstport, local_path,
                     remote_path="/root/ADpictures/withoutlogo", ):
        # img_name示例：07670ff76fc14ab496b0dd411a33ac95-6.webp
        picname = os.path.basename(local_path)
        username = "root"  # ssh 用户名
        password = "l8X6%WAqc9ifGX6o"  # 密码
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh_client.connect(dsthost, dstport, username, password)
        scpclient = SCPClient(ssh_client.get_transport(), socket_timeout=15.0)
        try:
            scpclient.put(local_path, remote_path)
            os.remove(local_path)
        except FileNotFoundError:
            print("系统找不到指定文件" + picname)
        finally:
            print(dsthost + ":" + picname + "--文件上传成功")
        ssh_client.close()
        result = remote_path + picname
        return result

    @staticmethod
    def filterThresh(boxes, scores, classes, category_index, thresh, box_to_display_str_map):
        for i in range(boxes.shape[0]):
            if scores[i] > thresh:
                box = tuple(boxes[i].tolist())  # numpy -> list -> tuple
                if classes[i] in category_index.keys():
                    class_name = category_index[classes[i]]
                else:
                    class_name = 'N/A'
                display_str = str(class_name)
                display_str = '{}: {}%'.format(display_str, int(100 * scores[i]))
                box_to_display_str_map[box].append(display_str)
            else:
                break  # 网络输出概率已经排序过，当遇到一个不满足后面的肯定不满足

    # 获取时间戳
    @staticmethod
    def getTimestamp(clock, days=0):
        """
        :param clock: 指定的时间,比如当天的凌晨一点即为1(24小时制)
        :param days:  与当前时间的相差的日期。-1 表示昨天；0 表示当天(默认)；1 表示明天
        :return:      返回13位时间戳
        """
        nowTime = datetime.now() + timedelta(days=days)
        str_time = nowTime.strftime("%Y-%m-%d") + " {}:00:00".format(clock)
        array_time = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        result = int(time.mktime(array_time.timetuple()) * 1000.0 + array_time.microsecond / 1000.0)
        return result

    @with_goto
    def drawBox(self, image, width, height, boxes, classes, scores, category_index, thresh):
        box_to_display_str_map = collections.defaultdict(list)
        LOGO.filterThresh(boxes, scores, classes, category_index, thresh, box_to_display_str_map)
        boxes = list(box_to_display_str_map.keys())
        if boxes == []:
            img = image.resize((width, height), Image.ANTIALIAS)
            return img
        else:
            box = boxes[0]
            xmin, ymin, xmax, ymax = box
            patch = Image.new('RGB', (abs(int(xmin) - int(xmax) - 5), abs(int(ymin) - int(ymax) - 5)), (240, 230, 140))
            image.paste(patch, (
            int(min(int(xmin), int(xmin) - 2)), int(min(int(ymin), int(ymin) - 2)), int(int(xmax) + 3),
            int(int(ymax) + 3)))
            result = inpaint(image)
            # Image.fromarray(result).resize((width, height), Image.ANTIALIAS).save(dstpath)
            img = Image.fromarray(result).resize((width, height), Image.ANTIALIAS)
            return img

    def abraseLogo(self, image, ratio=0.7):
        image = image.convert('RGB')
        width = image.size[0]  # 获取宽度
        height = image.size[1]  # 获取高度
        image.thumbnail((int(width * ratio), int(height * ratio)), Image.ANTIALIAS)
        img, _ = self.data_transforms(image)
        img = torch.unsqueeze(img, dim=0)
        with torch.no_grad():
            predictions = self.ssdmodel(img.to(self.device))[0]  # bboxes_out, labels_out, scores_out
            predict_boxes = predictions[0].cpu().numpy()
            predict_boxes[:, [0, 2]] = predict_boxes[:, [0, 2]] * image.size[0]
            predict_boxes[:, [1, 3]] = predict_boxes[:, [1, 3]] * image.size[1]
            predict_classes = predictions[1].cpu().numpy()
            predict_scores = predictions[2].cpu().numpy()
            img = self.drawBox(image, width, height, predict_boxes, predict_classes, predict_scores,
                               self.category_index, thresh=0.25)
        return img

    # def getScores(self,img,imgname):
    #     p_score, n_score = CNNIQAnet.piqeAndniqe(img)
    #     gray_img = img.convert('L')  # 转灰度图
    #     patches = NonOverlappingCropPatches(gray_img, 32, 32)
    #     with torch.no_grad():
    #         img_tensor = torch.stack(patches).to(self.device)
    #         patch_scores = self.cnniqamodel(img_tensor)
    #         cnn_score = patch_scores.mean().item()
    #     print("cnn_score:"+str(cnn_score),end='')
    #     print("   p_score:"+str(p_score),end='')
    #     print("   n_score:"+str(n_score))
    #     if cnn_score < 70 and  n_score < 18.6:
    #         result = self.addText(img)
    #         #self.saveImg(result, imgname)
    #         print(imgname + "质量过关")
    #         return result
    #     else:
    #         #self.saveImg(img, imgname)
    #         print(imgname + "质量不过关")
    #         return 'IQA no pass'

    def getScores(self, img, imgname):
        score = BRISQUE(img)  # 转灰度图
        print("brisque_score:" + str(score))
        if score < 70:
            result = self.addText(img)
            # self.saveImg(result, imgname)
            # logging.info(imgname + "质量过关")
            return result
        else:
            # self.saveImg(img, imgname)
            # logging.info(imgname + "质量不过关")
            return 'IQA no pass'

    @staticmethod
    def getArgument(keyword, flag):
        # ms 一个月700-800张
        start_time = LOGO.getTimestamp(0, -1)  # 昨天0点
        end_time = LOGO.getTimestamp(0)  # 今天0点

        search_dict = {'guid': 'lijing', 'token': 'C9naqdkliyoDcb4x', 'startDate': start_time, "endDate": end_time,
                       "userTag": "李晶",
                       'pageNo': 1, 'pageSize': 2000, 'appType': keyword} \
            if flag == 0 else \
            {'guid': 'lijing', 'token': 'C9naqdkliyoDcb4x', 'type': 'image',
             'keyword': keyword, 'pageNo': "1", 'pageSize':
                 "2000", 'startDate': start_time, "endDate": end_time, 'field': 'firstTime', "direction": ""}

        return search_dict

    # GAN
    @staticmethod
    def processedGAN(img):
        a = img.size[0]
        b = img.size[1]
        if a > b:
            img = G.get_1280_720(img)
        else:
            img = G.get_720_1280(img)
        return img

    # 素材洞察爬虫
    def wmzSpider(self, jsonlist, keyword, flag):
        keyword += "产品"
        for element in jsonlist:
            for dict in element["materials"]:
                url = "http:" + dict["url"] if not dict["url"].startswith("http:") else dict["url"]

                img_name = os.path.basename(url)
                img_text = requests.get(url)
                bytes_stream = BytesIO(img_text.content)
                img = Image.open(bytes_stream)
                img = self.abraseLogo(img)
                if flag == 1:
                    img = LOGO.processedGAN(img)
                elif flag == 2 and img.size != (1280, 720) and img.size != (720, 1280):
                    continue
                result = self.getScores(img, img_name)
                if result == 'IQA no pass':
                    logging.info(result)
                else:
                    tag = "M_gen" if flag == 1 else "clear_log"
                    buffered = BytesIO()
                    result.save(buffered, format='PNG')
                    img_str = base64.b64encode(buffered.getvalue())
                    finaldict = {"guid": 'lijing', "token": 'C9naqdkliyoDcb4x', "userTag": "李晶",
                                 "picList": img_str,
                                 "appType": keyword}
                    finaldict.update({"tag": tag})
                    response = requests.post(self.finalurl, data=finaldict).text
                    logging.info(response)

    # 排行榜爬虫
    def lsjSpider(self, jsonlist, keyword):
        keyword += "产品"
        sorted_pictures = sorted(jsonlist, key=lambda k: k['click'], reverse=True)
        pictures = len(sorted_pictures)
        number = 500 if pictures > 500 else pictures
        for element in sorted_pictures[:number]:
            url = element["url"]
            img_name = os.path.basename(url)
            img_text = requests.get(url)
            bytes_stream = BytesIO(img_text.content)
            img = Image.open(bytes_stream)
            img = LOGO.processedGAN(img)
            result = self.getScores(img, img_name)
            if result != 'IQA no pass':
                buffered = BytesIO()
                result.save(buffered, format='PNG')
                img_str = base64.b64encode(buffered.getvalue())
                finaldict = {"guid": 'lijing', "token": 'C9naqdkliyoDcb4x', "tag": "M_gen", "userTag": "李晶",
                             "picList": img_str,
                             "appType": keyword}
                response = requests.post(self.finalurl, data=finaldict).text
                logging.info(response)
            else:
                logging.info(result)

    # 推送图片
    def pushPic(self, keyword, flag):
        start_time = LOGO.getTimestamp(0, -1)  # 昨天0点
        end_time = LOGO.getTimestamp(0)  # 今天0点
        search_dict = {'guid': 'lijing', 'token': 'C9naqdkliyoDcb4x', 'startDate': start_time, "endDate": end_time,
                       "userTag": "李晶",
                       'pageNo': '1', 'pageSize': '1000', 'appType': keyword} \
            if flag == 0 else \
            {'guid': 'lijing', 'token': 'C9naqdkliyoDcb4x', 'type': 'image',
             'keyword': keyword, 'pageNo': "1", 'pageSize':
                 "1000", 'startDate': start_time, "endDate": end_time, 'field': 'firstTime', "direction": ""}
        search_url = self.spiderurl.get(flag)['url']
        response = requests.get(search_url, params=search_dict).json()
        jsonlist = response["data"]["content"]
        self.lsjSpider(jsonlist, keyword) if flag == 0 else self.wmzSpider(jsonlist, keyword, flag)

    # 入口函数
    def run(self):
        i =1
        for j in self.spiderurl.get(i)['topic']:
            try:
                self.pushPic(j, i)
            except Exception as e:
                logging.error(e)
                continue


if __name__ == '__main__':
    class_L = LOGO()
    scheduler = TornadoScheduler(timezone="Asia/Shanghai")
    scheduler.add_job(class_L.run, 'cron', hour=8)
    # scheduler.add_job(class_L.getPictureMaterial('清理'), 'interval', seconds=3)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        IOLoop.instance().start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
