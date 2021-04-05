import numpy as np
import cv2

class Cipher:
    def __init__(self):
        pass

    def char2int(self, character):
        return int(bytes(character, 'ASCII')[0])

    def mapper(self, character):
        specialMap = {
            ' ': [0, 0, 0.1],
            ',': [0, 0, 0.2],
            ':': [0, 0, 0.3],
            '.': [0, 0, 0.4],
            '?': [0, 0, 0.5],
            '-': [0, 0, 0.6],
        }

        if character in specialMap: return specialMap[character]

        min_value = self.char2int('a')
        max_value = self.char2int('z')

        value = self.char2int(character)

        if value >= min_value and value <= max_value:
            hue = (value - (min_value - 1)) / (max_value - (min_value - 1)) * 178
            return [hue, 1, 1]

        else:
            print('Character \'' + str(character) + '\' not mapped, using [0,0,0]')
            return [0, 0, 0]

    def text2color(self, text):
        return np.array(list(map(self.mapper, list(text))))

    def array2matrix(self, array):
        opSize = int(np.ceil((np.sqrt(array.shape[0]))))
        padded = np.pad(array, ((0, opSize**2 - array.shape[0]), (0,0)))
        reshaped = padded.reshape(opSize, opSize, 3)
        return np.float32(reshaped)

    def encode(self, text):
        colorArray = self.text2color(text.lower())

        paddedMessage = self.array2matrix(colorArray)

        rgbImage = np.float32(cv2.cvtColor(paddedMessage, cv2.COLOR_HSV2BGR))

        resized = cv2.resize(rgbImage, (1024, 1024), interpolation=cv2.INTER_NEAREST)

        return resized

cipher = Cipher()
encoded = cipher.encode("In the end the Party would announce that two and two made five, and you would have to believe it. It was inevitable that they should make that claim sooner or later: the logic of their position demanded it. Not merely the validity of experience, but the very existence of external reality, was tacitly denied by their philosophy. The heresy of heresies was common sense. And what was terrifying was not that they would kill you for thinking otherwise, but that they might be right. For, after all, how do we know that two and two make four? Or that the force of gravity works? Or that the past is unchangeable? If both the past and the external world exist only in the mind, and if the mind itself is controllable - what then?")

cv2.imshow('profile', encoded)
cv2.waitKey(0)

cv2.imwrite('profile.png', encoded * 255)
