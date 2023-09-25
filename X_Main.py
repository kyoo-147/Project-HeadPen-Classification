# -*- coding: utf-8 -*-
# Author: mihcuog@AILab
# Contatct: AI-Lab - Smart Things

import tkinter as tk
from tkinter import Message ,Text
from PIL import Image, ImageTk
import pandas as pd
#import datetime
from tkinter import font as tkFont
from tkinter import PhotoImage 
import time
import tkinter.ttk as ttk
import subprocess
import logging
from playsound import playsound


class X_Main():
    def __init__(self):
        # Create info ui
        #self.master = master
        self.play_x_main = playsound(r'C:\new\Start-Up NaVin\All_ProjectS_Com\X_Project_ButBi\alerts\xmain.wav')
        self.xmain = tk.Tk()  
        self.xmain.title("X_Main - @minhcuong-AILab")
        self.xmain.geometry("1300x800")
        self.xmain.resizable(False, False)
        # Background main x
        self.background_image = PhotoImage(file="asset/main0_ui.png")
        self.background_label = tk.Label(self.xmain, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)
        # Main gui
        #self.xmain.attributes('-fullscreen', True) setting fullscreen image
        self.button_X_Detect = tk.Button(self.xmain, text="DETECT",command=self.open_X_Detect,fg="white",anchor='w',justify='left',borderwidth=0  ,width=9  ,height=1 , activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")#.grid(row=8, column=2, padx=5)
        self.button_X_Detect.place(x=310, y=365)
        self.button_X_Stream = tk.Button(self.xmain, text="STREAM",command=self.open_X_Stream,fg="white",anchor='w',justify='left',borderwidth=0  ,width=11  ,height=1 , activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")#.grid(row=8, column=2, padx=5)
        self.button_X_Stream.place(x=310, y=457)
        # self.button_X_Recognition = tk.Button(self.xmain, text="NHẬN DIỆN",command=self.open_X_Recog,anchor='w',justify='left' ,fg="white",borderwidth=0    ,width=9  ,height=1, activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")
        # self.button_X_Recognition.place(x=310, y=430)
        self.button_X_Out = tk.Button(self.xmain, text="EXIT",command=self.out_X_Main,anchor='w',justify='left' ,fg="white",borderwidth=0    ,width=9  ,height=1, activebackground = "Red" ,font=('Helvetica', 15, ' bold '), background="#07080A")
        self.button_X_Out.place(x=330, y=550)

    # Open X_Detect Part---
    def open_X_Detect(self):
        playsound(r'C:\new\Start-Up NaVin\All_ProjectS_Com\X_Project_ButBi\alerts\alert.wav')
        print("******      X_Detected @minhcuong-AILab Already!")
        self.X_Detect_Path = "X_Detect.py"
        subprocess.call(['python', self.X_Detect_Path], shell=True)
    # Open X_Stream Part---
    def open_X_Stream(self):
        playsound(r'C:\new\Start-Up NaVin\All_ProjectS_Com\X_Project_ButBi\alerts\xstream.wav')
        print("******      X_Stream @minhcuong-AILab Already!")
        self.X_Stream_Path = "X_Stream.py"
        subprocess.call(['python', self.X_Stream_Path], shell=True)
    # Out X_Main Program---
    def out_X_Main(self):
        playsound(r'C:\new\Start-Up NaVin\All_ProjectS_Com\X_Project_ButBi\alerts\xclose.wav')
        print("******      X_Main - @minhcuong-AILab ~.~ Hope you enjoy that!!!")
        self.xmain.destroy()
    def run(self):
        self.xmain.mainloop()


def main():
    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Nhớ debug nha!!!")
    logging.info("Check kĩ thông tin đi")
    logging.warning("Đây là cảnh báo cho bạn nè!!!")
    logging.error("Lỗi chương trình rồi bạn ơi!!!")
    logging.critical("Bạn đã làm cái gì vậy?")
    running = X_Main()
    running.run()

if __name__ == "__main__":
    main()






