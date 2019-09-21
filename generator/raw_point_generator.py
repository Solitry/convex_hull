import bimpy
import bimpy_tools

from .generator_base import GeneratorBase


class RawPointGenerator(GeneratorBase):
    def __init__(self):
        self._strategy_list = [
            'random',
            'order',
        ]
        self._select_strategy = self._strategy_list[0]
    
    def render(self, is_lock):
        bimpy.indent(10)

        bimpy.text('- Raw Point')
        bimpy.same_line()
        bimpy_tools.help_marker('generate with raw points')

        bimpy.push_item_width(120)

        if bimpy.begin_combo('strategy##raw_point_generator', self._select_strategy):
            for item in self._strategy_list:
                is_selected = bimpy.Bool(self._select_strategy == item)

                if bimpy.selectable(item, is_selected) and not is_lock:
                    self._select_strategy = item

                if is_selected.value:
                    bimpy.set_item_default_focus()
            bimpy.end_combo()
        
        bimpy.pop_item_width()
        bimpy.unindent(10)

    def set_data(self, raw_points, convex_points):
        pass

    def generate(self, batch_size):
        pass
