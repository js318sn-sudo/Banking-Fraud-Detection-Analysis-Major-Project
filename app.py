import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------
st.set_page_config(
    page_title="🏦 Banking Fraud Detection Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------
# Custom CSS
# -----------------------------------------------------
st.markdown("""
<style>
.main{
    background-color:#F5F7FA;
}
h1,h2,h3{
    color:#003366;
}
[data-testid="metric-container"]{
    background:white;
    border-radius:10px;
    padding:15px;
    box-shadow:0px 0px 8px rgba(0,0,0,0.15);
}
.sidebar .sidebar-content{
    background:#002B5B;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# Title
# -----------------------------------------------------
st.title("🏦 Banking Fraud Detection Analysis Dashboard")
st.markdown("### End-to-End Data Analytics Major Project")

st.write("---")

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("creditcard.csv")

try:
    df = load_data()

    st.success("✅ Dataset Loaded Successfully")

    # -------------------------------------------------
    # Sidebar
    # -------------------------------------------------
    st.sidebar.title("Navigation")

    page = st.sidebar.radio(
        "Select Section",
        [
            "Dashboard",
            "Dataset Overview",
            "EDA",
            "Statistics",
            "Business Insights"
        ]
    )

    # -------------------------------------------------
    # KPI Calculation
    # -------------------------------------------------
    total_transactions = len(df)
    fraud_transactions = int(df["Class"].sum())
    legitimate_transactions = total_transactions - fraud_transactions
    fraud_rate = round((fraud_transactions / total_transactions) * 100, 4)
    total_amount = round(df["Amount"].sum(), 2)
    average_amount = round(df["Amount"].mean(), 2)

    # -------------------------------------------------
    # Dashboard
    # -------------------------------------------------
    if page == "Dashboard":

        st.header("Executive Dashboard")

        c1, c2, c3 = st.columns(3)

        c1.metric("Total Transactions", f"{total_transactions:,}")
        c2.metric("Fraud Transactions", f"{fraud_transactions:,}")
        c3.metric("Legitimate Transactions", f"{legitimate_transactions:,}")

        c4, c5, c6 = st.columns(3)

        c4.metric("Fraud Rate", f"{fraud_rate}%")
        c5.metric("Total Amount", f"${total_amount:,.2f}")
        c6.metric("Average Amount", f"${average_amount}")

        st.write("---")

        left, right = st.columns(2)

        with left:
            st.subheader("Fraud Distribution")

            fig = px.pie(
                names=["Legitimate", "Fraud"],
                values=[legitimate_transactions, fraud_transactions],
                color=["Legitimate","Fraud"],
                color_discrete_sequence=["green","red"]
            )

            st.plotly_chart(fig, use_container_width=True)

        with right:

            st.subheader("Transaction Class")

            fig2 = px.bar(
                x=["Legitimate","Fraud"],
                y=[legitimate_transactions, fraud_transactions],
                color=["Legitimate","Fraud"],
                color_discrete_sequence=["green","red"]
            )

            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Transaction Amount Distribution")

        fig3 = px.histogram(
            df,
            x="Amount",
            nbins=100,
            color_discrete_sequence=["royalblue"]
        )

        st.plotly_chart(fig3, use_container_width=True)

    # -------------------------------------------------
    # Dataset Overview
    # -------------------------------------------------
    elif page == "Dataset Overview":

        st.header("Dataset Overview")

        st.write("Shape:", df.shape)

        st.write("Columns")

        st.write(df.columns.tolist())

        st.write("Preview")

        st.dataframe(df.head(20), use_container_width=True)

        st.write("Missing Values")

        st.dataframe(df.isnull().sum())

        st.write("Statistics")

        st.dataframe(df.describe())

except FileNotFoundError:
    st.error("❌ creditcard.csv not found. Upload the dataset to the project folder.")
        # -------------------------------------------------
    # EDA
    # -------------------------------------------------
    elif page == "EDA":

        st.header("📊 Exploratory Data Analysis")

        st.sidebar.subheader("Filters")

        amount_range = st.sidebar.slider(
            "Transaction Amount",
            float(df["Amount"].min()),
            float(df["Amount"].max()),
            (
                float(df["Amount"].min()),
                float(df["Amount"].max())
            )
        )

        class_filter = st.sidebar.selectbox(
            "Transaction Type",
            ["All", "Legitimate", "Fraud"]
        )

        filtered_df = df[
            (df["Amount"] >= amount_range[0]) &
            (df["Amount"] <= amount_range[1])
        ]

        if class_filter == "Legitimate":
            filtered_df = filtered_df[filtered_df["Class"] == 0]

        elif class_filter == "Fraud":
            filtered_df = filtered_df[filtered_df["Class"] == 1]

        st.success(f"Filtered Records : {len(filtered_df):,}")

        st.write("---")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Transaction Amount Distribution")

            fig = px.histogram(
                filtered_df,
                x="Amount",
                nbins=80,
                color_discrete_sequence=["royalblue"]
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:

            st.subheader("Fraud vs Legitimate")

            class_counts = filtered_df["Class"].value_counts().reset_index()
            class_counts.columns = ["Class", "Count"]

            class_counts["Class"] = class_counts["Class"].replace({
                0: "Legitimate",
                1: "Fraud"
            })

            fig = px.bar(
                class_counts,
                x="Class",
                y="Count",
                color="Class",
                color_discrete_sequence=["green", "red"]
            )

            st.plotly_chart(fig, use_container_width=True)

        st.write("---")

        st.subheader("Transaction Amount Box Plot")

        fig = px.box(
            filtered_df,
            y="Amount",
            color="Class",
            color_discrete_sequence=["green", "red"]
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

        st.subheader("Time vs Amount")

        fig = px.scatter(
            filtered_df.sample(min(5000, len(filtered_df))),
            x="Time",
            y="Amount",
            color=filtered_df.sample(min(5000, len(filtered_df)))["Class"].astype(str),
            opacity=0.6
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

        st.subheader("Top 20 Highest Transactions")

        top20 = filtered_df.nlargest(20, "Amount")

        st.dataframe(top20, use_container_width=True)

        st.write("---")

        st.subheader("Correlation Heatmap")

        corr = filtered_df.corr(numeric_only=True)

        fig = px.imshow(
            corr,
            color_continuous_scale="RdBu_r",
            aspect="auto",
            text_auto=False
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

        st.subheader("Amount Distribution by Fraud")

        fig = px.violin(
            filtered_df,
            x="Class",
            y="Amount",
            box=True,
            points="outliers",
            color="Class",
            color_discrete_sequence=["green", "red"]
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

        st.subheader("Feature Selection")

        feature = st.selectbox(
            "Select PCA Feature",
            [col for col in filtered_df.columns if col.startswith("V")]
        )

        fig = px.histogram(
            filtered_df,
            x=feature,
            color="Class",
            nbins=80,
            barmode="overlay",
            color_discrete_sequence=["green", "red"]
        )

        st.plotly_chart(fig, use_container_width=True)
    # -------------------------------------------------
    # Statistics
    # -------------------------------------------------
    elif page == "Statistics":

        st.header("📈 Statistical Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric("Mean Amount", f"${df['Amount'].mean():.2f}")
        col2.metric("Median Amount", f"${df['Amount'].median():.2f}")
        col3.metric("Mode Amount", f"${df['Amount'].mode()[0]:.2f}")

        col4, col5, col6 = st.columns(3)

        col4.metric("Maximum", f"${df['Amount'].max():.2f}")
        col5.metric("Minimum", f"${df['Amount'].min():.2f}")
        col6.metric("Std Deviation", f"{df['Amount'].std():.2f}")

        st.write("---")

        st.subheader("Descriptive Statistics")

        st.dataframe(df.describe(), use_container_width=True)

        st.write("---")

        st.subheader("Correlation Matrix")

        corr = df.corr(numeric_only=True)

        fig = px.imshow(
            corr,
            color_continuous_scale="Viridis",
            aspect="auto"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.write("---")

        st.subheader("Skewness")

        st.dataframe(df.skew(numeric_only=True).to_frame("Skewness"))

        st.subheader("Kurtosis")

        st.dataframe(df.kurtosis(numeric_only=True).to_frame("Kurtosis"))

    # -------------------------------------------------
    # Business Insights
    # -------------------------------------------------

    elif page == "Business Insights":

        st.header("💼 Business Insights")

        fraud_rate = (fraud_transactions / total_transactions) * 100

        st.info(f"Fraud Rate : {fraud_rate:.4f}%")

        high_value = df[df["Amount"] > 1000]

        fraud_high = high_value[high_value["Class"] == 1]

        st.metric("High Value Transactions", len(high_value))

        st.metric("High Value Fraud", len(fraud_high))

        st.write("---")

        st.success("### Key Findings")

        st.markdown("""
        ✅ Fraud transactions are extremely rare.

        ✅ Dataset is highly imbalanced.

        ✅ Most transactions are low-value.

        ✅ High-value transactions require additional verification.

        ✅ Feature Engineering improves fraud detection.

        ✅ Time-based analysis reveals hidden fraud patterns.

        ✅ Continuous monitoring is recommended.
        """)

        st.write("---")

        st.warning("### Recommendations")

        st.markdown("""
        • Deploy Machine Learning models

        • Enable Real-Time Fraud Detection

        • Monitor High Value Transactions

        • Improve Customer Authentication

        • Build Interactive Power BI Dashboards

        • Automate Fraud Alerts
        """)

        st.write("---")

        st.subheader("Fraud Percentage")

        pie = px.pie(
            names=["Legitimate", "Fraud"],
            values=[legitimate_transactions, fraud_transactions],
            hole=0.5,
            color_discrete_sequence=["green", "red"]
        )

        st.plotly_chart(pie, use_container_width=True)

        st.write("---")

        st.subheader("Download Dataset")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Dataset",
            csv,
            "creditcard_dataset.csv",
            "text/csv"
        )

        st.write("---")

        st.subheader("Project Information")

        st.markdown("""
### 🏦 Banking Fraud Detection Analysis

**Major Project**

**Tools Used**

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- SQL
- Scikit-learn
- Power BI

**Dataset**

Credit Card Fraud Detection Dataset

**Total Features:** 31

**Transactions:** 284,807

**Fraud Cases:** 492

**Developer**

Your Name
        """)

# -------------------------------------------------
# Footer
# -------------------------------------------------

st.write("---")

st.markdown(
"""
<div style='text-align:center'>
<h4>🏦 Banking Fraud Detection Analysis Dashboard</h4>
<p>Developed using Streamlit | Python | Plotly | SQL | Power BI</p>
</div>
""",
unsafe_allow_html=True
)
st.markdown("""
<div style="background:linear-gradient(90deg,#0f4c81,#0077b6);
padding:25px;
border-radius:12px;
color:white;">
<h1>🏦 Banking Fraud Detection Analysis</h1>
<p>Interactive Banking Analytics Dashboard using Python, SQL, Statistics, Plotly & Streamlit</p>
</div>
""", unsafe_allow_html=True)

st.write("")
col1, col2, col3, col4 = st.columns(4)

col1.info("📂 Dataset\n\n284,807 Transactions")
col2.success("💳 Fraud Cases\n\n492")
col3.warning("📈 Features\n\n31")
col4.error("📊 Fraud Rate\n\n0.172%")
with st.expander("📖 About Dataset"):

    st.write("""
This project uses the Credit Card Fraud Detection dataset.

• Total Transactions : 284,807

• Features : 31

• Fraud Cases : 492

• Legitimate Cases : 284,315

• Highly Imbalanced Dataset
""")
show_data = st.checkbox("Show Full Dataset")

if show_data:
    st.dataframe(df)
st.download_button(
    "📥 Download Cleaned Dataset",
    df.to_csv(index=False),
    "cleaned_creditcard.csv",
    "text/csv"
)
st.markdown("---")

st.markdown("""
<center>

### 🏦 Banking Fraud Detection Analysis

Developed as a Major Project using

Python • Pandas • Plotly • Streamlit • SQL • Power BI

© 2026 All Rights Reserved

</center>
""", unsafe_allow_html=True)
