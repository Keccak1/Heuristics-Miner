from .relation_matrix.long_distance_dependency import LongDistanceDependencyMatrix
from .relation_matrix.loops_matrix.one_length_loop_relation import OneLengthLoopMatrix
from .relation_matrix.loops_matrix.two_length_loop_relation import TwoLengthLoopMatrix
from .relation_matrix.direct_dependency import DirectDependencyMatrix


class HeuristicsMinner:
    def __init__(self,
                 processes=None,
                 dependency_threshold=0,
                 relative_to_best_threshold=0,
                 all_task_connected=True,
                 one_loops_threshold=0,
                 two_loops_threshold=0,
                 long_distance_threshold=0):

        self._processes = processes
        self._dependency_threshold = dependency_threshold
        self._relative_to_best_threshold = relative_to_best_threshold
        self._all_task_connected = all_task_connected
        self._one_loops_threshold = one_loops_threshold
        self._two_loops_threshold = two_loops_threshold
        self._long_distance_threshold = long_distance_threshold

        self._direct_dependency_matrix = None
        self._long_distance_matrix = None
        self._one_loops_matrix = None
        self._two_loops_matrix = None

        if self._processes:
            self.update()

    @property
    def proceses(self):
        return self._processes

    @property
    def dependency_threshold(self):
        return self._dependency_threshold

    @property
    def relative_to_best_threshold(self):
        return self._relative_to_best_threshold

    @property
    def all_task_connected(self):
        return self._all_task_connected

    @property
    def one_loops_threshold(self):
        return self._one_loops_threshold

    @property
    def two_loops_threshold(self):
        return self._two_loops_threshold

    @property
    def long_distance_threshold(self):
        return self._long_distance_threshold

    @property
    def direct_dependency_matrix(self):
        return self._direct_dependency_matrix

    @property
    def long_distance_matrix(self):
        return self._long_distance_matrix

    @property
    def one_loops_matrix(self):
        return self._one_loops_matrix

    @property
    def two_loops_matrix(self):
        return self._two_loops_matrix

    def set_processes(self, processes):
        self._processes = processes

    def set_dependency_threshold(self, dependecy_threshold):
        self._dependency_threshold = dependecy_threshold

    def set_relative_to_best_threshold(self, relative_to_best_threshold):
        self._relative_to_best_threshold = relative_to_best_threshold

    def set_all_task_connected(self, all_task_connected):
        self._all_task_connected = all_task_connected

    def set_direct_dependecy_matrix_params(self,
                                           dependecy_threshold,
                                           relative_to_best_threshold,
                                           all_task_connected):

        self.set_dependency_threshold(dependecy_threshold)
        self.set_relative_to_best_threshold(relative_to_best_threshold)
        self.set_all_task_connected(all_task_connected)

    def set_one_length_loops_threshold(self, loop_threshold):
        self._one_loops_threshold = loop_threshold

    def set_two_length_loops_threshold(self, loop_threshold):
        self._two_loops_threshold = loop_threshold

    def set_long_distance_threshold(self, long_distance_threshold):
        self._long_distance_threshold = long_distance_threshold

    @classmethod
    def from_log(cls, log,
                 dependency_threshold=0,
                 relative_to_best_threshold=0,
                 all_task_connected=True,
                 one_loops_threshold=0,
                 two_loops_threshold=0,
                 long_distance_threshold=0):

        return cls(log.processes,
                   dependency_threshold,
                   relative_to_best_threshold,
                   all_task_connected,
                   one_loops_threshold,
                   two_loops_threshold,
                   long_distance_threshold)

    def _long_distance_matrix_params_changed(self):
        if self._long_distance_matrix:
            processes_changed = self._processes != self._long_distance_matrix.processes
            long_distance_threshold_changed = self._long_distance_threshold != self._long_distance_matrix.long_distance_threshold
            return processes_changed or \
                long_distance_threshold_changed

        return True

    def _direct_dependency_matrix_params_changed(self):
        if self._direct_dependency_matrix:
            processes_changed = self._processes != self._direct_dependency_matrix.processes
            direct_dependency_threshold_changed = self._dependency_threshold != self._direct_dependency_matrix.dependency_threshold
            relative_to_best_threshold_changed = self._relative_to_best_threshold != self._direct_dependency_matrix._relative_to_best_threshold
            all_task_connected_changed = self._all_task_connected != self._direct_dependency_matrix.all_task_connected

            return processes_changed or \
                direct_dependency_threshold_changed \
                or relative_to_best_threshold_changed \
                or all_task_connected_changed

        return True

    def _one_loops_matrix_params_changed(self):
        if self._one_loops_matrix:
            processes_changed = self._processes != self._one_loops_matrix.processes
            threshold_changed = self._one_loops_threshold != self._one_loops_matrix.loops_threshold
            return processes_changed or \
                threshold_changed

        return True

    def _two_loops_matrix_params_changed(self):
        if self._two_loops_matrix:
            processes_changed = self._processes != self._two_loops_matrix.processes
            threshold_changed = self._two_loops_threshold != self._two_loops_matrix.loops_threshold
            return processes_changed or threshold_changed \
                or self._two_loops_matrix is None

        return True

    def update(self):
        if self._processes:
            if self._long_distance_matrix_params_changed():
                self.update_long_distance_matrix()

            if self._direct_dependency_matrix_params_changed():
                self.update_direct_dependency_matrix()

            if self._one_loops_matrix_params_changed():
                self.update_one_length_loops_matrix()

            if self._two_loops_matrix_params_changed():
                self.update_two_length_loops_matrix()

    def update_long_distance_matrix(self):
        self._long_distance_matrix = LongDistanceDependencyMatrix(self._processes,
                                                                  self._long_distance_threshold)

    def update_direct_dependency_matrix(self):
        self._direct_dependency_matrix = DirectDependencyMatrix(self._processes,
                                                                self._dependency_threshold,
                                                                self._relative_to_best_threshold,
                                                                self._all_task_connected)

    def update_one_length_loops_matrix(self):
        self._one_loops_matrix = OneLengthLoopMatrix(self._processes,
                                                     self._one_loops_threshold)

    def update_two_length_loops_matrix(self):
        self._two_loops_matrix = TwoLengthLoopMatrix(self._processes,
                                                     self._two_loops_threshold)
