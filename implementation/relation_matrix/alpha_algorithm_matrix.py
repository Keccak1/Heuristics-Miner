import numpy as np

from itertools import combinations

from implementation.relation_matrix.i_matrix import IMatrix

INDEPENDANCE = np.int(0)                # #
TEMPORAL_INDEPENDANCE = np.int(2)       # ||
TEMPORAL_DEPENDENCY_RIGHT = np.int(1)   # ->
TEMPORAL_DEPENDENCY_LEFT = np.int(3)    # <-

class AlphaMinnerMatrix(IMatrix):
    def __init__(self, processes=None):
        super().__init__(processes, datatype=np.int)

    def get_relation(self, a, b):
        try:
            a_index = self.get_index(a)
            b_index = self.get_index(b)

        except ValueError as ve:
            raise ValueError(f"{ve} Pair {a,b} does not exists in matrix.")

        return self._matrix[a_index][b_index]

    def update_matrix(self):
        for f_c_num,  f_c in enumerate(self._activities):
            for s_c_num, s_c in enumerate(self._activities):
                rule = AlphaMinnerMatrix.get_rule(f_c, s_c, self._processes)
                self._matrix[f_c_num][s_c_num] = rule

    @staticmethod
    def common_processes(f_a, s_a, processes):
        return [process for process in processes if f_a in process.activities and s_a in process.activities]

    @staticmethod
    def get_rule(f_a, s_a, processes):

        c_processes = AlphaMinnerMatrix.common_processes(f_a, s_a, processes)
        if AlphaMinnerMatrix.is_independance(f_a, s_a, c_processes):
            return INDEPENDANCE

        if AlphaMinnerMatrix.is_temporal_independance(f_a, s_a, c_processes):
            return TEMPORAL_INDEPENDANCE

        if AlphaMinnerMatrix.is_temporal_dependency(f_a, s_a, c_processes):
            return TEMPORAL_DEPENDENCY_RIGHT

        if AlphaMinnerMatrix.is_temporal_dependency(s_a, f_a, c_processes):
            return TEMPORAL_DEPENDENCY_LEFT

    @staticmethod
    def is_independance(f_a, s_a, common_processes):
        result = True
        for process in common_processes:
            f_a_indexes = np.where(np.array(process.activities) == f_a)[0]
            s_a_indexes = np.where(np.array(process.activities) == s_a)[0]
            for f_i in f_a_indexes:
                for s_i in s_a_indexes:
                    result &= abs(f_i - s_i) != 1
        return result

    @staticmethod
    def is_temporal_independance(f_a, s_a, common_processes):
        return AlphaMinnerMatrix.is_temporal_dependency(
            f_a, s_a, common_processes) and AlphaMinnerMatrix.is_temporal_dependency(s_a, f_a, common_processes)

    @staticmethod
    def is_temporal_dependency(f_a, s_a, common_processes):
        result = False
        for process in common_processes:
            f_a_indexes = np.where(np.array(process.activities) == f_a)[0]
            s_a_indexes = np.where(np.array(process.activities) == s_a)[0]
            for f_i in f_a_indexes:
                for s_i in s_a_indexes:
                    result |= f_i+1 == s_i
        return result
