import numpy as np
import cv2
import argparse
from crypt.cipher import Cipher

parser = argparse.ArgumentParser(
    prog='rectangular_encode',
    description='Encodes text to rectangular image profile image')
parser.add_argument('text')
parser.add_argument('output')
parser.add_argument('--hsv_min_hue', default=0)
parser.add_argument('--hsv_max_hue', default=360)
args = parser.parse_args()


def array2matrix(array):
    opSize = int(np.ceil((np.sqrt(array.shape[0]))))
    padded = np.pad(array, ((0, opSize**2 - array.shape[0]), (0, 0)))
    reshaped = padded.reshape(opSize, opSize, 3)
    return np.float32(reshaped)


def encode(text):
    cipher = Cipher(hsv_min_hue=int(args.hsv_min_hue),
                    hsv_max_hue=int(args.hsv_max_hue))
    colorArray = cipher.encode(text)

    paddedMessage = array2matrix(colorArray)
    rgbImage = np.float32(cv2.cvtColor(paddedMessage, cv2.COLOR_HSV2BGR))
    resized = cv2.resize(rgbImage, (1024, 1024),
                         interpolation=cv2.INTER_NEAREST)

    return resized


cv2.imwrite(args.output, 255*encode(args.text))
