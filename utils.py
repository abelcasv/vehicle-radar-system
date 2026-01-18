"""
Auxiliary functions for detecting, tracking, and counting cars.
Separated from the main program to improve clarity and reuse.
"""

import cv2
import math

from scipy.ndimage import center_of_mass
from scipy.spatial import distance_matrix


# ************************************************************
# CLASS VEHICLE

class Vehicle:
    """
    It represents a car detected and tracked throughout the frames.
    """
    def __init__(self, center, bbox, vehicle_id):
        self.center = center               # Current center of the car
        self.bbox = bbox                   # (x, y, w, h)
        self.vehicle_id = vehicle_id       # Unique identifier
        self.frames_missing = 0            # Undetected frames
        self.counted = False               # To avoid duplication


# ************************************************************
# FRAME PREPROCESSING

def get_foreground_mask(frame, background_subtractor, kernel):
    """
    Applies background subtraction and morphological operations
    to obtain the motion mask.
    """
    fg_mask = background_subtractor.apply(frame)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
    return fg_mask


# ************************************************************
# VEHICLE ASSOCIATION

def find_closest_vehicle(center, vehicles, max_distance):
    """
    Finds the existing vehicle closest to a given center.
    """
    closest_vehicle = None
    min_distance = max_distance

    for vehicle in vehicles:
        distance = math.hypot(
            center[0] - vehicle.center[0],
            center[1] - vehicle.center[1]
        )
        if distance < min_distance:
            min_distance = distance
            closest_vehicle = vehicle

    return closest_vehicle


def process_detection(center, bbox, vehicles, visible_vehicles,
                      count_line_y, vehicle_count, vehicle_id_counter, max_distance):
    """
    Updates an existing vehicle or creates a new one from a detection.
    """
    vehicle = find_closest_vehicle(center, vehicles, max_distance)

    # CASE 1: existing vehicle
    if vehicle:
        vehicle.center = center
        vehicle.bbox = bbox
        vehicle.frames_missing = 0
        visible_vehicles.append(vehicle)

        # Count if it crosses the line for the first time
        if not vehicle.counted and center[1] >= count_line_y:
            vehicle_count += 1
            vehicle.counted = True

    # CASE 2: new vehicle
    else:
        new_vehicle = Vehicle(center, bbox, vehicle_id_counter)
        vehicle_id_counter += 1

        # Count immediately if already past the line
        if center[1] >= count_line_y:
            vehicle_count += 1
            new_vehicle.counted = True

        vehicles.append(new_vehicle)
        visible_vehicles.append(new_vehicle)

    return vehicle_count, vehicle_id_counter


# ************************************************************
# FILTER LOST VEHICLES

def filter_vehicles(vehicles, visible_vehicles, max_frames_missing):
    """
    Removes vehicles that have been missing for too many frames.
    """
    filtered_vehicles = []

    for vehicle in vehicles:
        if vehicle in visible_vehicles:
            filtered_vehicles.append(vehicle)
        else:
            vehicle.frames_missing += 1
            if vehicle.frames_missing < max_frames_missing:
                filtered_vehicles.append(vehicle)

    return filtered_vehicles


# ************************************************************
# DRAWING

def draw(frame, visible_vehicles, count_line_y, vehicle_count):
    """
    Draws bounding boxes, counting line, and vehicle count on the frame.
    """
    for vehicle in visible_vehicles:
        x, y, w, h = vehicle.bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Draw the counting line
    cv2.line(frame, (0, count_line_y),
             (frame.shape[1], count_line_y), (0, 0, 255), 2)

    # Draw the counter text
    cv2.putText(frame, f"Vehicles detected: {vehicle_count}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)
