from typing import Optional, Dict, Union

import bimpy

from common.value_type import Line

from .initializer_component import InitializerComponent


class LinesComponent(object):
    def __init__(self):
        self._line_number = bimpy.Int(4)
        self._last_line_number_value = self._line_number.value

        self._line_data = [
            [bimpy.Float(1), bimpy.Float(1), bimpy.Float(-1)],
            [bimpy.Float(1), bimpy.Float(-1), bimpy.Float(-0.5)],
            [bimpy.Float(-1), bimpy.Float(1), bimpy.Float(-0.5)],
            [bimpy.Float(0), bimpy.Float(-1), bimpy.Float(0.5)],
        ]

        self.initializer_component = InitializerComponent()

        self._highlight_line_index = None
        self._waitting_draw_line_index = None
    
    def render(self, is_lock):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)
        
        if not bimpy.tree_node('lines##lines_component'):
            return

        # number setting
        flags = bimpy.InputTextFlags.EnterReturnsTrue
        if is_lock:
            flags |= bimpy.InputTextFlags.ReadOnly
        
        if bimpy.input_int('number##lines_component', self._line_number, 1, 1, flags):
            self._line_number.value = max(3, self._line_number.value)
            if self._last_line_number_value > self._line_number.value:
                self._line_data = self._line_data[:self._line_number.value]  # cut back points
            else:
                self._line_data.extend([
                    [bimpy.Float(0), bimpy.Float(0), bimpy.Float(0)] 
                    for _ in range(self._last_line_number_value, self._line_number.value)
                ])
            self._last_line_number_value = self._line_number.value
            # print('line number change to {}'.format(self._line_number.value))

        # show line value setting
        bimpy.set_next_tree_node_open(self._line_number.value < 10, bimpy.Condition.FirstUseEver)

        self._highlight_line_index = None

        if bimpy.tree_node('line value ({})'.format(self._line_number.value)):
            for index in range(self._line_number.value):
                bimpy.push_item_width(210)
                bimpy.input_float3(
                    '{:<3d}'.format(index),
                    self._line_data[index][0],
                    self._line_data[index][1],
                    self._line_data[index][2],
                    flags=flags
                )
                bimpy.pop_item_width()

                if bimpy.is_item_hovered():
                    self._highlight_line_index = index

                bimpy.same_line()
                if bimpy.button('rev##lines_component{}'.format(index)) and not is_lock:
                    for j in range(3):
                        self._line_data[index][j].value = -self._line_data[index][j].value
                
                if bimpy.is_item_hovered():
                    self._highlight_line_index = index

                bimpy.same_line()
                if bimpy.button('draw##lines_component{}'.format(index)) and not is_lock:
                    self._waitting_draw_line_index = index
                    bimpy.set_window_focus('canvas window##canvas')
                
                if bimpy.is_item_hovered():
                    self._highlight_line_index = index

            bimpy.tree_pop()

        # random setting
        bimpy.new_line()
        if bimpy.button('random##lines_component') and not is_lock:
            initializer = self.initializer_component.build_initializer()
            random_lines = initializer.random(self._line_number.value)
            for index in range(self._line_number.value):
                self._line_data[index][0].value = random_lines[index].a
                self._line_data[index][1].value = random_lines[index].b
                self._line_data[index][2].value = random_lines[index].c
        
        self.initializer_component.render(is_lock)

        bimpy.tree_pop()

    def _set_one_line_data(self, index: int, line: Line):
        self._line_data[index][0].value = line.a
        self._line_data[index][1].value = line.b
        self._line_data[index][2].value = line.c

    def get_line_data(self):
        ret = [Line(im_line[0].value, im_line[1].value, im_line[2].value)
               for im_line in self._line_data]
        return ret

    def set_line_data(self, lines):
        assert len(lines) == self._line_number.value

        for i in range(self._line_number.value):
            self._set_one_line_data(i, lines[i])

    def get_highlight_line_index(self) -> Optional[int]:
        return self._highlight_line_index

    def if_is_drawing(self) -> bool:
        return self._waitting_draw_line_index is not None

    def get_waitting_draw_line_index(self) -> Optional[int]:
        return self._waitting_draw_line_index

    def set_waitting_draw_line_value(self, value: Optional[Dict[str, Union[Line, str]]]):
        r"""
        value: {
            'line': <Line value, None if not drawing>,
            'state': <draw state, can be 'none', 'doing', 'done'>
        }
        """

        if value['state'] == 'none' or value['line'] is None:
            return
        
        if value['state'] == 'doing':
            self._set_one_line_data(self._waitting_draw_line_index, value['line'])
        
        if value['state'] == 'done':
            self._set_one_line_data(self._waitting_draw_line_index, value['line'])
            self._waitting_draw_line_index = None
