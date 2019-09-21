import torch
import threading
from typing import List, Dict, Union

from common.value_type import Point, Sample
from net.convex_net import ConvexNet


class TrainningRunner(threading.Thread):
    def __init__(self):
        super().__init__()

        self._net = None
        self._optimizer = None
        self._loss_fn = None
        self._generator = None

        self._epoch = 0
        self._batch_size = 0
        self._batch_per_epoch = 0

        self._valid_size = 0

        self._epoch_now = 0
        self._batch_now = 0

        self._valid_tensor_input = None
        self._valid_tensor_target = None

        # each array contains measure format
        # {
        #    'loss': <loss value>,
        #    'acc': <acc value>,
        #    'epoch': <now epoch>,
        #    'batch': <now batch, Optional>,
        # }
        self._trainning_result = {'batch': [], 'epoch': [], 'valid': []}

        self._stop_flag = False
    
    def create_net(self, width):
        self._net = ConvexNet(width)
    
    def get_net(self):
        return self._net
    
    def set_net_value(self, lines):
        self._net.set_value(lines)
    
    def get_net_value(self):
        return self._net.get_value()
    
    def set_optimizer(self, optimizer):
        self._optimizer = optimizer
    
    def set_loss_function(self, loss_fn):
        self._loss_fn = loss_fn
    
    def set_generator(self, generator):
        self._generator = generator
    
    def set_trainning_params(self, params):
        self._epoch = params['epoch']
        self._batch_size = params['batch_size']
        self._batch_per_epoch = params['batch_per_epoch']
        self._valid_size = params['valid_size']
    
    def get_trainning_progress(self) -> Dict[str, int]:
        return {
            'epoch_now': self._epoch_now,
            'epoch_all': self._epoch,
        }
    
    def get_tranning_result(self) -> Dict[str, List[Dict[str, Union[float, int]]]]:
        ret = self._trainning_result
        self._trainning_result = {'batch': [], 'epoch': [], 'valid': []}
        return ret

    def run_one_batch(self):
        sample_list = self._generator.generate(self._batch_size)
        input, target = self._foramt_data(sample_list)

        self._optimizer.zero_grad()
        output = self._net(input)
        loss = self._loss_fn(output, target)
        loss.backward()
        self._optimizer.step()

        return loss.tolist(), self._calc_accuracy(output, target)

    def try_to_stop(self):
        self._stop_flag = True

    def run(self):
        self._stop_flag = False
        self._epoch_now = 0
        self._batch_now = 0

        self._create_valid_set()

        for epoch_now in range(self._epoch):
            self._epoch_now = epoch_now + 1

            epoch_batch_sum_loss = 0
            epoch_batch_sum_acc = 0

            for batch_now in range(self._batch_per_epoch):
                self._batch_now = batch_now + 1

                if self._stop_flag:
                    return

                batch_loss_value, batch_acc_value = self.run_one_batch()
                # print('batch {}-{}: {} {}'.format(self._epoch_now, self._batch_now, batch_loss_value, batch_acc_value))
                self._trainning_result['batch'].append({
                    'loss': batch_loss_value,
                    'acc': batch_acc_value,
                    'epoch': epoch_now,
                    'batch': batch_now,
                })

                epoch_batch_sum_loss += batch_loss_value
                epoch_batch_sum_acc += batch_acc_value
            
            valid_loss_value, valid_acc_value = self._run_valid_set()
            # print('valid {}: {} {}'.format(self._epoch_now, valid_loss_value, valid_acc_value))
            self._trainning_result['valid'].append({
                'loss': valid_loss_value,
                'acc': valid_acc_value,
                'epoch': epoch_now,
                'batch': None,
            })

            self._trainning_result['epoch'].append({
                'loss': epoch_batch_sum_loss / self._batch_per_epoch,
                'acc': epoch_batch_sum_acc / self._batch_per_epoch,
                'epoch': epoch_now,
                'batch': None,
            })

    @staticmethod
    def _foramt_data(data: List[Sample]):
        input_list = []
        target_list = []

        for sample in data:
            input_list.append([sample.point.x, sample.point.y])
            target_list.append(sample.tag)
        
        return torch.Tensor(input_list), torch.Tensor(target_list)

    def _create_valid_set(self):
        sample_list = self._generator.generate(self._valid_size)
        self._valid_tensor_input, self._valid_tensor_target = self._foramt_data(sample_list)

    def _run_valid_set(self):
        valid_output = self._net(self._valid_tensor_input)
        valid_loss = self._loss_fn(valid_output, self._valid_tensor_target)
        return valid_loss.tolist(), self._calc_accuracy(valid_output, self._valid_tensor_target)

    @staticmethod
    def _calc_accuracy(output, target):
        round_output = torch.round(output)
        return (round_output == target).float().mean().tolist()
