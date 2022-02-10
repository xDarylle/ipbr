import cv2
import numpy as np
from threading import Thread
from PIL import Image
import cam_modnet

class ThreadedCamera(object):
    def __init__(self, source = 0):

        self.capture = cv2.VideoCapture(source)
        self.thread = Thread(target = self.update, args = ())
        self.thread.daemon = True
        self.thread.start()

        self.status = False
        self.frame  = None

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def grab_frame(self):
        if self.status:
            return self.frame
        return None

class camera():
    def __init__(self):
        pretrained_ckpt = "pretrained/modnet_webcam_portrait_matting.ckpt"
        self.cmodnet = cam_modnet.cam_modnet(pretrained_ckpt)

    def get_preview(self, bg, camera):
        self.streamer = ThreadedCamera(camera)

        while(True):
            frame_np = self.streamer.grab_frame()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if frame_np is not None:

                frame_np = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
                frame_np = cv2.resize(frame_np, (910, 512), cv2.INTER_AREA)
                frame_np = frame_np[:, 120:792, :]
                frame_np = cv2.flip(frame_np, 1)

                fg_np = self.cmodnet.update(frame_np, bg)

                self.fg_np = cv2.cvtColor(np.uint8(fg_np), cv2.COLOR_RGB2BGR)

                cv2.imshow('MODNet - WebCam [Press \'Q\' To Exit]', self.fg_np)
                if cv2.waitKey(1) & 0xFF == ord("c"):
                    img_name = "C:/Users/daryl/Desktop/opencv_frame_{}.png"
                    cv2.imwrite(img_name, self.fg_np)
                    print("captured")

bg = Image.open("resources/bg.jpg")
url = "http://192.168.1.11:8080/video"
cam = camera()
cam.get_preview(bg, url)