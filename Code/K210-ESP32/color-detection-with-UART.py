# Untitled - By: HuangShukun - 周四 12月 14 2023

import sensor
import image
import lcd
import time
from modules import ybserial
import math
# 初始化LCD显示屏
lcd.init()

# 重置传感器
sensor.reset()

# 设置像素格式为RGB565
sensor.set_pixformat(sensor.RGB565)

# 设置帧大小为QVGA
sensor.set_framesize(sensor.QVGA)

# 运行传感器
sensor.run(1)

# 定义阈值，用于识别物体
green_threshold = (2, 80, -57, -10, -112, 42)
yellow_threshold=(0,0,0,0,0,0)
red_threshold=(0,0,0,0,0,0)
blue_threshold=(0,0,0,0,0,0)
serial = ybserial(baudrate=115200)


def find_best_box(blos,c):
    max_blos=blos[0]
    for b in blos:
        if(b[2]*b[3]>max_blos[2]*max_blos[3]):
            max_blos=b

    tmp = img.draw_rectangle(max_blos[0:4],color=c)
    tmp = img.draw_cross(max_blos[5], max_blos[6],color=c)
    return max_blos


while True:
    # 获取传感器拍摄的图像
    img = sensor.snapshot()

    # 在图像中寻找绿色物体的区域
    green_blobs = img.find_blobs([green_threshold], pixels_threshold=500, area_threshold=11844)
    yellow_blobs = img.find_blobs([yellow_threshold], pixels_threshold=500, area_threshold=11844)
    red_blobs = img.find_blobs([red_threshold], pixels_threshold=500, area_threshold=11844)
    blue_blobs = img.find_blobs([blue_threshold], pixels_threshold=500, area_threshold=11844)
    #serial.send(text)
    if(green_blobs):
        print(green_blobs)
        find_best_box(green_blobs,(0,249,26))
        serial.send_byte(0x01)
    if(yellow_blobs):
        find_best_box(yellow_blobs,(255,251,13))
        serial.send_byte(0x02)
    if(red_blobs):
        find_best_box(red_blobs,(255,39,0))
        serial.send_byte(0x03)
    if(blue_blobs):
        find_best_box(blue_blobs,(5,50,255))
        serial.send_byte(0x04)

    # 在LCD显示屏上显示图像
    lcd.display(img)
