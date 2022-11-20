import cv2 as cv
from time import time, sleep
import win32api, win32con
from windowcapture import WindowCapture, DESKTOP_SCALE
import pyautogui
import sys
sys.path.append('yolov7-main')
import detect as yolov7


def moveMouse(x, y, duration):
    steps = 20
    for i in range(0, steps):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x / steps), int(y / steps), 0, 0)
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
    moveMouse(200, 0, 1)
    sleep(1)
    moveMouse(200, 0, 1)
    sleep(1)
    moveMouse(200, 0, 1)
    sleep(1)
    moveMouse(200, 0, 1)
    sleep(1)
    print('char: rest.')


wincap = WindowCapture('Decentraland')
loop_time = time()
print('Started.')

while True:
    img = yolov7.detect('yolov7-main/yolov7_custom300epochs.pt', 0.1, 640, wincap.get_screenshot(), True, True)
    # get an updated image of the game
    #imS = cv.resize(wincap.get_screenshot(), (int(wincap.w / 1.5), int(wincap.h / 1.5)))
    #cv.imshow('Computer Vision', img)

    # debug the loop rate
    print('FPS {}'.format(int(1 / (time() - loop_time))))
    loop_time = time()
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    input("Press Enter to continue...")
    if cv.waitKey(1) == ord('q'):
       cv.destroyAllWindows()
       break
    #sleep(3)
    break

print('Done.')
