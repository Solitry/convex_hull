import bimpy

from loss_function import loss_function_type_list


class LossFunctionComponent(object):
    def __init__(self):
        self._loss_function_map = {}
        for type_item in loss_function_type_list:
            obj_item = type_item()
            self._loss_function_map[obj_item.__class__.__name__] = obj_item
        
        self._loss_function_list = sorted(list(self._loss_function_map))
        self._select_loss_function = self._loss_function_list[0]
    
    def render(self, is_lock):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)
        
        if not bimpy.tree_node('loss function##loss_function_component'):
            return
        
        if bimpy.begin_combo('select##loss_function_component', self._select_loss_function):
            for item in self._loss_function_list:
                is_selected = bimpy.Bool(self._select_loss_function == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_loss_function = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        self._loss_function_map[self._select_loss_function].render(is_lock)

        bimpy.tree_pop()

    def build_loss_function(self):
        return self._loss_function_map[self._select_loss_function].build()
