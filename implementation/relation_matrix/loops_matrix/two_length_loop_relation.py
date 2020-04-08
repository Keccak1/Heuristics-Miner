import numpy as np

from implementation.relation_matrix.util import filter_row
from implementation.relation_matrix.i_matrix import IMatrix


class TwoLengthLoopIterationMatrix(IMatrix):
    def __init__(self,
                 processes=None,
                 loops_threshold=0):

        super().__init__(processes, dtype=np.float64)

    @staticmethod
    def two_length_loops_value(T1fT2, T2fT1):
        return (T1fT2+T1fT2)/(T1fT2+T1fT2+1)

    def length_loops(self):
        matrix = self._reset_matrix()
        if self._processes:
            for process in self._processes:
                for i in range(len(process.activities-2)):
                    if process.activities[i] == process.activities[i+2]:
                        activity_index = self.get_index(process.activities[i])
                        matrix[activity_index][activity_index] += 1
        return matrix

    def two_length_loops_normalize(self):
        matrix = self.length_loops()
        if matrix:
            for idx, _ in np.ndenumrate(matrix):
                T1fT2, T2fT1 = self[idx], self[reversed(idx)]
                value = TwoLengthLoopIterationMatrix.two_length_loops_value(
                    T1fT2, T2fT1)
                self._set_on_index(idx, value)
