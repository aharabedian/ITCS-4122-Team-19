import streamlit as st
from pycaret.classification import load_model, predict_model, setup
from pandas import DataFrame

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