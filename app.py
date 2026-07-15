import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="🏦 Banking Fraud Detection Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.block-container{
    padding-top:1rem;
}

h1,h2,h3{
    color:#003366;
}

[data-testid="metric-container"]{
    background:white;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 3px 12px rgba(0,0,0,0.15);
    border-left:6px solid #0066cc;
}

section[data-testid="stSidebar"]{
    background:#002b5b;
}

footer{
    visibility:hidden;
}

#MainMenu{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# LOAD DATA
# ============================================

@st.cache_data
def load_data():

    df = pd.read_csv("creditcard.csv")

    df["Hour"] = (df["Time"] // 3600).astype(int)

    df["High_Value"] = np.where(
        df["Amount"] > 1000,
        "Yes",
        "No"
    )

    return df

try:

    df = load_data()

except FileNotFoundError:

    st.error("❌ creditcard.csv not found.")
    st.stop()

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("🏦 Banking Fraud Detection")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Dataset Overview",
        "EDA",
        "Statistical Analysis",
        "Business Insights",
        "About Project"
    ]
)

st.sidebar.markdown("---")

st.sidebar.success("Major Project")

st.sidebar.write("Python")
st.sidebar.write("Pandas")
st.sidebar.write("NumPy")
st.sidebar.write("Plotly")
st.sidebar.write("Streamlit")
st.sidebar.write("SQL")
st.sidebar.write("Power BI")

# ============================================
# KPI CALCULATIONS
# ============================================

total_transactions = len(df)

fraud_transactions = int(df["Class"].sum())

legitimate_transactions = total_transactions - fraud_transactions

fraud_rate = round(
    (fraud_transactions / total_transactions) * 100,
    4
)

total_amount = round(df["Amount"].sum(), 2)

average_amount = round(df["Amount"].mean(), 2)

highest_amount = round(df["Amount"].max(), 2)

high_value_transactions = len(df[df["Amount"] > 1000])
# ============================================
# DASHBOARD
# ============================================

