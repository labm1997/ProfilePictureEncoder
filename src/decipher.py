import numpy as np
import cv2

class Decipher:
    def __init__(self):
        pass

    def char2int(self, character):
        return int(bytes(character, 'ASCII')[0])

    def subsample(self, image, nrows):
        imageSize = image.shape[0]

        blockSize = round(imageSize / nrows)

        return image[round(blockSize / 2) : imageSize : blockSize, round(blockSize / 2) : imageSize : blockSize]

    def convert2hsv(self, image):
        hsvImage = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))

        return hsvImage

    def demapper(self, hsvColor):

        min_value = self.char2int('a')
        max_value = self.char2int('z')

        value = np.ceil(hsvColor[0]) / 178.0 * (max_value - (min_value - 1))  + (min_value - 1)

        if value >= min_value and value <= max_value:
            return chr(int(value))

        else:
            return ' '


    def decode(self, image, nrows):
        subsampled = self.subsample(image, nrows)

        hsvImage = self.convert2hsv(np.float32(subsampled / 255.0))

        hsvArray = hsvImage.reshape(-1, 3).tolist()

        decodedArray = list(map(self.demapper, hsvArray))

        return ''.join(decodedArray)

image = cv2.imread('profile.png')

decipher = Decipher()
decoded = decipher.decode(image, 27)

print(decoded)
