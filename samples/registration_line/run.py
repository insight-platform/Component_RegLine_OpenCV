#!/usr/bin/env python3
import cv2

from registration_line.config import DrawingConfig, RelativeDrawingConfig
from registration_line.draw import draw_line

# Sample code to draw a line with Begin and End labels at the ends of the line and two arrows showing the entry and
# exit directions if the line is crossed.
# The direction of entry and exit is determined by the start and end points,
# entry is clockwise, and exit is anti-clockwise.

if __name__ == '__main__':
    start_point = (150, 550)
    end_point = (450, 50)

    baseline_conf = DrawingConfig(
        color=(128, 0, 128, 255),
        width=2,
        start_label='Begin',
        start_label_offset=(0, 40),
        end_label='End',
        end_label_offset=(0, -20),
        label_font=cv2.FONT_HERSHEY_SIMPLEX,
        label_width=1
    )
    right_line_conf = RelativeDrawingConfig(
        color=(0, 0, 128, 255),
        width=2,
        label='Entry',
        label_offset=(10, 0),
        label_font=cv2.FONT_HERSHEY_SIMPLEX,
        label_width=1,
        start_point_percentage=65,
        length_percentage=27
    )
    left_line_conf = RelativeDrawingConfig(
        color=(0, 128, 0, 255),
        width=2,
        label='Exit',
        label_offset=(-60, 0),
        label_font=cv2.FONT_HERSHEY_SIMPLEX,
        label_width=1,
        start_point_percentage=45,
        length_percentage=16
    )

    image, coordinates = draw_line(start_point, end_point, baseline_conf, right_line_conf, left_line_conf)

    cv2.imshow('Image', image)
    cv2.imwrite("registration_line.png", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
