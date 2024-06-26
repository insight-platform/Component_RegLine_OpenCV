from typing import Tuple, Optional


class DrawingConfig:
    """Class to store the configuration of a line with two labels to be drawn

    :param color: The color of the line in BGR format with alpha channel
    :param width: The width of the line
    :param start_label: The label to be placed at the start of the line
    :param start_label_offset: The offset to move the start label from the start point
    :param end_label: The label to be placed at the end of the line
    :param end_label_offset: The offset to move the end label from the end point
    :param label_font: The font of the labels
    :param label_width: The width of the label text
    """
    def __init__(self, color: Tuple[int, int, int, int], width: int, start_label: Optional[str],
        start_label_offset: Optional[Tuple[int, int]], end_label: Optional[str],
        end_label_offset: Optional[Tuple[int, int]], label_font: int, label_width: int
    ):
        self._color = color
        self._width = width
        self._start_label = start_label
        self._start_label_offset = start_label_offset
        self._end_label = end_label
        self._end_label_offset = end_label_offset
        self._font = label_font
        self._label_width = label_width

    @property
    def color(self):
        return self._color

    @property
    def font(self):
        return self._font

    @property
    def width(self):
        return self._width

    @property
    def start_label(self):
        return self._start_label

    @property
    def start_label_offset(self):
        return self._start_label_offset

    @property
    def end_label(self):
        return self._end_label

    @property
    def end_label_offset(self):
        return self._end_label_offset

    @property
    def label_width(self):
        return self._label_width


class RelativeDrawingConfig(DrawingConfig):
    """Class to store the configuration of a line with two labels to be drawn relative to the other line.
    Start point is placed at the baseline and is determined by the offset percentage from the start of the baseline.
    Length is determined by the length percentage of the baseline.

    :param color: The color of the line in BGR format with alpha channel
    :param width: The width of the line
    :param start_label: The label to be placed at the start of the line
    :param start_label_offset: The offset to move the start label from the start point
    :param end_label: The label to be placed at the end of the line
    :param end_label_offset: The offset to move the end label from the end point
    :param label_font: The font of the labels
    :param label_width: The width of the label text
    :param start_point_percentage: The percentage of the baseline length to place the start point
    :param length_percentage: The percentage of the baseline length to determine the length of the line
    """
    def __init__(
        self, color: Tuple[int, int, int, int], width: int, start_label: Optional[str],
        start_label_offset: Optional[Tuple[int, int]], end_label: Optional[str],
        end_label_offset: Optional[Tuple[int, int]], label_font: int, label_width: int, start_point_percentage: int,
        length_percentage: int
    ):
        super().__init__(color, width, start_label, start_label_offset, end_label, end_label_offset, label_font,
            label_width
        )
        self._start_point_percentage = start_point_percentage
        self._length_percentage = length_percentage

    @property
    def start_point_percentage(self):
        return self._start_point_percentage

    @property
    def length_percentage(self):
        return self._length_percentage
