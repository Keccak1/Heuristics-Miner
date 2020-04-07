from functools import reduce
from abc import ABC, abstractmethod

from ..util import unique_concatenate
from implementation.process_mining_base import ProcessEvent, ProcessInstance, Log
import numpy as np


class IMatrix(ABC):

    def __init__(self, processes=None, dtype=np.int):
        self._activities = []
        self._matrix = None
        if processes:
            self.init_matrix(processes, dtype=dtype)


    def __getitem__(self, index):
        return self.matrix[index[0]][index[1]]
    
    def __set_on_index(self, index, val):
        self._matrix[index[0], index[1]] = val
    
    @abstractmethod
    def fill_matrix(self, processes):
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

    def get_index(self, activity):
        try:
            return self.activities.index(activity)
        except ValueError as ve:
            raise ValueError(f"{ve} Activty not exists.")

    def init_matrix(self, processes, dtype=np.int):
        self._activities = sorted(reduce(unique_concatenate,
                                         [p.activities for p in processes]))
        m_size = len(self._activities)
        self._matrix = np.zeros(shape=(m_size, m_size), dtype=dtype)
        self.fill_matrix(processes)
