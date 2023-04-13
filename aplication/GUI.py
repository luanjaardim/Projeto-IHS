from vision import *
from tracker import *
import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk

class ColorSettings:
    def __init__(self, frame):
        #hue sliders
        self.hue_min_slider = tk.Scale(frame, label='HUE Min', from_=0, to=180, orient=tk.HORIZONTAL)
        self.hue_min_slider.grid(row=0, column=0, pady=10, padx=20)
        self.hue_max_slider = tk.Scale(frame, label='HUE Max', from_=0, to=180, orient=tk.HORIZONTAL)
        self.hue_max_slider.set(180)
        self.hue_max_slider.grid(row=0, column=1, pady=10, padx=20)
        #saturation sliders
        self.sat_min_slider = tk.Scale(frame, label='Saturation Min', from_=0, to=255, orient=tk.HORIZONTAL)
        self.sat_min_slider.grid(row=1, column=0, pady=10, padx=20)
        self.sat_max_slider = tk.Scale(frame, label='Saturation Max', from_=0, to=255, orient=tk.HORIZONTAL)
        self.sat_max_slider.set(255)
        self.sat_max_slider.grid(row=1, column=1, pady=10, padx=20)
        #value sliders
        self.val_min_slider = tk.Scale(frame, label='Value Min', from_=0, to=255, orient=tk.HORIZONTAL)
        self.val_min_slider.grid(row=2, column=0, pady=10, padx=20)
        self.val_max_slider = tk.Scale(frame, label='Value Max', from_=0, to=255, orient=tk.HORIZONTAL)
        self.val_max_slider.set(255)
        self.val_max_slider.grid(row=2, column=1, pady=10, padx=20)
    def getValues(self):
        lowerValues = np.array([self.hue_min_slider.get(),self.sat_min_slider.get(),self.val_min_slider.get()])
        upperValues = (np.array([self.hue_max_slider.get(),self.sat_max_slider.get(),self.val_max_slider.get()]))
        return lowerValues, upperValues

class GUI:
    def __init__(self, root):

        self.tracker = Tracker()

        #setup camera
        self.camera = Vision()

        #create window
        self.window = root
        self.window.title("Projeto Torreta - Interface Hardware-Software") # Set the title of the window
        
        self.upperRow = tk.Frame()
        self.upperRow.pack()
        self.lowerRow = tk.Frame()
        self.lowerRow.pack()
        
        # Create the canvas for img preview
        self.canvas = tk.Canvas(self.upperRow, width=400, height=300)
        self.canvas.grid(row=0,column=0)
        self.maskCanvas = tk.Canvas(self.lowerRow, width=400, height=300)
        self.maskCanvas.grid(row=0,column=0)
        
        #image settings stuff
        self.settingsFrame = tk.LabelFrame(self.lowerRow, text='Configuração de Cores')
        self.settingsFrame.grid(row=0, column=1)
        self.inputField = ColorSettings(self.settingsFrame)
    
        # start the video display loop
        self.update()
    
    def update(self):
        #gets current frame from camera object
        frame = self.camera.getFrame()
        
        #get hsv frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #uptade threshold values
        lower_range, upper_range = self.inputField.getValues()
        #uptade threshold values on tracker
        self.tracker.update_HSV_thresh(lower_range, upper_range)
        #create a mask
        mask = cv2.inRange(hsv, lower_range, upper_range)

        #detect object position
        frame = self.tracker.detect(mask, frame)

        # Convert BGR to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        # Convert to PIL Image
        img = Image.fromarray(img) 
        # Convert to PhotoImage
        img = ImageTk.PhotoImage(img) 
        # Draw the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img) 
        self.canvas.img = img
        
        # Convert to PIL Image
        img = Image.fromarray(mask) 
        # Convert to PhotoImage
        img = ImageTk.PhotoImage(img) 
        # Draw the image on the canvas
        self.maskCanvas.create_image(0, 0, anchor=tk.NW, image=img) 
        self.maskCanvas.img = img

        #call itself again after 15ms
        self.window.after(15, self.update)

