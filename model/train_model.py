import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib


# Load data
df = pd.read_csv("Model_Data_Input.csv")

# Defined X and y, Dropped "ID" in X as it is not a feature 
X = df[["LIMIT_BAL","GENDER","EDUCATION_POSTGRAD","EDUCATION_GRADUATE","EDUCATION_HIGHSCHOOL","MARRIAGE_MARRIED",
        "MARRIAGE_SINGLE","AGE","PAY_STATUS_SEP05","PAY_STATUS_AUG05","PAY_STATUS_JUL05","PAY_STATUS_JUN05",
        "PAY_STATUS_MAY05","PAY_STATUS_APR05","BILL_AMT_SEP05","BILL_AMT_AUG05","BILL_AMT_JUL05","BILL_AMT_JUN05",
        "BILL_AMT_MAY05","BILL_AMT_APR05","PAY_AMT_SEP05","PAY_AMT_AUG05","PAY_AMT_JUL05","PAY_AMT_JUN05",
        "PAY_AMT_MAY05","PAY_AMT_APR05"]]
y = df["DEFAULT_NEXT_MONTH"]

# Pipeline
model = Pipeline([
    ("Regression", LogisticRegression(max_iter=500))
])

# Train
model.fit(X, y)

# Save model
joblib.dump(model, "default_model.pkl")
print("Model saved as default_model.pkl")

# Print feature names
print(model.named_steps['Regression'].feature_names_in_)