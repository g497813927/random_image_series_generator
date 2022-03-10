import json
import math
import os
from PIL import Image
import random

with open('bit_depth_info.json', 'r') as bit_depth_config_file:
    bit_depth_config = json.load(bit_depth_config_file)


class Generator(object):
    def __init__(self, mode='RGB', width=1920, height=1080):
        # Check if the mode is support
        if mode not in bit_depth_config:
            raise ValueError('The mode you requested, \'' + mode + '\' is not supported!')
        if 'uncompressed_image_format' not in bit_depth_config[mode]:
            raise ValueError('The mode you requested, \'' + mode + '\' is not supported!')
        # Set the preset value of the image
        self.mode = mode
        self.max_bit = bit_depth_config[mode]['max_bit']
        self.number_of_bit = bit_depth_config[mode]['number_of_bit']
        self.width = width
        self.height = height
        # Initialize the image with given size and color mode
        self.scratch = Image.new(mode=self.mode, size=(self.width, self.height))

    def create_random(self, file_name):
        if os.path.exists(file_name + "." + bit_depth_config[self.mode]['uncompressed_image_format']):
            raise FileExistsError('The file you requested to created is already exist!')
        for x_index in range(0, self.width):
            for y_index in range(0, self.height):
                color = []
                for bit in range(0, self.number_of_bit):
                    color.append(random.randint(0, int(math.pow(2, self.max_bit)) - 1))
                self.scratch.putpixel(xy=(x_index, y_index), value=tuple(color))
        self.scratch.save(file_name + "." + bit_depth_config[self.mode]['uncompressed_image_format'])
