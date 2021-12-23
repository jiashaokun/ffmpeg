#!/usr/bin/python3
# coding=utf-8

import os

import json

import subprocess

import platform


class Stream(object):
    def __init__(self):
        self.cmd = ""
        self.out_file = ""
        self.vcode_type = ""
        self.input_file = ""
        self.word_list_str = ""
        self.subbtitle_file = ""

        self.cmd = []
        self.img_file = []
        self.word_list = []
        self.img_dynamic_list = []

        self.image_list = {}
        self.dynamic_list = {}

        # 使用gpu加速后的视频大小
        self.gpu = False
        self.gpu_size = ""

    # 输入文件
    def input(self, file):
        self.input_file = file

    # 使用gpu加速 0代表原视频大小 该值越大，越慢(2000k 或者 5M)
    def fast(self, size=""):
        self.gpu = True
        self.gpu_size = size
        return

    # 添加图片
    def img(self, img, x="0", y="0", str_time="0", end_time="0"):
        if img == "":
            return False
        input_info = self.video_info()

        if end_time == "0":
            end_time = float(input_info["format"]["duration"]) + 10.0

        img_data = {
            "img": img,
            "x": str(x),
            "y": str(y),
            "str_time": str(str_time),
            "end_time": str(end_time)
        }

        self.img_file.append(img_data)

        img_input = []
        img_overlay = []

        for val in self.img_file:
            img_input.append(" -i %s" % val["img"])
            img_overlay.append(" overlay=x=%s:y=%s:enable='if(gt(t,%s),lt(t,%s))'" % (
                    val["x"],
                    val["y"],
                    val["str_time"],
                    val["end_time"]
                )
            )

        img_input_str = " ".join(img_input)
        img_overlay_str = ",".join(img_overlay)

        self.image_list = {
            "input": img_input_str,
            "overlay": img_overlay_str
        }

    # 添加动态图片 gif apng 等
    def img_dynamic(self, file, x="0", y="0", str_time="0", end_time="0"):
        input_info = self.video_info()
        if file == "":
            return False
        if end_time == "":
            end_time = float(input_info["format"]["duration"]) + 10.0

        apng = {
            "input": " -ignore_loop 0 -i %s" % file,
            "x": str(x),
            "y": str(y),
            "str_time": str(str_time),
            "end_time": str(end_time)
        }
        self.img_dynamic_list.append(apng)

        img_dy_input = []
        img_dy_overlay = []
        for val in self.img_dynamic_list:
            img_dy_input.append(val["input"])
            img_dy_overlay.append(" overlay=x=%s:y=%s:shortest=1:enable='if(gt(t,%s), lt(t,%s))'" % (
                    val["x"],
                    val["y"],
                    val["str_time"],
                    val["end_time"]
                )
            )
        img_dy_input_str = " ".join(img_dy_input)
        img_dy_overlay_str = ",".join(img_dy_overlay)

        self.dynamic_list = {
            "input": img_dy_input_str,
            "overlay": img_dy_overlay_str
        }

    # 添加文字水印
    def word_water_mark(self, c, x="0", y="0", str_time="0", end_time="0", font="", color="white"):
        if font == "":
            return False
        input_info = self.video_info()
        if c == "":
            return False
        if end_time == "0":
            end_time = float(input_info["format"]["duration"]) + 10.0

        text = " drawtext=text='%s':x=%s:y=%s:enable='if(gt(t,%s),lt(t,%s))':fontfile=%s:" \
               "fontcolor=%s" % (c, str(x), str(y), str(str_time), str(end_time), str(font), str(color))
        self.word_list.append(text)

        self.word_list_str = ",".join(self.word_list)

    # 添加字幕文件 subtitles=txt.srt
    def subbtitle(self, file):
        self.subbtitle_file = " subtitles=%s" % file

    # 编码方式 -vcodec
    def vcode(self, code):
        if code == "":
            return False
        self.vcode_type = " -vcodec %s" % code

    # 输出文件
    def out(self, file):
        if file == "":
            return False
        self.out_file = "%s" % file

    # 执行脚本
    def run(self):
        if self.input_file == "":
            return False
        im = "ffmpeg -i %s" % self.input_file
        ov = ""

        if len(self.dynamic_list) > 0 and self.dynamic_list["input"] != "":
            im = "%s %s" % (im, self.dynamic_list["input"])

            if ov != "":
                ov = "%s,%s" % (ov, self.dynamic_list["overlay"])
            else:
                ov = self.dynamic_list["overlay"]
        if len(self.image_list) > 0:
            im = "%s %s" % (im, self.image_list["input"])
            if ov != "":
                ov = "%s,%s" % (ov, self.image_list["overlay"])
            else:
                ov = self.image_list["overlay"]

        # 文字水印
        if self.word_list_str != "":
            if ov != "":
                ov = "%s,%s" % (ov, self.word_list_str)
            else:
                ov = self.word_list_str

        # 字幕
        if self.subbtitle_file != "":
            if ov != "":
                ov = "%s,%s" % (ov, self.subbtitle_file)
            else:
                ov = self.subbtitle_file

        if self.gpu == True:
            # 筛选mac或者其他的gpu
            info = platform.platform()
            listSys = str(info).split("-")
            if listSys[0] == "macOS" or listSys[0] == "Darwin":
                if self.gpu_size != "":
                    im = "%s -c:v %s -b:v %s" % (im, "h264_videotoolbox", self.gpu_size)
                else:
                    im = "%s -c:v %s" % (im, "h264_videotoolbox")
            else:
                if self.gpu_size != "":
                    im = "%s -c:v %s -b:v %s" % (im, "h264_nvenc", self.gpu_size)
                else:
                    im = "%s -c:v %s" % (im, "h264_nvenc")

        if self.vcode_type != "":
            self.cmd = "%s -filter_complex \"%s\" -y %s %s" % (im, ov, self.vcode_type, self.out_file)
        else:
            if ov != "":
                self.cmd = "%s -filter_complex \"%s\" -y %s" % (im, ov, self.out_file)
            else:
                self.cmd = "%s  -y %s" % (im, self.out_file)
        self.do()

    # 获取视频的相关时长信息
    def video_info(self):
        result = {}
        if os.path.isfile(self.input_file) is False:
            return result

        cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', self.input_file]
        returned_data = subprocess.check_output(cmd)
        return json.loads(returned_data.decode('utf-8'))

    # 执行命令
    def do(self):
        if self.cmd == "":
            return False
        print(self.cmd)
        res = subprocess.call(self.cmd, shell=True)
        if res != 0:
            return False
        return True


if __name__ == '__main__':
    stream = Stream()
    stream.input("face.mp4")
    stream.img("t1.png", "50", "60", "5", "10")
    stream.img("t2.png", "10", "10", "5", "10")
    stream.img_dynamic("a.gif", "100", "100", "15", "30")
    stream.img_dynamic("a.gif", "200", "200", "15", "30")
    stream.word_water_mark("测试文字水印1", "100", "100", "10", "50", "ttf.ttf", "white")
    stream.word_water_mark("测试文字水印2", "200", "200", "10", "50", "ttf.ttf", "black")
    stream.subbtitle("srt.srt")
    stream.fast("5M")
    stream.out("out.mp4")
    stream.run()

