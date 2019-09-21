import torch
import bimpy

import bimpy_tools
from common.value_type import Point, Sample
from common import geometry

from .generator_base import GeneratorBase


class PlaneRandomGenerator(GeneratorBase):
    def __init__(self):
        self._strategy_list = [
            'plane random',
            'balanced random',
        ]
        self._select_strategy = self._strategy_list[0]

        self._convex_points = None

    def render(self, is_lock):
        bimpy.indent(10)

        bimpy.text('- Plane')
        bimpy.same_line()
        bimpy_tools.help_marker(
            'generate with random points\n' \
            '* plane random: random on whole plane\n' \
            '* balanced random: balanced positive and negative samples'
        )

        bimpy.push_item_width(140)

        if bimpy.begin_combo('strategy##plane_random_generator', self._select_strategy):
            for item in self._strategy_list:
                is_selected = bimpy.Bool(self._select_strategy == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_strategy = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        bimpy.pop_item_width()
        bimpy.unindent(10)


    def set_data(self, raw_points, convex_points):
        self._convex_points = convex_points

    def generate(self, batch_size):
        assert self._convex_points is not None

        if self._select_strategy == 'plane random':
            return self._generate_plane(batch_size)
        else:
            return self._generate_balanced(batch_size)
    
    def _generate_plane(self, batch_size):
        ret = []
        for _ in range(batch_size):
            point = self._get_random_point_by_torch()
            in_convex_flag = geometry.is_in_convex(point, self._convex_points)
            tag = 0 if in_convex_flag else 1
            ret.append(Sample(point.x, point.y, tag))
        return ret

    def _generate_balanced(self, batch_size):
        group = [[], []]
        in_size = batch_size // 2
        out_size = batch_size - in_size

        while len(group[0]) < in_size or len(group[1]) < out_size:
            point = self._get_random_point_by_torch()
            in_convex_flag = geometry.is_in_convex(point, self._convex_points)
            tag = 0 if in_convex_flag else 1

            if in_convex_flag and len(group[0]) >= in_size:
                continue
            if not in_convex_flag and len(group[1]) >= out_size:
                continue
            
            group[tag].append(Sample(point.x, point.y, tag))
        
        return group[0] + group[1]
    
    @staticmethod
    def _get_random_point_by_torch() -> Point:
        rv = torch.rand(2).tolist()
        return Point(rv[0], rv[1])
