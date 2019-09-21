import bimpy


class TrainResultComponent(object):
    def __init__(self):
        self._measure_value = {
            'batch': {'loss': 0, 'acc': 0},
            'epoch': {'loss': 0, 'acc': 0},
            'valid': {'loss': 0, 'acc': 0},
        }
    
    def set_trainning_result(self, trainning_result):
        for name in self._measure_value:
            if trainning_result[name]:
                self._measure_value[name] = {
                    'loss': trainning_result[name][-1]['loss'],
                    'acc': trainning_result[name][-1]['acc'],
                }
    
    def render(self):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)

        if not bimpy.tree_node('result##train_result_component'):
            return
        
        for item in ['loss', 'acc']:
            for name in self._measure_value:
                bimpy.text('{:<6} {:<6}: {:.8f}'.format(
                    name, item, 
                    self._measure_value[name][item],
                ))
            bimpy.new_line()

        bimpy.tree_pop()
