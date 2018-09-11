#!/usr/local/bin/python3
# module sys

from ffmpeg import video

from ffmpeg import audio

from ffmpeg import image


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

video.ins_dynamic_img("test.mp4", img, "test.mp4")

# 视频静音 分离音频

video.separate_audio("test.mp4", "out.mp4")

# 视频静音 使用静音帧 将视频静音

video.video_ins_mute_audio("test.mp4", "mute.mp3", "out.mp4")

# 设置视频的分辨率 以及 码率
video.trans_code("test.mp4", "640", "480", "2000", "out.mp4")

# 视频加弹幕 context 弹幕内容 str_time 是第几秒显示 speet 速率 默认 150 当显示时间一定时 该值越大，速度越快
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

video.ins_barrage("test.mp4", bage, "out.mp4")

# 调整视频速率 speed 小于 1 减速，大于 1 加速 1 等速
video.playback_speed("test.mpt", "1.5", "out.mp4")

# 倒放视频 + 音频
video.a_v_reverse("test.mp4", "out.mp4")

# 倒放视频 音频不变
video.v_reverse("test.mp4", "out.mp4")

# 视频截取 从 str_second 开始截取 duration 时长的视频
video.v_intercept("1.mp4", "10", "5", "out.mp4")

# 视频转图片
video.video_trans_img("test.mp4", "a/b/c", "img_name", "png")

# 调整音频速率
audio.a_speed("test.mp3", "2", "out.mp3")

# 音频拼接
audio.a_split(["1.mp3", "2.mp3", "3.mp3"], "out.mp3")

# 设置音频音量大小
audio.a_volume("1.mp3", "8", "out.mp3")

# 音频截取
audio.a_intercept("1.mp3", "10", "5", "out.mp3")

# 图片转换gif动图
image.img_trans_gif("png/text_%02d.jpg", "out.gif")

# 图片转 mp4  5: 时长为 5 秒的 mp4
image.img_trans_video("png/text_%02d.jpg", "5", "out.mp4")

# gif 转 png
image.gif_trans_img("test.gif", "a/b/c", "img_name", "png")
