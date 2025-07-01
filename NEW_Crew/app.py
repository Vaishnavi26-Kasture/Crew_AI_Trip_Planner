import streamlit as st
from travel_planner import generate_travel_plan  # travel_planner = crew_ai logic
from utils.save_utils import save_document

st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("🧭 AI-Powered Travel Planner")

destination = st.text_input("Enter destination", value="Chandrapur")
budget = st.text_input("Enter budget in USD", value="1500")

if st.button("Generate Plan"):
    if destination and budget:
        with st.spinner("Planning your trip..."):
            result = generate_travel_plan(destination, budget)
            st.markdown(result)
            file_path = save_document(result)
            st.success("Travel plan saved ✅")
            with open(file_path, "rb") as f:
                st.download_button("📥 Download Itinerary", data=f, file_name=file_path.split("/")[-1])
    else:
        st.warning("Please enter destination and budget.")
