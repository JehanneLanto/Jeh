from icalendar import Calendar, Event
from datetime import datetime, timedelta

def to_ics(sol_df):
    cal = Calendar()
    cal.add('prodid', '-//CourseScheduler//v1//')
    cal.add('version', '2.0')

    for _, row in sol_df.iterrows():
        evt = Event()
        # Construit un datetime (date fictive 2025-09-01 + offset day)
        start = _day_to_date(row['day']) + _time_to_td(row['start'])
        end = _day_to_date(row['day']) + _time_to_td(row['end'])
        evt.add('dtstart', start)
        evt.add('dtend', end)
        evt.add('summary', f"{row['course_code']} – {row['section']}")
        cal.add_component(evt)
    return cal.to_ical()

def _day_to_date(day):
    base = datetime(2025, 9, 1)  # un lundi
    idx = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"].index(day)
    return base + timedelta(days=idx)

def _time_to_td(hhmm):
    h, m = map(int, hhmm.split(":"))
    return timedelta(hours=h, minutes=m)

# ---------- Vue calendrier Plotly ----------
import plotly.express as px

def gantt_dataframe(sol_df):
    """
    Convertit la solution en DataFrame contenant
    StartDT / EndDT (datetime) pour Plotly Timeline.
    """
    from datetime import datetime, timedelta
    base = datetime(2025, 9, 1)          # lundi fictif
    day_idx = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}

    df = sol_df.copy()
    df["StartDT"] = [
        base + timedelta(days=day_idx[d]) +
        timedelta(hours=int(t.split(":")[0]), minutes=int(t.split(":")[1]))
        for d, t in zip(df.day, df.start)
    ]
    df["EndDT"] = [
        base + timedelta(days=day_idx[d]) +
        timedelta(hours=int(t.split(":")[0]), minutes=int(t.split(":")[1]))
        for d, t in zip(df.day, df.end)
    ]
    return df
