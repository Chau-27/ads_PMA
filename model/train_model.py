import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, f1_score, r2_score
from sklearn.calibration import calibration_curve
from sklearn.calibration import CalibrationDisplay
import matplotlib.pyplot as plt

# Load data from GitHub
csv_url = "https://raw.githubusercontent.com/Chau-27/ads_PMA/main/model/Model_Data_Input.csv"
df = pd.read_csv(csv_url)

# Defined X and y, Dropped "ID" in X as it is not a feature 
X = df[["LIMIT_BAL","GENDER","EDUCATION_POSTGRAD","EDUCATION_GRADUATE","EDUCATION_HIGHSCHOOL","MARRIAGE_MARRIED",
        "MARRIAGE_SINGLE","AGE","PAY_STATUS_SEP05","PAY_STATUS_AUG05","PAY_STATUS_JUL05","PAY_STATUS_JUN05",
        "PAY_STATUS_MAY05","PAY_STATUS_APR05","BILL_AMT_SEP05","BILL_AMT_AUG05","BILL_AMT_JUL05","BILL_AMT_JUN05",
        "BILL_AMT_MAY05","BILL_AMT_APR05","PAY_AMT_SEP05","PAY_AMT_AUG05","PAY_AMT_JUL05","PAY_AMT_JUN05",
        "PAY_AMT_MAY05","PAY_AMT_APR05"]]
y = df["DEFAULT_NEXT_MONTH"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42, stratify=y
)

X = X_train
y = y_train


# Pipeline
model = Pipeline([
    ("Regression", LogisticRegression(max_iter=500))
])

# Train model
model.fit(X, y)

# Test model using the test set
y_pred = model.predict(X_test)

# Calculate confusion matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

accuracy = accuracy_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
sensitivity = recall
r2 = model.score(X_test, y_test)

print(f"Accuracy: {accuracy:.4f}")
print(f"Recall (Sensitivity): {recall:.4f}")
print(f"Precision: {precision:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"R2 Score: {r2:.4f}")

# Display probability calibration curve using sklearn's CalibrationDisplay
CalibrationDisplay.from_estimator(model, X_test, y_test, n_bins=10)
plt.title('Probability Calibration Curve (sklearn)')
plt.show()

# Save model
joblib.dump(model, "default_model.pkl")
print("Model saved as default_model.pkl")

# Print feature names
print(model.named_steps['Regression'].feature_names_in_)