import bimpy

from optimizer import optimizer_type_list


class OptimizerComponent(object):
    def __init__(self):
        self._optimizer_map = {}
        for type_item in optimizer_type_list:
            obj_item = type_item()
            self._optimizer_map[obj_item.__class__.__name__] = obj_item
        
        self._optimizer_list = sorted(list(self._optimizer_map))
        self._select_optimizer = self._optimizer_list[0]

    def render(self, is_lock):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)
        
        if not bimpy.tree_node('optimizer##optimizer_component'):
            return

        if bimpy.begin_combo('select##optimizer_component', self._select_optimizer):
            for item in self._optimizer_list:
                is_selected = bimpy.Bool(self._select_optimizer == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_optimizer = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        self._optimizer_map[self._select_optimizer].render(is_lock)

        bimpy.tree_pop()

    def build_optimizer(self, net):
        return self._optimizer_map[self._select_optimizer].build(net)
