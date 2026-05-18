import cv2
import mss
import win32gui
import numpy as np

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

    while True:
        left, top, width, height = getWindowCoordinate("Stardew Valley")
        screen = np.array(scr.grab({"left": left, "top": top, "width": width, "height": height}))
        cv2.imshow('Test', screen)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cv2.destroyAllWindows()

def main():
    getScreenGame()

if __name__ == "__main__":
    main()