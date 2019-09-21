import bimpy

from trainning.trainning_runner import TrainningRunner

from .convex_component import ConvexComponent
from .generator_component import GeneratorComponent
from .lines_component import LinesComponent
from .loss_function_component import LossFunctionComponent
from .optimizer_component import OptimizerComponent
from .train_component import TrainComponent
from .train_phase_component import TrainPhaseComponent
from .train_result_component import TrainResultComponent


class DashWindow(object):
    def __init__(self):
        self.lines_componnet = LinesComponent()
        self.generator_component = GeneratorComponent()
        self.optimizer_component = OptimizerComponent()
        self.train_component = TrainComponent()
        self.convex_component = ConvexComponent()
        self.train_phase_component = TrainPhaseComponent()
        self.loss_function_component = LossFunctionComponent()
        self.train_result_component = TrainResultComponent()

        self.trainning_runner = None
        self._is_tranning_runner_running = False

    def render(self):
        bimpy.set_next_window_pos(bimpy.Vec2(765, 30), bimpy.Condition.FirstUseEver)
        bimpy.set_next_window_size(bimpy.Vec2(410, 750), bimpy.Condition.FirstUseEver)

        if not bimpy.begin('dash window'):  # open fail
            bimpy.end()
            return
        
        is_lock = any([
            self.train_phase_component.if_is_trainning(),
            self.lines_componnet.if_is_drawing(),
            self.convex_component.if_is_drawing(),
        ])

        # dash board
        if bimpy.collapsing_header('convex setting', bimpy.TreeNodeFlags.DefaultOpen):
            self.convex_component.render(is_lock)
            bimpy.new_line()

        if bimpy.collapsing_header('train setting', bimpy.TreeNodeFlags.DefaultOpen):
            self.lines_componnet.render(is_lock)
            bimpy.new_line()
            self.generator_component.render(is_lock)
            bimpy.new_line()
            self.optimizer_component.render(is_lock)
            bimpy.new_line()
            self.loss_function_component.render(is_lock)
            bimpy.new_line()
            self.train_component.render(is_lock)
            bimpy.new_line()
        
        if bimpy.collapsing_header('train phase', bimpy.TreeNodeFlags.DefaultOpen):
            self.train_phase_component.render(self._is_tranning_runner_running)
            bimpy.new_line()
            self.train_result_component.render()
            bimpy.new_line()

        # padding
        for _ in range(5):
            bimpy.new_line()

        # trainning runner
        if self.train_phase_component.if_is_trainning_start():
            self.trainning_runner = TrainningRunner()

            line_data = self.lines_componnet.get_line_data()

            self.trainning_runner.create_net(width=len(line_data))
            self.trainning_runner.set_net_value(line_data)

            generator = self.generator_component.build_generator()
            generator.set_data(raw_points=[], convex_points=self.convex_component.get_convex_data())
            self.trainning_runner.set_generator(generator)

            self.trainning_runner.set_optimizer(
                self.optimizer_component.build_optimizer(self.trainning_runner.get_net()))

            self.trainning_runner.set_loss_function(
                self.loss_function_component.build_loss_function())
            
            self.trainning_runner.set_trainning_params(
                self.train_component.get_train_setting())
            
            self._is_tranning_runner_running = True
            self.trainning_runner.start()
        
        # if self.train_phase_component.if_is_trainning():
        if self._is_tranning_runner_running:
            # self.trainning_runner.run_once()
            line_data = self.trainning_runner.get_net_value()
            self.lines_componnet.set_line_data(line_data)

        # if self.trainning_runner is not None:
            self.train_phase_component.set_trainning_progress(
                self.trainning_runner.get_trainning_progress())
            
            self.train_result_component.set_trainning_result(
                self.trainning_runner.get_tranning_result())
        
        if self.train_phase_component.if_is_trainning_stop():
            self.trainning_runner.try_to_stop()
        
        if self._is_tranning_runner_running:
            self.trainning_runner.join(1e-2)
            self._is_tranning_runner_running = self.trainning_runner.is_alive()

        bimpy.end()

    def close(self):
        if self._is_tranning_runner_running:
            self.trainning_runner.try_to_stop()
            self.trainning_runner.join()
