import copy
from typing import Dict, List, Optional, Union

import bimpy

import bimpy_tools
from common.value_type import Point


class ConvexComponent(object):
    def __init__(self):
        self._convex_number = bimpy.Int(4)
        self._convex_data = [
            [bimpy.Float(0.15), bimpy.Float(0.15)],
            [bimpy.Float(0.85), bimpy.Float(0.15)],
            [bimpy.Float(0.85), bimpy.Float(0.85)],
            [bimpy.Float(0.15), bimpy.Float(0.85)],
        ]

        self._convex_data_backup = None
        self._convex_draw_flag = False
    
    def render(self, is_lock):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)
        
        if not bimpy.tree_node('convex points##convex_component'):
            return
        
        bimpy.same_line()
        bimpy_tools.help_marker('Convex points should be presented in counter-clockwise order')

        flags = bimpy.InputTextFlags.EnterReturnsTrue
        if is_lock:
            flags |= bimpy.InputTextFlags.ReadOnly
        
        last_convex_number_value = self._convex_number.value

        if bimpy.input_int('number##convex_component', self._convex_number, 1, 1, flags):
            self._convex_number.value = max(3, self._convex_number.value)
            if last_convex_number_value > self._convex_number.value:
                self._convex_data = self._convex_data[:self._convex_number.value]  # cut back points
            else:
                self._convex_data.extend([
                    [bimpy.Float(0), bimpy.Float(0)] 
                    for _ in range(last_convex_number_value, self._convex_number.value)
                ])
        
        # show convex value setting
        bimpy.set_next_tree_node_open(self._convex_number.value < 10, bimpy.Condition.FirstUseEver)

        if bimpy.tree_node('convex value ({})##convex_component'.format(self._convex_number.value)):
            for index in range(self._convex_number.value):
                bimpy.push_item_width(210)
                bimpy.input_float2(
                    '{:<3d}'.format(index),
                    self._convex_data[index][0],
                    self._convex_data[index][1],
                    flags=flags
                )
                bimpy.pop_item_width()
            bimpy.tree_pop()
        
        # draw part
        bimpy.new_line()
        if bimpy.button('draw convex##convex_component') and not is_lock:
            self._convex_data_backup = [[item[0].value, item[1].value]
                                        for item in self._convex_data]
            self._convex_draw_flag = True
            self._convex_data = []
            self._convex_number.value = 0

        bimpy.tree_pop()

    def get_convex_data(self):
        ret = [Point(im_point[0].value, im_point[1].value)
               for im_point in self._convex_data]
        return ret

    def if_is_drawing(self):
        return self._convex_draw_flag
    
    def get_convex_draw_flag(self):
        return self._convex_draw_flag
    
    def set_convex_draw_value(self, value: Dict[str, Union[List[Point], str]]):
        r"""
        value: {
            'convex': <convex point list, List[Point]>,
            'state': <str, 'none', 'doing', 'done', 'cancel'>, 
        }
        """
        
        if value['state'] == 'none':
            return
        
        if value['state'] == 'doing':
            self._convex_number.value = len(value['convex'])
            self._convex_data = [[bimpy.Float(item.x), bimpy.Float(item.y)]
                                 for item in value['convex']]
            return
        
        if value['state'] == 'cancel':
            self._convex_number.value = len(self._convex_data_backup)
            self._convex_data = [[bimpy.Float(item[0]), bimpy.Float(item[1])]
                                 for item in self._convex_data_backup]
            self._convex_draw_flag = False
        
        if value['state'] == 'done':
            if len(value['convex']) < 3:
                self._convex_number.value = len(self._convex_data_backup)
                self._convex_data = [[bimpy.Float(item[0]), bimpy.Float(item[1])]
                                     for item in self._convex_data_backup]
            else:
                self._convex_number.value = len(value['convex'])
                self._convex_data = [[bimpy.Float(item.x), bimpy.Float(item.y)]
                                     for item in value['convex']]

            self._convex_draw_flag = False
