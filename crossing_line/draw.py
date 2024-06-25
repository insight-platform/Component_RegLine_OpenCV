import math
from typing import Tuple, List

import cv2
import numpy as np

from crossing_line.config import DrawingConfig, RelativeDrawingConfig


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


def draw_rotated_rect(
    image: np.ndarray,
    rect_points: List[Tuple[int, int]],
    center: Tuple[int, int],
    angle: float,
    color: Tuple[int, int, int, int],
    fill: bool = False
):
    """Draw a rectangle on an image.
    Rectangle is defined by four points relative to the center point and rotated around the center by a given angle.
    Rectangle can be filled or just the outline can be drawn with a specific color.
    """

    rotated_points = [rotate_point(center, (center[0] + x, center[1] + y), angle) for x, y in rect_points]
    if fill:
        cv2.fillPoly(image, [np.array(rotated_points, np.int32)], color)
    else:
        cv2.polylines(image, [np.array(rotated_points, np.int32)], isClosed=True, color=color, thickness=2)


def draw_line(
    background_width: int,
    background_height: int,
    start_point: Tuple[int, int],
    end_point: Tuple[int, int],
    config: DrawingConfig,
    right_line_config: RelativeDrawingConfig,
    left_line_config: RelativeDrawingConfig,
) -> Tuple[np.ndarray, Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Draw a line by a given configuration on a background image.
    The line will have two arrows coming from it perpendicularly and pointing in opposite directions from each other.
    Each arrow has its own configuration.

    Return the image and the bounding box of the non-transparent pixels,
    i.e. the bounding box of the line with labels, arrows, and arrows' labels.
    """

    image = np.zeros((background_height, background_width, 4), dtype=np.uint8)

    rect_width, rect_height = 10, 10

    cv2.line(image, start_point, end_point, config.color, config.width)

    angle = np.degrees(np.arctan2(end_point[1] - start_point[1], end_point[0] - start_point[0]))

    start_rect_points = [
        (0, -rect_height // 2),
        (-rect_width, -rect_height // 2),
        (-rect_width, rect_height // 2),
        (0, rect_height // 2)
    ]
    end_rect_points = [
        (0, -rect_height // 2),
        (rect_width, -rect_height // 2),
        (rect_width, rect_height // 2),
        (0, rect_height // 2)
    ]

    draw_rotated_rect(image, start_rect_points, start_point, angle, config.color, fill=True)
    draw_rotated_rect(image, end_rect_points, end_point, angle, config.color, fill=False)

    cv2.putText(image, config.start_label, move_by_offset(start_point, config.start_label_offset), config.font, 1,
        config.color, config.label_width, cv2.LINE_AA
    )
    cv2.putText(image, config.end_label, move_by_offset(end_point, config.end_label_offset), config.font, 1,
        config.color, config.label_width, cv2.LINE_AA
    )

    draw_right_arrowed_line(image, start_point, end_point, angle, right_line_config)
    draw_left_arrowed_line(image, start_point, end_point, angle, left_line_config)

    return image, find_bbox_of_non_transparent_pixels(image)


def move_by_offset(point: Tuple[int, int], offset: Tuple[int, int]) -> Tuple:
    """Move a point by an offset."""

    return tuple(map(lambda x, y: int(x + y), point, offset))


def calculate_line_length(start_point: Tuple[int, int], end_point: Tuple[int, int]):
    """Calculate the length of a line by its start and end points."""

    length = math.sqrt((end_point[0] - start_point[0]) ** 2 + (end_point[1] - start_point[1]) ** 2)
    return length


def draw_arrowed_line(
    image: np.ndarray,
    baseline_start_point: Tuple[int, int],
    baseline_end_point: Tuple[int, int],
    rotate_angle: float,
    color: Tuple[int, int, int, int],
    width: int,
    percentage: int,
    length_percentage: int,
    font: int,
    label: str,
    label_offset: Tuple[int, int],
    label_width: int
):
    """Draw a line with an arrow at the end of the line extending from the baseline at the specified angle.
    Start point of the line is calculated by the percentage of the baseline from the start point.
    Length of the line is calculated by the percentage of the baseline length.
    The line will have a label at the end of the arrow moved by the label offset.
    """

    start_x = baseline_start_point[0] + (baseline_end_point[0] - baseline_start_point[0]) * (percentage / 100.0)
    start_y = baseline_start_point[1] + (baseline_end_point[1] - baseline_start_point[1]) * (percentage / 100.0)

    angle_rad = np.deg2rad(rotate_angle)

    length = calculate_line_length(baseline_start_point, baseline_end_point) * (length_percentage / 100.0)
    dx = length * np.cos(angle_rad)
    dy = length * np.sin(angle_rad)

    start_point = (int(start_x), int(start_y))
    end_point = (int(start_x + dx), int(start_y + dy))

    cv2.line(image, start_point, end_point, color, width)

    arrow_angle = np.arctan2(end_point[1] - start_point[1], end_point[0] - start_point[0])
    arrow_length = width * 8

    arrow_p1 = (int(end_point[0] - arrow_length * np.cos(arrow_angle - np.pi / 6)),
                int(end_point[1] - arrow_length * np.sin(arrow_angle - np.pi / 6)))
    arrow_p2 = (int(end_point[0] - arrow_length * np.cos(arrow_angle + np.pi / 6)),
                int(end_point[1] - arrow_length * np.sin(arrow_angle + np.pi / 6)))

    arrow_pts = np.array([end_point, arrow_p1, arrow_p2], np.int32)
    cv2.fillPoly(image, [arrow_pts], color)

    cv2.putText(image, label, move_by_offset(end_point, label_offset), font, 1, color, label_width, cv2.LINE_AA)


def draw_right_arrowed_line(
    image: np.ndarray,
    start_point: Tuple[int, int],
    end_point: Tuple[int, int],
    angle: float,
    config: RelativeDrawingConfig
):
    """Draw a line with an arrow pointing to the right from the baseline perpendicular to it."""

    draw_arrowed_line(image, start_point, end_point, angle + 90, config.color, config.width,
        config.start_point_percentage, config.length_percentage, config.font, config.end_label, config.end_label_offset,
        config.label_width
    )


def draw_left_arrowed_line(
    image: np.ndarray,
    start_point: Tuple[int, int],
    end_point: Tuple[int, int],
    angle: float,
    config: RelativeDrawingConfig
):
    """Draw a line with an arrow pointing to the left from the baseline perpendicular to it."""

    draw_arrowed_line(image, start_point, end_point, angle - 90, config.color, config.width,
        config.start_point_percentage, config.length_percentage, config.font, config.end_label, config.end_label_offset,
        config.label_width
    )


def find_bbox_of_non_transparent_pixels(image: np.ndarray) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Find the bounding box of the non-transparent pixels in the image."""

    alpha_channel = image[:, :, 3]
    mask = alpha_channel > 0
    coords = cv2.findNonZero(mask.astype(np.uint8))
    x, y, w, h = cv2.boundingRect(coords)

    return (x, y), (x + w, y + h)
