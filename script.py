import cv2
import mss
import win32gui
import numpy as np
from pynput.keyboard import Key, Controller

keyboard = Controller()

GREENZONE_UP = np.array([43, 255, 229])
GREENZONE_LOW = np.array([43, 255, 229])
FISH_UP = np.array([96, 243, 175])
FISH_LOW = np.array([76, 230, 100])

def useC(press):
    if press:
        keyboard.press("c")
    else:
        keyboard.release("c")

def getWindowCoordinate(name):
    try:
        hwnd = win32gui.FindWindow(None, name)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    
        width = right - left
        height = bottom - top
        return left, top, width, height
    except Exception as e:
        print(f"Error: {e}")

def getScreenGame():
    scr = mss.mss()
    template = cv2.imread("images/template.png", 0)
    fish = cv2.imread("images/fish.png", 0)
    greenZone = cv2.imread("images/greenzone.png", 0 )

    while True:
        left, top, width, height = getWindowCoordinate("Stardew Valley")
        
        screen = np.array(scr.grab({"left": left, "top": top, "width": width, "height": height}))
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

        findTemplate = cv2.matchTemplate(screenGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(findTemplate)
        if max_val > 0.5:
            fishRegion = np.array(scr.grab({"left": left, "top": top, "width": width, "height": height}))
        
        cv2.imshow('Test', screen)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    getScreenGame()