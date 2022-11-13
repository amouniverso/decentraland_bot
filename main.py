import cv2 as cv
from time import time, sleep
from windowcapture import WindowCapture, DESKTOP_SCALE

# initialize the WindowCapture class
wincap = WindowCapture('Decentraland')
# print(wincap.list_window_names())

loop_time = time()
while True:
    # get an updated image of the game
    imS = cv.resize(wincap.get_screenshot(), (int(wincap.w / DESKTOP_SCALE), int(wincap.h / DESKTOP_SCALE)))
    cv.imshow('Computer Vision', imS)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
       cv.destroyAllWindows()
       break

print('Done.')
