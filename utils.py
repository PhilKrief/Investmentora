import pandas as pd
import streamlit as st
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
import matplotlib.pyplot as plt
import copy 
from datetime import datetime, timedelta
import requests

def common_elements_investmentora():
    st.set_page_config(page_title="InvestMentora", page_icon=":robot_face:", layout='wide')
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
    if 'mandat' not in st.session_state:    
        st.session_state['mandat'] = True

    st.session_state["datafile"] = "Sources - PowerBI Dashboard - GPD_SSD_VMD RandomData.xlsx"

def page_header(page_title):
   
   # Add the logo image file in the same directory as your script
   logo_path = "media/desj.png"

   # Create a container to hold the logo and header
   header_container = st.container()

   # Add the logo to the container
   with header_container:
      logo_col, header_col = st.columns([1, 4])
      logo_col.image(logo_path, use_column_width=True)

      # Add the header text
      header_col.markdown("<h1 style='text-align: center;'>InvestMentora </h1>", unsafe_allow_html=True)
      header_text = f"<h2 style='text-align: center;'>{page_title} </h2>"
      header_col.markdown(header_text, unsafe_allow_html=True)
   st.write("---")  # Horizontal line for visual separation