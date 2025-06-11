import streamlit as st
import pandas as pd
from utils import build_timetable, load_model, predict_hours

st.set_page_config("AI Study Planner", layout="wide")
st.title("📚 AI Study Planner")

# Debug mode
DEBUG = True

# Page state
if "page" not in st.session_state:
    st.session_state.page = "details"
if "details" not in st.session_state:
    st.session_state.details = {}
if "subjects" not in st.session_state:
    st.session_state.subjects = []

# ───── Page 1: Student Details ─────
if st.session_state.page == "details":
    st.header("Step 1: Student Details")
    st.session_state.details["name"] = st.text_input("Your Name")
    st.session_state.details["standard"] = st.text_input("Class / Grade")
    st.session_state.details["duration_days"] = st.number_input("How many days is your timetable for?", 1, 100, 7)
    st.session_state.details["daily_hours"] = st.number_input("Study hours per day", 1, 16, 6)

    if st.button("Next"):
        if not st.session_state.details["name"] or not st.session_state.details["standard"]:
            st.error("Please fill in all details")
        else:
            st.session_state.page = "subjects"

# ───── Page 2: Subjects ─────
elif st.session_state.page == "subjects":
    st.header("Step 2: Subjects with Difficulty & Interest")

    subject = st.text_input("Subject")
    difficulty = st.slider("Difficulty Level (1 - Easy to 10 - Hard)", 1, 10, 5)
    interest = st.slider("Interest Level (1 - Low to 10 - High)", 1, 10, 5)

    if st.button("Add Subject"):
        if subject:  # Only add if subject name is not empty
            st.session_state.subjects.append({
                "subject": subject, 
                "difficulty": difficulty, 
                "interest": interest
            })
        else:
            st.warning("Please enter a subject name")

    if st.session_state.subjects:
        st.subheader("Subjects Added")
        st.dataframe(pd.DataFrame(st.session_state.subjects))

    if st.button("Generate Timetable"):
        if len(st.session_state.subjects) >= 1:
            st.session_state.page = "timetable"
        else:
            st.error("Please add at least one subject")

# ───── Page 3: Timetable Generation ─────
elif st.session_state.page == "timetable":
    st.header("Step 3: Timetable")

    details = st.session_state.details
    subjects = st.session_state.subjects

    try:
        model = load_model("study_time_model.pkl")
        if DEBUG:
            st.success("✅ Model loaded successfully")
            
        df = pd.DataFrame(subjects)
        df["predicted_hours"] = df.apply(
            lambda row: predict_hours(model, row["difficulty"], row["interest"]), 
            axis=1
        )
        
        if DEBUG:
            st.subheader("Debug Information")
            st.write("Subjects Data:", df)
            st.write(f"Total Days: {details['duration_days']}")
            st.write(f"Daily Hours: {details['daily_hours']}")

        # Generate timetable
        timetable = build_timetable(
            df,
            total_days=details["duration_days"],
            hours_per_day=details["daily_hours"]
        )
        
        if not timetable.empty:
            st.success("Timetable generated successfully!")
            st.dataframe(timetable)
            
            # Download option
            csv = timetable.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Timetable as CSV", 
                data=csv, 
                file_name="timetable.csv", 
                mime="text/csv"
            )
        else:
            st.error("Failed to generate timetable. The output was empty.")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if DEBUG:
            st.exception(e)