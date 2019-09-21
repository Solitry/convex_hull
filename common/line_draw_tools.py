from typing import Dict, List, Optional, Union

import bimpy

from common.utils import im_col32
from common.value_type import Line, Point


__all__ = ['render_line']


def intersection(line, limit):
    def intersection_x(a, b, c, x):
        return None if abs(b) < 1e-7 else Point(x, -(c + a * x) / b)
    
    def intersection_y(a, b, c, y):
        return None if abs(a) < 1e-7 else Point(-(c + b * y) / a, y)

    a, b, c = line.a, line.b, line.c

    raw_item = [
        intersection_x(a, b, c, -limit),
        intersection_x(a, b, c, limit),
        intersection_y(a, b, c, -limit),
        intersection_y(a, b, c, limit),
    ]
    
    select_item = [item for item in raw_item if item is not None]
    select_item.sort(key=lambda t: (t.x, t.y))

    if len(select_item) < 2:
        return None, None
    
    return select_item[0], select_item[-1]


def corner(line, limit):
    point_list = [
        Point(-limit, -limit),
        Point(-limit, limit),
        Point(limit, -limit),
        Point(limit, limit),
    ]

    max_approx_dis = 0
    ret = None

    for point in point_list:
        approx_dis = line.a * point.x + line.b * point.y + line.c
        if approx_dis > max_approx_dis:
            max_approx_dis = approx_dis
            ret = point
    
    return ret


def render_line(line, origin, scale, axis_limit, line_col, half_plane_col):
    if not line.is_valid():
        return

    start_point, end_point = intersection(line, axis_limit)
    if start_point is None:
        return

    corner_point = corner(line, axis_limit)
    if corner_point is None:
        return

    cross_result = (end_point - start_point) ^ (corner_point - start_point)
    if cross_result > 0:
        polygon = [start_point, corner_point, end_point]
    else:
        polygon = [start_point, end_point, corner_point]
    
    polygon_on_canvas = [
        bimpy.Vec2(item.x * scale + origin.x,
                   item.y * -scale + origin.y)
        for item in polygon
    ]

    bimpy.add_convex_poly_filled(polygon_on_canvas, half_plane_col)

    bimpy.add_line(
        bimpy.Vec2(start_point.x * scale + origin.x, start_point.y * -scale + origin.y),
        bimpy.Vec2(end_point.x * scale + origin.x, end_point.y * -scale + origin.y),
        line_col,
        1.0,
    )
