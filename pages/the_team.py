import streamlit as st
from project_functions import open_picture

st.set_page_config(
    page_title='The team',
    layout='centered',
    page_icon='👥',
    initial_sidebar_state="auto"
)

st.title("Meet the team")

team1_image = open_picture("IMG_5767.jpg")
team2_image = open_picture("IMG_5767.jpg")
team3_image = open_picture("homepage.webp")

col1, col2 = st.columns(2)
with col1:
    st.markdown(f'<img src="data:image/jpeg;base64,{team1_image}" width="80%" height="30%"><br><br>',
                unsafe_allow_html=True)

with col2:
    st.markdown("""
    ### Ogundeko Oluwaseun Emmanuel
    <p><b style="font-size:130%">Role:</b> Team Lead, delegation and management</p>
    <p><b>About:</b> Oluwaseun is a seasoned AI prompter with strength in firebrick</p>
    <br>Socials:<br>
    <a href="Linkedin">LinkedIn</a><br><a href="IG">Instagram</a>""", unsafe_allow_html=True)

col1a, col2a = st.columns(2)
with col1a:
    st.markdown(f'<img src="data:image/jpeg;base64,{team2_image}" width="80%" height="30%"><br><br>',
                unsafe_allow_html=True)

with col2a:
    st.markdown("""
    ### Ogundeko Oluwaseun Emmanuel
    ### Role:
    Team Lead, deligation and management""", unsafe_allow_html=True)

col1b, col2b = st.columns(2)
with col1b:
    st.markdown(f'<img src="data:image/jpeg;base64,{team3_image}" width="80%" height="30%"><br><br>',
                unsafe_allow_html=True)

with col2b:
    st.markdown("""
    ### Ogundeko Oluwaseun Emmanuel
    ### Role:
    Team Lead, deligation and management""", unsafe_allow_html=True)

