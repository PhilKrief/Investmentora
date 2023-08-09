import streamlit as st
import pandas as pd
import io
import base64


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

def personal_infomration():
    # Create a form and display the form
    name =  st.text_input("Nom")
    occupation = st.text_input("Occupation") 
    age = st.number_input("Age") 
    address = st.text_area("Adresse")    

# Define question function
def ask_question(question):
    st.subheader(question["text"])
    choice = st.radio("", question["choices"])
    return choice, question["score"].index(choice)

# Define questionnaire function
def questionnaire():
    st.write("Please answer the following questions to assess your risk level.")
    risk_level = 0
    for i, question in enumerate(questions.values()):
        choice, score = ask_question(question)
        st.write(score)
    return risk_level


   # Every form must have a submit button.
   
questions = {
    "Question 1": {
        "text": "What is your investment experience?",
        "choices": ["No experience", "Limited experience", "Moderate experience", "Extensive experience"],
        "score":[1,2,3,4]
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

questionnaire()

with st.form("Personal Information"):
   # Define questions and choices


   submitted = st.form_submit_button("Submit")

   if submitted:
       personal_information = pd.DataFrame(columns = ['Name', 'Occupation', 'Age', 'Address'], data = [[name, occupation, age, address]])
       st.session_state["personal_information"] = personal_information



def get_excel_bytes(df):
    # Create a downloadable Excel file from the DataFrame
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return output.read()


    # Download Button
st.download_button("Download", get_excel_bytes(st.session_state["personal_information"]), "Information Personelle - %s .xlsx" %name)

