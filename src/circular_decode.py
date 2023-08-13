import cv2
import numpy as np
from crypt.decipher import Decipher
import argparse

parser = argparse.ArgumentParser(
    prog='circular_decode',
    description='Decodes circular image profile image to text')
parser.add_argument('filename')
parser.add_argument('--hsv_min_hue', default=0)
parser.add_argument('--hsv_max_hue', default=360)
args = parser.parse_args()

# Load the image
image = cv2.imread(args.filename, cv2.IMREAD_ANYCOLOR)
width, height, depth = image.shape

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def get_radius_match(image_gray, radius, sample_size=100):
    sample_size = 100
    theta = np.linspace(0, 2*np.pi, sample_size)

    x = (width // 2 + radius * np.cos(theta)).astype(np.int64)
    y = (height // 2 + radius * np.sin(theta)).astype(np.int64)

    match = np.dot(image_gray[x, y].flatten(),
                   np.ones((sample_size,))) / sample_size

    return match, (x, y)


def detect_circles(image_gray, min_radius=50, max_radius=500):
    detected_circles = []

    current_circle_radiuses = []
    for radius in range(min_radius, max_radius):
        match, (x, y) = get_radius_match(image_gray, radius)

        if match < 5:
            image_gray[x, y] = 255

            if len(current_circle_radiuses) == 0:
                current_circle_radiuses.append(radius)
            elif np.abs(np.array(current_circle_radiuses) - radius).min() < 15:
                current_circle_radiuses.append(radius)
            else:
                # Close current circle
                # print(current_circle_radiuses)
                detected_circles.append(
                    np.array(current_circle_radiuses).max())
                current_circle_radiuses = []

    if len(current_circle_radiuses) > 0:
        # Close last circle
        # print(current_circle_radiuses)
        detected_circles.append(np.array(current_circle_radiuses).max())
        current_circle_radiuses = []

    return np.array(detected_circles)


def get_arcs_from_circles(detected_circles):
    distances = detected_circles[1:] - detected_circles[0:-1]
    mean_distance = int(distances.mean())
    print("All values should be near:", distances)

    arcs = []
    for i in range(len(detected_circles)):
        if i+1 < len(detected_circles):
            arcs.append([detected_circles[i], detected_circles[i+1]])
        else:
            arcs.append(
                [detected_circles[i], min(detected_circles[i] + mean_distance, height//2)])

    return np.array(arcs)


def detect_quadrant_angle(hsv_image, arcs):
    radius1, radius2 = arcs

    thetas = np.linspace(+np.pi/18, 2*np.pi - np.pi/18, 1000)

    # Detect divisions
    divisions = [0]
    on_division = False
    for theta in thetas:
        t = np.linspace(radius1, radius2)
        x = (width // 2 + t * np.cos(theta)).astype(np.int64)
        y = (height // 2 - t * np.sin(theta)).astype(np.int64)

        holes = np.sum(hsv_image[y, x][:, 2] == 0.0) / \
            hsv_image[y, x][:, 2].size

        if not on_division and holes > 0.5:
            on_division = True
            divisions.append(theta)

        elif on_division and holes < 0.4:
            on_division = False

    divisions = np.array(divisions)

    return np.mean(divisions[1:] - divisions[0:-1])


def get_hsv_from_arcs(hsv_image, arcs):
    radius1, radius2 = arcs

    radius = (radius1 + radius2) / 2.0

    quadrant_angle = detect_quadrant_angle(hsv_image, arcs)
    total_quadrants = int(2*np.pi / quadrant_angle)

    theta = np.array(
        [2*np.pi * (q+0.5) / total_quadrants for q in range(total_quadrants)])
    x = (width // 2 + radius * np.cos(theta)).astype(np.int64)
    y = (height // 2 - radius * np.sin(theta)).astype(np.int64)

    return hsv_image[y, x]


detected_circles = detect_circles(image_gray, min_radius=20, max_radius=500)
detected_arcs = get_arcs_from_circles(detected_circles)

for [arc1, arc2] in detected_arcs:
    cv2.circle(image, (width//2, height//2), arc1, (255, 0, 0), 1)
    cv2.circle(image, (width//2, height//2), arc2, (255, 0, 0), 1)

hsv_image = np.float32(cv2.cvtColor(
    np.float32(image / 255.0), cv2.COLOR_BGR2HSV))

for arcs in detected_arcs:
    arc_hsv = get_hsv_from_arcs(hsv_image, arcs)

    decipher = Decipher(hsv_min_hue=int(args.hsv_min_hue),
                        hsv_max_hue=int(args.hsv_max_hue))
    decoded = decipher.decode(arc_hsv)

    print(decoded, end="")

print("")
# Display the image with detected circles
cv2.imshow('Detected Arcs', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
