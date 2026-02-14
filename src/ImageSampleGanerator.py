from .helpers import *
from .SampleGenerator import *

import random


# TODO: full path, this could be accessed from anywhere
class ImageSampleGenerator(SampleGenerator):
    def __init__(self, folder = None, images = None, sample_size = 5):
        self.sample_size  = sample_size
        self.sample_shape = [sample_size, sample_size, 3]

        if (folder is not None):
            self.images = get_images_from_folder(folder)
        elif images is not None:
            self.images = images
        else:
            raise(Exception('Must provide either folder path or image list'))
        
    def get_sample(self):
        image = random.choice(self.images)
        return get_chunk_from_image(image, self.sample_size)