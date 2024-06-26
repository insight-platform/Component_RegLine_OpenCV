#!/usr/bin/env python3
import cv2

from registration_line.config import DrawingConfig, RelativeDrawingConfig
from registration_line.draw import draw_line

# Sample code to draw a line with Begin and End labels at the ends of the line and two arrows showing the entry and
# exit directions if the line is crossed.

if __name__ == '__main__':
    # NB: Start point must be always placed lower than the end point, i.e. the y coordinate of the start point is higher
    start_point = (150, 550)
    end_point = (450, 50)

    background_width = 700
    background_height = 600

    baseline_conf = DrawingConfig(
        (128, 0, 128, 255), 2, 'Begin', (0, 40), 'End', (0, -20), cv2.FONT_HERSHEY_SIMPLEX,
        1
    )
    right_line_conf = RelativeDrawingConfig((0, 0, 128, 255), 2, None, None, 'Entry', (10, 0), cv2.FONT_HERSHEY_SIMPLEX,
        1, 65, 27
    )
    left_line_conf = RelativeDrawingConfig((0, 128, 0, 255), 2, None, None, 'Exit', (-60, 0), cv2.FONT_HERSHEY_SIMPLEX,
        1, 45, 16
    )

    image, coordinates = draw_line(background_width, background_height, start_point, end_point,
        baseline_conf, right_line_conf, left_line_conf
    )

    cv2.imshow('Image', image)
    cv2.imwrite("registration_line.png", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
