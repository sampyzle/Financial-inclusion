import streamlit as st
import joblib
import numpy as np

# Load the financial inclusion model
model = joblib.load('fin_model')  

# Title and description
st.title("Financial Inclusion Predictor")
st.write("Fill in the details below to predict whether a person is likely to have a bank account.")

# Inputs for the model
country = st.selectbox('Country', ['Kenya', 'Rwanda', 'Tanzania', 'Uganda'])
location_type = st.selectbox('Location Type', ['Rural', 'Urban'])
cellphone_access = st.selectbox('Has Cellphone Access', ['No', 'Yes'])
household_size = st.number_input('Household Size', min_value=1, max_value=20, step=1)
age_of_respondent = st.number_input('Age of Respondent', min_value=18, max_value=100, step=1)
gender_of_respondent = st.selectbox('Gender', ['Female', 'Male'])
relationship_with_head = st.selectbox('Relationship with Head', [
    'Child', 'Head of Household', 'Other non-relative', 'Other relative', 'Parent', 'Spouse'])
marital_status = st.selectbox('Marital Status', [
    'Divorced/Separated', "Don't Know", 'Married/Living Together', 'Single/Never Married', 'Widowed'])
education_level = st.selectbox('Education Level', [
    'No Formal Education', 'Primary Education', 'Secondary Education', 'Vocational/Training', 'Tertiary Education'])
job_type = st.selectbox('Job Type', [
    'Self Employed', 'Government Dependent', 'Formally Employed Private', 'Informally Employed',
    'Formally Employed Government', 'Farming and Fishing', 'Remittance Dependent', 'Other Income', 
    'No Income', "Don't Know/Refused"])

# Encoding categorical inputs
encoded_inputs = np.array([
    {
        'Kenya': 0, 'Rwanda': 1, 'Tanzania': 2, 'Uganda': 3
    }[country],
    {
        'Rural': 0, 'Urban': 1
    }[location_type],
    {
        'No': 0, 'Yes': 1
    }[cellphone_access],
    household_size,
    age_of_respondent,
    0 if gender_of_respondent == 'Male' else 1,
    {
        'Child': 0, 'Head of Household': 1, 'Other non-relative': 2, 'Other relative': 3,
        'Parent': 4, 'Spouse': 5
    }[relationship_with_head],
    {
        'Divorced/Separated': 0, "Don't Know": 1, 'Married/Living Together': 2, 'Single/Never Married': 3, 'Widowed': 4
    }[marital_status],
    {
        'No Formal Education': 0, 'Primary Education': 1, 'Secondary Education': 2, 
        'Vocational/Training': 3, 'Tertiary Education': 4
    }[education_level],
    {
        'Self Employed': 0, 'Government Dependent': 1, 'Formally Employed Private': 2,
        'Informally Employed': 3, 'Formally Employed Government': 4, 'Farming and Fishing': 5,
        'Remittance Dependent': 6, 'Other Income': 7, 'No Income': 8, "Don't Know/Refused": 9
    }[job_type]
]).reshape(1, -1)

# Prediction
if st.button('Predict'):
    prediction = model.predict(encoded_inputs)
    st.write("Prediction:", "Has Bank Account" if prediction[0] == 1 else "Doesn't Have Bank Account")
