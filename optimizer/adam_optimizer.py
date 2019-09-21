import bimpy
import bimpy_tools
import torch

from .optimizer_base import OptimizerBase


class AdamOptimizer(OptimizerBase):
    def __init__(self):
        self._lr = bimpy.Float(0.001)
        self._betas_first = bimpy.Float(0.9)
        self._betas_second = bimpy.Float(0.999)
        self._eps = bimpy.Float(1e-8)
        self._weight_decay = bimpy.Float(0)
        self._amsgrad = bimpy.Bool(False)
    
    def render(self, is_lock):
        bimpy.indent(10)

        bimpy.text('- Adam')
        bimpy.same_line()
        bimpy_tools.help_marker('torch.optim.Adam')

        flags = bimpy.InputTextFlags.EnterReturnsTrue
        if is_lock:
            flags |= bimpy.InputTextFlags.ReadOnly

        bimpy.push_item_width(140)

        if bimpy.input_float('lr##adam_optimizer', self._lr, flags=flags):
            self._lr.value = max(0.0, self._lr.value)
        
        if bimpy.input_float2('momentum##adam_optimizer', self._betas_first, self._betas_second, flags=flags):
            self._betas_first.value = max(0.0, self._betas_first.value)
            self._betas_second.value = max(0.0, self._betas_second.value)
        
        if bimpy.input_float('eps##adam_optimizer', self._eps, decimal_precision=8, flags=flags):
            self._dampening.value = max(0.0, self._eps.value)
        
        if bimpy.input_float('weight_decay##adam_optimizer', self._weight_decay, flags=flags):
            self._weight_decay.value = max(0.0, self._weight_decay.value)

        bimpy.checkbox('amsgrad##adam_optimizer', self._amsgrad)

        bimpy.pop_item_width()
        bimpy.unindent(10)
    
    def build(self, net):
        optimizer = torch.optim.Adam(
            net.parameters(),
            lr=self._lr.value,
            betas=(self._betas_first.value, self._betas_second.value),
            eps=self._eps.value,
            weight_decay=self._weight_decay.value,
            amsgrad=self._amsgrad.value,
        )
        return optimizer
