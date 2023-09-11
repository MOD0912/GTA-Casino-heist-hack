import pyautogui
import time
import keyboard
import numpy as np
import cv2
import customtkinter as ctk
def pause():
    label.config(text="Script idle")
    root.update()
    while True:
        time.sleep(0.1)
        if keyboard.is_pressed("strg+e"):
            break
        if keyboard.is_pressed("strg+t"):
            exit()
    label.config(text="Print active")
    root.update()
    return True


def click(x, o, t, y):
    print("klick")
    t = list[2]
    xstart = list[0]
    ystart = list[1]
    y = o - 1
    if x == 625:
        x = 1
    else:
        x = 0
    if t == 0:
        time.sleep(0.2)
    t += 1
    list[2] = t
    if x > xstart:
        xchange = +1
    if x == xstart:
        xchange = 0 
    if x < xstart:
        xchange = -1
    if y > ystart:
        ychange = y - ystart
    if y == ystart:
        ychange = 0
    if y < ystart:
        ychange = y - ystart
    list[0] = x
    list[1] = y
    if xchange > 0:
        xdircetion = "d"
    if xchange < 0: 
        xdircetion = "a"
    try:
        keyboard.press_and_release(xdircetion)
    except:
        pass
    if ychange > 0:
        ydirection = "s"
        step = 1
    if ychange < 0:
        ydirection = "w"
        step = -1
    try:
        for esaf in range(0, ychange, step):
            keyboard.press_and_release(ydirection)
    except:
        pass
    if keyboard.is_pressed("strg+r"):
        quit = pause()
        if quit:
            return True
    keyboard.press_and_release("enter")
    if t == 4:
        keyboard.press_and_release("tab")
        list[3] = 0
        control = 0
        while True:
            time.sleep(0.1)
            checkimage = pyautogui.screenshot()
            checkimage = np.array(checkimage)   
            checkimage = checkimage[ycheck:ycheck+heightcheck, xcheck:xcheck+widthcheck]
            checkimage2 = sharpen_image(checkimage)
            for i in liist:
                checkbox = cv2.imread(f"pictures\checkbox{i}.bmp")
                checkbox2 = sharpen_image(checkbox)
                similarity2 = cv2.matchTemplate(checkimage2, checkbox2, cv2.TM_CCOEFF_NORMED)
                similarity = cv2.matchTemplate(checkimage, checkbox, cv2.TM_CCOEFF_NORMED)
                similarity2 = abs(np.max(similarity2) * 100)
                similarity = abs(np.max(similarity) * 100)
                if keyboard.is_pressed("strg+r"):
                    quit = pause()
                    if quit:
                        return True
                list[3] = similarity
                if similarity > 90:
                    control = 1
                if control == 1 and similarity < 30:
                    list[0] = 0
                    list[1] = 0
                    list[2] = 0
                    list[3] = 0
                    return True
        

def sharpen_image(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image


def controll(im, ima, x, o, p, y):
    gray1 = im
    gray2 = ima
    result = cv2.matchTemplate(gray1, gray2, cv2.TM_CCOEFF_NORMED)
    similarity = abs(np.max(result) * 100)
    if similarity > 50:
        print(similarity)
        quit = click(x, o, t, y)
        if quit:
            return True


def movetoandclick():
    a = 0
    while True:
        time.sleep(0.1)
        zahl = 0
        o = 0
        y = ystart
        image = pyautogui.screenshot()
        image = np.array(image)
        for i in range(0, 8):
            if i % 2 == 0:
                y = int(ys[o])
                o +=1
            if zahl == 1:
                x = x1
                zahl = zahl - 1
            else:
                x = x2   
                zahl = zahl + 1
            for p in range(0, 16):
                im = image[y:y+height, x:x+width]
                ima = cv2.imread(f"pictures/{p+1}.bmp") 
                ima = cv2.resize(ima, dsize=(width, height)) 
                a+=1
                
                if keyboard.is_pressed("strg+r"):
                    quit = pause()
                    if quit:
                        continue
                if keyboard.is_pressed("strg+t"):
                    exit()
                quit = controll(im, ima, x, o, p, y)
                if quit:
                    return

root = ctk.CTk()
root.geometry("80x20+0+0")
root.lift()
root.attributes("-topmost", True)
root.wm_overrideredirect(True)
label = ctk.CTkLabel(root, text="Script idle")
label.pack()
root.update()
while not keyboard.is_pressed("strg+e"):
    time.sleep(0.1)
    pass
label.configure(text="Print active")
root.update()
while True:
    w, h = pyautogui.size() 
    x1 = int(w / 3.072)
    x2 = int(w / 4.0)
    zahl = 0
    ystart = int(h / 3.898916967509025)
    width = int(w / 17.94392523364486)
    height = int(h / 10)
    ys = [h / 3.898916967509025, h / 2.5714285714285716, h / 1.9148936170212767, h / 1.5254237288135593]
    t = 0
    y = ystart
    ycheck = 475
    xcheck = 676
    heightcheck = 130
    widthcheck = 568
    list = [0, 0, 0, 0]
    liist = ["b", "w"]
    movetoandclick()

