from typing import Dict, List, Optional, Union

import bimpy

from common.line_draw_tools import render_line
from common.utils import im_col32
from common.value_type import Line, Point


class UserConvexDrawComponet(object):
    def __init__(self):
        self._convex_draw_flag = False
        self._convex_draw_state = 'none'
        self._convex_points = []

    def render(self, origin: bimpy.Vec2, scale: float):
        points_on_canvas = [
            bimpy.Vec2(item.x * scale + origin.x,
                       item.y * -scale + origin.y)
            for item in self._convex_points
        ]

        for index in range(len(points_on_canvas) - 1):
            bimpy.add_line(
                points_on_canvas[index],
                points_on_canvas[index + 1],
                im_col32(211, 85, 186),
                1.0,
            )
        
        for index in range(len(points_on_canvas)):
            bimpy.add_circle_filled(
                points_on_canvas[index],
                2.0,
                im_col32(204, 50, 153),
                16,
            )

    def if_is_drawing(self) -> bool:
        return self._convex_draw_flag

    def set_convex_draw_flag(self, convex_draw_flag):
        self._convex_draw_flag = convex_draw_flag
        if not self._convex_draw_flag:
            self._convex_draw_state = 'none'
            self._convex_points = []
        else:
            self._convex_draw_state = 'doing'

    def set_user_add_point(self, point: Point):
        meet_first_flag = False

        if self._convex_points:
            dist_to_final_point = (self._convex_points[-1] - point).length()
            # print('dist to final point', dist_to_final_point)
            if dist_to_final_point < 1e-2:
                return

            dist_to_first_point = (self._convex_points[0] - point).length()
            # print('dist to first point', dist_to_first_point)
            if dist_to_first_point < 1e-2:
                meet_first_flag = True
        
        if not meet_first_flag:
            self._add_point_to_convex(point)
        
        if meet_first_flag:
            self._convex_draw_state = 'done'

    def set_user_pop_point(self):
        self._pop_point_from_convex()
    
    def set_user_done(self):
        self._convex_draw_state = 'done'
    
    def set_user_cancel(self):
        self._convex_draw_state = 'cancel'
    
    def get_convex_draw_value(self) -> Dict[str, Union[List[Point], str]]:
        ret = {
            'convex': self._convex_points,
            'state': self._convex_draw_state,
        }

        # reset state in consideration of high-APM players
        if self._convex_draw_state in ['done', 'cancel']:
            self._convex_points = []
            self._convex_draw_state = 'none'

        return ret

    def _add_point_to_convex(self, point):
        # while len(self._convex_points) > 1:
        #     old_line = self._convex_points[-1] - self._convex_points[-2]
        #     new_line = point - self._convex_points[-2]
        #     cross_product = old_line ^ new_line
        #     print('cp', cross_product)
        #     if cross_product <= 0:
        #         self._convex_points.pop()
        #     else:
        #         break

        # print('-' * 20)

        for index in range(1, len(self._convex_points)):
            old_line = self._convex_points[index] - self._convex_points[index - 1]
            new_line = point - self._convex_points[index - 1]

            cross_product = old_line ^ new_line

            # print('index =', index)
            # print('index', self._convex_points[index])
            # print('prev ', self._convex_points[index - 1])
            # print('old', old_line)
            # print('new', new_line)
            # print('cp', cross_product)

            if cross_product > 0:
                continue

            self._convex_points = self._convex_points[:index]
            break
            
        if len(self._convex_points) > 1:
            old_line = self._convex_points[0] - self._convex_points[-1]
            new_line = point - self._convex_points[-1]
            cross_product = old_line ^ new_line
            if cross_product > 0:
                return
        
        self._convex_points.append(point)

    def _pop_point_from_convex(self):
        if self._convex_points:
            self._convex_points.pop()
