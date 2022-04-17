from flask import Flask, render_template
import PIL.Image
from PIL import Image, ImageTk
import pytesseract as tess
tess.pytesseract.tesseract_cmd =  r"C:\Users\zanix\Documents\HackTJ 2022 Flask\app\tesseract.exe"

from tkinter import *
import pyautogui
import datetime
import pyperclip
import time

app = Flask(__name__)

class Application():
    
    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        self.text = ""
        # root.configure(background = 'red')
        # root.attributes("-transparentcolor","red")

        root.attributes("-transparentcolor", "blue")
        root.geometry('500x60+200+200')  # set new geometry
        root.title('Selector')
        self.menu_frame = Frame(master, bg="blue")
        self.menu_frame.pack(fill=BOTH, expand=YES)

        self.buttonBar = Frame(self.menu_frame,bg="")
        self.buttonBar.pack(fill=BOTH,expand=YES)
        

        self.snipButton = Button(self.buttonBar, width = 3, command=self.createScreenCanvas, background='red')
        self.snipButton.pack(expand=YES)

        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        

        label = Label(root, text = " ")
        label.pack()   

    def takeBoundedScreenShot(self, x1, y1, x2, y2):     
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        x = datetime.datetime.now()
        im.save(r"C:\Users\zanix\Documents\HackTJ 2022 Flask\app\snips\img.png")
        img_path = r"C:\Users\zanix\Documents\HackTJ 2022 Flask\app\snips\img.png"
        img = PIL.Image.open(img_path)
        tess.tesseract_cmd = img_path
        self.text = tess.image_to_string(img)
        pyperclip.copy(self.text)
        print(self.text)
        

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

        self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
        self.screenCanvas.pack(fill=BOTH, expand=YES)

        self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
        self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
        self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.master_screen.attributes('-fullscreen', True)
        self.master_screen.attributes('-alpha', .3)
        self.master_screen.lift()
        self.master_screen.attributes("-topmost", True)

    def on_button_release(self, event):

        if self.start_x <= self.curX and self.start_y <= self.curY:
            self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

        elif self.start_x >= self.curX and self.start_y <= self.curY:
            self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

        elif self.start_x <= self.curX and self.start_y >= self.curY:
            self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

        elif self.start_x >= self.curX and self.start_y >= self.curY:
            self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)

        self.exitScreenshotMode()
        return event

    def exitScreenshotMode(self):
        print("Screenshot mode exited")
        self.screenCanvas.destroy()
        self.master_screen.withdraw()
        root.deiconify()

    def exit_application(self):
        print("Application exit")
        root.quit()

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.screenCanvas.canvasx(event.x)
        self.start_y = self.screenCanvas.canvasy(event.y)

        self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

    def on_move_press(self, event):
        self.curX, self.curY = (event.x, event.y)
        # expand rectangle as you drag the mouse
        self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

@app.route('/')
def json():
    return render_template('json.html')

@app.route('/background_process_test')
def background_process_test():
    
    global root
    root = Tk()
    app = Application(root)
    root.mainloop()
    return ("nothing")

    

if __name__ == "__main__":
    
    app.run()