if page == "Dashboard":

    st.title("🏦 Banking Fraud Detection Dashboard")

    st.markdown("""
    Welcome to the **Banking Fraud Detection Analysis Dashboard**.

    This dashboard provides an interactive analysis of fraudulent and
    legitimate credit card transactions.
    """)

    st.write("---")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Transactions",
        f"{total_transactions:,}"
    )

    col2.metric(
        "Fraud",
        f"{fraud_transactions:,}"
    )

    col3.metric(
        "Legitimate",
        f"{legitimate_transactions:,}"
    )

    col4.metric(
        "Fraud Rate",
        f"{fraud_rate}%"
    )

    st.write("")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Total Amount",
        f"${total_amount:,.2f}"
    )

    col6.metric(
        "Average Amount",
        f"${average_amount:,.2f}"
    )

    col7.metric(
        "Highest Amount",
        f"${highest_amount:,.2f}"
    )

    col8.metric(
        "High Value",
        f"{high_value_transactions:,}"
    )

    st.write("---")

    left, right = st.columns(2)

    with left:

        st.subheader("Fraud Distribution")

        pie_df = pd.DataFrame({
            "Type": [
                "Legitimate",
                "Fraud"
            ],
            "Count": [
                legitimate_transactions,
                fraud_transactions
            ]
        })

        fig = px.pie(
            pie_df,
            names="Type",
            values="Count",
            hole=0.5,
            color="Type",
            color_discrete_map={
                "Legitimate": "#2ecc71",
                "Fraud": "#e74c3c"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Transaction Amount Distribution")

        fig = px.histogram(
            df,
            x="Amount",
            nbins=60,
            color_discrete_sequence=["royalblue"]
        )

        fig.update_layout(
            xaxis_title="Transaction Amount",
            yaxis_title="Frequency"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.write("---")

    st.subheader("Hourly Transactions")

    hourly = (
        df.groupby("Hour")
        .size()
        .reset_index(name="Transactions")
    )

    fig = px.line(
        hourly,
        x="Hour",
        y="Transactions",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Transactions"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")
    # ============================================
# DATASET OVERVIEW
# ============================================

elif page == "Dataset Overview":

    st.title("📂 Dataset Overview")

    st.markdown(
        "Explore the structure and quality of the credit card transaction dataset."
    )

    st.write("---")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Fraud Cases", fraud_transactions)
    c4.metric("Legitimate", legitimate_transactions)

    st.write("---")

    st.subheader("Dataset Preview")

    rows = st.slider(
        "Select Number of Rows",
        5,
        50,
        10
    )

    st.dataframe(
        df.head(rows),
        use_container_width=True
    )

    st.write("---")

    st.subheader("Column Information")

    info_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values
    })

    st.dataframe(
        info_df,
        use_container_width=True
    )

    st.write("---")

    st.subheader("Missing Value Analysis")

    missing = df.isnull().sum().reset_index()

    missing.columns = [
        "Column",
        "Missing"
    ]

    fig = px.bar(
        missing,
        x="Column",
        y="Missing",
        color="Missing",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.success(
        f"Total Missing Values : {df.isnull().sum().sum()}"
    )

    st.write("---")

    st.subheader("Duplicate Records")

    duplicates = df.duplicated().sum()

    c1, c2 = st.columns(2)

    c1.metric(
        "Duplicate Rows",
        duplicates
    )

    c2.metric(
        "Unique Rows",
        len(df) - duplicates
    )

    st.write("---")

    st.subheader("Dataset Statistics")

    st.dataframe(
        df.describe().T,
        use_container_width=True
    )

    st.write("---")

    st.subheader("Transaction Class Distribution")

    class_df = (
        df["Class"]
        .value_counts()
        .rename(index={
            0: "Legitimate",
            1: "Fraud"
        })
        .reset_index()
    )

    class_df.columns = [
        "Transaction",
        "Count"
    ]

    fig = px.bar(
        class_df,
        x="Transaction",
        y="Count",
        color="Transaction",
        color_discrete_map={
            "Legitimate": "#2ecc71",
            "Fraud": "#e74c3c"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    st.subheader("Correlation Heatmap")

    corr = df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Dataset",
        csv,
        "creditcard.csv",
        "text/csv"
    )
    # ============================================
# EXPLORATORY DATA ANALYSIS
# ============================================

elif page == "EDA":

    st.title("📊 Exploratory Data Analysis")

    st.markdown(
        "Interactive analysis of transaction patterns and fraud."
    )

    st.write("---")

    # Sidebar Filters
    st.sidebar.subheader("EDA Filters")

    transaction_type = st.sidebar.selectbox(
        "Transaction Type",
        ["All", "Legitimate", "Fraud"]
    )

    amount_range = st.sidebar.slider(
        "Amount Range",
        float(df["Amount"].min()),
        float(df["Amount"].max()),
        (
            float(df["Amount"].min()),
            float(df["Amount"].max())
        )
    )

    filtered_df = df[
        (df["Amount"] >= amount_range[0]) &
        (df["Amount"] <= amount_range[1])
    ]

    if transaction_type == "Fraud":
        filtered_df = filtered_df[
            filtered_df["Class"] == 1
        ]

    elif transaction_type == "Legitimate":
        filtered_df = filtered_df[
            filtered_df["Class"] == 0
        ]

    st.success(f"Filtered Records : {len(filtered_df):,}")

    st.write("---")

    # ================================
    # Amount Histogram
    # ================================

    left, right = st.columns(2)

    with left:

        st.subheader("Transaction Amount")

        fig = px.histogram(
            filtered_df,
            x="Amount",
            nbins=70,
            color_discrete_sequence=["royalblue"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.subheader("Fraud Comparison")

        fraud_df = (
            filtered_df["Class"]
            .value_counts()
            .rename(index={
                0: "Legitimate",
                1: "Fraud"
            })
            .reset_index()
        )

        fraud_df.columns = [
            "Transaction",
            "Count"
        ]

        fig = px.bar(
            fraud_df,
            x="Transaction",
            y="Count",
            color="Transaction",
            color_discrete_map={
                "Legitimate": "#2ecc71",
                "Fraud": "#e74c3c"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.write("---")

    # ================================
    # Box Plot
    # ================================

    st.subheader("Amount Box Plot")

    fig = px.box(
        filtered_df,
        x="Class",
        y="Amount",
        color="Class",
        color_discrete_sequence=[
            "#2ecc71",
            "#e74c3c"
        ]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    # ================================
    # Scatter Plot
    # ================================

    st.subheader("Time vs Amount")

    sample_df = filtered_df.sample(
        min(len(filtered_df), 5000),
        random_state=42
    )

    fig = px.scatter(
        sample_df,
        x="Time",
        y="Amount",
        color=sample_df["Class"].astype(str),
        opacity=0.6
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    # ================================
    # Hourly Transactions
    # ================================

    st.subheader("Hourly Transactions")

    hourly_df = (
        filtered_df.groupby("Hour")
        .size()
        .reset_index(name="Transactions")
    )

    fig = px.line(
        hourly_df,
        x="Hour",
        y="Transactions",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    # ================================
    # Top Transactions
    # ================================

    st.subheader("Top 20 Transactions")

    top20 = filtered_df.nlargest(
        20,
        "Amount"
    )[
        ["Time", "Amount", "Class"]
    ]

    st.dataframe(
        top20,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # ================================
    # PCA Feature Analysis
    # ================================

    st.subheader("PCA Feature Analysis")

    feature = st.selectbox(
        "Choose PCA Feature",
        [col for col in df.columns if col.startswith("V")]
    )

    fig = px.histogram(
        filtered_df,
        x=feature,
        color="Class",
        nbins=60,
        barmode="overlay"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
    # ============================================
# STATISTICAL ANALYSIS
# ============================================

elif page == "Statistical Analysis":

    st.title("📈 Statistical Analysis")

    st.markdown(
        "Comprehensive statistical summary of the transaction dataset."
    )

    st.write("---")

    # =====================================
    # KPI Statistics
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Mean",
        f"${df['Amount'].mean():.2f}"
    )

    col2.metric(
        "Median",
        f"${df['Amount'].median():.2f}"
    )

    col3.metric(
        "Mode",
        f"${df['Amount'].mode()[0]:.2f}"
    )

    col4.metric(
        "Std Dev",
        f"{df['Amount'].std():.2f}"
    )

    st.write("")

    col5, col6, col7, col8 = st.columns(4)

    col5.metric(
        "Variance",
        f"{df['Amount'].var():.2f}"
    )

    col6.metric(
        "Minimum",
        f"${df['Amount'].min():.2f}"
    )

    col7.metric(
        "Maximum",
        f"${df['Amount'].max():.2f}"
    )

    col8.metric(
        "Range",
        f"${df['Amount'].max()-df['Amount'].min():.2f}"
    )

    st.write("---")

    # =====================================
    # Descriptive Statistics
    # =====================================

    st.subheader("📋 Descriptive Statistics")

    st.dataframe(
        df.describe().T,
        use_container_width=True
    )

    st.write("---")

    # =====================================
    # Quartiles
    # =====================================

    st.subheader("Quartile Analysis")

    quartiles = pd.DataFrame({
        "Statistic":[
            "Q1 (25%)",
            "Median (50%)",
            "Q3 (75%)"
        ],
        "Value":[
            df["Amount"].quantile(0.25),
            df["Amount"].quantile(0.50),
            df["Amount"].quantile(0.75)
        ]
    })

    st.dataframe(
        quartiles,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # =====================================
    # Distribution
    # =====================================

    st.subheader("Distribution of Amount")

    fig = px.histogram(
        df,
        x="Amount",
        marginal="box",
        nbins=80,
        color_discrete_sequence=["royalblue"]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    # =====================================
    # Correlation
    # =====================================

    st.subheader("Correlation Matrix")

    corr = df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        color_continuous_scale="Viridis",
        aspect="auto"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    # =====================================
    # Skewness & Kurtosis
    # =====================================

    left, right = st.columns(2)

    with left:

        st.subheader("Skewness")

        skew_df = pd.DataFrame({
            "Feature": df.columns,
            "Skewness": df.skew(numeric_only=True).values
        })

        st.dataframe(
            skew_df,
            use_container_width=True,
            hide_index=True
        )

    with right:

        st.subheader("Kurtosis")

        kurt_df = pd.DataFrame({
            "Feature": df.columns,
            "Kurtosis": df.kurtosis(numeric_only=True).values
        })

        st.dataframe(
            kurt_df,
            use_container_width=True,
            hide_index=True
        )

    st.write("---")

    # =====================================
    # Insights
    # =====================================

    st.success("""
### 📊 Statistical Insights

✅ Fraud transactions represent a very small percentage of total transactions.

✅ Transaction amounts are highly right-skewed due to a few very large payments.

✅ Most transactions occur within a relatively low amount range.

✅ PCA-transformed features show limited direct correlation.

✅ Statistical analysis confirms that the dataset is highly imbalanced and suitable for fraud detection modeling.
""")
    # ============================================
# BUSINESS INSIGHTS
# ============================================

elif page == "Business Insights":

    st.title("💼 Business Insights")

    st.markdown(
        "Key findings and recommendations from the fraud detection analysis."
    )

    st.write("---")

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Fraud Rate", f"{fraud_rate:.4f}%")
    c2.metric("High Value Transactions", high_value_transactions)
    c3.metric("Average Amount", f"${average_amount:.2f}")
    c4.metric("Maximum Amount", f"${highest_amount:.2f}")

    st.write("---")

    # High Value Transactions
    st.subheader("💰 Top 15 Highest Transactions")

    top15 = df.nlargest(
        15,
        "Amount"
    )[
        ["Time", "Amount", "Class"]
    ]

    st.dataframe(
        top15,
        use_container_width=True,
        hide_index=True
    )

    st.write("---")

    # Fraud Comparison

    fraud_summary = pd.DataFrame({
        "Category": ["Legitimate", "Fraud"],
        "Count": [
            legitimate_transactions,
            fraud_transactions
        ]
    })

    fig = px.bar(
        fraud_summary,
        x="Category",
        y="Count",
        color="Category",
        color_discrete_map={
            "Legitimate": "#2ecc71",
            "Fraud": "#e74c3c"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.write("---")

    st.subheader("📌 Key Business Findings")

    st.success("""
✔ Fraud transactions account for only a very small percentage of all transactions.

✔ Most transactions involve relatively small payment amounts.

✔ A limited number of high-value transactions contribute significantly to the overall transaction value.

✔ Continuous monitoring is essential because fraud patterns evolve over time.

✔ Feature engineering improves fraud analysis and future machine learning performance.
""")

    st.write("---")

    st.subheader("🚀 Recommendations")

    st.info("""
• Deploy Real-Time Fraud Detection

• Verify High Value Transactions

• Use Machine Learning Models

• Monitor Hourly Fraud Trends

• Improve Customer Authentication

• Build Power BI Executive Dashboards

• Regularly Retrain Fraud Models
""")

    st.write("---")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Dataset",
        csv,
        "creditcard_dataset.csv",
        "text/csv"
    )

# ============================================
# ABOUT PROJECT
# ============================================

elif page == "About Project":

    st.title("ℹ️ About Project")

    st.markdown("""
# 🏦 Banking Fraud Detection Analysis

This project demonstrates an end-to-end Data Analytics workflow using the
Credit Card Fraud Detection Dataset.

### Technologies Used

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- SQL
- Scikit-learn
- Statistics
- Power BI
- Git & GitHub

### Dataset

Credit Card Fraud Detection Dataset

- Total Transactions: **284,807**
- Fraud Transactions: **492**
- Legitimate Transactions: **284,315**
- Features: **31**

### Project Workflow

- Data Cleaning
- Data Preprocessing
- Exploratory Data Analysis
- Statistical Analysis
- Feature Engineering
- Data Visualization
- Business Insights
- Dashboard Development

### Future Enhancements

- Machine Learning Model
- Real-Time Fraud Detection
- Cloud Deployment
- Automated Alerts
- Power BI Integration
""")

    st.write("---")

    st.subheader("👨‍💻 Developer")

    st.info("""
Major Project

Developed using Streamlit & Python

Designed for Banking Fraud Detection Analytics
""")

# ============================================
# FOOTER
# ============================================

st.write("---")

st.markdown(
"""
<div style='text-align:center;'>

### 🏦 Banking Fraud Detection Analysis Dashboard

Developed using ❤️ Streamlit | Python | Plotly | SQL | Power BI

© 2026 All Rights Reserved

</div>
""",
unsafe_allow_html=True
)
