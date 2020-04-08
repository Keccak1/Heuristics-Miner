import numpy as np

from implementation.relation_matrix.util import filter_row
from implementation.relation_matrix.i_matrix import IMatrix


class DirectDependencyMatrix(IMatrix):

    def __init__(self,
                 processes=None,
                 dependency_threshold=0,
                 relative_to_best_threshold=0,
                 all_task_connected=True,
                 dtype=np.float64):

        super().__init__(processes, dtype)
        self._dependency_threshold = dependency_threshold
        self._relative_to_best_threshold = relative_to_best_threshold
        self._all_task_connected = all_task_connected

    @property
    def dependency_threshold(self):
        return self._dependency_threshold

    @property
    def relative_to_best(self):
        return self._relative_to_best

    @property
    def all_task_connected(self):
        return self._all_task_connected

    @staticmethod
    def direct_dependency_value(T1fT2, T2fT1):
        return (T1fT2-T2fT1)/(T1fT2+T2fT1+1)

    @staticmethod
    def calculate_relative_to_best_threshold(row, relative_to_best_threshold):
        return np.max(row)*(1-relative_to_best_threshold)

    def set_dependency_threshold(self, dependency_threshold):
        self._dependency_threshold = dependency_threshold

    def set_relative_to_best(self, relative_to_best):
        self._relative_to_best = relative_to_best

    def set_all_task_connected(self, all_task_connected):
        self._all_task_connected = all_task_connected

    def set_processes(self, processes):
        super().set_processes(processes, dtype=np.float64)

    def update_matrix(self):
        self._matrix = self.direct_dependency_instances()
        self._matrix = self.direct_dependency_normalize()
        self._matrix = self.with_thresholds()

    def direct_dependency_instances(self):
        matrix = self._reset_matrix()
        if self._processes:
            for process in self._processes:
                for i in range(len(process.activities-1)):
                    following_activity_idx = self.get_index(
                        process.activities[i])
                    followed_activity_idx = self.get_index(
                        process.activities[i+1])
                    matrix[following_activity_idx][followed_activity_idx] += 1
        return matrix

    def direct_dependency_normalize(self):
        matrix = self.direct_dependency_instances()
        if matrix:
            for idx, _ in np.ndenumrate(matrix):
                T1fT2, T2fT1 = self[idx], self[reversed(idx)]
                v = DirectDependencyMatrix.direct_dependency_value(
                    T1fT2, T2fT1)
                self._set_on_index(idx, v)
        return matrix

    def with_thresholds(self):
        matrix = self.direct_dependency_normalize()
        if matrix:
            matrix = self.with_dependency_threshold()
            matrix = self.with_relative_to_best_threshold()
        return matrix

    def with_dependency_threshold(self):
        matrix = self.direct_dependency_normalize()
        if matrix:
            for row in matrix:
                if self._all_task_connected and np.max(row) <= self._dependency_threshold:
                    filter_row(row, row >= np.max(row))
                else:
                    filter_row(row, row >= self._dependency_threshold)
        return matrix

    def with_relative_to_best_threshold(self):
        matrix = self.direct_dependency_normalize()
        if matrix:
            for row in matrix:
                filter_row(row, row >= DirectDependencyMatrix.calculate_relative_to_best_threshold(
                    row, self._relative_to_best_threshold))
        return matrix
