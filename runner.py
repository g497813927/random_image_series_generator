import os
import generator

mode = 'RGB'
width = 1920
height = 1080
total_number_need = 3600
path = 'out/'
generator = generator.Generator(mode=mode, width=width, height=height, uncompressed=True)
if not os.path.exists(path):
    os.mkdir(path)
for count in range(0, total_number_need):
    generator.create_random("{}test-{}".format(path, str(count)))
