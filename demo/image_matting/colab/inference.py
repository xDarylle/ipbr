import math
import os
import sys
import argparse
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms

from src.models.modnet import MODNet


if __name__ == '__main__':
    # define cmd arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str, help='path of input images')
    parser.add_argument('--matte-path', type=str, help='path of matte images')
    parser.add_argument('--output-path', type=str, help='path of output images')
    parser.add_argument('--ckpt-path', type=str, help='path of pre-trained MODNet')
    parser.add_argument('--background-path', type=str, help='path of background')
    parser.add_argument('--foreground-path', type=str, help='path of foreground')
    args = parser.parse_args()

    # check input arguments
    if not os.path.exists(args.input_path):
        print('Cannot find input path: {0}'.format(args.input_path))
        exit()
    if not os.path.exists(args.output_path):
        print('Cannot find output path: {0}'.format(args.output_path))
        exit()
    if not os.path.exists(args.ckpt_path):
        print('Cannot find ckpt path: {0}'.format(args.ckpt_path))
        exit()
    if not os.path.exists(args.background_path):
        print('Cannot find background path: {0}'.format(args.ckpt_path))
        exit()
    if not os.path.exists(args.foreground_path):
        print('Cannot find foreground path: {0}'.format(args.ckpt_path))
        exit()
    if not os.path.exists(args.matte_path):
        print('Cannot find matte path: {0}'.format(args.ckpt_path))
        exit()

    # define hyper-parameters
    ref_size = 512

    # define image to tensor transform
    im_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ]
    )

    #get foreground
    def getForeground(image, matte, image_name):

        # obtain predicted foreground
        image = np.asarray(image)

        matte = np.repeat(np.asarray(matte)[:, :, None], 3, axis=2) / 255
        foreground = image * matte + np.full(image.shape, 255) * (1 - matte)
        foreground = Image.fromarray(np.uint8(foreground))
        foreground_name= image_name.split('.')[0] + '.png'
        Image.fromarray(np.uint8(foreground)).save(os.path.join(args.foreground_path, foreground_name))
        return Image.fromarray(np.uint8(foreground))

    def default_resize(image):
        basewidth = 1080
        width, height = image.size
        wpercent = (basewidth / width)
        hsize = int(height * wpercent)
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)
        return image

    def resize_bg(bg):
        baseheight = 800
        width, height = bg.size
        new_width = int(baseheight * width/height)
        bg = bg.resize((new_width, baseheight), Image.ANTIALIAS)
        return bg

    def getOffset(image):
        w, h = 600, 800
        im_w, im_h = image.size
        offset = ((w - im_w) // 2, (h - im_h))
        return offset

    #combine foreground and background
    def combine(image, bg, matte, image_name):

        #resize image by width
        image = default_resize(image)
        matte = default_resize(matte)

        #resize bg by height
        bg = resize_bg(bg)

        #convert to RGBA to avoid incompatibility
        final = Image.new("RGBA", (600,800), "WHITE")
        image = image.convert("RGBA")
        bg = bg.convert("RGBA")

        #combine foreground and background
        final.paste(bg, getOffset(bg), bg)
        final.paste(image, getOffset(image), matte)

        final_name = image_name.split('.')[0] + '.png'
        Image.fromarray(np.uint8(final)).save(os.path.join(args.output_path, final_name))
        return final


    # create MODNet and load the pre-trained ckpt
    modnet = MODNet(backbone_pretrained=False)
    modnet = nn.DataParallel(modnet).cuda()
    modnet.load_state_dict(torch.load(args.ckpt_path))
    modnet.eval()

    # inference images
    im_names = os.listdir(args.input_path)
    for im_name in im_names:
        print('Process image: {0}'.format(im_name))

        # read image
        im = Image.open(os.path.join(args.input_path, im_name))

        # unify image channels to 3
        im = np.asarray(im)
        if len(im.shape) == 2:
            im = im[:, :, None]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] == 4:
            im = im[:, :, 0:3]

        # convert image to PyTorch tensor
        im = Image.fromarray(im)
        im = im_transform(im)

        # add mini-batch dim
        im = im[None, :, :, :]

        # resize image for input
        im_b, im_c, im_h, im_w = im.shape
        if max(im_h, im_w) < ref_size or min(im_h, im_w) > ref_size:
            if im_w >= im_h:
                im_rh = ref_size
                im_rw = int(im_w / im_h * ref_size)
            elif im_w < im_h:
                im_rw = ref_size
                im_rh = int(im_h / im_w * ref_size)
        else:
            im_rh = im_h
            im_rw = im_w
        
        im_rw = im_rw - im_rw % 32
        im_rh = im_rh - im_rh % 32
        im = F.interpolate(im, size=(im_rh, im_rw), mode='area')

        # inference
        _, _, matte = modnet(im.cuda(), True)

        # resize and save matte
        matte = F.interpolate(matte, size=(im_h, im_w), mode='area')
        matte = matte[0][0].data.cpu().numpy()
        matte_name = im_name.split('.')[0] + '.png'
        Image.fromarray(((matte * 255).astype('uint8')), mode='L').save(os.path.join(args.matte_path, matte_name))

    backgrounds = os.listdir(args.background_path)
    for background_name in backgrounds:
        background = Image.open(os.path.join(args.background_path, background_name))

    image_names = os.listdir(args.input_path)
    for image_name in image_names:
        matte_name = image_name.split('.')[0] + '.png'
        image = Image.open(os.path.join(args.input_path, image_name))
        matte = Image.open(os.path.join(args.matte_path, matte_name))
        foreground = getForeground(image,matte,image_name)
        final = combine(foreground, background, matte, image_name)








