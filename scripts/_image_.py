from PIL import Image
import numpy as np
import cv2

class _image_():

    def unify_channel(self, im):

        if len(im.shape) == 2:
            im = im[:, :, None]
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] == 4:
            im = im[:, :, 0:3]

        return im

    def change_background(self, image, matte, background):

        new_image = image * matte + background * (1 - matte)

        return new_image

    def crop(self, img, matte):
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        matte = cv2.cvtColor(matte, cv2.COLOR_RGBA2BGR)

        gray = cv2.cvtColor(matte, cv2.COLOR_BGR2GRAY)

        # threshold
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        hh, ww = thresh.shape

        # make bottom 2 rows black where they are white the full width of the image
        thresh[hh - 3:hh, 0:ww] = 0

        # get bounds of white pixels
        white = np.where(thresh == 255)
        xmin, ymin, xmax, ymax = np.min(white[1]), np.min(white[0]), np.max(white[1]), np.max(white[0])
        print(xmin, xmax, ymin, ymax)

        # crop the image at the bounds adding back the two blackened rows at the bottom
        img = img[ymin:ymax + 3, xmin:xmax]
        matte = matte[ymin:ymax + 3, xmin:xmax]

        # convert to image format
        img = Image.fromarray(img)
        matte = Image.fromarray(matte)
        return img, matte






