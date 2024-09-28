import PIL.Image
from sklearn.svm import LinearSVC
import numpy as np  
import cv2 as cv
import PIL

class Model:
    def __init__(self ):
        self.model=LinearSVC()
    
    def train_model(self, counter):
        img_list=np.array([])
        class_list=np.array([])

        for i in range(1, counter[0]):
            img=cv.imread(f'1/frame{i}.jpg')[:,:,0]
            img=img.reshape(307200)
            img_list=np.append(img_list,[img])
            class_list=np.append(class_list,1)
            
        for i in range(1, counter[1]):
            img=cv.imread(f'2/frame{i}.jpg')[:,:,0]
            img=img.reshape(307200)
            img_list=np.append(img_list,[img])
            class_list=np.append(class_list,2)

        img_list=img_list.reshape(counter[0] -1 +counter[1] -1,307200)
        self.model.fit(img_list, class_list)
        print("model succesfully trained")

    def predict(self,frame):
        frame=frame[1]
        cv.imwrite(f"frame.jpg",cv.cvtColor(frame,cv.COLOR_RGB2GRAY))
        img=PIL.Image.open('frame.jpg')
        img.resize((150,150),PIL.Image.Resampling.LANCZOS)
        img.save('frame.jpg')

        img=cv.imread('frame.jpg')[:,:,0]
        img=img.reshape(307200)
        prediction =self.model.predict([img])

        return prediction[0]