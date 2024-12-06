'''Final Visualizations Combined'''

import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sns

data = pd.read_csv('college_admissions.csv')

'''Plot 1: Static Box Plot of In State vs Out of State University Attendance by Parent Income'''

instate = alt.Chart(data).mark_boxplot(color='#4E79A7').encode(
    alt.Y('attend_instate:Q', title = 'Attendance Rate Relative to Applications'),
    alt.X('par_income_bin:N', title = 'Income Bracket (%)')
).properties(title = 'Income Bracket and In State Attendance')

oostate = alt.Chart(data).mark_boxplot(color='#F28E2B').encode(
    alt.Y('attend_oostate:Q', title = 'Attendance Rate Relative to Applications'),
    alt.X('par_income_bin:N', title = 'Income Bracket (%)')
).properties(title = 'Income Bracket and Out of State Attendance')
state_attend_plot = instate | oostate
state_attend_plot.save('state_attend_plot.png')

'''Plot 2: Interactive Scatter Plot of University Tiers and Attendance by Parent Income'''
options = [None, 'Highly selective private', 'Highly selective public', 'Ivy Plus', 'Other elite schools (public and private)', 
           'Selective private', 'Selective public']
labels = ['All', 'Highly selective private', 'Highly selective public', 'Ivy Plus', 'Other elite schools (public and private)', 
           'Selective private', 'Selective public']

# selection options
input_radio = alt.binding_radio(options = options, labels = labels, name = 'School Tier: ')
selection = alt.selection_point(fields = ['tier'], bind = input_radio)

# main plot
scattertier = alt.Chart(data).mark_point().encode(
    alt.Y('rel_apply:Q', title = 'Application Rate', scale=alt.Scale(domain=[data['rel_apply'].min(), data['rel_apply'].max()])),
    alt.X('par_income_bin:N', title = 'Income Bracket'),
    alt.Color('tier'),
    alt.Tooltip(['tier', 'par_income_bin'])
).properties(title = 'Application Rate and Income Bin', width = 500, height = 500).add_params(
    selection).transform_filter(selection)

app_boxplot = alt.Chart(data).mark_boxplot().encode(
    alt.Y('rel_apply:Q', title='Application Rate', scale=alt.Scale(domain=[data['rel_apply'].min(), data['rel_apply'].max()])),
    alt.X('tier:N', title='Selected Tier'),
    alt.Color('tier'),
    alt.Tooltip(['tier', 'rel_apply', 'par_income_bin'])
).properties(width = 100, height = 500).transform_filter(selection) 


# Combine scatter plot and box plot horizontally
combined_chart = alt.hconcat(
    scattertier,
    app_boxplot
).resolve_scale(
    y='shared'  # Ensures the Y-axis is consistent between plots
)

combined_chart.save('scattertier.html')



'''Plot 3: Interactive Map of Average Household Income and University Tiers by State'''


states = {'American University': 'DC', 'Amherst College': 'MA', 'Auburn University': 'AL', 'Barnard College': 'NY', 'Bates College': 'ME', 
          'Baylor University': 'TX', 'Binghamton University': 'NY', 'Boston College': 'MA', 'Boston University': 'MA', 
          'Bowdoin College': 'ME', 'Brandeis University': 'MA','Brigham Young University': 'UT', 'Brown University': 'RI', 
          'Bryn Mawr College': 'PA', 'Bucknell University': 'PA','California Institute of Technology': 'CA', 'Carleton College': 'MN', 
          'Carnegie Mellon University': 'PA','Case Western Reserve University': 'OH', 'Claremont McKenna College': 'CA', 
          'Clark University': 'MA', 'Clemson University': 'SC', 'Colby College': 'ME', 'Colgate University': 'NY',
          'College of the Holy Cross': 'MA', 'College of William and Mary': 'VA', 'Colorado School of Mines': 'CO',
          'Columbia University In The City Of New York': 'NY', 'Connecticut College': 'CT', 'Cornell University': 'NY',
          'Dartmouth College': 'NH','Davidson College': 'NC','Duke University': 'NC','Elon University': 'NC','Emory University': 'GA',
          'Florida State University': 'FL','Fordham University': 'NY','Franklin & Marshall College': 'PA',
          'George Washington University': 'DC', 'Georgetown University': 'DC','Georgia Institute Of Technology': 'GA',
          'Gonzaga University': 'WA','Hamilton College': 'NY','Harvard University': 'MA','Haverford College': 'PA',
          'Howard University': 'DC','Johns Hopkins University': 'MD','Kenyon College': 'OH','Lafayette College': 'PA',
          'Lehigh University': 'PA','Loyola Marymount University': 'CA','Macalester College': 'MN','Marquette University': 'WI',
          'Massachusetts Institute Of Technology': 'MA','Michigan State University': 'MI','Middlebury College': 'VT', 
          'New York University': 'NY','North Carolina State University': 'NC','Northeastern University': 'MA',
          'Northwestern University': 'IL','Oberlin College': 'OH','Occidental College': 'CA','Ohio State University': 'OH',
          'Pepperdine University': 'CA','Pomona College': 'CA','Princeton University': 'NJ','Purdue University': 'IN',
          'Reed College': 'OR','Rensselaer Polytechnic Institute': 'NY','Rice University': 'TX','Rutgers, The State University Of New Jersey': 'NJ',
          'Santa Clara University': 'CA','Scripps College': 'CA','Southern Methodist University': 'TX','Stanford University': 'CA',
          'State University Of New York At Buffalo': 'NY','State University Of New York At Stony Brook': 'NY','Swarthmore College': 'PA',
          'Syracuse University': 'NY','Texas A&M University': 'TX','Texas Christian University': 'TX','Trinity College of Hartford, CT': 'CT',
          'Tufts University': 'MA','University Of Alabama': 'AL','University Of Arkansas': 'AK','University Of California, Berkeley': 'CA',
          'University Of California, Davis': 'CA','University Of California, Irvine': 'CA',
          'University Of California, Los Angeles': 'CA','University Of California, Riverside': 'CA',
          'University Of California, San Diego': 'CA','University Of California, Santa Barbara': 'CA','University Of California, Santa Cruz': 'CA',
          'University Of Chicago': 'IL','University Of Connecticut': 'CT','University Of Delaware': 'DE',
          'University Of Florida': 'FL','University Of Georgia': 'GA','University Of Idaho': 'ID','University Of Iowa': 'IA',
          'University Of Kansas': 'KS','University Of Kentucky': 'KY','University Of Miami': 'FL',
          'University Of Michigan - Ann Arbor': 'MI','University Of Mississippi': 'MS','University Of Montana': 'MO',
          'University Of Nevada, Reno': 'NV','University Of New Hampshire': 'NH','University Of New Mexico': 'NM',
          'University Of North Carolina - Chapel Hill': 'NC','University Of North Dakota': 'ND',
          'University Of Notre Dame': 'IN','University Of Oklahoma': 'OK','University Of Oregon': 'OR',
          'University Of Pennsylvania': 'Pennsylvania','University Of Pittsburgh System': 'Pennsylvania','University Of Rhode Island': 'Rhode Island',
          'University Of Richmond': 'VA','University Of Rochester': 'NY','University Of South Florida': 'FL',
          'University Of Southern California': 'CA','University Of Texas At Austin': 'TX','University Of Utah': 'UT',
          'University Of Virginia': 'VA','University Of Wyoming': 'WY','Vanderbilt University': 'TN','Vassar College': 'NY',
          'Villanova University': 'PN','Virginia Polytechnic Institute & State University': 'VA',
          'Wake Forest University': 'NC','Washington And Lee University': 'VA','Washington University In St. Louis': 'MO',
          'Wellesley College': 'MA','Wesleyan University': 'CT','Whitman College': 'WA', 'Williams College': 'MA',
          'Worcester Polytechnic Institute': 'MA','Yale University': 'CT','Yeshiva University': 'NY'}

