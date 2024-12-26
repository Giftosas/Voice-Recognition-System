import streamlit as st
from funcs import open_picture

st.set_page_config(
    page_title='The team',
    layout='centered',
    page_icon='👥',
    initial_sidebar_state="auto"
)

st.title("Meet the team")

team2_image = open_picture("Gift.jpg")
team3_image = open_picture("homepage.webp")
linked = open_picture("linkedin.png")

col1, col2 = st.columns(2)
# Gift
with col1:
    st.markdown(f'<img style="border: 2px solid black" src="data:image/jpeg;base64,{open_picture("Gift.jpg")}" width="80%" height="30%"><br><br>',
                unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    ### Osariemen Gift Omokpamwan 
    <p><b style="font-size:100%">TEAM LEAD:</b> Guided, motivated, and coordinated my team to achieve our project 
    goals efficiently while ensuring effective communication and resolving challenges.</p>
    
    <a href="https://www.linkedin.com/in/osariemen-omokpamwan-6a9938142">
    <img src="data:image/jpeg;base64,{open_picture("linkedin.png")}" width="10%" height="10%"></a>
    
    <a href="https://github.com/Giftosas">
    <img src="data:image/jpeg;base64,{open_picture("github.png")}" width="10%" height="10%"></a>
    
    """, unsafe_allow_html=True)

# Kamsi
col1a, col2a = st.columns(2)
with col1a:
    st.markdown(f'<img style="border: 2px solid powderblue" src="data:image/jpeg;base64,{open_picture("kamsi.jpg")}" width="80%" height="30%"><br><br>',
                unsafe_allow_html=True)

with col2a:
    st.markdown(f"""
    ### Okorafor Kamsi Emmanuel 
    <p><b style="font-size:100%">DEVELOPER:</b> Built this beauty.</p>
    
    <a href="https://www.linkedin.com/in/kamsi-okorafor-bab167195">
    <img src="data:image/jpeg;base64,{open_picture("linkedin.png")}" width="10%" height="10%"></a>
    
    <a href="https://x.com/iamkhamzi">
    <img src="data:image/jpeg;base64,{open_picture("X.png")}" width="10%" height="10%"></a>
    """, unsafe_allow_html=True)

# Lypha
col1b, col2b = st.columns(2)
with col1b:
    st.markdown(f'<img src="data:image/jpeg;base64,{team3_image}" width="80%" height="30%"><br><br>',
                unsafe_allow_html=True)

with col2b:
    st.markdown("""
    ### Ogundeko Oluwaseun Emmanuel
    ### Role:
    Team Lead, delegation and management""", unsafe_allow_html=True)
