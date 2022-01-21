from PIL import Image
import modnet
import _image_

url = "../MODNet/pretrained/modnet_photographic_portrait_matting.ckpt"
model = modnet._modnet(url)
_image_ = _image_._image_()
im = Image.open("../input/rap.jpg")

matte = model.get_matte(im)

cropped = _image_.crop(matte, matte)






