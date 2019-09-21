from abc import ABCMeta, abstractmethod
from typing import List


class LossFnBase(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, is_locl: bool):
        pass

    @abstractmethod
    def build(self):
        pass
