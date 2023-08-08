import pandas as pd
import streamlit as st

import streamlit as st
st.set_page_config(page_title="InvestMenTora", page_icon=":robot_face:", layout='wide')
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


#Sidebar contents
st.sidebar.title("Sidebar")



import streamlit as st

def main():
    # Add custom CSS styles
   st.markdown(
        """
        <style>
        /* Add your custom CSS styles here */
        .custom-header {
            font-size: 24px;
            color: #007bff;
            margin-bottom: 16px;
        }
        .section {
            background-color: #f7f7f7;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True, )

    # Title and Introduction
    #Page Titles
   



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
      header_col.markdown("<h2 style='text-align: center;'>Outil d'analyse et automatisation </h2>", unsafe_allow_html=True)

   st.write("---")  # Horizontal line for visual separation

   # Overview Section

   overview_html = f"""<div class="section">
   <div class="custom-header">Aperçu</div>
   <p>InvestMenTora est un outil d'analyse et d'automatisation qui permet aux gestionnaires de portefeuille de gérer leurs portefeuilles de fonds privés. Cette série d'applications est destinée à illustrer les progrès de l'IA et de l'automatisation dans les activités quotidiennes d'un GP.</p>
   </div>"""

   st.markdown(overview_html, unsafe_allow_html=True)
   st.write("---")  # Horizontal line for visual separation
   guide_html = f"""<div class="section">
   <div class="custom-header">Guide</div>
   <p>Étape 1 : Téléchargez vos données. Si vous souhaitez utiliser un ensemble de valeurs générées aléatoirement pour chacun des mandats privés de GPD, veuillez cocher la case ci-dessous. </p> </div>"""
   st.markdown(guide_html, unsafe_allow_html=True)

   randomdata = st.checkbox("Voulez-vous utiliser des données aléatoires?")

   if randomdata:
      st.session_state["datafile"] = "Sources - PowerBI Dashboard - GPD_SSD_VMD RandomData.xlsx"
   else:
      st.session_state["datafile"] = st.sidebar.file_uploader("Please upload an excel file: ", type=['xlsx'])

   GPD = st.checkbox("Voulez-vous continuer avec les mandats GPD? ")
  

   if GPD:
      guide = st.radio("Voulez-vous etre guider? ", ("J'ai besoin d'etre guider", "Je veux choisir moi meme mes mandats"))
      #Guide = st.checkbox("Voulez-vous etre guider? ")
      if GPD and guide:
         st.write("lien vers Questionnaire")
      if GPD and not guide:   
         st.write("lien vers rendements")



if __name__ == "__main__":
   main()





