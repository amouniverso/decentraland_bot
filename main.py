import cv2 as cv
from time import time, sleep
import win32api, win32con
from windowcapture import WindowCapture, DESKTOP_SCALE
import pyautogui
import sys
import random
sys.path.append('yolov7-main')
import detect as yolov7
import os
import subprocess

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

def click_wallet(menuScreen):
    walletX = menuScreen.left + ((menuScreen.right - menuScreen.left) / 3)
    walletY = menuScreen.top + ((menuScreen.bot - menuScreen.top) / 3)
    pyautogui.click(walletX, walletY + 200)
    sleep(2)
    pyautogui.click(walletX, walletY + 200)
    sleep(2)


def click_profile(gameScreen):
    pyautogui.press('p')
    sleep(1)

def click_graphics(gameScreen):
    pyautogui.click(gameScreen.left + 100, gameScreen.top + 400)
    sleep(2)

def select_resolution(gameScreen):
    pyautogui.click(gameScreen.left + 1400, gameScreen.top + 360)
    sleep(1)
    pyautogui.click(gameScreen.left + 1400, gameScreen.top + 520)
    sleep(2)
    pyautogui.click(gameScreen.left + 1500, gameScreen.top + 370)
    sleep(1)
    pyautogui.click(gameScreen.left + 1500, gameScreen.top + 610)
    sleep(1)

def set_fps(gameScreen):
    pyautogui.click(gameScreen.left + 1000, gameScreen.top + 490)
    sleep(1)
    pyautogui.click(gameScreen.left + 1000, gameScreen.top + 640)
    sleep(1)
    pyautogui.press('p')

def goto_wondermine(gameScreen):
    pyautogui.press('m')
    sleep(1)
    pyautogui.press('p')
    sleep(1)
    pyautogui.press('m')
    sleep(1)
    pyautogui.drag(0, 800, 1, button='left')
    pyautogui.move(0, -800)
    pyautogui.drag(0, 800, 1, button='left')
    sleep(1)
    pyautogui.moveTo(gameScreen.left + 280, gameScreen.top + 520)
    pyautogui.click()
    sleep(1)
    pyautogui.moveTo(gameScreen.left + 400, gameScreen.top + 1000)
    pyautogui.click()
    sleep(20)
    pyautogui.keyDown('w')
    sleep(5)
    pyautogui.keyUp('w')
    pyautogui.click()
    pyautogui.scroll(10)

def init_game():
    os.startfile('C:\\Program Files\\Decentraland\\decentraland.exe')
    print('app opened.')
    sleep(5)
    menuScreen = WindowCapture('Decentraland BETA 0.1.44')
    click_wallet(menuScreen)
    sleep(40)
    gameScreen = WindowCapture('Decentraland')
    click_profile(gameScreen)
    click_graphics(gameScreen)
    select_resolution(gameScreen)
    set_fps(gameScreen)
    gameScreen = WindowCapture('Decentraland')
    goto_wondermine(gameScreen)
    print('wondermine initialized.')
    return gameScreen


print('bot started.')
wincap = init_game()
detector = yolov7.Detector('yolov7-main/yolov7_custom300epochs.pt', 0.45, 640, True, True)
loop_time = time()
rest_time = time()
kill_time = time()
restart_time = 0
while True:
    if (time() - restart_time) > 60 * 60 * 12 and kill_time == 0:
        wincap = init_game()
        restart_time = 0
        kill_time = time()
        print('app restarted.')
    if (time() - kill_time) > 60 * 60 * 2 and restart_time == 0:
        subprocess.call("TASKKILL /F /IM Decentraland.exe", shell=True)
        kill_time = 0
        restart_time = time()
        print('app closed.')
    if restart_time == 0:
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
        # imS = cv.resize(img, (int(wincap.w / 1.5), int(wincap.h / 1.5)))
        # cv.imshow('Computer Vision', imS)
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
                pyautogui.click()
                pyautogui.keyDown('s')
                # move_mouse(2500, 0, 0.5)
        else:
            if time() - rest_time > 1:
                print('RESET')
                pyautogui.click()
                pyautogui.click()
                move_mouse(0, 3000, 0)
                sleep(0.1)
                move_mouse(0, -1500, 0)
                move_mouse(1000, 0, 0)
                rest_time = time()

        # debug the loop rate
        print('FPS {}'.format(int(1 / (time() - loop_time))))
        loop_time = time()
    else:
        print('restart_time', (time() - restart_time) / 3600)
        sleep(60)
