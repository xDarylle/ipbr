from PIL import Image
import numpy as np
import sys
sys.path.append('scripts')
import modnet
import image

import cv2
import time

class main():
    def __init__(self):
        url = "pretrained/modnet_photographic_portrait_matting.ckpt"
        self.model = modnet._modnet(url)

    ''' Process if follow_input_size is False. 
        This uses a define size for the output.
        Crops the input image so that only the portrait will remain and then will be aligned in bottom-center when pasting into
        an image container.
    '''
    def process(self, img, background, def_size, isSaveTransparent):
        img = np.array(img)
        background = np.array(background)

        # rescale
        img = image.rescale(img, def_size, True)
        bg = image.rescale(background, def_size, False)

        # get matte
        matte = self.model.get_matte(img)
        matte = np.uint8(matte)

        img_orig = img
        matte_orig = matte

        matte = image.optimize_matte(np.array(matte))

        # crop
        im, matte = image.crop(img, matte)

        # create container
        img = image.create_containter(im, matte, def_size, False)
        matte = image.create_containter(matte, matte, def_size, False)
        bg = image.create_containter(bg, bg, def_size, True)

        img = image.unify_channel(np.array(img))
        matte = image.unify_channel(np.array(matte))
        bg = image.unify_channel(np.array(bg))

        # change bg
        new_image = image.change_background(img, matte, bg)

        # get transparent foreground
        if isSaveTransparent:
            transparent = image.get_foreground(img_orig, matte_orig)
        else:
            transparent = None

        return new_image, transparent

    ''' Process if follow_input_size is True. 
        This will use the width and height of the input image for the output.
        Does not involve cropping and rescaling of input image. 
    '''
    def process_v2(self, img, background, isSaveTransparent):
        size = img.size

        img = np.array(img)
        background = np.array(background)

        # get matte
        matte = self.model.get_matte(img)
        matte = np.uint8(matte)

        # rescale background to match foreground
        bg = image.rescale(background, size, False)

        matte = image.optimize_matte(matte)

        # create container for background
        bg = image.create_containter(bg, bg, size, True)

        # unify channels to 3
        img = image.unify_channel(img)
        matte = image.unify_channel(matte)
        bg = image.unify_channel(np.array(bg))

        # change background
        new_image = image.change_background(img, matte, bg)

        # get transparent foreground
        if isSaveTransparent:
            transparent = image.get_foreground(img, matte)
        else:
            transparent = None

        return new_image, transparent

    ''' Process for capturing image using camera. 
        This uses a define size for the output.
        This involves a resize function instead of cropping, rescaling and creating container for images.
    '''
    def process_capture(self, img, background, def_size, isSaveTransparent):
        # get matte
        matte = self.model.get_matte(img)

        img_orig = img
        matte_orig = matte

        # resize img and matte
        img = image.resize(img, def_size)
        matte = image.resize(matte, def_size)

        matte = image.optimize_matte(matte)

        # rescale background
        background = image.rescale(background, def_size, False)
        background = image.create_containter(background, background, def_size, True)

        # unify channels to 3
        img = image.unify_channel(img)
        matte = image.unify_channel(np.uint8(matte))
        background = image.unify_channel(background)

        # change background
        new_image = image.change_background(img, matte, background)

        # get transparent foreground
        if isSaveTransparent:
            transparent = image.get_foreground(Image.fromarray(img_orig), Image.fromarray(np.uint8(matte_orig)))
        else:
            transparent = None

        return new_image, transparent







