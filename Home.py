import streamlit as st
from source.pages.header import *
from config import *
from utils.functions import *
from PIL import Image

st.set_page_config(
         page_title="ARBO AFRICA DASHBOARD",
         layout="wide",
         initial_sidebar_state="expanded",
         page_icon="img/cropped-ceri_branco-01-150x150.png"
     )


page_style = """
<style>
 .main {
    opacity: 0.8;
    background-size: cover;
    align: center;
    justify: center;
 }
 [data-testid="stHeader"] {
   background-color: rgba(0,0,0,0)
 }
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

page_title = """
  <div>
      <h1 style="color: #195CA9; margin-top: 0; margin: 0 0 0 0; padding: 0 0 0 0;">CLIMADE AFRICA DASHBOARD</h1>
      <strong style="color:green">Interpret this data with care</strong>
  </div>
  <br/>
"""
 
page_infos = """
  <div>
      <strong>INFO</strong>
      <p>The data displayed on the dashboard is sourced from <a href='https://www.bv-brc.org/'>BV-BRC</a></p>
  </div>
  <br/>
"""
 
page_reference = """
  <div>
      <strong>CITE US:</strong>
      <p>Xavier, J.S., Moir, M., Tegally, H., Sitharam, N. et al. SARS-CoV-2 Africa dashboard for real-time COVID-19 information. Nat Microbiol 8, 1–4 (2023). https://doi.org/10.1038/s41564-022-01276-9</p>
  </div>
  <br/>
"""
 
page_contacts = """
  <div>
      <strong>CONTACT US:</strong>
      <ul>
          <li>Joicy Xavier: <a>joicy.xavier@ufvjm.edu.br</a></li>
      </ul>
  </div>
"""
 
with st.container():
  col1, col2 = st.columns((2,1))

  with col1:

    col1_style = """
        <style>
            div[data-testid="column"]:nth-of-type(1)
            {
              border-bottom: 2px solid grey;
              padding: 0 2em 2em 0;
            } 
        </style>
    """

    st.markdown(col1_style,unsafe_allow_html=True)
    st.markdown(page_title, unsafe_allow_html=True)
    st.markdown(page_infos, unsafe_allow_html=True)
    st.markdown(page_reference, unsafe_allow_html=True)
    st.markdown(page_contacts, unsafe_allow_html=True)

  with col2:
      
    bg = get_base64_of_bin_file("img/bg2.png")

    col2_style = """
      <style>
          div[data-testid="column"]:nth-of-type(2)
              {
                text-align: center;
                align: center;
                background-image: url("data:image/png;base64,%s");
                background-size: cover;
              } 
      </style>
      """% bg
    
    st.markdown(col2_style,unsafe_allow_html=True)
 


st.markdown(css_changes, unsafe_allow_html=True)
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
st.sidebar.success("Select an arbovirus above.")