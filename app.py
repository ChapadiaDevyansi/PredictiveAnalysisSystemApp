import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Google Maps Business Analysis",
    page_icon="📍",
    layout="wide"
)

from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).parent / "Cleaned_Surat_Business_Dataset.csv"
df = pd.read_csv(DATA_FILE)


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------
st.sidebar.title("📍 Navigation")

page = st.sidebar.radio(
    "Go to",
    (
        "🏠 Dashboard",
        "📊 Business Overview",
        "🎯 Opportunity Analysis",
        "🤖 Machine Learning",
        "💡 Business Insights"
    )
)

st.sidebar.markdown("---")

# --------------------------------------------------
# Filters
# --------------------------------------------------
st.sidebar.header("🔍 Filters")

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].dropna().unique())
)

area = st.sidebar.multiselect(
    "Area",
    sorted(df["Address/Street"].dropna().unique())
)

website = st.sidebar.multiselect(
    "Website",
    sorted(df["Website(Yes/No)"].dropna().unique())
)

website_needed = st.sidebar.multiselect(
    "Website Needed",
    sorted(df["Website Needed?(Yes/No)"].dropna().unique())
)

# --------------------------------------------------
# Apply Filters
# --------------------------------------------------
filtered_df = df.copy()

if category:
    filtered_df = filtered_df[
        filtered_df["Category"].isin(category)
    ]

if area:
    filtered_df = filtered_df[
        filtered_df["Address/Street"].isin(area)
    ]

if website:
    filtered_df = filtered_df[
        filtered_df["Website(Yes/No)"].isin(website)
    ]

if website_needed:
    filtered_df = filtered_df[
        filtered_df["Website Needed?(Yes/No)"].isin(website_needed)
    ]    

# --------------------------------------------------
# Dashboard
# --------------------------------------------------

