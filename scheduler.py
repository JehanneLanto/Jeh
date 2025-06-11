from __future__ import annotations
import pandas as pd
from ortools.sat.python import cp_model

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def minutes(hhmm: str) -> int:
    h, m = map(int, hhmm.split(":"))
    return h * 60 + m

def solve_schedule(df: pd.DataFrame) -> list[dict]:
    model = cp_model.CpModel()
    section_vars = {}

    # 1. Variables binaires : choisir ou non chaque section
    for idx, row in df.iterrows():
        var = model.NewBoolVar(f"{row.course_code}_{row.section}")
        section_vars[idx] = var

    # 2. Contrainte : choisir exactement 1 section par cours
    for course, group in df.groupby("course_code"):
        model.Add(sum(section_vars[idx] for idx in group.index) == 1)

    # 3. Contrainte : pas de chevauchement temporel
    for i, row_i in df.iterrows():
        for j, row_j in df.iterrows():
            if i >= j:  # éviter doublons
                continue
            same_day = row_i.day == row_j.day
            overlap = (minutes(row_i.start) < minutes(row_j.end)
                       and minutes(row_j.start) < minutes(row_i.end))
            if same_day and overlap:
                model.Add(section_vars[i] + section_vars[j] <= 1)

    # 4. (Optionnel) – objectif : minimiser le # de jours sur le campus
    day_used = {d: model.NewBoolVar(f"used_{d}") for d in DAYS}
    for idx, row in df.iterrows():
        model.Add(day_used[row.day] >= section_vars[idx])
    model.Minimize(sum(day_used[d] for d in DAYS))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status != cp_model.OPTIMAL:
        raise RuntimeError("Aucun horaire faisable trouvé.")
    return [
        df.loc[idx].to_dict()
        for idx in df.index
        if solver.Value(section_vars[idx])
    ]
