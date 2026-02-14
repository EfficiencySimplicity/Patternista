from .SampleGenerator import *

import numpy as np



class FloatSampleGenerator(SampleGenerator):
    def __init__(self, sample_shape=[], minval=0, maxval=1):
        self.sample_shape = sample_shape
        self.minval       = minval
        self.maxval       = maxval

    def get_sample(self):
        return np.random.uniform(self.minval, self.maxval, self.sample_shape)