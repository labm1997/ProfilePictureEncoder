import numpy as np
import cv2
import sys


class Cipher:
    def __init__(self, hsv_min_hue=0, hsv_max_hue=360):
        self.hsv_min_hue = hsv_min_hue
        self.hsv_max_hue = hsv_max_hue

        self.specialMap = {
            ' ': [0, 0, 0.1],
            ',': [0, 0, 0.2],
            ':': [0, 0, 0.3],
            '.': [0, 0, 0.4],
            '?': [0, 0, 0.5],
            '-': [0, 0, 0.6],
        }

    def char2int(self, character):
        return int(bytes(character, 'ASCII')[0])

    def mapper(self, character):

        if character in self.specialMap:
            return self.specialMap[character]

        min_value = self.char2int('a')
        max_value = self.char2int('z') + 1

        value = self.char2int(character)

        if value >= min_value and value <= max_value:
            hue = (value - min_value) / (max_value - min_value) * \
                (self.hsv_max_hue - self.hsv_min_hue) + self.hsv_min_hue
            return [hue, 1, 1]

        else:
            print('Character \'' + str(character) +
                  '\' not mapped, using [0,0,0]')
            return [0, 0, 0]

    def encode(self, text):
        return np.array(list(map(self.mapper, list(text))))

    # def array2matrix(self, array):
    #     opSize = int(np.ceil((np.sqrt(array.shape[0]))))
    #     padded = np.pad(array, ((0, opSize**2 - array.shape[0]), (0, 0)))
    #     reshaped = padded.reshape(opSize, opSize, 3)
    #     return np.float32(reshaped)

    # def encode(self, text):
    #     colorArray = self.text2color(text.lower())

    #     paddedMessage = self.array2matrix(colorArray)

    #     rgbImage = np.float32(cv2.cvtColor(paddedMessage, cv2.COLOR_HSV2BGR))

    #     resized = cv2.resize(rgbImage, (1024, 1024),
    #                          interpolation=cv2.INTER_NEAREST)

    #     return resized

# if len(sys.argv) != 2:
#     print("Espera-se um argumento contendo a mensagem")
#     exit(1)


# cipher = Cipher()
# encoded = cipher.encode(
#     "Voce, que tem ideias tao modernas. E o mesmo homem que vivia nas cavernas.")
# # encoded = cipher.encode(sys.argv[1])

# # cv2.imshow('profile', encoded)
# # cv2.waitKey(0)

# cv2.imwrite('profile_3.png', encoded * 255)
