import pyautogui
import time

class Controller:
    def __init__(self):
        pass
    
    def mouse_move(self,r,data):
        pyautogui.moveTo(data['x'] * ( r[0] / data['w'] ), data['y'] * ( r[1] / data['h'] ) )
        pass

    def mouse_click_up(self,data):
        key = ['left', 'middle', 'right']
        pyautogui.mouseUp(button=key[data['button']])

    def mouse_click_down(self,data):
        key = ['left', 'middle', 'right']
        pyautogui.mouseDown(button=key[data['button']])

    def press_key_up(self, data):
        pyautogui.keyUp(data['key'])

    def press_key_down(self, data):
        pyautogui.keyDown(data['key'])