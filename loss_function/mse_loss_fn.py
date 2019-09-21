import torch
import bimpy
import bimpy_tools

from .loss_fn_base import LossFnBase


class MSELossFn(LossFnBase):
    def __init__(self):
        self._reduction_list = ['mean', 'sum', 'none']
        self._select_redution = self._reduction_list[0]
    
    def render(self, is_lock):
        bimpy.indent(10)

        bimpy.text('- MSE loss')
        bimpy.same_line()
        bimpy_tools.help_marker('torch.nn.MSELoss')

        bimpy.push_item_width(120)

        if bimpy.begin_combo('reduction##mse_loss_fn', self._select_redution):
            for item in self._reduction_list:
                is_selected = bimpy.Bool(self._select_redution == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_redution = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        bimpy.pop_item_width()
        bimpy.unindent(10)
    
    def build(self):
        return torch.nn.MSELoss(reduction=self._select_redution)
