import numpy as np

from abc import abstractmethod

from implementation.relation_matrix.i_matrix import IMatrix
from implementation.relation_matrix.util import filter_row


class ILoopMatrix(IMatrix):
    def __init__(self,
                 processes=None,
                 loops_threshold=0):

        super().__init__(processes, dtype=np.float64)
        self._loops_threshold = loops_threshold

    @property
    def loops_threshold(self):
        return self._loops_threshold

    def set_loops_threshold(self, loops_threshold):
        self._loops_threshold = loops_threshold

    @abstractmethod
    def length_loops(self):
        pass

    @abstractmethod
    def length_loops_normalize(self):
        pass

    def with_threshold(self):
        matrix = self.length_loops_normalize()
        for row in matrix:
            filter_row(row, row >= self.loops_threshold)
        return matrix

    def update(self):
        self._matrix = self.length_loops()
        self._matrix = self.length_loops_normalize()
        self._matrix = self.with_threshold()
