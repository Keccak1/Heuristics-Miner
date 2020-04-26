import numpy as np

from implementation.relation_matrix.util import matrix_on, set_on_index
from implementation.relation_matrix.loops_matrix.i_loop_matrix import ILoopMatrix


class TwoLengthLoopMatrix(ILoopMatrix):

    def __init__(self,
                 processes=None,
                 loops_threshold=0):

        super().__init__(processes, loops_threshold)

    @staticmethod
    def two_length_loops_value(T1fT2, T2fT1):
        return (T1fT2+T1fT2)/(T1fT2+T1fT2+1)

    def length_loops(self):
        matrix = self._reset_matrix()
        if self._processes:
            for process in self._processes:
                for i in range(len(process.activities)-2):
                    if process.activities[i] == process.activities[i+2]:
                        activity_index = self.get_index(process.activities[i])
                        matrix[activity_index][activity_index] += 1
        return matrix

    def length_loops_normalize(self):
        matrix = self.length_loops()
        if matrix.any():
            for idx, _ in np.ndenumerate(matrix):
                T1fT2, T2fT1 = matrix_on(matrix, idx), matrix_on(
                    matrix, tuple(reversed(idx)))
                value = TwoLengthLoopMatrix.two_length_loops_value(
                    T1fT2, T2fT1)
                set_on_index(matrix, idx, value)
        return matrix
