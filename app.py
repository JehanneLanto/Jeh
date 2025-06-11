from utils import gantt_dataframe
import streamlit as st
import pandas as pd
from scheduler import solve_schedule
import utils

st.title("CourseScheduler 🗓️")

uploaded = st.file_uploader("Charge un CSV de sections de cours :", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    try:
        solution = solve_schedule(df)
    except RuntimeError as e:
        st.error(str(e))
    else:
        sol_df = pd.DataFrame(solution)
        st.success("Horaire généré ✅")
        st.dataframe(sol_df)

        if st.button("Télécharger .ics"):
            ics = utils.to_ics(sol_df)
            st.download_button(
                label="Download calendar",
                data=ics,
                file_name="schedule.ics",
                mime="text/calendar",
            )
else:
    st.info("💡 Ou essaie le jeu de données d’exemple.")
    if st.button("Utiliser l’exemple"):
        df = pd.read_csv("sample_courses.csv")
        solution = solve_schedule(df)
        st.dataframe(pd.DataFrame(solution))

from utils import gantt_dataframe

if st.checkbox("Afficher le calendrier hebdo 🗓️"):
    gdf = gantt_dataframe(sol_df)
    import plotly.express as px
    fig = px.timeline(
        gdf,
        x_start="StartDT",
        x_end="EndDT",
        y="course_code",
        color="course_code",
        title="Vue hebdomadaire",
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=420, margin=dict(t=40, b=20))
    st.plotly_chart(fig, use_container_width=True)
