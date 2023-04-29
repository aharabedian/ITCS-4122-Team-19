import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
from pycaret.classification import load_model, predict_model, setup
from pandas import DataFrame

st.header("Prediction of Student Dropout Rate By Factor")

tab1, tab2 = st.tabs(["ML Prediction Model", "Charts"])

marital_status = {
    "Single":1,
    "Married":2,
    "Widower":3,
    "Divorced":4,
    "Facto union":5,
    "Legally separated":6,
}

nationality = {
    "Portuguese":1,
    "German":2,
    "Spanish":3,
    "Italian":4,
    "Dutch":5,
    "English":6,
    "Lithuanian":7,
    "Angolan":8,
    "Cape Verdean":9,
    "Guinean":10,
    "Mozambican":11,
    "Santomean":12,
    "Turkish":13,
    "Brazilian":14,
    "Romanian":15,
    "Moldova (Republic of)":16,
    "Mexican":17,
    "Ukrainian":18,
    "Russian":19,
    "Cuban":20,
    "Colombian":21,
}

course = {
    "Biofuel Production Technologies":1,
    "Animation and Multimedia Design":2,
    "Social Service (evening attendance)":3,
    "Agronomy":4,
    "Communication Design":5,
    "Veterinary Nursing":6,
    "Informatics Engineering":7,
    "Equiniculture":8,
    "Management":9,
    "Social Service":10,
    "Tourism":10,
    "Nursing":11,
    "Oral Hygiene":12,
    "Advertising and Marketing Management":13,
    "Journalism and Communication":14,
    "Basic Education":15,
    "Management (evening attendance)":16,
}

gender = {
    "Male":1,
    "Female":2
}

course_schedule = {
    "Daytime":1,
    "Evening":2
}

with st.sidebar:
    debug = st.checkbox("Debug")

yes_no = ["Displaced","Educational special needs","Debtor","Tuition fees up to date","Scholarship holder","International"]

with tab1:
    st.header("Select student parameters")
    st_marital_status = st.selectbox("Marital Status", marital_status)
    st_nationality = st.selectbox("Nationality", nationality)
    st_course = st.selectbox("Course of study", course)
    st_gender = st.selectbox("Gender", gender)
    st_course_schedule = st.selectbox("Course schedule", course_schedule)

    st.subheader("Check the box to indicate yes/no for the following options.")
    st_yes_no = {}
    for option in yes_no:
        st_yes_no[option] = st.checkbox(option, value=False)

    if debug:
        st.write(st_yes_no)

    st.subheader("Enter a value for the following.")

    st_enrollment_age = st.slider("Age at enrollment", 15, 80, 20)
    st_sem1_credits = st.slider("1st Semester Credits Achieved", 0, 20, 12)
    st_sem2_credits = st.slider("2nd Semester Credits Achieved", 0, 20, 12)
    st_unemployment = st.slider("Unemployment rate", 0.0, 20.0, 11.5)
    st_inflation = st.slider("Inflation rate", -1.0, 1.3, 5.0)
    st_gdp = st.slider("GDP", 0.0, 20.0, 11.5)

    # Construct dataframe
    data = {
     'Marital status':marital_status[st_marital_status],
     'Course':course[st_course],
     'Daytime/evening attendance':course_schedule[st_course_schedule],
     'Nacionality':nationality[st_nationality],
     'Displaced':int(st_yes_no['Displaced']),
     'Educational special needs':int(st_yes_no['Educational special needs']),
     'Debtor':int(st_yes_no['Debtor']),
     'Tuition fees up to date':int(st_yes_no['Tuition fees up to date']),
     'Gender':gender[st_gender],
     'Scholarship holder':int(st_yes_no['Scholarship holder']),
     'Age at enrollment':st_enrollment_age,
     'International':int(st_yes_no['International']),
     'Curricular units 1st sem (approved)':st_sem1_credits,
     'Curricular units 2nd sem (approved)':st_sem2_credits,
     'Unemployment rate':st_unemployment,
     'Inflation rate':st_inflation,
     'GDP':st_gdp,
    }

    if debug:
        st.write(data)

    data_df = DataFrame(data, index=[0])
    if debug:
        st.write(data_df)

    # Load model
    model = load_model("saved_dt_model")
    if debug:
        st.write(model)

    prediction = predict_model(model, data_df)
    if debug:
        st.write(prediction)

    st.metric("Prediction", prediction['prediction_label'][0])



st.write("---")

