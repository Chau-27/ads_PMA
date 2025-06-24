import streamlit as st
import pandas as pd

st.set_page_config(page_title="Credit Default Dashboard", layout="wide")

st.title("Customer Default Risk Dashboard")

# ✅ Load data from Excel (specify the correct sheet)
@st.cache_data
def load_data():
    df = pd.read_excel("Dashboard/Processed_data_for_dashboard.xlsx", sheet_name="Data")
    return df

df = load_data()

# ✅ Sidebar filters
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

# ✅ Apply filters
filtered_df = df[
    (df["LIMIT_BAL"] >= limit_range[0]) & (df["LIMIT_BAL"] <= limit_range[1]) &
    (df["AGE"] >= age_range[0]) & (df["AGE"] <= age_range[1])
]

if selected_education != "All":
    filtered_df = filtered_df[filtered_df["EDUCATION"] == selected_education]

if selected_gender != "All":
    filtered_df = filtered_df[filtered_df["SEX"] == selected_gender]

# ✅ Summary
st.subheader("Summary Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Customers", len(filtered_df))
col2.metric("Default Rate", f"{filtered_df['default payment next month'].mean()*100:.2f} %")

# ✅ Visualization: Default Rate by Age Group
st.subheader("Default Rate by Age Group")

age_bins = pd.cut(filtered_df["AGE"], bins=[20, 30, 40, 50, 60, 70, 80])
default_by_age = filtered_df.groupby(age_bins)["default payment next month"].mean()

# ✅ Convert index to string so Streamlit can render
default_by_age.index = default_by_age.index.astype(str)

st.bar_chart(default_by_age)
