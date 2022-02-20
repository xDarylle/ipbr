from PIL import Image
import numpy as np
import sys
sys.path.append('scripts')
import modnet
import image

class main():
    def __init__(self):
        url = "pretrained/modnet_photographic_portrait_matting.ckpt"
        self.model = modnet._modnet(url)
        self.im = image._image_()

    ''' Process if follow_input_size is False. 
        This uses a define size for the output.
        Crops the input image so that only the portrait will remain and then will be aligned in bottom-center when pasting into
        an image container.
    '''
    def process(self, img, background, def_size, isSaveTransparent):

        # get matte
        matte = self.model.get_matte(img)
        matte = Image.fromarray(np.uint8(matte))

        # crop
        im, matte = self.im.crop(img, matte)

        # rescale
        im = self.im.rescale(im, def_size, True)
        matte = self.im.rescale(matte, def_size, True)
        bg = self.im.rescale(background, def_size, False)

        # create container
        foreground = self.im.paste(im, matte, def_size)
        matte = self.im.paste(matte, matte, def_size)
        background = self.im.paste(bg, bg, def_size)

        # change bg
        new_image = self.im.change_background(foreground, matte, background)

        # get transparent foreground
        if isSaveTransparent:
            transparent = self.im.get_foreground(foreground, matte)
        else:
            transparent = None

        return new_image, transparent

    ''' Process if follow_input_size is True. 
        This will use the width and height of the input image for the output.
        Does not involve cropping and rescaling of input image. 
    '''
    def process_v2(self, img, background, isSaveTransparent):

        # get matte
        matte = self.model.get_matte(img)
        matte = Image.fromarray(np.uint8(matte))

        # rescale background to match foreground
        bg = self.im.rescale(background, img.size, False)

        # create container for background
        bg = self.im.paste(bg, bg, img.size)

        # unify channels to 3
        img = self.im.unify_channel(img)
        matte = self.im.unify_channel(matte)
        bg =  self.im.unify_channel(bg)

        # change background
        new_image = self.im.change_background(img, matte, bg)

        # get transparent foreground
        if isSaveTransparent:
            transparent = self.im.get_foreground(img, matte)
        else:
            transparent = None

        return new_image, transparent



