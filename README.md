# ffmpeg python

>* 该项目是使用 python 对 FFmpeg 的类库做了一次封装使用，因最近不搞视频，所以很长时间不维护了，大家可以参照写法，使用 python 构建自己的视频处理服务（Dont forget GPU）。

## 系统依赖
ffmpeg 3.0 及以上
ffprobe 3.0 及以上
python 3.0 及以上

mac，linux，windows 相应的 gpu 显卡驱动 （使用硬编码时需支持）

### ffmpeg安装参见
[安装ffmpeg](https://note.youdao.com/s/PgfOK55h)

[ffmpeg命令总结](https://note.youdao.com/s/68D7uJUL)

### Install
```shell
pip install ffmpeg
```

### Use Demo 向视频（指定位置和时间，默认坐标为 0 ）添加 n 张图片
```shell
from ffmpeg import video

# 输入视频
input_file = "demo.mp4"

# 输出视频
out_file = "demo_out.mp4"

# 图片列表
img_data = [
        {
            "img": "demo1.png",
            "x": "",
            "y": "",
            "str_time": "5",
            "end_time": "15",
        },
        {
            "img": "demo2.png",
            "x": "",
            "y": "",
            "str_time": "20",
            "end_time": "25.5"
        }
    ]

video.ins_img(input_file, img_data, out_file)
```

### Demo 视频添加动图 gif apng 等

```shell
from ffmpeg import video

input_file = "demo.mp4"

out_file = "demo_out.mp4"

img_data = {
    "img": "img.apng",
    "x": "20",
    "y": "20",
    "str_time": "2",
    "end_time": "10"
}


video.ins_dynamic_img(input_file, img_data, out_file)
```

### 图片处理   图片转 mp4  5: 时长为 5 秒的 mp4
```shell
from ffmpeg import image

image.img_trans_video("png/text_%02d.jpg", "5", "out.mp4")
```

### 复合模式
```python
from ffmpeg import stream
stream = Stream()
# 输入文件
stream.input(input_file)
# 图片
stream.img("t1.png")
stream.img("t2.png", "10", y=10, str_time=5, end_time=10)
# 动图
stream.img_dynamic("t1.apng", "10", "10", "5", "10")
stream.img_dynamic("t2.gif", x=10, y=10, str_time=5, end_time=9)
# 文字水印
stream.word_water_mark("test1", x="10", y="10", str_time="0", end_time="20", font="ttf.ttf", color="blue")
stream.word_water_mark("test2", x="10", y="10", str_time="0", end_time="20", font="ttf.ttf", color="blue")
# 字幕
stream.subbtitle("tt.srt")
# 显卡加速，该方式目前只适用于 mac 和 navida, 参数size是视频大小，该值越大，越慢
stream.fast("5M")
# 输出文件
stream.out(out_file)
stream.run()
```

