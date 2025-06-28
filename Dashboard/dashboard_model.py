import streamlit as st
import pandas as pd
import joblib
import requests
import io

# Set up the Streamlit page configuration
st.set_page_config(page_title="Credit Default Dashboard", layout="wide")

st.title("Customer Default Risk Dashboard")

# Load data from GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Chau-27/ads_PMA/main/Dashboard/Processed_data_for_dashboard.xlsx"
    response = requests.get(url)
    df = pd.read_excel(io.BytesIO(response.content), sheet_name="Data")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Options")

# Credit Limit filter
limit_min = int(df["LIMIT_BAL"].min())
limit_max = int(df["LIMIT_BAL"].max())
limit_range = st.sidebar.slider("Credit Limit (LIMIT_BAL)", limit_min, limit_max, (limit_min, limit_max))

# Age filter
age_min = int(df["AGE"].min())
age_max = int(df["AGE"].max())
age_range = st.sidebar.slider("Age", age_min, age_max, (age_min, age_max))

# Education filter
education_options = ["All"] + sorted(df["EDUCATION"].unique())
selected_education = st.sidebar.selectbox("Education", education_options)

# Gender filter
gender_options = ["All"] + sorted(df["SEX"].unique())
selected_gender = st.sidebar.selectbox("Gender", gender_options)

# Apply filters
filtered_df = df[
    (df["LIMIT_BAL"] >= limit_range[0]) & (df["LIMIT_BAL"] <= limit_range[1]) &
    (df["AGE"] >= age_range[0]) & (df["AGE"] <= age_range[1])
]

if selected_education != "All":
    filtered_df = filtered_df[filtered_df["EDUCATION"] == selected_education]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["SEX"] == selected_gender]

# Create Summary Metrics
st.subheader("Summary Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Customers", len(filtered_df))
col2.metric("Default Rate", f"{filtered_df['default payment next month'].mean()*100:.2f} %")

# Visualization: Default Rate by Age Group
st.subheader("Default Rate by Age Group")

age_bins = pd.cut(filtered_df["AGE"], bins=[20, 30, 40, 50, 60, 70, 80])
default_by_age = filtered_df.groupby(age_bins)["default payment next month"].mean()

# Convert index to string so Streamlit can render
default_by_age.index = default_by_age.index.astype(str)

st.bar_chart(default_by_age)

# Load model
model = joblib.load("Dashboard/default_model.pkl")

# Arrange input bar for the model
with st.expander("Enter Customer Information", expanded=True):
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        LIMIT_BAL = st.number_input("Credit Limit", min_value=0, value=0)
        AGE = st.number_input("Age", min_value=0, max_value=100, value=0)
        GENDER_LABEL = st.selectbox("Gender", ["Female", "Male"])
        GENDER = 0 if GENDER_LABEL == "Female" else 1
        marriage_status = st.selectbox("Marriage Status", ["Married", "Single"])
        MARRIAGE_MARRIED = int(marriage_status == "Married")
        MARRIAGE_SINGLE = int(marriage_status == "Single")
        education_level = st.selectbox(
            "Education Level",
            ["None", "High School", "Graduate", "Postgraduate"]
        )
        EDUCATION_HIGHSCHOOL = int(education_level == "High School")
        EDUCATION_GRADUATE = int(education_level == "Graduate")
        EDUCATION_POSTGRAD = int(education_level == "Postgraduate")

    with col2:
        PAY_STATUS_SEP05 = st.number_input("Pay Status Sep 2005", value=0)
        PAY_STATUS_AUG05 = st.number_input("Pay Status Aug 2005", value=0)
        PAY_STATUS_JUL05 = st.number_input("Pay Status Jul 2005", value=0)
        PAY_STATUS_JUN05 = st.number_input("Pay Status Jun 2005", value=0)
        PAY_STATUS_MAY05 = st.number_input("Pay Status May 2005", value=0)
        PAY_STATUS_APR05 = st.number_input("Pay Status Apr 2005", value=0)

    with col3:
        BILL_AMT_SEP05 = st.number_input("Bill Amount Sep 2005", value=0)
        BILL_AMT_AUG05 = st.number_input("Bill Amount Aug 2005", value=0)
        BILL_AMT_JUL05 = st.number_input("Bill Amount Jul 2005", value=0)
        BILL_AMT_JUN05 = st.number_input("Bill Amount Jun 2005", value=0)
        BILL_AMT_MAY05 = st.number_input("Bill Amount May 2005", value=0)
        BILL_AMT_APR05 = st.number_input("Bill Amount Apr 2005", value=0)
    with col4:
        PAY_AMT_SEP05 = st.number_input("Pay Amount Sep 2005", value=0)
        PAY_AMT_AUG05 = st.number_input("Pay Amount Aug 2005", value=0)
        PAY_AMT_JUL05 = st.number_input("Pay Amount Jul 2005", value=0)
        PAY_AMT_JUN05 = st.number_input("Pay Amount Jun 2005", value=0)
        PAY_AMT_MAY05 = st.number_input("Pay Amount May 2005", value=0)
        PAY_AMT_APR05 = st.number_input("Pay Amount Apr 2005", value=0)

# Prepare model input
input_df = pd.DataFrame({
    "LIMIT_BAL": [LIMIT_BAL],
    "GENDER": [GENDER],
    "EDUCATION_HIGHSCHOOL": [EDUCATION_HIGHSCHOOL],
    "EDUCATION_GRADUATE": [EDUCATION_GRADUATE],
    "EDUCATION_POSTGRAD": [EDUCATION_POSTGRAD],
    "MARRIAGE_MARRIED": [MARRIAGE_MARRIED],
    "MARRIAGE_SINGLE": [MARRIAGE_SINGLE],
    "AGE": [AGE],
    "PAY_STATUS_SEP05": [PAY_STATUS_SEP05],
    "PAY_STATUS_AUG05": [PAY_STATUS_AUG05],
    "PAY_STATUS_JUL05": [PAY_STATUS_JUL05],
    "PAY_STATUS_JUN05": [PAY_STATUS_JUN05],
    "PAY_STATUS_MAY05": [PAY_STATUS_MAY05],
    "PAY_STATUS_APR05": [PAY_STATUS_APR05],
    "BILL_AMT_SEP05": [BILL_AMT_SEP05],
    "BILL_AMT_AUG05": [BILL_AMT_AUG05],
    "BILL_AMT_JUL05": [BILL_AMT_JUL05],
    "BILL_AMT_JUN05": [BILL_AMT_JUN05],
    "BILL_AMT_MAY05": [BILL_AMT_MAY05],
    "BILL_AMT_APR05": [BILL_AMT_APR05],
    "PAY_AMT_SEP05": [PAY_AMT_SEP05],
    "PAY_AMT_AUG05": [PAY_AMT_AUG05],
    "PAY_AMT_JUL05": [PAY_AMT_JUL05],
    "PAY_AMT_JUN05": [PAY_AMT_JUN05],
    "PAY_AMT_MAY05": [PAY_AMT_MAY05],
    "PAY_AMT_APR05": [PAY_AMT_APR05]
})

# Ensure input_df columns are in the same order as the trained model
expected_features = model.named_steps['Regression'].feature_names_in_
input_df = input_df[expected_features]

# Predict probability
predicted_proba = model.predict_proba(input_df)[0][1]  # Probability of class 1 (default)

# Show probability
st.metric("Predicted Default Probability", f"{predicted_proba*100:.2f}%")