# %%
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px

# %%
@st.cache
def load_data():
    df = pd.read_csv('PSDAS_dataset.csv')
    return df

# %%
df = pd.read_csv('PSDAS_dataset.csv')

# %%
course_names = {
    1:"Biofuel Production Technologies",
    2:"Animation and Multimedia Design",
    3:"Social Service (evening attendance)",
    4:"Agronomy",
    5:"Communication Design",
    6:"Veterinary Nursing",
    7:"Informatics Engineering",
    8:"Equiniculture",
    9:"Management",
    10:"Social Service",
    11:"Tourism",
    12:"Nursing",
    13:"Oral Hygiene",
    14:"Advertising and Marketing Management",
    15:"Journalism and Communication",
    16:"Basic Education",
    17:"Management (evening attendance)"
}

df2=df.replace({'Course': course_names})
df2

# %%
temp=pd.DataFrame()
temp['count']=[df['Gender'].value_counts()[0],df['Gender'].value_counts()[1]]
temp['gender']=['female','male']
if st.sidebar.checkbox('Pie Chart of Gender'):
    fig = px.pie(temp, values='count', names='gender',
                     title='Gender Makeup',
                     height=300, width=200)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)


# %%
col1, col2 = st.columns(2)
with col1:
    section = st.selectbox(
        'What Majors would you like to compare?',
        ('Biofuel Production Technologies','Animation and Multimedia Design','Social Service (evening attendance)',
         'Agronomy','Communication Design','Veterinary Nursing','Informatics Engineering','Equiniculture',
         'Management','Social Service','Tourism','Nursing','Oral Hygiene','Advertising and Marketing Management',
         'Journalism and Communication','Basic Education','Management (evening attendance)'))
with col2:
    attribute = st.selectbox(
        'What attributes would you like to look at?',
        ('Gender','Marital Status')
        )

# %%
if attribute == 'Marital Status':
    temp=pd.DataFrame()
    temp1=pd.DataFrame(df)
    temp1=df.loc[df['Course_name'].isin(section)]
    
    temp['status']=['Single','Married','Widower','Divorced','Facto Union','Legally Separated']
    temp['count']=[temp1['Marital status'].value_counts()[1],temp1['Marital status'].value_counts()[2],
                   temp1['Marital status'].value_counts()[3],temp1['Marital status'].value_counts()[4],
                   temp1['Marital status'].value_counts()[5],temp1['Marital status'].value_counts()[6]]

    fig = px.pie(temp, values='count', names='status',
                     title='Marital Makeup',
                     height=300, width=200)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)

# %%
temp=pd.DataFrame()
temp['status']=['Single','Married','Widower','Divorced','Facto Union','Legally Separated']
temp['count']=[df['Marital status'].value_counts()[1],df['Marital status'].value_counts()[2],df['Marital status'].value_counts()[3],
               df['Marital status'].value_counts()[4],df['Marital status'].value_counts()[5],df['Marital status'].value_counts()[6]]
if st.sidebar.checkbox('Pie Chart of Marital Status'):
    fig = px.pie(temp, values='count', names='status',
                     title='Marital Makeup',
                     height=300, width=200)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)


