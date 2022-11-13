import numpy as np
import win32gui, win32ui, win32con
import time

DESKTOP_SCALE = 2.25

class WindowCapture:

    # properties
    w = 0
    h = 0
    hwnd = None
    left = 0
    top = 0
    right = 0
    bot = 0

    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

        # get the window size
        _left, _top, _right, _bot = win32gui.GetWindowRect(self.hwnd)
        self.left = int(_left * DESKTOP_SCALE)
        self.top = int(_top * DESKTOP_SCALE)
        self.right = int(_right * DESKTOP_SCALE)
        self.bot = int(_bot * DESKTOP_SCALE)
        self.w = self.right - self.left
        self.h = self.bot - self.top

        win32gui.SetForegroundWindow(self.hwnd)
        time.sleep(1.0)

        # account for the window border and titlebar and cut them off
        # border_pixels = 8
        # titlebar_pixels = 30
        # self.w = self.w - (border_pixels * 2)
        # self.h = self.h - titlebar_pixels - border_pixels
        # self.cropped_x = border_pixels
        # self.cropped_y = titlebar_pixels
        # #
        # # # set the cropped coordinates offset so we can translate screenshot
        # # # images into actual screen positions
        # self.offset_x = window_rect[0] + self.cropped_x
        # self.offset_y = window_rect[1] + self.cropped_y

    def get_screenshot(self):
        hdesktop = win32gui.GetDesktopWindow()
        hwndDC = win32gui.GetWindowDC(hdesktop)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.w, self.h)

        saveDC.SelectObject(saveBitMap)

        saveDC.BitBlt((0, 0), (self.w, self.h), mfcDC, (self.left, self.top), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        # saveBitMap.SaveBitmapFile(saveDC, 'debug.bmp')
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # # free resources
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        return img

    # find the name of the window you're interested in.
    # once you have it, update window_capture()
    # https://stackoverflow.com/questions/55547940/how-to-get-a-list-of-the-name-of-every-open-window
    def list_window_names(self):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)

    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)