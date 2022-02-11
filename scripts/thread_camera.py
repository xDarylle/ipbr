import cv2
from threading import Thread

class ThreadedCamera(object):
    def __init__(self, source):

        self.capture = cv2.VideoCapture(source)
        self.thread = Thread(target = self.update, args = ())
        self.thread.daemon = True
        self.stopped = False
        self.thread.start()

        self.status = False
        self.frame  = None

    def update(self):
        while True:
            if not self.stopped:
                if self.capture.isOpened():
                    (self.status, self.frame) = self.capture.read()

            if self.stopped:
                break

    def grab_frame(self):
        if self.status:
            return self.frame
        return None

    def stop(self):
        self.stopped = True
        print("camera stopped", self.stopped)