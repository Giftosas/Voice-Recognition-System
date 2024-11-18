import streamlit as st

homepage = st.Page("pages/homepage.py", title="Welcome", icon=":material/home:")
new_user_page = st.Page("pages/new_users.py", title="New Users", icon=":material/add_circle:")
team_page = st.Page("pages/the_team.py", title="The team", icon=":material/groups:")
verify_page = st.Page("pages/verify_users.py", title="User Verification", icon=":material/verified_user:")

pg = st.navigation([homepage, new_user_page, verify_page, team_page])

pg.run()
