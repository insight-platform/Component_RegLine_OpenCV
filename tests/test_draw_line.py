#!/usr/bin/env python3
import cv2
import numpy as np

from registration_line.config import DrawingConfig, RelativeDrawingConfig
from registration_line.draw import draw_line

if __name__ == '__main__':
    start_point = (150, 550)
    end_point = (450, 50)

    background_width = 700
    background_height = 600

    baseline_conf = DrawingConfig((128, 0, 128, 255), 2, 'Begin', (0, 40), 'End', (0, -20), cv2.FONT_HERSHEY_SIMPLEX,
        1
    )
    right_line_conf = RelativeDrawingConfig(
        (0, 0, 128, 255), 2, 'Entry', (10, 0), cv2.FONT_HERSHEY_SIMPLEX,
        1, 65, 27
    )
    left_line_conf = RelativeDrawingConfig(
        (0, 128, 0, 255), 2, 'Exit', (-60, 0), cv2.FONT_HERSHEY_SIMPLEX,
        1, 45, 16
    )

    image, coordinates = draw_line(start_point, end_point, baseline_conf, right_line_conf, left_line_conf)

    expected_image = cv2.imread("../samples/registration_line/registration_line.png", cv2.IMREAD_UNCHANGED)

    assert np.array_equal(image, expected_image)
    assert coordinates == ((88, 58), (519, 649))
