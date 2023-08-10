import streamlit as st
import pandas as pd
import io
import base64


if "datafile" not in st.session_state:
   st.session_state["datafile"] = True
if "network" not in st.session_state:
   st.session_state["network"] = True
if "profile" not in st.session_state:
   st.session_state["profile"] = True
if "funddata" not in st.session_state:
   st.session_state["funddata"] = True
if "periodes" not in st.session_state:
   st.session_state["periodes"] = True
if "personal_information" not in st.session_state:
   st.session_state["personal_information"] = True
if 'risk_score' not in st.session_state:
   st.session_state['risk_score'] = True

st.session_state["datafile"] = "Sources - PowerBI Dashboard - GPD_SSD_VMD RandomData.xlsx"


def personal_information():
    # Create a form and display the form
    name =  st.text_input("Nom")
    occupation = st.text_input("Occupation") 
    age = st.number_input("Age") 
    address = st.text_area("Adresse")    

# Define question function
def ask_question(question):
    choice = st.radio(question['text'], question["choices"])
    return choice, question['score'][question["choices"].index(choice)]

# Define questionnaire function
def questionnaire(questions):
    st.write("Please answer the following questions to assess your risk level.")
    risk_level = 0
    for i, question in enumerate(questions.values()):
        print(i)
        choice, score = ask_question(question)
        risk_level += score
    return risk_level


   # Every form must have a submit button.

def get_excel_bytes(df):
    # Create a downloadable Excel file from the DataFrame
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.read()


    # Download Button

def risk_score_comment(risk_level):
    if risk_level <= 5:
        mandat = "A"
        riskdis = "80/20"
    elif (risk_level > 5) & (risk_level<=7):
        mandat = "B"
        riskdis = "70/20"
    elif (risk_level > 7) & (risk_level<=9):
        mandat = "C"
        riskdis = "60/40"
    elif (risk_level > 9) & (risk_level<=12):
        mandat = "D"
        riskdis = "50/50"   
    elif (risk_level > 12) & (risk_level<=13):
        mandat = "E"    
        riskdis = "40/60"
    elif (risk_level ==14):
        mandat = "F"
        riskdis = "30/70"
    elif (risk_level ==15):
        mandat = "G"
        riskdis = "20/80"
    elif (risk_level ==16):
        mandat = "H"
        riskdis = "10/90"
    elif (risk_level ==17):
        mandat = "I"
        riskdis = "0/100"   
    risk_level_str = f"Ton niveau de risque est: {risk_level}. Cette niveau de risque coresponde a un portefeuille de fonds privés d'un mandat {mandat}. Cette mandat a un composition de risk de {riskdis}."
    return risk_level_str

# Define page title and description

# Add the logo image file in the same directory as your script
logo_path = "media/desj.png"

# Create a container to hold the logo and header
header_container = st.container()

# Add the logo to the container
with header_container:
    logo_col, header_col = st.columns([1, 3])
    logo_col.image(logo_path, use_column_width=True)

    # Add the header text
    header_col.markdown("<h1 style='text-align: center;'>InvestMenTora </h1>", unsafe_allow_html=True)
    header_col.markdown("<h2 style='text-align: center;'>Information Personelle </h2>", unsafe_allow_html=True)

st.write("---")  # Horizontal line for visual separation
  
questions = {
    "Question 1": {
        "text": "What is your investment experience?",
        "choices": ["No experience", "Limited experience", "Moderate experience", "Extensive experience"],
        "score":[4,3,2,1]
    },
    "Question 2": {
        "text": "What is your investment goal?",
        "choices": ["Preservation of capital", "Income", "Growth", "Aggressive growth"],
        'score':[1,2,3,4],
    },
    "Question 3": {
        "text": "What is your investment time horizon?",
        "choices": ["Less than 1 year", "1-5 years", "5-10 years", "More than 10 years"],
        "score":[4,3,2,1],
    },
    "Question 4": {
        "text": "What is your risk tolerance?",
        "choices": ["Very low", "Low", "Moderate", "High", "Very high"],
        'score':[1,2,3,4,5],
    }
}


personal_info =  st.checkbox("Voulez-vous mettre les informations personnelles?")
with st.form("Personal Information"):
   # Define questions and choices

    if personal_info:
        personal_information()
    
    risk_level = questionnaire(questions)
    submitted = st.form_submit_button("Submit")

    if submitted:
        st.write(risk_score_comment(risk_level))
        if personal_info:
            personal_information = pd.DataFrame(columns = ['Name', 'Occupation', 'Age', 'Address'], data = [[name, occupation, age, address]])
            st.session_state["personal_information"] = personal_information
            st.download_button("Download", get_excel_bytes(st.session_state["personal_information"]), "Information Personelle - %s .xlsx" %name)
