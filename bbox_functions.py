import numpy as np
import cv2
import os


vehicle_bbox_info ={ # type : [class, (kernel_size), l]
    'Motorcycle': [0, (18, 10), 0],    # Motorcycle
    'Car': [1, (40, 20), 3],    # Car
    'Taxi': [2, (40, 20), 3],    # Taxi
    'Bus': [3, (110, 30), 50],  # Bus
    'Medium Vehicle': [4, (50, 20), 8],    # Medium Vehicle
    'Heavy Vehicle': [5, (50, 25), 10],   # Heavy Vehicle
}


def create_bbox_for_vehicles(vehicle_type, vehicle_img_coordinate, vehicle_direction_angle):
    '''
        vehicle_type: The type of the vehicle either in string format of in integer
        ex) Motorcycle = 0
            Car = 1
            Taxi =2
            Bus = 3
            Medium Vehicle = 4
            Heavy Vehicle = 5
    '''

    vehicle_class = vehicle_bbox_info[vehicle_type][0]
    kernel_size = vehicle_bbox_info[vehicle_type][1]
    l = vehicle_bbox_info[vehicle_type][2]

    new_x = vehicle_img_coordinate[0] - l * np.cos(vehicle_direction_angle)
    new_y = vehicle_img_coordinate[1] - l * np.sin(vehicle_direction_angle)
    vehicle_img_coordinate = (new_x, new_y)

    # cv2.boxPoints((centerX, centerY), (w, h), angle_in_degree)
    box = (vehicle_img_coordinate, kernel_size, np.rad2deg(vehicle_direction_angle))

    return box


def adjust_bbox_for_crop(bbox_rect, vehicle_type, TL_pts, w, h, intersect_area_threshold = 0.2):
    centerX = (TL_pts[0] + w / 2)
    centerY = (TL_pts[1] + h / 2)
    crop_rect = ((centerX, centerY), (w, h), 0)

    ret, intersecting_region = cv2.rotatedRectangleIntersection(bbox_rect, crop_rect)
    if ret == 2 : # totally overlap
        bbox_rect_cropped = intersecting_region.reshape((intersecting_region.shape[0],2)) - TL_pts
    elif ret == 1: # partially overlap
        bbox_kernel_size = vehicle_bbox_info[vehicle_type][1]
        bbox_area = bbox_kernel_size[0] * bbox_kernel_size[1]
        intersecting_area = cv2.contourArea(intersecting_region)
        # print(vehicle_type,':', bbox_area, ':', cv2.contourArea(intersecting_region))
        if intersecting_area > bbox_area * intersect_area_threshold:
            bbox_rect_cropped = intersecting_region.reshape((intersecting_region.shape[0], 2)) - TL_pts
        else:
            bbox_rect_cropped = None
    else:
        bbox_rect_cropped = None

    return bbox_rect_cropped
