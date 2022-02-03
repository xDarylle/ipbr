from PIL import Image
import numpy as np
import cv2

class _image_():

    # unify channel to 3
    def unify_channel(self, im):

        if len(im.shape) == 2:
            im = im[:, :, None]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] == 4:
            im = im[:, :, 0:3]

        return im

    # combine background ang foreground
    def change_background(self, image, matte, background):
        image = np.array(image)
        matte = np.array(matte)/255
        background = np.array(background)

        new_image = image * matte + background * (1 - matte)

        return Image.fromarray(np.uint8(new_image))

    # crop foreground
    def crop(self, img, matte):
        img = np.array(img)
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

        # convert to image format
        img = Image.fromarray(img)
        matte = Image.fromarray(matte)
        return img, matte

    # scale image to match the basesize
    def rescale(self, img, basesize):
        basewidth, baseheight = basesize
        width, height = img.size
        padding = 100

        # scale to width
        if width < height:
            basewidth = basewidth - padding
            new_height = int(height * basewidth / width)
            img = img.resize((basewidth, new_height), Image.ANTIALIAS)

        # scale to height
        if width > height:
            new_width = int(baseheight * width / height)
            img = img.resize((new_width, baseheight), Image.ANTIALIAS)

        return img


    # create a container for image
    def paste(self, img, matte, size):
        img = img.convert("RGBA")
        matte = matte.convert("RGBA")

        size_width, size_height = size
        img_width, img_height = img.size

        x = int((size_width - img_width) / 2)
        y = int(size_height - img_height)

        temp = Image.new("RGBA", size, "BLACK")

        temp.paste(img, (x,y), matte)
        return temp







