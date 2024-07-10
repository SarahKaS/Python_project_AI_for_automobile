
import numpy as np
import matplotlib.pyplot as plt
import json
import time

class BoundingBox:
    def __init__(self, x_center=0, y_center=0, width=0, height=0, iou=0):
        self.x_center = x_center
        self.y_center = y_center
        self.width = width
        self.height = height
        self.iou = iou


def read_lean_map_of_bboxes(input_json_file_path: str):
    with open(input_json_file_path, 'r') as json_stream:
        raw_object = json.load(json_stream)
    return {k: [BoundingBox(**item) for item in v] for k, v in raw_object.items()}


def get_minimum_and_maximum_height(boxes, iou):
    iou_threshold = iou
    max_height = 0
    min_height = 0
    height_pass_list = []

    for name, detection_bounding_box_list in detection_boxes.items():
        for det_box in detection_bounding_box_list:
            #print(det_box.iou)
            if det_box.iou > iou_threshold:
                height_pass_list.append(det_box.height)

    max_height = max(height_pass_list)
    min_height = min(height_pass_list)

    return min_height, max_height


def create_historgram(boxes, iou_threshold):
    count_boxes = 0
    iou_pass_list = []

    for name, detection_bounding_box_list in detection_boxes.items():
        for det_box in detection_bounding_box_list:
            if det_box.iou > iou_threshold:
                iou_pass_list.append(det_box.iou)
                count_boxes += 1

    #plt.style.use('Solarize_Light2')

    # We can add the option True density to get a normalized histogram
    plt.figure(figsize=(10, 6))
    plt.hist(iou_pass_list, bins=30, histtype='bar', range=[iou_threshold, 1], color='steelblue', edgecolor='blue')
    plt.xlabel('iou', fontsize=15)
    plt.ylabel('occurrences', fontsize=15)
    plt.title('Boxes that pass the threshold', fontsize=15)





def calculate_average_iou(boxes, iou):

    iou_threshold = iou
    count_boxes_pass = 0
    tot_iou_pass = 0

    for name, detection_bounding_box_list in detection_boxes.items():
        for det_box in detection_bounding_box_list:
            #print(det_box.iou)
            if det_box.iou > iou_threshold:
                tot_iou_pass += det_box.iou
                count_boxes_pass += 1

    iou_avg = tot_iou_pass / count_boxes_pass
    return iou_avg



def calculate_iou_for_2_boxes(box1, box2):
    x1 = box1.x_center
    y1 = box1.y_center
    w1 = box1.width
    h1 = box1.height

    x2 = box2.x_center
    y2 = box2.y_center
    w2 = box2.width
    h2 = box2.height

    # overlap_area
    w_overlap = min((x1 + (w1/2)), (x2 + (w2/2))) - max((x1 - (w1/2)), (x2 - (w2/2)))
    h_overlap = min((y1 + (h1/2)), (y2 + (h2/2))) - max((y1 - (h1/2)), (y2 - (h2/2)))

    # make iou null for two boxes that do not overlap (h_overlap or w_overlap negative)
    if w_overlap>0 and h_overlap>0:
        overlap_area = w_overlap * h_overlap
    else:
        overlap_area=0


    # union_area
    union_area = w1*h1 + w2*h2 - overlap_area

    # iou
    iou = overlap_area / union_area

    return iou


if __name__ == '__main__':
    path_detection_boxes_json = "Q1_system_output.json"
    path_groundtruth_boxes_json = "Q1_gt.json"
    iou_threshold = 0.5

    detection_boxes = read_lean_map_of_bboxes(path_detection_boxes_json)
    ground_truth_boxes = read_lean_map_of_bboxes(path_groundtruth_boxes_json)

    for name, detection_bounding_box_list in detection_boxes.items():
        ground_truth_bounding_box_list = ground_truth_boxes[name]
        for det_box in detection_bounding_box_list:
            for gt_bbox in ground_truth_bounding_box_list:
                iou = calculate_iou_for_2_boxes(det_box, gt_bbox)
                # saving the highest iou for a detection bounding box
                if iou > getattr(det_box, 'iou', 0):
                    det_box.iou = iou

    # calculate average iou for the boxes that pass > iou_threshold
    average_iou = calculate_average_iou(detection_boxes, iou_threshold)
    print(f"The average_iou is: {average_iou}")

    # create histogram for the boxes that pass iou_threshold.
    # x_axis: iou, y_axis: occurrences
    create_historgram(detection_boxes, iou_threshold)

    # find the minimum and the maximum height for the boxes that pass > iou_threshold
    min_height, max_height = get_minimum_and_maximum_height(detection_boxes, iou_threshold)
    print(f"The min_height is: {min_height} and the max_height is: {max_height}")
    plt.show()



