#!/usr/local/bin/python3

#############################################
# File Name: setup.py
# Author: mage
# Mail: 363604236@qq.com
# Created Time:  2018-9-9 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "ffmpeg",
    version = "1.2.1",
    keywords = ("python ffmpeg"),
    description = "ffmpeg python package url [https://github.com/jiashaokun/ffmpeg]",
    long_description = "ffmpeg python package",
    license = "MIT Licence",

    url = "https://github.com/jiashaokun/ffmpeg",
    author = "SkeyJIA",
    author_email = "363604236@qq.com",

    packages = ['ffmpeg'],
    include_package_data = True,
    platforms = "any",
)
