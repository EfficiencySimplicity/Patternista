import numpy as np
from .helpers import *



def abs_difference(a, b):
    return 1 - np.abs(a - b)


def average_update(a, b, examples_seen, learning_rate='auto'):
    if learning_rate == 'auto': average_amount = 1 / (examples_seen+1)
    else: average_amount = learning_rate

    return (a * (1 - average_amount)) + (b * average_amount)


# TODO: add a seperate update_fn for the uncertainty
# TODO: docstrings
# TODO: plotting patterns for various shapes, make sure to apply squeeze() for tiny dimensions
class PatternMatcher:
    def __init__(self, num_patterns, pattern_initializer, comparison_fn = abs_difference, update_fn = average_update):
        self.num_patterns     = num_patterns
        self.sample_generator = pattern_initializer
        self.pattern_shape    = pattern_initializer.sample_shape

        self.patterns         = np.array([pattern_initializer.get_sample() for i in range(num_patterns)])
        self.examples_seen    = np.ones([self.num_patterns])

        self.comparison_fn    = comparison_fn
        self.update_fn        = update_fn

    def train_sample(self, sample = None, learning_rate = 'auto'):
        sample = sample or self.sample_generator.get_sample()

        most_similar = self.get_most_similar(sample)
        
        self.patterns[most_similar]      = self.update_fn(self.patterns[most_similar], sample, self.examples_seen[most_similar], learning_rate)
        self.examples_seen[most_similar] += 1

    def get_most_similar(self, sample):
        return np.argmax(self.get_similarity_scores(sample))

    def get_similarity_scores(self, sample):
        return np.average(self.comparison_fn(self.patterns, sample), axis=list(range(1, len(self.pattern_shape)+1)))
    
    def get_activation_map(self, image):
        if (len(self.pattern_shape) != 3):
            raise Exception(f"This function only available with a 3D pattern shape, this PatternMatcher has shape: {self.pattern_shape}")
        
        w,h,c = image.shape
        x_tiles = int(math.floor(w / self.pattern_shape[0]))-1
        y_tiles = int(math.floor(h / self.pattern_shape[1]))-1

        activation_map = np.zeros([self.num_patterns,
                                   w-self.pattern_shape[0]+1,
                                   h-self.pattern_shape[1]+1])

        # per-pattern for now
        for i, pattern in enumerate(self.patterns):
            tiled = np.tile(pattern, [x_tiles, y_tiles, 1])

            max_x = w - tiled.shape[0] + 1
            max_y = h - tiled.shape[1] + 1

            for x in range(0, max_x):
                for y in range(0, max_y):
                    padded = np.pad(tiled, [[x, max_x - x - 1],[y, max_y - y - 1],[0,0]])

                    subbed = self.comparison_fn(padded, image)
                    subbed = subbed[x:tiled.shape[0] + x, y:tiled.shape[1] + y]
                    subbed = pixellate(subbed, chunk_size=self.pattern_shape[0])
                    
                    activation_map[i, 
                                   x:x + tiled.shape[0]:self.pattern_shape[0], 
                                   y:y + tiled.shape[1]:self.pattern_shape[1]] = subbed
                    
        return activation_map

    # separation should be easy
    # divergence