# Python_Project_AI_for_Automobile
Analysis of detection files with Python

PART 1
This code aims to analyze the output of a Ground truth file (boxes labeled by real person) and a DETECTION FILE (boxes labeled by a system).
For each image, the file contains the following data: x_center, Y_center, width and height.
A dictionary maps a frame to the boxes and an Iou threshold. Then it outputs the minimum and the maximum height for all the boxes which pass the threshold.

PART 2
This code uses a file including bounding boxes and their details. 
It treats outliers and generates graphs of the distance X(t) and the velocity v(t) before and after outliers removement.

PART 3
This code uses an images file and a tsv detection file that includes the coordinates for each object.
It opens the images, draws the relevant objects and save them into a new output file.
