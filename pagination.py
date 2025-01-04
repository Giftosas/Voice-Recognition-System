import streamlit as st

# Page Navigation
homepage = st.Page("webpages/homepage.py", title="Welcome", icon=":material/home:")
new_user_page = st.Page("webpages/new_users.py", title="New Users", icon=":material/add_circle:")
team_page = st.Page("webpages/the_team.py", title="The team", icon=":material/groups:")
verify_page = st.Page("webpages/verify_users.py", title="User Verification", icon=":material/verified_user:")

pg = st.navigation([homepage, new_user_page, verify_page, team_page])

pg.run()
