import streamlit as st
import csv
import os
from email.message import EmailMessage
import smtplib
import ssl

# Streamlit page configuration
st.set_page_config(page_title='Asthma Disease Tracker', layout='wide')
st.title('Asthma Disease Dashboard')

st.info(' 👈 Enter the name in the sidebar to save the data')

# Define feature weights based on importance values
feature_weights = {
    'Pains': 0.161170,
    'Tiredness': 0.147855,
    'Runny-Nose': 0.146093,
    'Dry-Cough': 0.140978,
    'Nasal-Congestion': 0.140762,
    'Sore-Throat': 0.131730,
    'Difficulty-in-Breathing': 0.131413
}

# Function to send email alerts
def email_alert(username, date, severity_percentage, symptoms, other_diseases):
    if severity_percentage < 60:
        return  # No need to send an email if severity is below 60%

    email_sender = "99220040028@klu.ac.in"
    email_password = "enil xnjy hgnv msdn"  # Use environment variable for security
    email_recipient = "99220040061@klu.ac.in"
    subject = f"Asthma Alert for {username}"

    body = f"""
Dear Doctor,

I hope this message finds you well.

Symptoms:
- Tiredness: {symptoms['Tiredness']}
- Dry Cough: {symptoms['Dry-Cough']}
- Difficulty in Breathing: {symptoms['Difficulty-in-Breathing']}
- Sore Throat: {symptoms['Sore-Throat']}
- Pains: {symptoms['Pains']}
- Nasal Congestion: {symptoms['Nasal-Congestion']}
- Runny Nose: {symptoms['Runny-Nose']}

Other Reported Diseases: {', '.join(other_diseases)}

Date: {date}
Severity Percentage: {severity_percentage}%

Please review the patient's condition.

Best regards,  
Asthma Alert System
"""

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recipient
    em['Subject'] = subject
    em.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_recipient, em.as_string())
        st.success('Email sent successfully!')
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Function to calculate severity percentage
def calculate_severity_percentage(symptoms):
    severity_percentage = sum(value * feature_weights.get(symptom, 0) for symptom, value in symptoms.items())
    return round(severity_percentage * 100, 2)

# Sidebar for user input
with st.sidebar:
    username = st.text_input("Enter the username: ")
    date = st.date_input("Enter the date:")

# Symptom selection UI
co1, co2, co3 = st.columns(3)
with co1:
    tiredness = st.selectbox('Tiredness', ['Select', 'No', 'Yes'])
    dry_cough = st.selectbox('Dry Cough', ['Select', 'No', 'Yes'])
    difficulty_breathing = st.selectbox('Difficulty in Breathing', ['Select', 'No', 'Yes'])
with co2:
    sore_throat = st.selectbox('Sore Throat', ['Select', 'No', 'Yes'])
    pains = st.selectbox('Pains', ['Select', 'No', 'Yes'])
with co3:
    nasal_congestion = st.selectbox('Nasal Congestion', ['Select', 'No', 'Yes'])
    runny_nose = st.selectbox('Runny Nose', ['Select', 'No', 'Yes'])

# New input for other diseases
other_diseases = st.multiselect(
    'Select any other reported diseases:',
    ['Fever', 'Cold', 'Cough', 'Other']
)

# Convert user inputs to binary values, treating "Select" as "No"
user_input = {key: 1 if value == 'Yes' else 0 for key, value in {
    'Tiredness': tiredness if tiredness != 'Select' else 'No',
    'Dry-Cough': dry_cough if dry_cough != 'Select' else 'No',
    'Difficulty-in-Breathing': difficulty_breathing if difficulty_breathing != 'Select' else 'No',
    'Sore-Throat': sore_throat if sore_throat != 'Select' else 'No',
    'Pains': pains if pains != 'Select' else 'No',
    'Nasal-Congestion': nasal_congestion if nasal_congestion != 'Select' else 'No',
    'Runny-Nose': runny_nose if runny_nose != 'Select' else 'No'
}.items()}

# Buttons
coo1, coo2 = st.columns(2)
with coo1:
    send_email = st.button('Send Email')
with coo2:
    predict_button = st.button('Predict Severity')

# Process actions
severity_percentage = 0
if predict_button:
    if not username:
        st.warning("Please enter a username before predicting severity.")
    else:
        severity_percentage = calculate_severity_percentage(user_input)
        if severity_percentage > 60:
            st.error(f'{severity_percentage}% High risk of Asthma attack! An alert has been sent to the doctor.')
            email_alert(username, date, severity_percentage, user_input, other_diseases)
        else:
            st.info(f'{severity_percentage}% Low risk of Asthma attack.')

if send_email:
    if severity_percentage > 60:
        email_alert(username, date, severity_percentage, user_input, other_diseases)
    else:
        st.warning("Severity is below 60%. Email alert not required.")

# CSV file handling
file_path = 'user_data.csv'
existing_data = []

if os.path.exists(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_data.append(row)

# Update data if prediction was made
if predict_button and username:
    existing_data.append({'Username': username, 'Date': date, 'Severity': severity_percentage})

# Write updated data to CSV
with open(file_path, mode='w', newline='') as file:
    fieldnames = ['Username', 'Date', 'Severity']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(existing_data)
