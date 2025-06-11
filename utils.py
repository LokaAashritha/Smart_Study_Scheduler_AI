import pandas as pd
import numpy as np
import joblib
from collections import defaultdict

def load_model(path="study_time_model.pkl"):
    return joblib.load(path)

def predict_hours(model, difficulty, interest):
    return max(1, round(model.predict([[difficulty, interest]])[0]))

def build_timetable(subject_df, total_days, hours_per_day):
    timetable = {}
    
    # Define available hours (4 AM to 11 PM) and break times
    all_hours = list(range(4, 24))  # 4 AM to 11 PM
    meal_breaks = {
        'Breakfast': [8, 9],    # 8 AM - 9 AM
        'Lunch': [13, 14],      # 1 PM - 2 PM
        'Snacks': [16, 17],     # 4 PM - 5 PM
        'Dinner': [20, 21]      # 8 PM - 9 PM
    }
    
    # Remove break hours from available hours
    break_hours = []
    for meal, hours in meal_breaks.items():
        break_hours.extend(range(hours[0], hours[1]))
    available_hours = [h for h in all_hours if h not in break_hours]
    
    # Calculate score and allocate hours
    subject_df["score"] = subject_df["difficulty"] * 0.6 + (10 - subject_df["interest"]) * 0.4
    total_score = subject_df["score"].sum()
    subject_df["daily_allocation"] = (subject_df["score"] / total_score * hours_per_day).round().astype(int)
    
    # Verify we have enough available hours
    total_allocated = subject_df["daily_allocation"].sum()
    if total_allocated > len(available_hours):
        st.warning(f"Too many study hours ({total_allocated}) for available time slots ({len(available_hours)}). Reducing study hours.")
        hours_per_day = len(available_hours)
        subject_df["daily_allocation"] = (subject_df["score"] / total_score * hours_per_day).round().astype(int)
    
    # Sort subjects by score (highest first)
    sorted_subjects = subject_df.sort_values("score", ascending=False)
    
    # Create a fixed schedule pattern with breaks
    time_slots = []
    subject_assignments = []
    
    # Assign subjects to time slots with breaks
    hour_idx = 0
    subject_idx = 0
    allocation_counts = sorted_subjects["daily_allocation"].tolist()
    
    while hour_idx < len(all_hours) and sum(allocation_counts) > 0:
        current_hour = all_hours[hour_idx]
        
        # Check if this is a break hour
        if current_hour in break_hours:
            # Find which meal break this is
            for meal, hours in meal_breaks.items():
                if current_hour in range(hours[0], hours[1]):
                    time_slots.append(f"{current_hour%12 if current_hour%12!=0 else 12} {'AM' if current_hour<12 else 'PM'} - {(current_hour+1)%12 if (current_hour+1)%12!=0 else 12} {'AM' if (current_hour+1)<12 else 'PM'}")
                    subject_assignments.append(f"⏸ {meal}")
                    break
            hour_idx += 1
            continue
        
        # Assign study time
        if subject_idx < len(sorted_subjects) and allocation_counts[subject_idx] > 0:
            time_slots.append(f"{current_hour%12 if current_hour%12!=0 else 12} {'AM' if current_hour<12 else 'PM'} - {(current_hour+1)%12 if (current_hour+1)%12!=0 else 12} {'AM' if (current_hour+1)<12 else 'PM'}")
            subject_assignments.append(sorted_subjects.iloc[subject_idx]["subject"])
            allocation_counts[subject_idx] -= 1
            hour_idx += 1
            
            # Move to next subject if current one is fully allocated
            if allocation_counts[subject_idx] == 0:
                subject_idx += 1
        else:
            hour_idx += 1
    
    # Create the timetable for all days
    for day in range(1, total_days + 1):
        day_slots = {}
        for slot, subject in zip(time_slots, subject_assignments):
            day_slots[slot] = subject
        timetable[f"Day {day}"] = day_slots

    return pd.DataFrame(timetable).transpose()