import numpy as np

from abc import abstractmethod

from implementation.relation_matrix.i_matrix import IMatrix
from implementation.relation_matrix.util import filter_matrix


class ILoopMatrix(IMatrix):
    def __init__(self,
                 processes=None,
                 loops_threshold=0):

        self._loops_threshold = loops_threshold
        super().__init__(processes, datatype=np.float64)

    @property
    def loops_threshold(self):
        return self._loops_threshold

    @abstractmethod
    def length_loops(self):
        pass

    @abstractmethod
    def length_loops_normalize(self):
        pass

    @classmethod
    def from_log(cls, log, loops_threshold=0):
        return cls(log.processes, loops_threshold=loops_threshold)

    def set_loops_threshold(self, loops_threshold):
        self._loops_threshold = loops_threshold

    def with_threshold(self):
        matrix = self.length_loops_normalize()
        if matrix.any():
            return filter_matrix(matrix, matrix >= self.loops_threshold)

    def update_matrix(self):
        self._matrix = self.with_threshold()
