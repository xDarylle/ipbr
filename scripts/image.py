from PIL import Image
import numpy as np
import cv2
import math

# unify channel to 3
def unify_channel(im):

    if len(im.shape) == 2:
        im = im[:, :, None]
    if im.shape[2] == 1:
        im = np.repeat(im, 3, axis=2)
    elif im.shape[2] == 4:
        im = im[:, :, 0:3]

    return im

# combine background ang foreground
def change_background(img, matte, background):
    img= np.array(img)
    matte = np.array(matte)/255
    background = np.array(background)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    background = cv2.cvtColor(np.uint8(background), cv2.COLOR_BGR2RGB)

    new_image = img * matte + background * (1 - matte)

    return np.uint8(new_image)

# get foreground with transparent background
def get_foreground(image, matte):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    matte = Image.fromarray(matte)

    image.convert("RGBA")

    try:
        image.putalpha(matte)
    except:
        alpha = matte.split()[-1]
        image.putalpha(alpha)

    return image

# crop foreground
def crop(img, matte):
    matte = cv2.cvtColor(np.array(matte), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(matte, cv2.COLOR_BGR2GRAY)

    # threshold
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    hh, ww = thresh.shape

    # make bottom 2 rows black where they are white the full width of the image
    thresh[hh - 3:hh, 0:ww] = 0

    # get bounds of white pixels
    white = np.where(thresh == 255)
    xmin, ymin, xmax, ymax = np.min(white[1]), np.min(white[0]), np.max(white[1]), np.max(white[0])

    # crop the image at the bounds adding back the two blackened rows at the bottom
    img = img[ymin:ymax + 3, xmin:xmax]
    matte = matte[ymin:ymax + 3, xmin:xmax]

    return img, matte

# resize captured image using camera
def resize(img, basesize):
    basewidth, baseheight = basesize
    height, width = img.shape[:2]

    if width/height >= basewidth/baseheight:
        # rescale image by height
        extenstion = baseheight * .1
        new_baseheight = int(baseheight + extenstion)
        new_width = int(new_baseheight * width / height)

        img = cv2.resize(img, (new_width, new_baseheight), interpolation= cv2.INTER_LANCZOS4)

        # get x coordinate where to start crop
        x = int((new_width - basewidth) / 2)

    else:
        # rescale image by width
        extenstion = basewidth * .1
        new_basewidth = int(basewidth + extenstion)
        new_height = int(new_basewidth * height / width)

        img = cv2.resize(img, (new_basewidth, new_height),  interpolation= cv2.INTER_LANCZOS4)

        # get x coordinate where to start crop
        x = int((new_basewidth - basewidth) / 2)

    y = 0

    # crop image
    img = img[y:y+baseheight, x:x+basewidth]

    return img

# scale image to match the basesize
def rescale(img, basesize, isNotBackground):
    basewidth, baseheight = basesize
    height, width = img.shape[:2]

    # scale to height
    if width >= height:
        new_width = int(baseheight * width / height)

        if new_width < basewidth and not isNotBackground:
            baseheight += basewidth - new_width
            new_width = int(baseheight * width / height)

        img = cv2.resize(img, (new_width, baseheight), interpolation= cv2.INTER_LANCZOS4)

    # scale to width
    if width < height:
        # if foreground scale to baseheight
        if isNotBackground:
            baseheight = math.ceil(baseheight * 0.85)
            new_width = math.ceil(baseheight * width / height)
            if new_width < basewidth:
                baseheight = math.ceil(baseheight * basewidth / new_width)
                new_width = basewidth

            img = cv2.resize(img, (new_width, baseheight),  interpolation= cv2.INTER_LANCZOS4)
            return img

        new_height = math.ceil(height * basewidth / width)

        if new_height < baseheight and not isNotBackground:
            basewidth += baseheight - new_height
            new_height = math.ceil(height * basewidth / width)

        img = cv2.resize(img, (basewidth, new_height), interpolation= cv2.INTER_LANCZOS4)

    return img

# create a container for image
def create_containter(img, matte, size, isBackground):
    img = Image.fromarray(img)
    matte = Image.fromarray(matte)

    img = img.convert("RGBA")
    matte = matte.convert("RGBA")

    size_width, size_height = size
    img_width, img_height = img.size

    # align img to center
    x = math.ceil((size_width - img_width) / 2)
    if not isBackground:
        y = math.ceil(size_height - img_height)
        # top padding
        if y < (size_height * 0.05) and img_height >= size_height:
            y = math.ceil(size_height * 0.05) - math.ceil(img_height * 0.01)
    else:
        y = 0

    temp = Image.new("RGBA", size, "BLACK")

    temp.paste(img, (x,y), matte)

    return temp

def optimize_matte(matte):
    kernel = np.ones((6, 6), np.uint8)
    erosion = cv2.erode(matte, kernel, cv2.BORDER_REFLECT, iterations=1)

    return erosion

def downscale(img, baseheight):
    height, width = img.shape[:2]

    new_width = int(baseheight * width / height)

    img = cv2.resize(img, (new_width, baseheight), interpolation=cv2.INTER_AREA)

    return img