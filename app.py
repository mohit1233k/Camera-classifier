import tkinter as tk
import os
from tkinter import Image, simpledialog
import cv2 as cv
import PIL.Image , PIL.ImageTk
import camera
import model

class App:
    def __init__(self, window=tk.Tk(),window_title="Camera Classifier"):
        self.window =window
        self.window_title = window_title

        self.counter =[1,1]
        self.model=model.Model() 
        self.auto_predict =False
        self.camera =camera.camera()
        self.init_gui()
        self.delay= 5
        self.update()
        self.window.attributes('-topmost',True)
        self.window.mainloop()

    def Auto_predict_toggle(self):
        self.auto_predict =not self.auto_predict
    
    def init_gui(self):

        self.canvas =tk.Canvas(self.window , width=self.camera.width , height = self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto= tk.Button(self.window , text="Auto prediction", width=50, command=self.Auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER,expand=True)

        self.class1 =simpledialog.askstring("Classname One", " Enter the name of first class:", parent=self.window)
        self.btn_class1=tk.Button(self.window, text=self.class1.upper(),width=50, command=lambda :self.save_for_class(1))

        self.class2=simpledialog.askstring("Classname two","Enter the name of second class:",parent=self.window)

        self.btn_class2=tk.Button(self.window, text=self.class2.upper(), width=50 ,command=lambda: self.save_for_class(2))

        self.btn_class1.pack(anchor=tk.CENTER,expand=True)
        self.btn_class2.pack(anchor=tk.CENTER,expand=True)

        self.btn_train=tk.Button(self.window , text ="Train model", width =50 , command=lambda: self.model.train_model(self.counter))
        self.btn_train.pack(anchor=tk.CENTER,expand=True)

        self.btn_predict=tk.Button(self.window,text="predict" ,width= 50, command = self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self. btn_reset =tk.Button(self.window , text="Reset",width= 50,command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER,expand= True)

        self.class_label =tk.Label(self.window, text="Class")
        self.class_label.config(font=("Arial",20))
        self.class_label.pack(anchor=tk.CENTER,expand=True)

    def save_for_class(self, class_num):
        ret,frame= self.camera.get_frame()
        if not os.path.exists("1"):
            os.mkdir("1")
        if not os.path.exists("2"):
            os.mkdir("2")
        
        cv.imwrite(f'{class_num}/frame{self.counter[class_num-1]}.jpg',cv.cvtColor(frame,cv.COLOR_RGB2GRAY))
        img=PIL.Image.open(f'{class_num}/frame{self.counter[class_num-1]}.jpg')
        img.resize((150,150),PIL.Image.Resampling.LANCZOS)
        img.save(f'{class_num}/frame{self.counter[class_num-1]}.jpg')

        self.counter[class_num-1]+=1

    def reset(self):
        for directory in ["1","2"]:

            for file in os.listdir(directory):
                file_path=os.path.join(directory,file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        
        self.counter=[1,1]
        self.model=model.Model()
        self.class_label.config(text="CLASS")

    def update(self):
        if self.auto_predict:
            self.predict()
            pass
        ret,frame=self.camera.get_frame()

        if ret:
            self.photo=PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor=tk.NW)

        self.window.after(self.delay,self.update)

    def predict(self):
        frame=self.camera.get_frame()
        prediction = self.model.predict(frame)

        if prediction==1:
            self.class_label.config(text=self.class1)
            return self.class1
        elif prediction==2:
            self.class_label.config(text=self.class2)
            return self.class2
     


         

