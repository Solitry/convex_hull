import math

import bimpy
import torch
from torch.nn import init

import bimpy_tools
from common.value_type import Line

from .init_base import InitBase


class LinearLayerInit(InitBase):
    def __init__(self):
        self._a = bimpy.Float(math.sqrt(5))

        self._mode_list = ['fan_in', 'fan_out']
        self._select_mode = self._mode_list[0]

        self._nonlinearity_list = ['leaky_relu', 'relu']
        self._select_nonlinearity = self._nonlinearity_list[0]
    
    def render(self, is_lock):
        bimpy.indent(10)

        bimpy.text('- Linear layer init')
        bimpy.same_line()
        bimpy_tools.help_marker('Initializer used in torch.nn.Linear, use Kaiming uniform')

        bimpy.push_item_width(120)

        flags = bimpy.InputTextFlags.EnterReturnsTrue
        if is_lock:
            flags |= bimpy.InputTextFlags.ReadOnly

        if bimpy.input_float('a##sgd_optimizer', self._a, flags=flags):
            self._a.value = max(0.0, self._a.value)

        if bimpy.begin_combo('mode##linear_layer_init', self._select_mode):
            for item in self._mode_list:
                is_selected = bimpy.Bool(self._select_mode == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_mode = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()

        if bimpy.begin_combo('nonlinearity##linear_layer_init', self._select_nonlinearity):
            for item in self._nonlinearity_list:
                is_selected = bimpy.Bool(self._select_nonlinearity == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_nonlinearity = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        bimpy.pop_item_width()
        bimpy.unindent(10)

    def random(self, line_size):
        weight = torch.Tensor(line_size, 2)
        bias = torch.Tensor(line_size)

        init.kaiming_uniform_(weight, a=self._a.value)
        fan_in, _ = init._calculate_fan_in_and_fan_out(weight)
        bound = 1 / math.sqrt(fan_in)
        init.uniform_(bias, -bound, bound)

        weight_list = weight.tolist()
        bias_list = bias.tolist()

        return [Line(a=weight_list[index][0],
                     b=weight_list[index][1],
                     c=bias_list[index])
                for index in range(line_size)]
