import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


data = pd.read_csv('ds4200_final_project/college_admissions.csv')
'''
Interactive Visualization 1: Interactive Scatterplot
    Plots different tiers of colleges against income bin of attendees, allows users to examine each specific tier on its own.
'''

options = [None, 'Highly selective private', 'Highly selective public', 'Ivy Plus', 'Other elite schools (public and private)', 
           'Selective private', 'Selective public']
labels = ['All', 'Highly selective private', 'Highly selective public', 'Ivy Plus', 'Other elite schools (public and private)', 
           'Selective private', 'Selective public']

# selection options
input_radio = alt.binding_radio(options = options, labels = labels, name = 'School Tier: ')
selection = alt.selection_point(fields = ['tier'], bind = input_radio)

#plot
scattertier = alt.Chart(data).mark_point().encode(
    alt.Y('rel_apply:Q', title = 'Application Rate', scale=alt.Scale(domain=[data['rel_apply'].min(), data['rel_apply'].max()])),
    alt.X('par_income_bin:N', title = 'Income Bracket'),
    alt.Color('tier'),
    alt.Tooltip(['tier', 'par_income_bin'])
).properties(title = 'Application Rate and Income Bin', width = 500, height = 500).add_params(
    selection).transform_filter(selection)


scattertier.show()


