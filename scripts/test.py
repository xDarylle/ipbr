from PIL import Image
import numpy as np
import modnet
import image

def_size = (600, 900)

def start():
    # load pre-trainded model and instantiate modnet and image class
    url = "../MODNet/pretrained/modnet_photographic_portrait_matting.ckpt"
    model = modnet._modnet(url)
    _image_ = image._image_()

    im = Image.open("../input/jumalon.jpg")
    bg = Image.open("../background/bg.jpg")

    im = np.array(im)
    im = _image_.unify_channel(im)

    # predict matte
    matte = model.get_matte(im)
    matte = _image_.unify_channel(matte)
    matte = matte / 255
    new_image = im * matte + np.full(im.shape, 255) * (1 - matte)
    new_image = Image.fromarray(np.uint8(new_image)).save("C:/Users/daryl/Desktop/pic.png")

start()












