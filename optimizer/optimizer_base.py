from abc import ABCMeta, abstractmethod


class OptimizerBase(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, is_lock):
        # type: (bool) -> None
        pass

    @abstractmethod
    def build(self, net):
        pass
