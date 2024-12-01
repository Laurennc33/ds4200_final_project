import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


data = pd.read_csv('ds4200_final_project/college_admissions.csv')
'''
Static Plot 1: In and Out of State Bar Graphs
    Compares income bracket with attendance to universities in state vs out of state
'''
instate = alt.Chart(data).mark_bar(color='#4E79A7').encode(
    alt.X('par_income_bin:N', title = 'Income Bracket (percentage)'),
    alt.Y('attend_instate:Q', title = 'Attendance Rate')
).properties(title = 'Income Bracket and In State Attendance')

oostate = alt.Chart(data).mark_bar(color='#F28E2B').encode(
    alt.X('par_income_bin:N', title = 'Income Bracket (percentage)'),
    alt.Y('attend_oostate:Q', title = 'Attendance Rate')
).properties(title = 'Income Bracket and Out of State Attendance')

# plot next to each other
state_attend_plot = instate | oostate
state_attend_plot.save('state_attend_plot.png')

