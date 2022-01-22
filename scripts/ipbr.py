from PIL import Image
import numpy as np
import modnet
import _image_

def_size = (600, 900)

url = "../MODNet/pretrained/modnet_photographic_portrait_matting.ckpt"
model = modnet._modnet(url)
_image_ = _image_._image_()

im = Image.open("../input/rap.jpg")
bg = Image.open("../background/bg.jpg")

# predict matte
matte = model.get_matte(im)
matte = Image.fromarray(np.uint8(matte))

# crop
im, matte = _image_.crop(im, matte)

# rescale
im = _image_.rescale(im, def_size, 0)
matte = _image_.rescale(matte, def_size, 0)
bg = _image_.rescale(bg, def_size, 1)

# paste
foreground = _image_.paste(im, matte, def_size)
matte = _image_.paste(matte, matte, def_size)
background = _image_.paste(bg, bg, def_size)

# change bg
new_image = _image_.change_background(foreground, matte, background)

new_image.show()












