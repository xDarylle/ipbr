import cv2
import cvzone
import numpy as np
from PIL import Image

import cam_modnet

pretrained_ckpt = '../MODNet/pretrained/modnet_webcam_portrait_matting.ckpt'
cmodnet = cam_modnet.cam_modnet(pretrained_ckpt)

bg = Image.open('../background/bg.jpg')

url = "https://192.168.1.7:8080/video"
cap = cv2.VideoCapture(url)

while(True):
    _, frame_np = cap.read()
    frame_np = cv2.cvtColor(frame_np, cv2.COLOR_BGR2RGB)
    frame_np = cv2.resize(frame_np, (910, 512), cv2.INTER_AREA)
    frame_np = frame_np[:, 120:792, :]
    frame_np = cv2.flip(frame_np, 1)

    fg_np = cmodnet.update(frame_np, bg)

    fg_np = cv2.cvtColor(np.uint8(fg_np), cv2.COLOR_RGB2BGR)
    cv2.imshow('MODNet - WebCam [Press \'Q\' To Exit]', fg_np)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if cv2.waitKey(1) & 0xFF == ord("c"):
        img_name = "C:/Users/daryl/Desktop/opencv_frame_{}.png"
        cv2.imwrite(img_name, fg_np)
        print("captured")
