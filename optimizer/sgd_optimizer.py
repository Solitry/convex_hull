import bimpy
import bimpy_tools
import torch

from .optimizer_base import OptimizerBase


class SGDOptimizer(OptimizerBase):
    def __init__(self):
        self._lr = bimpy.Float(0.1)
        self._momentum = bimpy.Float(0)
        self._dampening = bimpy.Float(0)
        self._weight_decay = bimpy.Float(0)
        self._nesterov = bimpy.Bool(False)

        self._hint_nesterov = False
    
    def render(self, is_lock):
        bimpy.indent(10)

        bimpy.text('- SGD')
        bimpy.same_line()
        bimpy_tools.help_marker('torch.optim.SGD')

        flags = bimpy.InputTextFlags.EnterReturnsTrue
        if is_lock:
            flags |= bimpy.InputTextFlags.ReadOnly

        bimpy.push_item_width(120)

        if bimpy.input_float('lr##sgd_optimizer', self._lr, flags=flags):
            self._lr.value = max(0.0, self._lr.value)
        
        if bimpy.input_float('momentum##sgd_optimizer', self._momentum, flags=flags):
            self._momentum.value = max(0.0, self._momentum.value)
        
        if bimpy.input_float('dampening##sgd_optimizer', self._dampening, flags=flags):
            self._dampening.value = max(0.0, self._dampening.value)
        
        if bimpy.input_float('weight_decay##sgd_optimizer', self._weight_decay, flags=flags):
            self._weight_decay.value = max(0.0, self._weight_decay.value)

        if bimpy.checkbox('nesterov##sgd_optimizer', self._nesterov):
            self._hint_nesterov = False

        if self._nesterov.value:
            if self._momentum.value == 0 or self._dampening.value > 0:
                self._nesterov.value = False
                self._hint_nesterov = True
        
        bimpy.same_line()
        bimpy_tools.help_marker('Nesterov momentum requires a momentum and zero dampening', self._hint_nesterov)

        bimpy.pop_item_width()
        bimpy.unindent(10)
    
    def build(self, net):
        optimizer = torch.optim.SGD(
            net.parameters(),
            lr=self._lr.value,
            momentum=self._momentum.value,
            dampening=self._dampening.value,
            weight_decay=self._weight_decay.value,
            nesterov=self._nesterov.value,
        )
        return optimizer
