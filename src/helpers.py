import numpy as np
import random
import math

import glob
from   PIL import Image

import matplotlib.pyplot as plt



def get_images_from_folder(folder):
    images = []

    for filename in glob.glob(f'data/{folder}/*.jpg') + glob.glob(f'data/{folder}/*.png'):
        im = Image.open(filename)
        im = np.array(im).astype(np.float32) / 255
        images.append(im)

    return images


def get_chunk_from_image(image, size):
    chunk = image[random.randint(0, image.shape[0] - size):, 
                  random.randint(0, image.shape[1] - size):]
    chunk = chunk[:size, :size]
    return chunk


def pixellate(image, chunk_size = 5):
    w, h, c = image.shape
    s       = chunk_size

    pixel_map = image.reshape(w//s, s, h//s, s, c)
    pixel_map = pixel_map.transpose(0,2,1,3,4)

    pixel_map = np.average(pixel_map, axis = (2,3,4))
    return pixel_map


# https://stackoverflow.com/questions/2197020/create-grid-out-of-number-of-elements

def plot_image_grid(images):

    x = math.floor(math.sqrt(len(images)))
    y = math.ceil(len(images) / x)

    f, axarr = plt.subplots(y, x)

    for i in range(x * y):

        im_x = math.floor(i / x)
        im_y = i % x

        axarr[im_x, im_y].axis('off')

        if (i < len(images)): axarr[im_x, im_y].imshow(images[i])

    plt.show()