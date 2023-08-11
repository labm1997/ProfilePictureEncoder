import numpy as np
import cv2
import argparse
from crypt.decipher import Decipher

parser = argparse.ArgumentParser(
    prog='rectangular_decode',
    description='Decodes rectangular image profile to text')
parser.add_argument('filename')
parser.add_argument('n_rows')
parser.add_argument('--hsv_min_hue', default=0)
parser.add_argument('--hsv_max_hue', default=360)
args = parser.parse_args()


def subsample(image, nrows):
    imageSize = image.shape[0]

    blockSize = round(imageSize / nrows)

    return image[round(blockSize / 2): imageSize: blockSize, round(blockSize / 2): imageSize: blockSize]


def convert2hsv(image):
    hsvImage = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))

    return hsvImage


def decode(image, nrows):
    subsampled = subsample(image, nrows)

    hsvImage = convert2hsv(np.float32(subsampled / 255.0))

    hsvArray = hsvImage.reshape(-1, 3).tolist()

    decipher = Decipher(hsv_min_hue=int(args.hsv_min_hue),
                        hsv_max_hue=int(args.hsv_max_hue))

    return decipher.decode(hsvArray)


image = cv2.imread(args.filename)
decoded = decode(image, int(args.n_rows))

print(decoded)
