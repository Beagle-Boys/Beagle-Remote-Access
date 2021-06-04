import pyautogui
import time
from src.utils.utils import pil_img_to_bytes

class VideoStream:
    
    def __init__(self):
        pass
    
    def getRes(self):
        return pyautogui.screenshot().size
    
    
    def getFrame(self):
        screenshot = pyautogui.screenshot()
        return pil_img_to_bytes(screenshot)