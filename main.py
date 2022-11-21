import cv2 as cv
from time import time, sleep
import win32api, win32con
from windowcapture import WindowCapture, DESKTOP_SCALE
import pyautogui
import sys
sys.path.append('yolov7-main')
import detect as yolov7


def rel_mouse_event(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)


def move_mouse(x, y, duration):
    steps = 20
    for i in range(0, steps):
        rel_mouse_event(int(x / steps), int(y / steps))
        sleep(duration / steps)

def moveChar():
    sleep(3)
    print('moving...')
    pyautogui.keyDown('w')
    sleep(2)
    pyautogui.keyUp('w')
    pyautogui.keyDown('s')
    sleep(2)
    pyautogui.keyUp('s')
    move_mouse(200, 0, 1)
    sleep(1)
    move_mouse(200, 0, 1)
    sleep(1)
    move_mouse(200, 0, 1)
    sleep(1)
    move_mouse(200, 0, 1)
    sleep(1)
    print('char: rest.')

loop_time = time()
print('Started.')
detector = yolov7.Detector('yolov7-main/yolov7_custom300epochs.pt', 0.45, 640, True, True)
wincap = WindowCapture('Decentraland')

rest_time = time()
while True:
    print('rest time', time() - rest_time)
    windowCenterY = wincap.h / 2
    windowCenterX = wincap.w / 2
    img, det = detector.detect(wincap.get_screenshot())
    pyautogui.keyUp('w')
    pyautogui.keyUp('s')

    dBoxCenterX = None
    dBoxCenterY = None
    c1 = None
    c2 = None
    if len(det):
        for *xyxy, conf, cls in reversed(det):
            c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
            print('Detection box: ', c1, c2)
            c1x, c1y = c1
            c2x, c2y = c2
            dBoxCenterX = c1x + ((c2x - c1x) / 2)
            dBoxCenterY = c1y + ((c2y - c1y) / 2)
            print('Detection box center, xy: ', dBoxCenterX, dBoxCenterY)
    imS = cv.resize(img, (int(wincap.w / 1.5), int(wincap.h / 1.5)))
    cv.imshow('Computer Vision', imS)
    # cv.waitKey(1)  # 1 millisecond

    if dBoxCenterY is not None and dBoxCenterX is not None:
        rest_time = time()
        diffX = windowCenterX - dBoxCenterX
        diffY = windowCenterY - dBoxCenterY
        print('DIFF, xy:', int(diffX), int(diffY))
        print('c2[0] - c1[0]', c2[0] - c1[0])
        move_mouse(int(-diffX), int(-diffY + 220), 0.1)
        if c2[0] - c1[0] < 600:
            pyautogui.keyDown('w')
        else:
            pyautogui.keyUp('w')
            pyautogui.click()
            pyautogui.keyDown('s')
            # move_mouse(2500, 0, 0.5)
    else:
        if time() - rest_time > 3:
            print('RESET')
            pyautogui.click()
            move_mouse(1000, -100, 0.1)
            rest_time = time()

    # debug the loop rate
    print('FPS {}'.format(int(1 / (time() - loop_time))))
    loop_time = time()
    if cv.waitKey(1) == ord('q'):
       cv.destroyAllWindows()
       break
    # sleep(1)
print('Done.')
