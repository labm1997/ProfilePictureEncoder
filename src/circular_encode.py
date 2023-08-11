import numpy as np
import cv2
import sys
import argparse
from crypt.cipher import Cipher

parser = argparse.ArgumentParser(
    prog='circular_encode',
    description='Encodes text to circular image profile image')
parser.add_argument('text')
parser.add_argument('output')
parser.add_argument('--hsv_min_hue', default=0)
parser.add_argument('--hsv_max_hue', default=360)
parser.add_argument('--scale', default=1)
args = parser.parse_args()

width, height = 1024, 1024
image = np.zeros((height, width, 3), dtype=np.uint8)

cipher = Cipher(hsv_min_hue=int(args.hsv_min_hue),
                hsv_max_hue=int(args.hsv_max_hue))
encoded = cipher.encode(args.text)


def draw_arc(image, radius=200, quadrant=0, total_quadrants=4, color=(255, 0, 0), thickness=10, scale=1):
    # Define the parameters for the arc
    center = (width // 2, height // 2)
    # radius = 200
    #
    start_angle = (-360 / total_quadrants) * quadrant - \
        thickness / (2*np.pi*radius) * 360 / 2 * 1.1
    end_angle = (-360 / total_quadrants) * (quadrant+1) + \
        thickness / (2*np.pi*radius) * 360 / 2 * 1.1

    # Draw the arc on the image
    cv2.ellipse(image, center, (int(radius * scale), int(radius * scale)), 0,
                start_angle, end_angle, color, int(thickness * scale))


def hsv_to_bgr(hsv):
    color = cv2.cvtColor(
        np.array([[[hsv[0], hsv[1], hsv[2]]]], dtype=np.float32), cv2.COLOR_HSV2BGR)[0][0]
    return (int(255*color[0]), int(255*color[1]), int(255*color[2]))


# Display the image with the arc
thickness = 20
radio_0 = 20
levels = 30
scale = float(args.scale)

i = 0
for level in range(levels):
    radius = radio_0 + thickness * level
    total_quadrants = int(2*np.pi*radius / 40)

    for quadrant in range(total_quadrants):
        # hue = (250+np.random.random() * 100)
        hsv = encoded[i] if len(encoded) > i else (0, 0, 0)
        draw_arc(image, radius=radius, quadrant=quadrant, total_quadrants=total_quadrants,
                 color=hsv_to_bgr(hsv), thickness=thickness-2, scale=scale)

        i += 1

if (i < len(encoded)):
    print("WARNING, text not entirely on image")
# cv2.imshow('Arc of Circle', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
cv2.imwrite(args.output, image)
