import bimpy


class TrainPhaseComponent(object):
    def __init__(self):
        self._is_trainning = False
        self._is_trainning_start = False
        self._is_trainning_stop = False

        self._trainning_progress = None
    
    def if_is_trainning(self):
        return self._is_trainning
    
    def if_is_trainning_start(self):
        return self._is_trainning_start
    
    def if_is_trainning_stop(self):
        return self._is_trainning_stop

    def set_trainning_progress(self, trainning_progress):
        self._trainning_progress = trainning_progress

    def render(self, is_running):
        bimpy.set_next_tree_node_open(True, bimpy.Condition.FirstUseEver)

        if not bimpy.tree_node('progress##train_phase_component'):
            return

        self._is_trainning_start = False
        self._is_trainning_stop = False
        if self._is_trainning:
            if bimpy.button('stop##train_phase_component'):
                # print('stop')
                self._is_trainning = False
                self._is_trainning_stop = True
            if not is_running:
                # print('run over stop')
                self._is_trainning = False
                self._is_trainning_stop = True
        else:
            if bimpy.button('start##train_phase_component'):
                # print('start {}'.format(is_running))
                if not is_running:
                    self._is_trainning = True
                    self._is_trainning_start = True

        if self._trainning_progress is not None:
            bimpy.text('epoch: {} / {}'.format(
                self._trainning_progress['epoch_now'],
                self._trainning_progress['epoch_all'],
            ))

        bimpy.tree_pop()
