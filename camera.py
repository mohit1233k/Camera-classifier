import cv2 as cv

class camera:

    def __init__(self) -> None:
        self.camera =cv.VideoCapture(0)
        if not self.camera.isOpened():
            return ValueError("camera not opened")
        self.width =self.camera.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height=self.camera.get(cv.CAP_PROP_FRAME_HEIGHT)
    def __del__ (self):
        if self.camera.isOpened():
            self.camera.release()
    
    def get_frame(self):
        if self.camera.isOpened():
            ret,frame= self.camera.read()
        
            if ret:
                return ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            else :
                return(None, ret)
        
        else:
            return None