import streamlit as st

#st.set_page_config(
#    page_title="Home",
#    page_icon=":chart_with_upwards_trend:",
#    layout="wide",
#)

#st.title("🎈 My new app")
#st.write(
#    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
#)

# Set page config (optional, apply to all pages)
st.set_page_config(page_title="My App", layout="wide")

# Define each page
home = st.Page("pages/home.py", title="Home", icon="🏠")
data = st.Page("pages/local_area_economy.py", title="Local Area Economy", icon="📊")

# Create the navigation menu
pg = st.navigation([home, data])

# Run the selected page
pg.run()
