from abc import ABCMeta, abstractmethod
from typing import List

from common.value_type import Point, Sample


class GeneratorBase(object, metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def render(self, is_lock: bool):
        pass
    
    @abstractmethod
    def set_data(self, raw_points: List[Point], convex_points: List[Point]):
        pass

    @abstractmethod
    def generate(self, batch_size) -> List[Sample]:
        pass
