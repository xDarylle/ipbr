import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import image
import cv2
import sys
sys.path.append('scripts')
from MODNet.src.models.modnet import MODNet

class cam_modnet():

    def __init__(self, model_path):
        # create MODNet and load the pre-trained ckpt
        self.modnet = MODNet(backbone_pretrained=False)
        self.modnet = nn.DataParallel(self.modnet).cuda()

        # check if gpu supports cuda else use cpu
        GPU = True if torch.cuda.device_count() > 0 else False
        if GPU:
            modnet = self.modnet.cuda()
            modnet.load_state_dict(torch.load(model_path))
        else:
            self.modnet.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        self.modnet.eval()

        # define image to tensor transform
        self.im_transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ]
        )

    ''' Process for updating the background for live preview. 
    '''
    def update(self, frame, bg, is_not_custom, size, isSaveTransparent):
        # prepare the frame
        frame_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_np = image.resize(frame_np, (910, 512))
        frame_np = frame_np[:, 120:792, :]

        frame_PIL = Image.fromarray(frame_np)
        frame_tensor = self.im_transform(frame_PIL)
        frame_tensor = frame_tensor[None, :, :, :]

        GPU = True if torch.cuda.device_count() > 0 else False
        if GPU:
            frame_tensor = frame_tensor.cuda()

        # inference
        with torch.no_grad():
            _, _, matte_tensor = self.modnet(frame_tensor, True)

        matte_tensor = matte_tensor.repeat(1, 3, 1, 1)
        matte_np = matte_tensor[0].data.cpu().numpy().transpose(1, 2, 0)

        matte_np = image.optimize_matte(matte_np*255)

        frame_np = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)
        shape = frame_np.shape

        # check if custom size is set
        if is_not_custom:
            h,w = frame_np.shape[0:2]
            def_size = (w,h)
        else:
            def_size = size
            frame_np = image.resize(frame_np,def_size)
            matte_np = image.resize(matte_np,def_size)
            frame_np = image.unify_channel(frame_np)
            frame_np = np.array(frame_np)
            matte_np = np.array(matte_np)

        # resize background
        bg = image.rescale(bg, def_size, False)
        bg = image.create_containter(bg, bg, def_size, True)
        bg = image.unify_channel(bg)
        bg = np.array(bg)

        # combine background and foreground
        fg_np = image.change_background(frame_np, matte_np, bg)

        # get transparent foreground
        if isSaveTransparent:
            transparent = image.get_foreground(Image.fromarray(frame_np), Image.fromarray(np.uint8(matte_np*255)))
        else:
            transparent = None

        return np.array(np.uint8(fg_np)), transparent