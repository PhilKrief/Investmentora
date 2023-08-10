import pandas as pd
import streamlit as st
from utils import *

common_elements_investmentora()

def main():
    # Add custom CSS styles
   st.markdown(
        """
        <style>
        /* Add your custom CSS styles here */
        .custom-header {
            font-size: 24px;
            color: #00874E;
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
   
   page_header("Outil d'analyse et automatisation")



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
   st.write("---")  # Horizontal line for visual separation

   GPD = st.checkbox("Voulez-vous continuer avec les mandats GPD? ")
   if GPD:
      guide = st.radio(" ", ("J'ai besoin d'etre guider", "Je veux choisir moi meme mes mandats"), label_visibility="hidden")
      if GPD and (guide == "J'ai besoin d'etre guider"):
         st.markdown('<a href="https://investmentora.streamlit.app/Information" target="_self" >Questionnaire</a>', unsafe_allow_html=True)
      if GPD and (guide == "Je veux choisir moi meme mes mandats"):  
         st.markdown('<a href="https://investmentora.streamlit.app/Rendement" target="_self">Comparaison des mandats</a>', unsafe_allow_html=True)



if __name__ == "__main__":
   main()





