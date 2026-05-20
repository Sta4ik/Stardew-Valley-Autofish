import cv2
import mss
import win32gui
import numpy as np
from pynput.keyboard import Key, Controller

keyboard = Controller()

GREENZONE_UP = np.array([85, 255, 255])
GREENZONE_LOW = np.array([40, 80, 80])
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
    heightFishRegion, widthFishRegion = template.shape[:2]

    while True:
        left, top, width, height = getWindowCoordinate("Stardew Valley")
        
        screen = np.array(scr.grab({"left": left, "top": top, "width": width, "height": height}))
        screenGray = cv2.cvtColor(screen, cv2.COLOR_BGRA2GRAY)

        findTemplate = cv2.matchTemplate(screenGray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, maxFishRegionCoord = cv2.minMaxLoc(findTemplate)
        if max_val > 0.5:
            fishingRegion = np.array(scr.grab({"left": left + maxFishRegionCoord[0], "top": top + maxFishRegionCoord[1], "width": widthFishRegion, "height": heightFishRegion}))
            fishingRegionBGR = cv2.cvtColor(fishingRegion, cv2.COLOR_BGRA2BGR)
            fishingRegionHSV = cv2.cvtColor(fishingRegionBGR, cv2.COLOR_BGR2HSV)

            maskGreen = cv2.inRange(fishingRegionHSV, GREENZONE_LOW, GREENZONE_UP)
            contours, _ = cv2.findContours(maskGreen, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                contour = max(contours, key=cv2.contourArea)
                _, y, _, h = cv2.boundingRect(contour)
                greenY = y + h/2
            print(greenY)
        cv2.imshow('Test', screen)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    getScreenGame()