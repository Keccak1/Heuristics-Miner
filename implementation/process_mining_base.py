from .util import unique_list


class ProcessEvent:
    def __init__(self, activity, datetime):
        self._activity = activity
        self._datetime = datetime

    def __repr__(self):
        return f"activity: {self._activity}, datetime: {self._datetime}"

    @property
    def activity(self):
        return self._activity

    @property
    def datetime(self):
        return self.datetime

    def __gt__(self, pc2):
        return self.datetime > pc2.datetime


class ProcessInstance:
    def __init__(self, case_id):
        self._case_id = case_id
        self._process_events = []

    def __repr__(self):
        data = [f"case: {self._case_id}"]
        data += ["\t"+str(pe) for pe in self._process_events]
        return "\n".join(data)

    @property
    def start_event(self):
        return self._process_events[0] if not self.is_empty() else None

    @property
    def end_event(self):
        return self._process_events[-1] if not self.is_empty() else None

    @property
    def case_id(self):
        return self._case_id

    @property
    def processes_events(self):
        return self._process_events

    @property
    def activities(self):
        return [p.activity for p in self._process_events]

    @property
    def events(self):
        return sorted(self._process_events)

    def is_empty(self):
        return len(self._process_events) == 0

    def add_event(self, process_event):
        self._process_events.append(process_event)


class Log:
    def __init__(self, name):
        self._name = name
        self._processes = []

    @property
    def name(self):
        return self._name

    def __repr__(self):
        data = [f"name: {self.name}"]
        data += ["---\n"+str(p) for p in self._processes]
        return "\n".join(data)

    @property
    def processes(self):
        return self._processes

    def add_process(self, process):
        self.processes.append(process)

    def add_process_event(self, case_id, process_event):
        process_filter = list(
            filter(lambda p: p.case_id == case_id, self.processes))
        if not process_filter:
            process = ProcessInstance(case_id)
            self.add_process(process)
        else:
            process = process_filter[0]

        process.add_event(process_event)
