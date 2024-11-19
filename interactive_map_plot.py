import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


data = pd.read_csv('college_admissions.csv')

'''
Interactive Plot 2: Map of Income and College Tier List
'''
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
          'Tufts University': 'MA','University Of Alabama': 'AL','University Of Arkansas': 'AR','University Of California, Berkeley': 'CA',
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

# plot
fig = px.choropleth(
    data, 
    locations = "state",
    locationmode = 'USA-states',
    scope = 'usa',
    color = 'avg_inc', 
    hover_name = 'state', 
    hover_data = 'list',
    color_continuous_scale= 'Viridis'
)
fig.update_layout(title_text='List of College Tiers and Average Household Income by State')

# Save the plot to an HTML file
fig.write_html("map.html")

fig.show()