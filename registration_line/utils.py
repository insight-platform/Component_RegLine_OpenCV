import math
from typing import Tuple

import cv2
import numpy as np


def move_by_offset(point: Tuple[int, int], offset: Tuple[int, int]) -> Tuple:
    """Move a point by an offset."""

    return tuple(map(lambda x, y: int(x + y), point, offset))


def calculate_length(start_point: Tuple[int, int], end_point: Tuple[int, int]) -> float:
    """Calculate the length of a line by its start and end points."""

    length = math.sqrt((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)
    return length


def rotate_point(center: Tuple[int, int], point: Tuple[int, int], angle: float) -> Tuple[int, int]:
    """Rotate a point around a center by a given angle."""

    angle_rad = np.deg2rad(angle)
    cos_angle = np.cos(angle_rad)
    sin_angle = np.sin(angle_rad)

    x, y = point
    cx, cy = center

    x -= cx
    y -= cy

    x_new = x * cos_angle - y * sin_angle
    y_new = x * sin_angle + y * cos_angle

    x_new += cx
    y_new += cy

    return int(x_new), int(y_new)


def find_bbox_of_non_transparent_pixels(image: np.ndarray) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Find the bounding box of the non-transparent pixels in the image."""

    alpha_channel = image[:, :, 3]
    mask = alpha_channel > 0
    coords = cv2.findNonZero(mask.astype(np.uint8))
    x, y, w, h = cv2.boundingRect(coords)

    return (x, y), (x + w, y + h)


def adjust_coordinates(
    coordinates: Tuple[Tuple[int, int], Tuple[int, int]],
    top_left: Tuple[int, int]
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Adjust coordinates by moving them to a new top-left point."""

    (x, y), (x2, y2) = coordinates
    x += top_left[0]
    y += top_left[1]
    x2 += top_left[0]
    y2 += top_left[1]

    return (x, y), (x2, y2)
