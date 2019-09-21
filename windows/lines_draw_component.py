from typing import Dict, List, Optional, Union

import bimpy

from common.line_draw_tools import render_line
from common.utils import im_col32
from common.value_type import Line, Point


class LinesDrawComponent(object):
    def __init__(self):
        self._axis_limit = 100

        self._lines = []  # type: List[Line]

        self._highlight_line_index = None  # type: Optional[int]
        self._waitting_draw_line_index = None  # type: Optional[int]
    
    def render(self, origin: bimpy.Vec2, scale: float):
        line_col = im_col32(255, 255, 255)
        half_plane_col = im_col32(180, 238, 180, 50)

        line_col_highlight = im_col32(0, 69, 255)
        half_plane_col_highlight = im_col32(0, 140, 255, 50)

        if not self._lines:
            return

        for index, line in enumerate(self._lines):
            # print(line)
            if index == self._highlight_line_index:
                continue
            if index == self._waitting_draw_line_index:
                continue

            render_line(line, origin, scale, self._axis_limit, line_col, half_plane_col)
        
        if self._highlight_line_index is not None and self._highlight_line_index != self._waitting_draw_line_index:
            render_line(
                self._lines[self._highlight_line_index],
                origin,
                scale,
                self._axis_limit, 
                line_col_highlight,
                half_plane_col_highlight,
            )

    def set_lines(self, lines):
        self._lines = lines

    def set_highlight_line_index(self, highlight_index: Optional[int]):
        self._highlight_line_index = highlight_index

    def set_waitting_draw_line_index(self, waitting_draw_index: Optional[int]):
        self._waitting_draw_line_index = waitting_draw_index
