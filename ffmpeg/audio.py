#!/usr/local/bin/python3

import subprocess


# 调整音频播放速率
def audio_speed(input_file, speed, out_file):
    try:
        cmd = "ffmpeg -y -i %s -filter_complex \"atempo=tempo=%s\" %s" % (input_file, speed, out_file)
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False
