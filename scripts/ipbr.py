from PIL import Image
import numpy as np
import modnet
import image

class main():
    def __init__(self):
        url = "../MODNet/pretrained/modnet_photographic_portrait_matting.ckpt"
        self.model = modnet._modnet(url)
        self.im = image._image_()

    def process(self, img, background, def_size):

        # get matte
        matte = self.model.get_matte(img)
        matte = Image.fromarray(np.uint8(matte))

        # crop
        im, matte = self.im.crop(img, matte)

        # rescale
        im = self.im.rescale(im, def_size)
        matte = self.im.rescale(matte, def_size)
        bg = self.im.rescale(background, def_size)

        # paste
        foreground = self.im.paste(im, matte, def_size)
        matte = self.im.paste(matte, matte, def_size)
        background = self.im.paste(bg, bg, def_size)

        # change bg
        new_image = self.im.change_background(foreground, matte, background)

        return new_image


