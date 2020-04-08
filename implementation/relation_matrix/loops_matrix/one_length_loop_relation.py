import numpy as np

from implementation.relation_matrix.loops_matrix.i_loop_matrix import ILoopMatrix


class OneLengthLoopMatrix(ILoopMatrix):
    def __init__(self,
                 processes=None,
                 loops_threshold=0):

        super().__init__(processes, loops_threshold)

    @staticmethod
    def one_length_loops_value(instances_size):
        return instances_size / (instances_size+1)

    def length_loops(self):
        matrix = self._reset_matrix()
        if self._processes:
            for process in self._processes:
                for i in range(len(process.activities-1)):
                    if process.activities[i] == process.activities[i+1]:
                        activity_index = self.get_index(process.activities[i])
                        matrix[activity_index][activity_index] += 1
        return matrix

    def length_loops_normalize(self):
        matrix = self.length_loops()
        if matrix:
            for i in len(matrix):
                loops_size = matrix[i][i]
                value = OneLengthLoopMatrix.one_length_loops_value(loops_size)
                self._set_on_index((i, i), value)
        return matrix
