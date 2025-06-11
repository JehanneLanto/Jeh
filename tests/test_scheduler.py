import pandas as pd
from scheduler import solve_schedule

def test_no_overlap():
    df = pd.read_csv("sample_courses.csv")
    sol = solve_schedule(df)
    # pas deux cours même slot
    times = [(s['day'], s['start'], s['end']) for s in sol]
    assert len(times) == len(set(times))