if page == "🏠 Dashboard":

    st.title("📍 Google Maps Business Analysis Dashboard")
    st.markdown("### Surat Local Business Analysis")
    st.markdown("""
            This application analyzes Surat businesses using business analytics and machine learning to identify digital growth opportunities.
        """)

    st.divider()

    st.subheader("📈 Key Performance Indicators")

    total_businesses = len(filtered_df)
    total_categories = filtered_df["Category"].nunique()
    total_areas = filtered_df["Address/Street"].nunique()

    avg_rating = round(filtered_df["Rating"].mean(), 2)

    with_website = (
        filtered_df["Website(Yes/No)"] == "Yes"
    ).sum()

    without_website = (
        filtered_df["Website(Yes/No)"] == "No"
    ).sum()

    website_needed = (
        filtered_df["Website Needed?(Yes/No)"] == "Yes"
    ).sum()

    opportunity = (
        filtered_df["Opportunity Flag(High Rating + No Website)"] == "Yes"
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏪 Total Businesses", total_businesses)
    col2.metric("📂 Categories", total_categories)
    col3.metric("📍 Areas", total_areas)
    col4.metric("⭐ Avg Rating", avg_rating)

    col5, col6, col7, col8 = st.columns(4)

    col5.metric("🌐 With Website", with_website)
    col6.metric("❌ Without Website", without_website)
    col7.metric("💻 Website Needed", website_needed)
    col8.metric("🚀 Opportunities", opportunity)

   

    # ===========================
# BUSINESS OVERVIEW PAGE
# ===========================

if page == "📊 Business Overview":

    st.title("📊 Business Overview")
    st.markdown("Overview of Surat Local Businesses")
    st.divider()

    # ------------------------
    # KPI Calculations
    # ------------------------

    total_businesses = len(filtered_df)
    total_categories = filtered_df["Category"].nunique()
    total_areas = filtered_df["Address/Street"].nunique()
    avg_rating = round(filtered_df["Rating"].mean(), 2)

    with_website = (
        filtered_df["Website(Yes/No)"] == "Yes"
    ).sum()

    without_website = (
        filtered_df["Website(Yes/No)"] == "No"
    ).sum()

    website_needed = (
        filtered_df["Website Needed?(Yes/No)"] == "Yes"
    ).sum()

    opportunities = (
        filtered_df["Opportunity Flag(High Rating + No Website)"] == "Yes"
    ).sum()

    # ------------------------
    # KPI Cards
    # ------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("🏪 Total Businesses", total_businesses)
    c2.metric("📂 Categories", total_categories)
    c3.metric("📍 Areas", total_areas)
    c4.metric("⭐ Average Rating", avg_rating)

    c5, c6, c7, c8 = st.columns(4)

    c5.metric("🌐 With Website", with_website)
    c6.metric("❌ Without Website", without_website)
    c7.metric("💻 Website Needed", website_needed)
    c8.metric("🚀 Opportunity Businesses", opportunities)

    st.markdown("---")

    # ------------------------
    # Top Categories & Area
    # ------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("🏆 Top 10 Business Categories")

        top_categories = (
            filtered_df["Category"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        top_categories.columns = ["Category", "Count"]

        fig = px.bar(
            top_categories,
            x="Count",
            y="Category",
            orientation="h",
            text="Count",
            color="Count",
            color_continuous_scale="Blues"
        )

        fig.update_layout(
            height=500,
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("📍 Top 10 Business Areas")

        area_data = (
            filtered_df["Address/Street"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        area_data.columns = ["Area", "Businesses"]

        fig = px.bar(
            area_data,
            x="Businesses",
            y="Area",
            orientation="h",
            text="Businesses",
            color="Businesses",
            color_continuous_scale="Greens"
        )

        fig.update_layout(
            height=500,
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ------------------------
    # Pie Charts
    # ------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("🌐 Website Distribution")

        website_data = (
            filtered_df["Website(Yes/No)"]
            .value_counts()
            .reset_index()
        )

        website_data.columns = ["Website", "Count"]

        fig = px.pie(
            website_data,
            names="Website",
            values="Count",
            hole=0.55,
            color="Website",
            color_discrete_map={
                "Yes": "#2E86DE",
                "No": "#E74C3C"
            }
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("💻 Website Need Distribution")

        need_data = (
            filtered_df["Website Needed?(Yes/No)"]
            .value_counts()
            .reset_index()
        )

        need_data.columns = ["Need", "Count"]

        fig = px.pie(
            need_data,
            names="Need",
            values="Count",
            hole=0.55,
            color="Need",
            color_discrete_map={
                "Yes": "#F39C12",
                "No": "#27AE60"
            }
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")

        st.plotly_chart(fig, use_container_width=True)

        # ===========================
# OPPORTUNITY ANALYSIS PAGE
# ===========================

elif page == "🎯 Opportunity Analysis":

    st.title("🎯 Opportunity Analysis")
    st.markdown("Identify high-potential businesses without websites.")
    st.divider()

    # Opportunity Data
    opportunity_df = filtered_df[
        filtered_df["Opportunity Flag(High Rating + No Website)"] == "Yes"
    ]

    # ------------------------
    # Row 1
    # ------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Top Categories with Most Opportunities")

        opp_category = (
            opportunity_df["Category"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        opp_category.columns = ["Category", "Businesses"]

        fig = px.bar(
            opp_category,
            x="Businesses",
            y="Category",
            orientation="h",
            text="Businesses",
            color="Businesses",
            color_continuous_scale="Oranges"
        )

        fig.update_layout(
            height=450,
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("🚀 Opportunity Distribution")

        opp_distribution = (
            filtered_df["Opportunity Flag(High Rating + No Website)"]
            .value_counts()
            .reset_index()
        )

        opp_distribution.columns = ["Opportunity", "Count"]

        fig = px.pie(
            opp_distribution,
            names="Opportunity",
            values="Count",
            hole=0.55,
            color="Opportunity",
            color_discrete_map={
                "Yes": "#27AE60",
                "No": "#95A5A6"
            }
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ------------------------
    # Row 2
    # ------------------------

    col3, col4 = st.columns(2)

    with col3:

        st.subheader("📍 Opportunity Businesses by Area")

        opp_area = (
            opportunity_df["Address/Street"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        opp_area.columns = ["Area", "Businesses"]

        fig = px.bar(
            opp_area,
            x="Businesses",
            y="Area",
            orientation="h",
            text="Businesses",
            color="Businesses",
            color_continuous_scale="Purples"
        )

        fig.update_layout(
            height=450,
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    with col4:

        st.subheader("⭐ Average Rating by Category")

        avg_rating = (
            filtered_df.groupby("Category")["Rating"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig = px.bar(
            avg_rating,
            x="Rating",
            y="Category",
            orientation="h",
            text="Rating",
            color="Rating",
            color_continuous_scale="Teal"
        )

        fig.update_layout(
            height=450,
            yaxis=dict(categoryorder="total ascending"),
            coloraxis_showscale=False
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ------------------------
    # Scatter Plot
    # ------------------------

    st.subheader("📈 Reviews vs Rating")

    scatter_df = opportunity_df.copy()

    fig = px.scatter(
        scatter_df,
        x="No. of Reviews",
        y="Rating",
        color="Category",
        hover_name="Shop Name",
        size="Rating",
        size_max=18
    )

    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)


    # ===========================
# MACHINE LEARNING PAGE
# ===========================

elif page == "🤖 Machine Learning":

    st.title("🤖 Machine Learning Analysis")
    st.markdown("Prediction model performance and evaluation")
    st.divider()

    st.subheader("🏆 Best Performing Model")

    col1, col2 = st.columns(2)

    with col1:
     st.metric(
        label="Best Model",
        value="Decision Tree"
    )

    with col2:
     st.metric(
        label="Accuracy",
        value="92.81%"
    )

    # ------------------------
    # Model Comparison
    # ------------------------

    st.subheader("📊 Model Accuracy Comparison")

    model_df = pd.DataFrame({
        "Model": [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest"
        ],
        "Accuracy (%)": [
            60.43,
            92.81,
            92.09
        ]
    })

    st.dataframe(model_df, use_container_width=True)

    fig = px.bar(
        model_df,
        x="Model",
        y="Accuracy (%)",
        color="Model",
        text="Accuracy (%)"
    )

    fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")

    fig.update_layout(height=450)

    st.plotly_chart(fig, use_container_width=True)

    st.success("🏆 Best Performing Model: Decision Tree (92.81% Accuracy)")

    st.divider()

    st.subheader("🌳 Feature Importance")

    feature_df = pd.DataFrame({
      "Feature": [
        "No. of Reviews",
        "Category",
        "Rating",
        "Website",
        "Address"
    ],
      "Importance": [
        0.34,
        0.20,
        0.16,
        0.15,
        0.14
    ]
    })

    fig_feature = px.bar(
    feature_df,
    x="Feature",
    y="Importance",
    color="Importance",
    text="Importance"
    )

    fig_feature.update_traces(texttemplate="%{text:.2f}", textposition="outside")

    st.plotly_chart(fig_feature, use_container_width=True)

    st.divider()

    st.subheader("🎯 Decision Tree Confusion Matrix")

    col1, col2, col3 = st.columns([1,3,1])

    with col2:
       st.image(
        "decision_tree_confusion_matrix.png",
        width=650,
        caption="Decision Tree Confusion Matrix"
    )

    st.divider()

    st.subheader("📌 Machine Learning Insights")

    st.markdown("""
    - ✅ Decision Tree achieved the highest accuracy (**92.81%**) and was selected as the final prediction model.
    - ✅ Random Forest achieved **92.09%** accuracy with similar performance.
    - ✅ Logistic Regression achieved **60.43%** accuracy after applying class balancing.
    - ✅ Number of Reviews was the most influential feature, followed by Business Category, Rating, Website Availability, and Address/Street.
    - ✅ The Decision Tree model can predict whether a business is likely to require a website based on business characteristics.
    """)

   # ===========================
# BUSINESS INSIGHTS PAGE
# ===========================

elif page == "💡 Business Insights":

    st.title("💡 Business Insights")
    st.markdown("### 📊 Key Findings from the Business Analysis")
    st.divider()

    st.markdown("### 🌐 Digital Presence")
    st.write(
        "• Out of **691 businesses**, **535 businesses (77.42%)** do not have a website. "
        "This highlights a significant digital presence gap and shows that many local businesses "
        "still rely mainly on offline customers or Google Maps to reach their audience."
    )

    st.markdown("### ⭐ Customer Satisfaction")
    st.write(
        "• The average business rating is **4.35/5**, indicating that most businesses provide "
        "good customer service. This positive reputation creates an excellent opportunity for "
        "businesses to strengthen their online presence."
    )

    st.markdown("### 🚀 Opportunity Businesses")
    st.write(
        "• **46 highly rated businesses** without websites were identified as strong opportunities "
        "for digital transformation. These businesses can potentially attract more customers by "
        "building their own websites."
    )

    st.markdown("### 📍 Area-wise Analysis")
    st.write(
        "• **Palanpur Canal Road, Rander Road, and Gujarat Gas Circle** have the highest "
        "concentration of businesses. These areas should be given priority for website development "
        "and digital awareness initiatives."
    )

    st.markdown("### 🏪 Category Analysis")
    st.write(
        "• Business categories such as **Clothing Stores, Medical Stores, Electronics Stores, "
        "and Grocery Stores** show the highest potential for website adoption due to their "
        "frequent customer interactions."
    )

    st.markdown("### 🤖 Predictive Business Insight")
    st.write(
        "• The machine learning model can help identify businesses that are most likely to require "
        "a website. This allows businesses and decision-makers to prioritize digital transformation "
        "efforts more efficiently."
    )

    st.markdown("### 📈 Growth Potential")
    st.write(
        "• Businesses with strong customer engagement, positive ratings, and higher review counts "
        "have greater potential to grow through digital platforms. Investing in a website can "
        "improve visibility, customer trust, and long-term business growth."
    )
