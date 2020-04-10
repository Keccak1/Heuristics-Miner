import numpy as np

from implementation.relation_matrix.util import filter_row, set_on_index, matrix_on
from implementation.relation_matrix.i_matrix import IMatrix


class DirectDependencyMatrix(IMatrix):

    def __init__(self,
                 processes=None,
                 dependency_threshold=0,
                 relative_to_best_threshold=0,
                 all_task_connected=True,
                 dtype=np.float64):

        self._dependency_threshold = dependency_threshold
        self._relative_to_best_threshold = relative_to_best_threshold
        self._all_task_connected = all_task_conSnected
        super().__init__(processes, datatype=np.float64)

    @property
    def dependency_threshold(self):
        return self._dependency_threshold

    @property
    def relative_to_best(self):
        return self._relative_to_best_threshold

    @property
    def all_task_connected(self):
        return self._all_task_connected

    @classmethod
    def from_log(cls,
                 log,
                 dependency_threshold=0,
                 relative_to_best_threshold=1,
                 all_task_connected=True):

        return cls(log.processes,
                   dependency_threshold,
                   relative_to_best_threshold,
                   all_task_connected)

    @staticmethod
    def direct_dependency_value(T1fT2, T2fT1):
        return (T1fT2-T2fT1)/(T1fT2+T2fT1+1)

    @staticmethod
    def calculate_relative_to_best_threshold(row, relative_to_best_threshold):
        return np.max(row)*(1-relative_to_best_threshold)

    def set_dependency_threshold(self, dependency_threshold):
        self._dependency_threshold = dependency_threshold

    def set_relative_to_best_threshold(self, relative_to_best_threshold):
        self._relative_to_best_threshold = relative_to_best_threshold

    def set_all_task_connected(self, all_task_connected):
        self._all_task_connected = all_task_connected

    def update_matrix(self):
        self._matrix = self.with_thresholds()

    def direct_dependency_instances(self):
        matrix = self._reset_matrix()
        if self._processes:
            for process in self._processes:
                for i in range(len(process.activities)-1):
                    following_activity_idx = self.get_index(
                        process.activities[i])
                    followed_activity_idx = self.get_index(
                        process.activities[i+1])
                    matrix[following_activity_idx][followed_activity_idx] += 1
        return matrix

    def direct_dependency_normalize(self):
        instances_matrix = self.direct_dependency_instances()
        matrix = self._reset_matrix()
        if instances_matrix.any():
            for idx, _ in np.ndenumerate(instances_matrix):
                T1fT2 = matrix_on(instances_matrix, idx)
                T2fT1 = matrix_on(instances_matrix, list(reversed(idx)))
                val = DirectDependencyMatrix.direct_dependency_value(
                    T1fT2, T2fT1)
                set_on_index(matrix, idx, val)
        return matrix

    def with_thresholds(self):
        matrix = self.direct_dependency_normalize()
        if matrix.any():
            matrix = self.with_dependency_threshold()
            matrix = self.with_relative_to_best_threshold()
        return matrix

    def with_dependency_threshold(self):
        matrix = self.direct_dependency_normalize()
        if matrix.any():
            for row in matrix:
                if self._all_task_connected and np.max(row) <= self._dependency_threshold:
                    filter_row(row, row >= np.max(row))
                else:
                    filter_row(row, row >= self._dependency_threshold)
        return matrix

    def with_relative_to_best_threshold(self):
        matrix = self.with_dependency_threshold()
        if matrix.any():
            for row in matrix:
                filter_row(row, row >= DirectDependencyMatrix.calculate_relative_to_best_threshold(
                    row, self._relative_to_best_threshold))
        return matrix
