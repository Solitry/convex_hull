import bimpy


class TrainComponent(object):
    def __init__(self):
        self._epoch = bimpy.Int(500)
        self._batch_size = bimpy.Int(256)
        self._batch_per_epoch = bimpy.Int(10)
        self._valid_size = bimpy.Int(1024)
    
    def render(self, is_lock):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)
        
        if not bimpy.tree_node('trainning##train_component'):
            return
        
        flags = bimpy.InputTextFlags.EnterReturnsTrue
        if is_lock:
            flags |= bimpy.InputTextFlags.ReadOnly
        
        bimpy.push_item_width(120)

        if bimpy.input_int('epoch##train_component', self._epoch, 0, 0, flags=flags):
            self._epoch.value = max(1, self._epoch.value)
        
        if bimpy.input_int('batch_size##train_component', self._batch_size, 0, 0, flags=flags):
            self._batch_size.value = max(1, self._batch_size.value)
        
        if bimpy.input_int('batch_per_epoch##train_component', self._batch_per_epoch, 0, 0, flags=flags):
            self._batch_per_epoch.value = max(1, self._batch_per_epoch.value)
        
        if bimpy.input_int('valid_size##train_component', self._valid_size, 0, 0, flags=flags):
            self._valid_size.value = max(0, self._valid_size.value)

        bimpy.pop_item_width()

        bimpy.tree_pop()

    def get_train_setting(self):
        return {
            'epoch': self._epoch.value,
            'batch_size': self._batch_size.value,
            'batch_per_epoch': self._batch_per_epoch.value,
            'valid_size': self._valid_size.value,
        }
