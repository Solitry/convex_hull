import bimpy

from initializer import init_type_list


class InitializerComponent(object):
    def __init__(self):
        self._initializer_map = {}
        for type_item in init_type_list:
            obj_item = type_item()
            self._initializer_map[obj_item.__class__.__name__] = obj_item

        self._initializer_list = sorted(list(self._initializer_map))
        self._select_initializer = self._initializer_list[0]
    
    def render(self, is_lock):
        bimpy.set_next_tree_node_open(False, bimpy.Condition.FirstUseEver)
        
        if not bimpy.tree_node('initializer##initializer_component'):
            return
        
        if bimpy.begin_combo('select##initializer_component', self._select_initializer):
            for item in self._initializer_list:
                is_selected = bimpy.Bool(self._select_initializer == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_initializer = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        self._initializer_map[self._select_initializer].render(is_lock)

        bimpy.tree_pop()
    
    def build_initializer(self):
        return self._initializer_map[self._select_initializer]
