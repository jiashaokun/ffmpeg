#!/usr/local/bin/python3

from ffmpeg import video

img = {
    "img": "/Users/master/yx/yxp/web/video/6/1/999/img.apng",
    "x": "20",
    "y": "20",
    "str_time": "2",
    "end_time": "10"
}


video.video_add_gif("/Users/master/yx/yxp/web/video/6/1/999/test.mp4", img, "/Users/master/yx/yxp/web/video/6/1/999/c_test.mp4")