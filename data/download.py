# -*- coding: utf-8 -*-

import os
import requests 
import time
import random 
from urllib.parse import quote
import  string
import numpy as np

def converter(number):
    if number < 10:
        return "00" + str(number)
    elif number < 100:
        return "0" + str(number)
    return str(number)

def download():
    for i in range(1, 121):
        url_chinese = r"https://zh.m.wikisource.org/zh-hans/紅樓夢/第number回".replace("number", converter(i))
        url = quote(url_chinese, safe = string.printable)   # safe表示可以忽略的字符
        print(url_chinese)
        response = requests.get(url)
        response.encoding = "utf-8"
        if response.status_code == 200:
            writer = open("Dream_of_Red_Chamber_" + str(i) + ".html", "w")
            writer.write(response.text + "\n")
            writer.close()
            time_interval = np.random.normal(6.0, 1.0)
            time.sleep(time_interval)
        else:
            print("Error in getting " + url)
            break

def main():
    download()
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
