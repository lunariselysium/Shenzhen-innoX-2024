import sensor
import image
import time
import lcd

lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 100)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)

clock = time.clock()
color_thresholds = [
    (5, 67, 15, 75, -10, 51),# Red
    (6, 27, -30, -9, -9, 14)x, # Green
    (14, 66, 1, 38, -56, -12),# Blue
    (19, 100, -6, 26, 65, 23),# Yellow
]
color_strings = ['Red', 'Green', 'Blue', 'Yellow']

while True:
    clock.tick()
    img = sensor.snapshot()
    for color_idx, threshold in enumerate(color_thresholds):
        blobs = img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10)
        if blobs:
            for blob in blobs:
                color_new = (255 , 255,255)
                if color_idx == 0 :
                    color_new = (255 , 0,0)
                elif color_idx == 1:
                    color_new = ( 0,255 ,0)
                elif color_idx == 2:
                    color_new = ( 0,0,255)
                elif color_idx == 3:
                    color_new = ( 255,255,0)
                img.draw_rectangle(blob.rect(), color=color_new,thickness = 3)
                img.draw_cross(blob.cx(), blob.cy(), color=color_new)
                img.draw_string(blob.cx() + 10, blob.cy() - 10, color_strings[color_idx], color=color_new)
    lcd.display(img)
    print(clock.fps())
