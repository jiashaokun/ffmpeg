#!/usr/local/bin/python3
# module sys

from ffmpeg import video


# 添加多个图片
img = [
        {
            "img": "01.png",
            "x": "",
            "y": "",
            "str_time": "5",
            "end_time": "15",
        },
        {
            "img": "01.png",
            "x": "",
            "y": "",
            "str_time": "20",
            "end_time": "25.5"
        }
    ]

video.ins_img("test.mp4", img,"out.mp4")


# 添加动图 gif apng
img = {
    "img": "img.apng",
    "x": "20",
    "y": "20",
    "str_time": "2",
    "end_time": "10"
}

video.ins_gif("test.mp4", img, "test.mp4")

# 视频静音 分离音频

video.separate_audio("test.mp4", "out.mp4")

# 视频静音 使用静音帧 将视频静音

video.video_ins_mute_audio("test.mp4", "mute.mp3", "out.mp4")

# 设置视频的分辨率 以及 码率
video.trans_code("test.mp4", "640", "480", "2000", "out.mp4")
