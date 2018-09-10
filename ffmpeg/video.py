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


def video_add_img(input_file, img_data, out_file):
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


def video_add_gif(input_file, img_data, out_file):
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


"""
video_add_img("/Users/master/yx/yxp/web/video/6/1/999/test.mp4", img,"/Users/master/yx/yxp/web/video/6/1/999/c_out.mp4")
video_add_gif("/Users/master/yx/yxp/web/video/6/1/999/test.mp4", img, "/Users/master/yx/yxp/web/video/6/1/999/c_test.mp4")
"""
