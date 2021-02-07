# -*- coding: utf-8 -*-

import os
import requests 
import time
import random 
from urllib.parse import quote
import  string
import numpy as np 


def number_to_chinese():
    D = dict()
    digits = list("零一二三四五六七八九十")

    result = dict()
    for number in range(1, 100):
        if number <= 10:
            result[number] = digits[number]
        else:
            a = number//10
            b = number%10
            if a == 1:
                if b == 0:
                    result[number] = "十"
                else:
                    result[number] = "十" + digits[b]
            else:
                if b == 0:
                    result[number] = digits[a] + "十"
                else:
                    result[number] = digits[a] + "十" + digits[b]

    return result


def download():
    converter = number_to_chinese()
    for i in range(1, 81):
        url_chinese = r"https://zh.m.wikisource.org/zh-hans/脂硯齋重評石頭記/第number回".replace("number", converter[i])
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