@st.cache
def load_data():
    df = pd.read_csv('PSDAS_dataset.csv')
    return df

df = pd.read_csv('PSDAS_dataset.csv')

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

df['Course_name']=df2['Course']
with tab2:
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
            ('Gender','Marital Status','Nationality', 'Scholarship Holder', 'Dropout')
            )

    if attribute == 'Gender':
        temp=pd.DataFrame()
        temp1=pd.DataFrame(df)
        temp1=df.loc[df['Course_name']==section]
        temp['count']=[temp1['Gender'].value_counts()[0],temp1['Gender'].value_counts()[1]]
        temp['gender']=['female','male']
        fig = px.pie(temp, values='count', names='gender',
                         title='Gender Makeup',
                         height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)

    if attribute == 'Marital Status':
        temp=pd.DataFrame()
        temp1=pd.DataFrame(df)
        temp1=df.loc[df['Course_name']==section]

        temp['status']=['Single','Married','Widower','Divorced','Facto Union','Legally Separated']
        temp['count']=[len(temp1[temp1['Marital status'] == 1]),len(temp1[temp1['Marital status'] == 2]),
                       len(temp1[temp1['Marital status'] == 3]),len(temp1[temp1['Marital status'] == 4]),
                       len(temp1[temp1['Marital status'] == 5]),len(temp1[temp1['Marital status'] == 6])]

        fig = px.pie(temp, values='count', names='status',
                         title='Marital Makeup',
                         height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)

    if attribute == 'Nationality':
        temp=pd.DataFrame()
        temp1=pd.DataFrame(df)
        temp1=df.loc[df['Course_name']==section]

        temp['status']=['Portuguese', 'German', 'Spanish', 'Italian', 'Dutch', 'English', 'Lithuanian', 'Angolan', 'Cape Verdean', 'Guinean', 'Mozambican',                  'Santomean', 'Turkish', 'Brazilian', 'Romanian', 'Moldova (Republic of)', 'Mexican', 'Ukrainian', 'Russian', 'Cuban', 'Colombian']
        temp['count']=[len(temp1[temp1['Nacionality'] == 1]),len(temp1[temp1['Nacionality'] == 2]),
                       len(temp1[temp1['Nacionality'] == 3]),len(temp1[temp1['Nacionality'] == 4]),
                       len(temp1[temp1['Nacionality'] == 5]),len(temp1[temp1['Nacionality'] == 6]),
                       len(temp1[temp1['Nacionality'] == 7]),len(temp1[temp1['Nacionality'] == 8]),
                       len(temp1[temp1['Nacionality'] == 9]),len(temp1[temp1['Nacionality'] == 10]),
                       len(temp1[temp1['Nacionality'] == 11]),len(temp1[temp1['Nacionality'] == 12]),
                       len(temp1[temp1['Nacionality'] == 13]),len(temp1[temp1['Nacionality'] == 14]),
                       len(temp1[temp1['Nacionality'] == 15]),len(temp1[temp1['Nacionality'] == 16]),
                       len(temp1[temp1['Nacionality'] == 17]),len(temp1[temp1['Nacionality'] == 18]),
                       len(temp1[temp1['Nacionality'] == 19]),len(temp1[temp1['Nacionality'] == 20]),
                       len(temp1[temp1['Nacionality'] == 21])]
        fig = px.bar(temp, x="status", y="count",
                     barmode='group', height=400, title = 'Nationality Makeup')
        #fig = px.pie(temp, values='count', names='status',
         #                title='Nationality',
          #               height=300, width=200)
        #fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)

    if attribute == 'Scholarship Holder':
        temp=pd.DataFrame()
        temp1=pd.DataFrame(df)
        temp1=df.loc[df['Course_name']==section]

        temp['count']=[len(temp1[temp1['Scholarship holder'] == 0]),len(temp1[temp1['Scholarship holder'] == 1])]
        temp['gender']=['No Scholarship','Has Scholarship']
        fig = px.pie(temp, values='count', names='gender',
                         title='Scholarship Makeup',
                         height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)

    if attribute == 'Dropout':
        temp=pd.DataFrame()
        temp1=pd.DataFrame(df)
        temp1=df.loc[df['Course_name']==section]

        temp['count']=[len(temp1[temp1['Target'] == 'Dropout']),
                       len(temp1[temp1['Target'] == 'Graduate'])]
        temp['gender']=['Dropout','Graduate']
        fig = px.pie(temp, values='count', names='gender',
                         title='Dropout Rate',
                         height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)
