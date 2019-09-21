from abc import ABCMeta, abstractmethod
from typing import List

from common.value_type import Line


class InitBase(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, is_lock: bool):
        pass

    @abstractmethod
    def random(self, line_size) -> List[Line]:
        pass
