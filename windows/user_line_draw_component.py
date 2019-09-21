from typing import Dict, List, Optional, Union

import bimpy

from common.line_draw_tools import render_line
from common.utils import im_col32
from common.value_type import Line, Point


class UserLineDrawComponent(object):
    def __init__(self):
        self._waitting_draw_line_index = None  # type: Optional[int]
        self._waitting_draw_line_abc = None  # type: Optional[Line]
        self._waitting_draw_line_state = 'none'  # type: str

        self._start_point = None  # type: Optional[Point]
        self._end_point = None  # type: Optional[Point]
    
    def render(self, origin: bimpy.Vec2, scale: float):
        if not self.if_is_drawing():
            # print('not drawing')
            return

        if self._waitting_draw_line_abc is None or not self._waitting_draw_line_abc.is_valid():
            # print('line is None or not valid {}'.format(self._waitting_draw_line_abc))
            return
        
        render_line(
            self._waitting_draw_line_abc,
            origin,
            scale,
            100,
            im_col32(0, 69, 255),
            im_col32(0, 140, 255, 50),
        )

    def if_is_drawing(self) -> bool:
        return self._waitting_draw_line_index is not None
    
    # def set_raw_drawing_start_point(self, mouse_pos: bimpy.Vec2, origin: bimpy.Vec2, scale: float):
    #     self.set_drawing_start_point(Point(
    #         (mouse_pos.x - origin.x) / scale,
    #         (mouse_pos.y - origin.y) / -scale,
    #     ))
    
    # def set_raw_drawing_end_point(self, mouse_pos: bimpy.Vec2, origin: bimpy.Vec2, scale: float, done: bool):
    #     self.set_drawing_end_point(Point(
    #         (mouse_pos.x - origin.x) / scale,
    #         (mouse_pos.y - origin.y) / -scale,
    #     ), done)

    def set_drawing_start_point(self, start_point: Point):
        self._start_point = start_point

    def set_drawing_end_point(self, end_point: Point, done: bool):
        self._end_point = end_point

        self._waitting_draw_line_abc = self._calc_line(self._start_point, self._end_point)

        if done and self._waitting_draw_line_abc is not None:
            self._waitting_draw_line_state = 'done'
            # print('done')
    
    @staticmethod
    def _calc_line(start_point: Point, end_point: Point) -> Optional[Line]:
        delta = end_point - start_point
        if delta.length() < 1e-7:
            return None

        delta.normalize_()
        a, b = -delta.y, delta.x
        c = -(start_point.x * a + start_point.y * b)
        return Line(a, b, c)

    def set_waitting_draw_line_index(self, waitting_draw_index: Optional[int]):
        self._waitting_draw_line_index = waitting_draw_index

        if waitting_draw_index is None:
            self._waitting_draw_line_abc = None
            self._waitting_draw_line_state = 'none'
        else:
            self._waitting_draw_line_state = 'doing'
    
    def get_waitting_draw_line_value(self) -> Optional[Dict[str, Union[Line, str]]]:
        return {
            'line': self._waitting_draw_line_abc,
            'state': self._waitting_draw_line_state,
        }

    def get_waitting_draw_line_index(self):
        return self._waitting_draw_line_index
