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
    template = cv2.imread("images/template.png", 0)

    while True:
        left, top, width, height = getWindowCoordinate("Stardew Valley")
        
        screen = np.array(scr.grab({"left": left, "top": top, "width": width, "height": height}))
        screen_bgr = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)
        screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)

        findTemplate = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(findTemplate)

        
        cv2.imshow('Test', screen)

        if cv2.waitKey(1) & 0xFF == 27:
            break
    
    cv2.destroyAllWindows()

def main():
    getScreenGame()

if __name__ == "__main__":
    main()