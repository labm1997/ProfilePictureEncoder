import numpy as np
import cv2
import sys

class Decipher:
    def __init__(self, hsv_min_hue=0, hsv_max_hue=360):
        self.hsv_min_hue = hsv_min_hue
        self.hsv_max_hue = hsv_max_hue

        self.specialMap = {
            0.1: ' ',
            0.2: ',',
            0.3: ':',
            0.4: '.',
            0.5: '?',
            0.6: '-',
        }

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
        if(hsvColor[1] == 0):
            rounded = round(hsvColor[2] * 10) / 10.0
            if(rounded in self.specialMap):
                return self.specialMap[rounded]
            else:
                return '#'

        min_value = self.char2int('a')
        max_value = self.char2int('z') + 1

        value = (np.ceil(hsvColor[0]) - self.hsv_min_hue) * (max_value - min_value) / (self.hsv_max_hue - self.hsv_min_hue) + min_value

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

if len(sys.argv) != 2:
    print("Espera-se um argumento contendo o número de blocos na horizontal")
    exit(1)

image = cv2.imread('profile.png')

decipher = Decipher()
decoded = decipher.decode(image, int(sys.argv[1]))

print(decoded)
