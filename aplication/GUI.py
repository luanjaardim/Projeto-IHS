from vision import *
import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk
import json

class ColorSettings:
    def __init__(self, frame):
        #hue sliders
        self.hue_min_slider = tk.Scale(frame, label='HUE Min', from_=0, to=180, orient=tk.HORIZONTAL)
        self.hue_min_slider.grid(row=0, column=0, pady=10, padx=20)
        self.hue_max_slider = tk.Scale(frame, label='HUE Max', from_=0, to=180, orient=tk.HORIZONTAL)
        self.hue_max_slider.grid(row=0, column=1, pady=10, padx=20)
        #saturation sliders
        self.sat_min_slider = tk.Scale(frame, label='Saturation Min', from_=0, to=255, orient=tk.HORIZONTAL)
        self.sat_min_slider.grid(row=1, column=0, pady=10, padx=20)
        self.sat_max_slider = tk.Scale(frame, label='Saturation Max', from_=0, to=255, orient=tk.HORIZONTAL)
        self.sat_max_slider.grid(row=1, column=1, pady=10, padx=20)
        #value sliders
        self.val_min_slider = tk.Scale(frame, label='Value Min', from_=0, to=255, orient=tk.HORIZONTAL)
        self.val_min_slider.grid(row=2, column=0, pady=10, padx=20)
        self.val_max_slider = tk.Scale(frame, label='Value Max', from_=0, to=255, orient=tk.HORIZONTAL)
        self.val_max_slider.grid(row=2, column=1, pady=10, padx=20)
    def getValues(self):
        lowerValues = np.array([self.hue_min_slider.get(),self.sat_min_slider.get(),self.val_min_slider.get()])
        upperValues = (np.array([self.hue_max_slider.get(),self.sat_max_slider.get(),self.val_max_slider.get()]))
        return lowerValues, upperValues

class GUI:
    def __init__(self, root, camera):

        #setup camera
        self.camera = camera

        #create window
        self.window = root
        self.window.title("Projeto Torreta - Interface Hardware-Software") # Set the title of the window
        
        self.upperRow = tk.Frame()
        self.upperRow.pack()
        self.lowerRow = tk.Frame()
        self.lowerRow.pack()
        
        # Create the canvas for img preview
        self.canvas = tk.Canvas(self.upperRow)
        self.canvas.grid(row=0,column=0)
        
        #image settings stuff
        self.maskCanvas = tk.Canvas(self.lowerRow, width=40, height=40)
        self.maskCanvas.grid(row=0,column=0)
        self.settingsFrame = tk.LabelFrame(self.lowerRow, text='Configuração de Cores',  width=40, height=40)
        self.settingsFrame.grid(row=0, column=1)
        self.inputField = ColorSettings(self.settingsFrame)
    

        #get saved colors from json
        # self.loadColor()

        # start the video display loop
        self.update()
    
    def update(self):
        #gets current frame from camera object
        frame = camera.getFrame()
        
        #preview canvas

        # Convert BGR to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        # Convert to PIL Image
        img = Image.fromarray(img) 
        # Convert to PhotoImage
        img = ImageTk.PhotoImage(img) 
        # Draw the image on the canvas
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img) 
        self.canvas.img = img

        #mask canvas

        #get hsv frame
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Convert to PIL Image
        img = Image.fromarray(hsv) 
        # Convert to PhotoImage
        img = ImageTk.PhotoImage(img) 
        # Draw the image on the canvas
        self.maskCanvas.create_image(0, 0, anchor=tk.NW, image=img) 
        self.maskCanvas.img = img

        self.window.after(15, self.update)

    def saveColors(self):
        #get values
        min, max = self.slider.getValues()
        #create dictionary
        red = {"hue": {"min":str(min[0]),"max":str(max[0])}, "sat": {"min":str(min[1]),"max":str(max[1])}, "val": {"min":str(min[2]),"max":str(max[2])}}
        # Write the dictionary to a JSON file
        with open("colors.json", "w") as json_file:
            json.dump(red, json_file)
        #apply to the running program
        self.camera.color_min = np.array([self.readJson('hue', 'min'), self.readJson('sat', 'min'), self.readJson('val', 'min')], np.uint8)
        self.camera.color_max = np.array([self.readJson('hue', 'max'), self.readJson('sat', 'max'), self.readJson('val', 'max')], np.uint8)

    def readJson(self, value, minMax):
        # Load the JSON data
        with open('colors.json', 'r') as file:
            # Load the JSON data
            data = json.load(file)
            return data[value][minMax]
    
    def loadColor(self):
        #red
        self.slider.hue_min_slider.set(self.readJson('hue', 'min'))
        self.slider.hue_max_slider.set(self.readJson('hue', 'max'))
        self.slider.sat_min_slider.set(self.readJson('sat', 'min'))
        self.slider.sat_max_slider.set(self.readJson('sat', 'max'))
        self.slider.val_min_slider.set(self.readJson('val', 'min'))
        self.slider.val_max_slider.set(self.readJson('val', 'max'))

camera = Vision()
root = tk.Tk()

app = GUI(root, camera)

root.mainloop()
