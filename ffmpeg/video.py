#!/usr/local/bin/python3
# module sys


import subprocess

"""
ffmpeg -i input.mp4 -i 1.png -i 2.png -filter_complex "overlay=x=100:y=100:enable='if(gt(t,5),lt(t,10))',overlay=x=100:y=100:enable='if(gt(t,15),lt(t,20))'" -y 0.mp4

img = [
        {
            "img": "/Users/master/yx/yxp/web/video/6/1/999/c_01.png",
            "x": "",
            "y": "",
            "str_time": "5",
            "end_time": "15",
        },
        {
            "img": "/Users/master/yx/yxp/web/video/6/1/999/c_01.png",
            "x": "",
            "y": "",
            "str_time": "20",
            "end_time": "25.5"
        }
    ]
"""


def ins_img(input_file, img_data, out_file):
    try:
        if len(img_data) <= 0:
            return False

        img_list = []
        img_list_str = " -i "
        png_complex = []
        complex_png_str = ","

        for img in img_data:
            if len(img["x"]) == 0:
                img["x"] = "0"

            if len(img["y"]) == 0:
                img["y"] = "0"
            img_list.append(img["img"])

            if len(img["str_time"]) > 0:
                if len(img["end_time"]) > 0:
                    cmp_str = "overlay=x=%s:y=%s:enable='if(gt(t,%s),lt(t,%s))'" % (img["x"], img["y"], img["str_time"], img["end_time"])
                else:
                    cmp_str = "overlay=x=%s:y=%s:enable='if(gt(t,%s))'" % (img["x"], img["y"], img["str_time"])
            else:
                cmp_str = "overlay=x=%s:y=%s" % (img["x"], img["y"])

            png_complex.append(cmp_str)

        img_str_list = img_list_str.join(img_list)
        complex_png_str = complex_png_str.join(png_complex)

        cmd = "ffmpeg -i %s -i %s -filter_complex \"%s\" -y %s" % (input_file, img_str_list, complex_png_str, out_file)

        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True

    except Exception:
        return False


"""
img = {
    "img": "/Users/master/yx/yxp/web/video/6/1/999/img.apng",
    "x": "20",
    "y": "20",
    "str_time": "2",
    "end_time": "10"
}
"""


def ins_gif(input_file, img_data, out_file):
    try:
        if img_data["img"] == "":
            return False

        if img_data["x"] == "":
            img_data["x"] = 0

        if img_data["y"] == "":
            img_data["y"] = 0

        if img_data["str_time"] != "":
            if img_data["end_time"] != "":
                comp = "overlay=x=%s:y=%s:shortest=1:enable='if(gt(t,%s), lt(t,%s))'" % (img_data["x"], img_data["y"],
                                                                                         img_data["str_time"],
                                                                                         img_data["end_time"])
            else:
                comp = "overlay=x=%s:y=%s:shortest=1:enable='if(gt(t,%s)'" % (img_data["x"], img_data["y"],
                                                                              img_data["str_time"])
        else:
            comp = "overlay=x=%s:y=%s:shortest=1"

        cmd = "ffmpeg -i %s -ignore_loop 0 -i %s -filter_complex \"%s\" -y %s" % (input_file, img_data["img"], comp,
                                                                                  out_file)

        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


# 视频静音 分离音频流

def separate_audio(input_file, out_file):
    try:
        cmd = "ffmpeg -y -i %s -vcodec copy -an %s" % (input_file, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


# 视频静音 使用静音帧 为视频静音
def video_ins_mute_audio(input_file, mute_mp3_file, out_file):
    try:
        cmd = "ffmpeg -y -i %s -filter_complex '[1:0]apad' -shortest %s" % (input_file, mute_mp3_file, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


# 视频设置分辨率 及 码率
def trans_code(input_file, width, height, rate, out_file):
    try:
        cmd = "ffmpeg -y -i %s -s %sx%s -b %sk -acodec copy %s" % (input_file, width, height, rate, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


# 弹幕内容 str_time 是第几秒显示 speet 速率 默认 150 当显示时间一定时 该值越大，速度越快
bage = [
    {
        "context": "Hello World 1 !!!",
        "fontcolor": "white",
        "fontsize": "40",
        "fontfile": "PingFang-SC-Regular.ttf",
        "y": "100",
        "str_time": "2",
        "speet": "150",
    },
    {
        "context": "Hello World 2 !!!",
        "fontcolor": "white",
        "fontsize": "40",
        "fontfile": "PingFang-SC-Regular.ttf",
        "y": "200",
        "str_time": "2",
        "speet": "150",
    },
]


# 视频添加弹幕
def ins_barrage(input_file, barrage, out_file):
    try:
        if len(barrage) == 0:
            return False

        bag = []
        bag_str = ", "
        vf_str = ""

        for val in barrage:
            if val["fontsize"] == "":
                val["fontsize"] = 40

            if val["fontcolor"] == "":
                val["fontcolor"] = "white"

            if val["y"] == "":
                val["y"] = "100"

            if val["str_time"] == "":
                val["str_time"] = 0
            else:
                val["str_time"] = int(val["str_time"])

            if val["speet"] == "":
                val["speet"] = 150
            else:
                val["speet"] = int(val["speet"])

            txt = "drawtext=text='%s':fontcolor=%s:fontsize=%s:fontfile=%s:y=%s:x=w-(t-%d)*%d:enable='gte(t,%d)'" % (
                val["context"],
                val["fontcolor"],
                val["fontsize"],
                val["fontfile"],
                val["y"],
                val["str_time"],
                val["speet"],
                val["str_time"]
            )
            bag.append(txt)

            vf_str = bag_str.join(bag)

        cmd = "ffmpeg -y -i %s -vf \"%s\" %s" % (input_file, vf_str, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


ins_barrage("/Users/master/yx/yxp/web/video/6/1/999/test.mp4", bage, "/Users/master/yx/yxp/web/video/6/1/999/b_out.mp4")

"""
video_add_img("/Users/master/yx/yxp/web/video/6/1/999/test.mp4", img,"/Users/master/yx/yxp/web/video/6/1/999/c_out.mp4")
video_add_gif("/Users/master/yx/yxp/web/video/6/1/999/test.mp4", img, "/Users/master/yx/yxp/web/video/6/1/999/c_test.mp4")
"""
