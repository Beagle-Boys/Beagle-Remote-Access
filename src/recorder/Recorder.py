import pyautogui
import time
from src.utils.utils import pil_img_to_bytes
from PIL import ImageDraw

class VideoStream:
    
    def __init__(self):
        pass
    
    def getRes(self):
        return pyautogui.screenshot().size
    
    
    def getFrame(self):
        screenshot = pyautogui.screenshot()
        pointer = pyautogui.position()
        draw = ImageDraw.Draw(screenshot)
        x = pointer[0]
        y = pointer[1]
        r = 5
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(255,0,0,0))
        return pil_img_to_bytes(screenshot)