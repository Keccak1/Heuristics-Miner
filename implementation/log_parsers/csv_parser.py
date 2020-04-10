import pandas as pd
from .util import _2dt
from .dt_type import DtType
from implementation.process_mining_base import Log, ProcessInstance, ProcessEvent


def from_csv(f, case_column, activity_column, dt_column, dt_type, dt_pattern="", name=""):
    l = Log(name)
    df = pd.read_csv(f).sort_values(by=[dt_column])
    for _, row in df.iterrows():
        case_id = row[case_column]
        pe = ProcessEvent(activity=row[activity_column],
                          datetime=_2dt(dt=row[dt_column],
                                        dt_type=dt_type,
                                        pattern=dt_pattern))
        
        l.add_process_event(case_id, pe)
    return l
