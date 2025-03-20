import pyautogui
import time
import keyboard
import numpy as np
import cv2
import customtkinter as ctk
import os

ctk.deactivate_automatic_dpi_awareness()

'''
commands:
    strg+e = start script
    strg+r = pause script
    strg+t = exit script
'''

class FingerprintHack:
    def __init__(self):
        self.state = {'x': 0, 'y': 0, 't': 0, 'similarity': 0}
        self.liist = ["b", "w"]
        self.counter = 0
        self.setup_ui()

    def setup_ui(self):
        self.root = ctk.CTk()
        self.root.geometry("80x20+0+0")
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.wm_overrideredirect(True)
        self.label = ctk.CTkLabel(self.root, text="Script idle")
        self.label.pack()
        self.root.update()

    def pause(self):
        self.label.configure(text="Script idle")
        self.root.update()
        while True:
            time.sleep(0.1)
            if keyboard.is_pressed("strg+e"):
                break
            if keyboard.is_pressed("strg+t"):
                exit()
        self.label.configure(text="Print active")
        self.root.update()
        return True

    def click(self, x, o, t, y):
        print("klick")
        t = self.state['t']
        xstart = self.state['x']
        ystart = self.state['y']
        y = o - 1
        x = 1 if x == self.x1 else 0
        if t == 0:
            time.sleep(0.2)
        t += 1
        self.state['t'] = t
        xchange = 1 if x > xstart else -1 if x < xstart else 0
        ychange = y - ystart if y != ystart else 0
        self.state['x'] = x
        self.state['y'] = y
        xdirection = "d" if xchange > 0 else "a" if xchange < 0 else None
        ydirection = "s" if ychange > 0 else "w" if ychange < 0 else None
        step = 1 if ychange > 0 else -1 if ychange < 0 else 0

        if xdirection:
            try:
                keyboard.press_and_release(xdirection)
            except:
                pass
        if ydirection:
            try:
                for _ in range(0, abs(ychange), step):
                    keyboard.press_and_release(ydirection)
            except:
                pass
        if keyboard.is_pressed("strg+r"):
            if self.pause():
                return True
        keyboard.press_and_release("enter")
        if t == 4:
            keyboard.press_and_release("tab")
            self.state['similarity'] = 0
            control = 0
            while True:
                time.sleep(0.1)
                checkimage = np.array(pyautogui.screenshot())[self.ycheck:self.ycheck+self.heightcheck, self.xcheck:self.xcheck+self.widthcheck]
                checkimage = cv2.resize(checkimage, (130, 568))
                checkimage2 = self.sharpen_image(checkimage)
                cv2.imwrite(f"try/checkimage{self.counter}.bmp", checkimage)
                self.counter += 1
                for i in self.liist:
                    checkbox = cv2.imread(f"pictures/checkbox{i}.bmp")
                    checkbox2 = self.sharpen_image(checkbox)
                    # Ensure the template is smaller than or equal to the source image
                    if checkbox2.shape[0] > checkimage2.shape[0] or checkbox2.shape[1] > checkimage2.shape[1]:
                        checkbox2 = cv2.resize(checkbox2, (checkimage2.shape[1], checkimage2.shape[0]))
                    if checkbox.shape[0] > checkimage.shape[0] or checkbox.shape[1] > checkimage.shape[1]:
                        checkbox = cv2.resize(checkbox, (checkimage.shape[1], checkimage.shape[0]))
                    # Debugging: Print shapes of images
                    print(f"checkimage2 shape: {checkimage2.shape}, checkbox2 shape: {checkbox2.shape}")
                    similarity2 = abs(np.max(cv2.matchTemplate(checkimage2, checkbox2, cv2.TM_CCOEFF_NORMED)) * 100)
                    similarity = abs(np.max(cv2.matchTemplate(checkimage, checkbox, cv2.TM_CCOEFF_NORMED)) * 100)
                    if keyboard.is_pressed("strg+r"):
                        if self.pause():
                            return True
                    self.state['similarity'] = similarity

                    print(f"similarity: {similarity}, similarity2: {similarity2}")
                    if similarity > 60 or similarity2 > 60:
                        control = 1
                        print("found")
                    if control == 1 and similarity < 30:
                        self.state.update({'x': 0, 'y': 0, 't': 0, 'similarity': 0})
                        print("reset")
                        return True

    def sharpen_image(self, image):
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        return cv2.filter2D(image, -1, kernel)

    def controll(self, im, ima, x, o, p, y):
        similarity = abs(np.max(cv2.matchTemplate(im, ima, cv2.TM_CCOEFF_NORMED)) * 100)
        if similarity > 50:
            cv2.imwrite(f"try/checkimage{self.counter}.bmp", im)
            self.counter += 1
            print(similarity)
            if self.click(x, o, self.state['t'], y):
                return True

    def movetoandclick(self):
        while True:
            time.sleep(0.1)
            o = 0
            y = self.ystart
            image = np.array(pyautogui.screenshot())
            for i in range(8):
                if i % 2 == 0:
                    y = int(self.ys[o])
                    o += 1
                x = self.x1 if i % 2 == 0 else self.x2
                for p in range(16):
                    im = image[y:y+self.height, x:x+self.width]
                    ima = cv2.imread(f"pictures/{p+1}.bmp")
                    ima = cv2.resize(ima, (self.width, self.height))
                    if keyboard.is_pressed("strg+r"):
                        if self.pause():
                            continue
                    if keyboard.is_pressed("strg+t"):
                        exit()
                    if self.controll(im, ima, x, o, p, y):
                        return

    def clear_try_folder(self):
        for file in os.listdir("try"):
            os.remove(f"try/{file}")

    def run(self):
        while not keyboard.is_pressed("strg+e"):
            time.sleep(0.1)

        self.label.configure(text="Print active")
        self.root.update()

        self.clear_try_folder()

        while True:
            w, h = pyautogui.size()
            self.x1 = int(w / 3.072)
            self.x2 = int(w / 4.0)
            self.ystart = int(h / 3.898916967509025)
            self.width = int(w / 17.94392523364486)
            self.height = int(h / 10)
            self.ys = [h / 3.898916967509025, h / 2.5714285714285716, h / 1.9148936170212767, h / 1.5254237288135593]
            self.ycheck = int(h * 0.44)
            self.xcheck = int(w * 0.35)
            self.heightcheck = int(h * 0.12)
            self.widthcheck = int(w * 0.3)
            self.state = {'x': 0, 'y': 0, 't': 0, 'similarity': 0}
            self.movetoandclick()

if __name__ == "__main__":
    hack = FingerprintHack()
    hack.run()

