import pyautogui
import time

class Controller:
    def __init__(self):
        pass
    
    def mouse(self,r,data):
        pyautogui.moveTo(data['x'] * ( r[0] / data['w'] ), data['y'] * ( r[1] / data['h'] ) )
        pass