# add states column
states = pd.DataFrame(states.items(), columns = ['name', 'state'])
data = data.merge(states, on='name')

# read in income data
income = pd.read_csv('MedianHouseholdIncome2015.csv', encoding = 'latin1')

income['Median Income'] = pd.to_numeric(income['Median Income'], errors='coerce')

# add ccolumn for average income by state
avg_inc = income.groupby('Geographic Area')['Median Income'].mean()
incomedf = pd.DataFrame(avg_inc.items(), columns = ['state', 'avg_inc'])

data = data.merge(incomedf, on='state')

# add column of list of tiers by state
tier_ls = data.groupby('state')['tier'].unique()
tier_df = pd.DataFrame({'state':tier_ls.index, 'list':tier_ls.values})

data = data.merge(tier_df, on = 'state')

school_ls = data.groupby('state')['name'].unique()
school_ls_df = pd.DataFrame({'state': school_ls.index, 'school_list': school_ls.values})
school_ls_df['school_list'] = school_ls_df['school_list'].apply(lambda x: ', '.join(x))

data = data.merge(school_ls_df, on = 'state')

def truncate_list(text, max_items=4):
    items = text.split(', ')
    return ', '.join(items[:max_items]) + '...' if len(items) > max_items else text

data['school_list'] = data['school_list'].apply(truncate_list)

sat_tier = {
    'Ivy Plus': '1460-1510',
    'Highly selective private': '1410-1460',
    'Other elite schools (public and private)': '1290-1340', 
    'Highly selective public': '1180-1230',
    'Selective private': '1170-1220',
    'Selective public': '1110-1160'
}

sat_df = pd.DataFrame(list(sat_tier.items()), columns=['tier', 'SATs'])


data = data.merge(sat_df, on='tier')

# plot
fig = px.choropleth(
    data,
    locations='state',
    locationmode='USA-states',
    scope='usa',
    color='avg_inc',
    hover_name='state',
    hover_data={
        'list': True,
        'school_list': True,
        'avg_inc': True,
        'SATs': True
    },
    color_continuous_scale='sunset'
)

fig.update_layout(title_text='List of College Tiers and Average Household Income by State')

# Save the plot to an HTML file
fig.write_html("map.html")



'''Plot 4: Static Bar Chart of Top University Ranks by Combined Score'''


# Create a new column 'rank_score' by combining different factors
# Here, we'll take the average of 'attend', 'attend_sat', and 'rel_apply'
data['rank_score'] = data[['attend', 'attend_sat', 'rel_apply']].mean(axis=1)

# Sort universities based on the 'rank_score'
df_sorted = data[['name', 'rank_score']].sort_values(by='rank_score', ascending=False)

# Assign ranks based on sorted order
df_sorted['rank'] = range(1, len(df_sorted) + 1)

# Limit the plot to the top N universities (e.g., top 20)
top_n = 20
df_top_n = df_sorted.head(top_n)

# Plot the universities based on their rank score (not rank)
plt.figure(figsize=(12, 8))  # Increase figure size for readability
plt.barh(df_top_n['name'], df_top_n['rank_score'], color='skyblue')

# Improve labels and title
plt.xlabel('Combined Rank Score', fontsize=14)
plt.ylabel('University', fontsize=14)
plt.title(f'Top {top_n} Universities Based on Combined Rank Score', fontsize=16)



# Adjust font size for better readability
plt.xticks(fontsize=12)
plt.yticks(fontsize=10)

# Show the plot
plt.tight_layout()  # Ensure everything fits within the plot
plt.savefig('static_university_rank.png')
