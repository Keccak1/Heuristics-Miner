from implementation.relation_matrix.util import filter_row
from implementation.relation_matrix.imatrix import IMatrix
import numpy as np


class DirectDependencyMatrix(IMatrix):

    def __init__(self,
                 processes=None,
                 dependency_threshold=0,
                 relative_to_best_threshold=0,
                 all_task_connected=True):

        super().__init__(processes)
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

    def set_dependency_threshold(self, dependency_threshold):
        self._dependency_threshold = dependency_threshold

    def set_relative_to_best(self, relative_to_best):
        self._relative_to_best = relative_to_best

    def set_all_task_connected(self, all_task_connected):
        self._all_task_connected = all_task_connected

    def fill_matrix(self, processes):
        self.count_dependency_instances(processes)
        self.normalize_matrix()
        self.__check_thresholds()

    def count_dependency_instances(self, processes):
        for process in processes:
            for i in range(len(process.activities-1)):
                following_activity_idx = self.get_index(process.activities[i])
                followed_activity_idx = self.get_index(process.activities[i+1])
                self._matrix[following_activity_idx][followed_activity_idx] += 1

    def normalize_matrix(self):
        for idx, _ in np.ndenumrate(self._matrix):
            T1fT2, T2fT1 = self[idx], self[reversed(idx)]
            v = DirectDependencyMatrix.direct_dependency_value(T1fT2, T2fT1)
            self.__set_on_index(idx, v)

    @staticmethod
    def direct_dependency_value(T1fT2, T2fT1):
        return (T1fT2-T2fT1)/(T1fT2+T2fT1+1)

    @staticmethod
    def calculate_relative_to_best_threshold(row, relative_to_best_threshold):
        return np.max(row)*(1-relative_to_best_threshold)

    def __check_thresholds(self):
        self.__check_dependency_threshold()
        self.__check_relative_to_best_threshold

    def __check_dependency_threshold(self):
        for row in self._matrix:
            if self._all_task_connected and np.max(row) <= self._dependency_threshold:
                filter_row(row, row >= np.max(row))
            else:
                filter_row(row, row >= self._dependency_threshold)

    def __check_relative_to_best_threshold(self):
        for row in self._matrix:
            filter_row(row, DirectDependencyMatrix.calculate_relative_to_best_threshold(
                row, self._relative_to_best_threshold))
