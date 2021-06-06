import pyautogui
import time

class Controller:
    def __init__(self):
        pass
    
    def mouse_move(self,r,data):
        pyautogui.moveTo(data['x'] * ( r[0] / data['w'] ), data['y'] * ( r[1] / data['h'] ) )
        pass

    def mouse_click(self, r, data):
        key = ['left', 'middle', 'right']
        pyautogui.click(data['x'] * ( r[0] / data['w'] ), data['y'] * ( r[1] / data['h'] ) , button=key[data['button']])

    def press_key(self, data):
        pyautogui.press(data['key'])