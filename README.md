# Smart Study Scheduler AI

Project Overview

A Streamlit-based application that generates personalized study timetables for students. It leverages a machine learning model to recommend optimal study hours based
on subject difficulty and user interest, promoting balanced study routines.

---

Features

The Smart Study Scheduler AI offers these core functionalities:

- Personalized Study Hour Prediction: Recommends optimal study hours for each subject using AI, based on your perceived difficulty and interest levels.
- Generates Daily Study Timetables: Creates a structured, hour-by-hour study plan for each day, tailored to the recommended hours.
- Sleep-Friendly Scheduling (No Late-Night Slots): Automatically avoids assigning study sessions between 11 PM and 4 AM, prioritizing your well-being and effective learning.
- Timetable Download: Lets you download your generated timetable as a CSV file for easy access and sharing.

---

Technologies Used

This project is built primarily with Python 3.10+ and utilizes the following key libraries:

- Streamlit: For building the interactive web application.
- Pandas: For efficient data handling and numerical operations.
- Scikit-learn: For the machine learning functionalities (specifically, the Linear Regression model).
- Joblib: For saving and loading the trained machine learning model.

---

How to Run Locally

This project runs smoothly on Windows, macOS, and Linux. Just make sure you have Python 3.10+ and Git installed on your system.

1. Clone the Repository

To get a copy of the project files on your computer:

- Open your terminal or command prompt.
- Navigate to your desired directory (e.g., cd Documents/Projects).
- Run the following command:

    ```bash
    git clone https://github.com/LokaAashritha/Smart_Study_Scheduler_AI.git
    ```

- Then, move into the project's folder:

    ```bash
    cd Smart_Study_Scheduler_AI
    ```

    Your Command Prompt should now show something like C:\Users\YourName\Documents\Projects\Smart_Study_Scheduler_AI>

2. Create and Activate a Virtual Environment

- While in the Smart_Study_Scheduler_AI directory, create a virtual environment:

    ```bash
    python -m venv venv
    ```

- Now, activate this environment:

    - On Windows (Command Prompt/PowerShell):

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS/Linux (Bash/Zsh):

        ```bash
        source venv/bin/activate
        ```

    (You'll know it's active when you see (venv) appear in your command prompt.)

3. Install Dependencies

Install all necessary Python libraries listed in requirements.txt into your active virtual environment:

- With (venv) active, run:

    ```bash
    pip install -r requirements.txt
    ```

4. Train the Machine Learning Model

Your app needs a brain! This step generates the study_time_model.pkl file.

- With (venv) active, run:

    ```bash
    python train_model.py
    ```

    (You should see a success message like ✅ Model trained and saved. when it's done.)

5. Run the Application

Finally, launch your Smart Study Scheduler AI!

- With (venv) active, run:

    ```bash
    streamlit run app.py
    ```

    Your default web browser should automatically open to http://localhost:8501, displaying your application.

---

Project Structure

Smart-Study-Scheduler-AI/
- README.md              
- requirements.txt      
- app.py                 
- train_model.py        
- utils.py               
- study_time_model.pkl

