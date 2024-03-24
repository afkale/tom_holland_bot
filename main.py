'''
Python bot for tim hortons
'''
import json
import tkinter as tk
import cv2
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
from pygame import mixer
from bot.hortons import HortonsBot


mixer.init()
mixer.music.load('sound.mp3')


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interfaz con Cámara")
        self.root.geometry("600x500")

        self.info_label = tk.Label(
            root, text="Tom Holland", font=("Helvetica", 16))

        self.frame = tk.Frame(root)
        self.frame.pack()

        self.cap = cv2.VideoCapture(0)

        self.bot = HortonsBot()
        self.readed_urls = []

        self.frame_loop()

    def print_codes(self):
        if not hasattr(self, 'code_list'):
            self.code_list = tk.Listbox(self.root)
        printed_codes = self.code_list.get(0, tk.END)
        for code in self.bot.codes:
            if code not in printed_codes:
                self.code_list.insert(tk.END, code)
        self.code_list.pack()

    def print_camera(self, image):
        if not hasattr(self, 'camera_label'):
            self.camera_label = tk.Label(self.frame, image=image)
            self.camera_label.image = image
            self.camera_label.pack()
        else:
            self.camera_label.configure(image=image)
            self.camera_label.image = image

    def frame_loop(self):
        _, frame = self.cap.read()
        if frame is not None:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image=image)

            barcodes = decode(frame) or []
            for barcode in barcodes:
                url = barcode.data.decode('utf-8')
                if url in self.readed_urls:
                    print("Este codigo se esta procesando")
                    continue
                mixer.music.play()
                self.readed_urls.append(url)
                self.bot.fill_out_survey(url)
                self.print_codes()
            self.print_camera(image)
        self.root.after(10, self.frame_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()
