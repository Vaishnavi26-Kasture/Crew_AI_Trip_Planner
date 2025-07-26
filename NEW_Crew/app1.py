import streamlit as st
from travel_planner import generate_travel_plan  # travel_planner = crew_ai logic
from utils.save_utils import save_document

st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("🧭 AI-Powered Travel Planner")

# Inputs for start and destination
start_location = st.text_input("Enter your starting location", value="Nagpur")
destination = st.text_input("Enter your destination", value="Chandrapur")

# Input for budget in dollars
budget_usd = st.text_input("Enter your budget in USD ($)", value="20")

if st.button("Generate Plan"):
    if start_location and destination and budget_usd:
        with st.spinner("Planning your trip..."):
            # You can update generate_travel_plan to accept start location and USD
            result = generate_travel_plan(start_location, destination, budget_usd)
            st.markdown(result)

            # Save and enable download
            file_path = save_document(result)
            st.success("Travel plan saved ✅")
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Itinerary", data=f, file_name=file_path.split("/")[-1])
    else:
        st.warning("Please fill in all fields (start, destination, budget).")
