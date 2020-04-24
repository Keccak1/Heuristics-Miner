import numpy as np

from implementation.relation_matrix.util import filter_row, filter_matrix, set_on_index, matrix_on
from implementation.relation_matrix.i_matrix import IMatrix


class LongDistanceDependencyMatrix(IMatrix):

    def __init__(self,
                 processes=None,
                 long_distance_threshold=0):

        self._long_distance_threshold = long_distance_threshold
        super().__init__(processes, datatype=np.float64)

    @property
    def long_distance_threshold(self):
        return self._long_distance_threshold

    @property
    def instances_vector(self):
        matrix = self.long_distance_dependency_instances()
        if matrix.any():
            return [np.max(row) for row in matrix]

    @classmethod
    def from_log(cls, log, long_distance_threshold=0):
        return cls(log.processes, long_distance_threshold)

    @staticmethod
    def caluclate_long_dlong_distance_value(value_on_index, max_value):
        return value_on_index/(max_value+1)

    def set_long_distance_threshold(self, long_distance_threshold):
        self._long_distance_threshold = long_distance_threshold

    def update_matrix(self):
        self._matrix = self.long_distance_dependency_normalize()

    def long_distance_dependency_instances(self):
        matrix = self._reset_matrix()
        for row_idx, _ in enumerate(self._activities):
            for value_idx in range(row_idx+1, len(self._activities)):
                followed_activity = self._activities[row_idx]
                following_activity = self._activities[value_idx]
                instances_amount = self._count_long_dinstance_dependecy_instances(followed_activity,
                                                                                  following_activity)
                set_on_index(matrix, (row_idx, value_idx),
                             instances_amount)
        return matrix

    def long_distance_dependency_normalize(self):
        matrix = self.long_distance_dependency_instances()
        if matrix.any():
            for idx, _ in np.ndenumerate(matrix):
                max_value = self.instances_vector[idx[0]]
                value = matrix_on(matrix, idx)
                set_on_index(matrix, idx, LongDistanceDependencyMatrix.caluclate_long_dlong_distance_value(
                    value, max_value))
        return matrix

    def with_threshold(self):
        matrix = self.long_distance_dependency_normalize()
        if matrix.any():
            filter_matrix(matrix, matrix >= self._long_distance_threshold)
        return matrix

    def _count_long_dinstance_dependecy_instances(self,
                                                  followed_activity,
                                                  following_activity):
        counter = 0
        for process in self._processes:
            followed_activity_instances = [activity_idx for activity_idx, activity in enumerate(
                process.activities) if activity == followed_activity]
            following_activity_instances = [activity_idx for activity_idx, activity in enumerate(
                process.activities) if activity == following_activity]
            for followed_activity_instance in followed_activity_instances:
                counter += len(list(filter(lambda x: x >
                                           followed_activity_instance, following_activity_instances)))
        return counter
