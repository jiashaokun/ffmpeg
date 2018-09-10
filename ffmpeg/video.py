#!/usr/local/bin/python3
# module sys


import subprocess


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


# 视频添加动图 gif apng
def ins_dynamic_img(input_file, img_data, out_file):
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


# 调整视频速率 speed 小于 1 减速，大于 1 加速 1 等速
def playback_speed(input_file, speed, out_file):
    try:
        if speed == "":
            speed = "1"
        cmd = "ffmpeg -y -i %s -filter_complex \"setpts=PTS/%s\" %s" % (input_file, speed, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True

    except Exception:
        return False


# 视频倒放 ( 视频 + 音频 )
def a_v_reverse(input_file, out_file):
    try:
        cmd = "ffmpeg -y -i %s -vf vf reverse -af areverse %s " % (input_file, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


# 视频倒放 (视频)
def v_reverse(input_file, out_file):
    try:
        cmd = "ffmpeg -y -i %s -vf vf reverse %s " % (input_file, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False
