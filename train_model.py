import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Sample training data
data = {
    "difficulty": [1, 3, 5, 7, 9],
    "interest": [9, 7, 5, 3, 1],
    "hours": [1, 2, 3, 4, 5]  # Example mapping
}
df = pd.DataFrame(data)

model = LinearRegression()
model.fit(df[["difficulty", "interest"]], df["hours"])

joblib.dump(model, "study_time_model.pkl")
print("✅ Model trained and saved.")
