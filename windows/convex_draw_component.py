import bimpy
from typing import Optional, List

from common.value_type import Point
from common.utils import im_col32


class ConvexDrawComponent(object):
    def __init__(self):
        self._convex_points = []  # type: List[Points]
    
    def render(self, origin: bimpy.Vec2, scale: float):
        if not self._convex_points:
            return
        
        points_on_canvas = [
            bimpy.Vec2(item.x * scale + origin.x,
                       item.y * -scale + origin.y)
            for item in self._convex_points
        ]

        bimpy.add_convex_poly_filled(points_on_canvas, im_col32(50, 50, 50))

    def set_convex_points(self, convex_points):
        self._convex_points = convex_points
