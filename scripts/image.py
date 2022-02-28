from PIL import Image
import numpy as np
import cv2

class _image_():

    # unify channel to 3
    def unify_channel(self, im):
        im = np.array(im)

        if len(im.shape) == 2:
            im = im[:, :, None]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] == 4:
            im = im[:, :, 0:3]

        return Image.fromarray(im)

    # combine background ang foreground
    def change_background(self, image, matte, background):
        image = np.array(image)
        matte = np.array(matte)/255
        background = np.array(background)

        new_image = image * matte + background * (1 - matte)

        return Image.fromarray(np.uint8(new_image))

    # get foreground with transparent background
    def get_foreground(self, image, matte):
        image.convert("RGBA")

        try:
            image.putalpha(matte)
        except:
            alpha = matte.split()[-1]
            image.putalpha(alpha)

        return image

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

    # resize image from camera
    def resize(self, img, basesize):
        basewidth, baseheight = basesize
        height, width = img.shape[:2]

        if width/height >= basewidth/baseheight:
            extenstion = baseheight * .1
            new_baseheight = int(baseheight + extenstion)
            new_width = int(new_baseheight * width / height)

            img = cv2.resize(img, (new_width, new_baseheight), interpolation= cv2.INTER_LANCZOS4)

            x = int((new_width - basewidth) / 2)
        else:
            extenstion = basewidth* .1
            new_basewidth = int(basewidth + extenstion)
            new_height = int(new_basewidth * height / width)

            img = cv2.resize(img, (new_basewidth, new_height),  interpolation= cv2.INTER_LANCZOS4)

            x = int((new_basewidth - basewidth) / 2)

        y = 0

        img = img[y:y+baseheight, x:x+basewidth]
        return img

    # scale image to match the basesize
    def rescale(self, img, basesize, isNotBackground):
        basewidth, baseheight = basesize
        width, height = img.size

        # scale to height
        if width >= height:
            new_width = int(baseheight * width / height)

            if new_width < basewidth and not isNotBackground:
                baseheight += basewidth - new_width
                new_width = int(baseheight * width / height)

            img = img.resize((new_width, baseheight), Image.LANCZOS)

        # scale to width
        if width < height:
            # downscale to 90 percent
            if isNotBackground:
                basewidth = int((width * basewidth/baseheight) * .90)

            new_height = int(height * basewidth / width)

            if new_height < baseheight and not isNotBackground:
                basewidth += baseheight - new_height
                new_height = int(height * basewidth / width)

            img = img.resize((basewidth, new_height), Image.LANCZOS)

        return img

    # create a container for image
    def create_containter(self, img, matte, size, isBackground):
        img = img.convert("RGBA")
        matte = matte.convert("RGBA")

        size_width, size_height = size
        img_width, img_height = img.size

        if not isBackground:
            x = int((size_width - img_width) / 2)
            y = int(size_height - img_height)
            if y < (size_height * 0.15):
                y = int(size_height * 0.15)
        else:
            x,y = 0,0

        temp = Image.new("RGBA", size, "BLACK")

        temp.paste(img, (x,y), matte)
        return temp


