import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torchvision.transforms as transforms
import image

from scripts.MODNet.src.models.modnet import MODNet

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

        self.im = image._image_()

    # replace background of current frame
    def update(self, frame, bg):
        frame_PIL = Image.fromarray(frame)
        frame_tensor = self.im_transform(frame_PIL)
        frame_tensor = frame_tensor[None, :, :, :]

        GPU = True if torch.cuda.device_count() > 0 else False
        if GPU:
            frame_tensor = frame_tensor.cuda()

        with torch.no_grad():
            _, _, matte_tensor = self.modnet(frame_tensor, True)

        matte_tensor = matte_tensor.repeat(1, 3, 1, 1)
        matte_np = matte_tensor[0].data.cpu().numpy().transpose(1, 2, 0)

        matte = Image.fromarray(np.uint8(matte_np * 255))
        frame = Image.fromarray(frame)

        def_size = frame.size
        #
        # #  rescale
        # frame = self.im.rescale(frame, def_size, True)
        # matte = self.im.rescale(matte, def_size, True)
        bg = self.im.rescale(bg, def_size, False)
        #
        # # paste
        # foreground = self.im.paste(frame, matte, def_size)
        # matte = self.im.paste(matte, matte, def_size)
        background = self.im.paste(bg, bg, def_size)

        #replace background of the frame
        frame = self.im.unify_channel(frame)
        matte = self.im.unify_channel(matte)
        background = self.im.unify_channel(background)
        new_image = self.im.change_background(frame, matte, background)

        return np.array(new_image)

