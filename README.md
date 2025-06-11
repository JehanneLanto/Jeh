# CourseScheduler 🗓️

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://courseschedule.streamlit.app)
![CI](https://github.com/JehanneLanto/Jeh/actions/workflows/python.yml/badge.svg)

Optimisation d’emploi du temps :

* Input * : un simple CSV listant les sections de cours  
* Solve * : modèle CP-SAT (Google OR-Tools) 
* Vue Gantt * : calendrier hebdomadaire interactif (Plotly)  
* Export * : génère un fichier *schedule.ics* importable dans Google / Apple Calendar  
* CI/CD * : tests PyTest + GitHub Actions

---

# Démo 

1. Ouvrez la démo ➜ [CourseScheduler](https://courseschedule.streamlit.app)  
2. Cliquez « Utiliser l’exemple » pour charger un set de cours  
3. Téléchargez le document et insérez
4. Cochez « Afficher le calendrier hebdo » – le Gantt apparaît  
5. Téléchargez le `.ics` et importez-le dans ton agenda

