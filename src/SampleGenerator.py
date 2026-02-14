import numpy as np



class SampleGenerator:
    def __init__(self, sample_shape):
        self.sample_shape = sample_shape

    def get_sample(self):
        return np.zeros(self.sample_shape)