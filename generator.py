"""
This module handles the image processing for the project
"""
from PIL import Image
import json
import math
import os
import random


class Generator(object):
    """
    A class that handle the image processing

    ...

    Attributes
    ----------
    bit_depth_config : dict
        dictionary for storing the configuration of each color mode,
        please make sure having `bit_depth_info.json` in the project directory
    mode : str
        color mode for this object, please refer the `bit_depth_info.json` to see the available selection
    width : int
        width for the image
    height : int
        height for the image
    uncompressed : bool
        whether the output image should save in an uncompressed way
    max_bit : int
        shows the number of possible selection in one dimension of the color mode
        (which is defined in the attribute mode), can be checked at `bit_depth_info.json`
    number_of_bit: int
        shows the number of dimension of the color mode (which is defined in the attribute mode),
        can be checked at `bit_depth_info.json`
    file_format : str
        file format for the export image, is determined by the attribute `mode` and `uncompressed`
    scratch : Image object
        the object for temperately store the image that will be generated

    Methods
    -------
    create_random(self, file_name):
        Create and save the image, with the configuration, into the `file_name` specified in the parameter
    """

    def __init__(self, mode='RGB', width=1920, height=1080, uncompressed=True):
        """
        Constructor for the Generator object.

        Parameters
        ----------
        mode : str
            color mode for this object, please refer the `bit_depth_info.json` to see the available selection
        width : int
            width for the image
        height : int
            height for the image
        uncompressed : bool
            whether the output image should save in an uncompressed way

        Raises
        ------
        FileNotFoundError
            when the configuration json file, `bit_depth_info.json` is not found in the project directory
        ValueError
            when the mode requested in the parameter is not supported
        """
        if not os.path.exists('bit_depth_info.json'):
            raise FileNotFoundError('Cannot find the configuration json file for this project!')
        with open('bit_depth_info.json', 'r') as bit_depth_config_file:
            self.bit_depth_config = json.load(bit_depth_config_file)
        # Check if the mode is support
        if mode not in self.bit_depth_config:
            raise ValueError('The mode you requested, \'' + mode + '\' is not supported!')
        # Check if the client need the uncompressed image file
        self.mode = mode
        if uncompressed:
            # Check if the mode have the configuration of uncompressed image format
            if 'uncompressed_image_format' not in self.bit_depth_config[mode]:
                raise ValueError('The mode you requested, \'' + mode + '\' is not supported!')
            self.file_format = self.bit_depth_config[self.mode]['uncompressed_image_format']
        else:
            self.file_format = 'jpeg'
        # Set the configuration of the image
        self.max_bit = self.bit_depth_config[mode]['max_bit']
        self.number_of_bit = self.bit_depth_config[mode]['number_of_bit']
        self.width = width
        self.height = height
        # Initialize the image with given size and color mode
        self.scratch = Image.new(mode=self.mode, size=(self.width, self.height))

    def create_random(self, file_name):
        """
        Create and save the image, with the configuration, into the file_name specified in the parameter

        Parameters
        ----------
        file_name : str
            name of the output file, naming should follow the standard naming conventions defined in OS

        Raises
        ------
        FileExistsError
            when the specified file name exist in the path
        """
        # Check if the file exist for the given file_name
        if not os.path.exists(file_name + "." + self.file_format):
            raise FileExistsError('The file you requested to created is already exist!')
        # Iterate every pixel of the image
        for x_index in range(0, self.width):
            for y_index in range(0, self.height):
                # Set the list of color in the specified pixel
                color = []
                # Loop to add each bit into the color list
                # (times for the loop is the total bit for that method,
                # the random range is 0 to the max_bit th power of 2 - 1)
                for bit in range(0, self.number_of_bit):
                    color.append(random.randint(0, int(math.pow(2, self.max_bit)) - 1))
                # Put the generated color list into the pixel
                self.scratch.putpixel(xy=(x_index, y_index), value=tuple(color))
        # Save the image with the file name and the format
        self.scratch.save(file_name + "." + self.file_format)
