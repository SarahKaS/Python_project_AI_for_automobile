import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PIL
from PIL import Image
import os
from os import listdir


# Load the detection file
data = pd.read_csv("Q3_Draw_task_labels.tsv", sep='\t')

# print(data.head(10))
# print(data.describe())


folder_dir = "./Q3_Draw_task_images/Q3_Draw_task_images"

# create new empty folder Images_draw_output for output:
output_path = "./Q3_Draw_task_images/Images_draw_output"
os.makedirs(output_path, exist_ok = True)


img = []
new_img = []
index = 0
num = 0
draw_indx = 0

# open each image from the folder and find all its "crops"
for images in os.listdir(folder_dir):
    img.append(Image.open(os.path.join(folder_dir, images)))
    draw_indx = 0
    for index in range(0,len(data)):
        if images.endswith(data['name'][index]):
            drawn_image = img[num].crop((data['x_center'][index] - (data['width'][index]/2),
                                               data['y_center'][index] - (data['height'][index]/2),
                                               data['x_center'][index] + (data['width'][index]/2),
                                               data['y_center'][index] + (data['height'][index]/2)))
            new_img.append(drawn_image)
            drawn_image.save(os.path.join(output_path, "drawn_image_{}_name_{}".format(draw_indx, data['name'][index])))
            draw_indx += 1
    num += 1


