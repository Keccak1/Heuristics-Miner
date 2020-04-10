import numpy as np

from functools import reduce
from abc import ABC, abstractmethod

from implementation.process_mining_base import ProcessEvent, ProcessInstance, Log
from ..util import unique_concatenate


class IMatrix(ABC):

    def __init__(self,
                 processes=None,
                 datatype=np.float64):

        self._activities = []
        self._matrix = None
        if processes:
            self.set_processes(processes, datatype=datatype)

    def __getitem__(self, index):
        return self.matrix[index[0]][index[1]]

    def _set_on_index(self, index, val):
        self._matrix[index[0], index[1]] = val

    def _copy_matrix(self):
        return np.copy(self._matrix)

    def _reset_matrix(self):
        return np.full(self._matrix.shape,
                       0,
                       self._matrix.dtype)

    @abstractmethod
    def update_matrix(self):
        pass

    @classmethod
    def from_log(cls, log):
        return cls(log.processes)

    @property
    def matrix(self):
        return self._matrix

    @property
    def activities(self):
        return self._activities

    @property
    def dtype(self):
        return self._matrix.dtype

    def get_index(self, activity):
        try:
            return self.activities.index(activity)
        except ValueError as ve:
            raise ValueError(f"{ve} Activty not exists.")

    def set_processes(self, processes, datatype=np.float64):
        self._processes = processes
        self._activities = sorted(reduce(unique_concatenate,
                                         [p.activities for p in processes]))

        m_size = len(self._activities)
        self._matrix = np.zeros(shape=(m_size, m_size), dtype=datatype)
        self.update_matrix()
