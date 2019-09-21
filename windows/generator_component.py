import bimpy

from generator import generator_type_list


class GeneratorComponent(object):
    def __init__(self):
        self._generator_map = {}
        for type_item in generator_type_list:
            obj_item = type_item()
            self._generator_map[obj_item.__class__.__name__] = obj_item
        
        self._generator_list = sorted(list(self._generator_map))
        self._select_generator = self._generator_list[0]

    def render(self, is_lock):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)
        
        if not bimpy.tree_node('generator##generator_component'):
            return
        
        if bimpy.begin_combo('select##generator_component', self._select_generator):
            for item in self._generator_list:
                is_selected = bimpy.Bool(self._select_generator == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_generator = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        self._generator_map[self._select_generator].render(is_lock)

        bimpy.tree_pop()

    def build_generator(self):
        return self._generator_map[self._select_generator]
