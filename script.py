import cv2
import mss
import win32gui
import numpy as np
from pynput.keyboard import Key, Controller

keyboard = Controller()

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
            findFish = cv2.matchTemplate(screenGray, fish, cv2.TM_CCOEFF_NORMED)
            _, maxFish, _, fishCoord = cv2.minMaxLoc(findFish)

            findGreenZone = cv2.matchTemplate(screenGray, greenZone, cv2.TM_CCOEFF_NORMED)
            _, maxGreen, _, greenCoord = cv2.minMaxLoc(findGreenZone)

            greenY = greenCoord[1]
            fishY = fishCoord[1]
            print(maxGreen, greenY, maxFish, fishY)
            if greenY - fishY > 0:
                print("C")
                useC(True)
            else:
                useC(False)
        
        cv2.imshow('Test', screen)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cv2.destroyAllWindows()

def main():
    getScreenGame()

if __name__ == "__main__":
    main()