import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
import sys
sys.path.append('scripts')
import MODNet.src.models.modnet
import image

class _modnet():

    def __init__(self, model_path):
        # create MODNet and load the pre-trained ckpt
        self.modnet = MODNet.src.models.modnet.MODNet(backbone_pretrained=False)
        self.modnet = nn.DataParallel(self.modnet).cuda()
        self.modnet.load_state_dict(torch.load(model_path))
        self.modnet.eval()

        # define hyper-parameters
        self.ref_size = 512

        # define image to tensor transform
        self.im_transform = transforms.Compose(
            [
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
            ]
        )

    # predict alpha matte
    def get_matte(self, im):

        # unify image channels to 3
        im = image.unify_channel(im)

        # convert image to PyTorch tensor
        im = self.im_transform(im)

        # add mini-batch dim
        im = im[None, :, :, :]

        # resize image for input
        im_b, im_c, im_h, im_w = im.shape
        if max(im_h, im_w) < self.ref_size or min(im_h, im_w) > self.ref_size:
            if im_w >= im_h:
                im_rh = self.ref_size
                im_rw = int(im_w / im_h * self.ref_size)
            elif im_w < im_h:
                im_rw = self.ref_size
                im_rh = int(im_h / im_w * self.ref_size)
        else:
            im_rh = im_h
            im_rw = im_w

        im_rw = im_rw - im_rw % 32
        im_rh = im_rh - im_rh % 32
        im = F.interpolate(im, size=(im_rh, im_rw), mode='area')

        # inference
        _, _, matte = self.modnet(im.cuda() if torch.cuda.is_available() else im, True)

        # resize
        matte = F.interpolate(matte, size=(im_h, im_w), mode='area')
        matte = matte[0][0].data.cpu().numpy()

        return matte * 255







