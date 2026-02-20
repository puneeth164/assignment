import streamlit as st
import pandas as pd
import plotly.express as px

# --- START: Placeholder data generation for Streamlit app to run without KeyErrors ---
# This section adds dummy columns to the 'df' DataFrame to match the expectations of the Streamlit app,
# which is designed for Premier League data, while 'df' currently holds IPL data.
# The values in these columns are placeholders and will not provide meaningful insights for a Premier League dashboard.
# To get a functional dashboard, please load a proper Premier League dataset or adapt the dashboard code for IPL data.

if "date" in df.columns:
    # Ensure 'date' is datetime and create 'MatchDate' and 'Season'
    df["MatchDate"] = pd.to_datetime(df["date"])
    df["Season"] = df["MatchDate"].dt.year.astype(str)
else:
    # Fallback if 'date' column is also missing (unlikely given current df)
    df["MatchDate"] = pd.to_datetime("2023-01-01") # Default date
    df["Season"] = "2023" # Default season

# Create other required columns with placeholder values
if "HomeTeam" not in df.columns:
    # Using existing data to make a slightly more sensible placeholder if possible, else generic
    if "batting_team" in df.columns and not df["batting_team"].empty:
        df["HomeTeam"] = df["batting_team"].iloc[0]
    else:
        df["HomeTeam"] = "Placeholder Home"
if "FullTimeHomeGoals" not in df.columns:
    df["FullTimeHomeGoals"] = 1 # Placeholder value
if "FullTimeAwayGoals" not in df.columns:
    df["FullTimeAwayGoals"] = 0 # Placeholder value
if "FullTimeResult" not in df.columns:
    df["FullTimeResult"] = "H" # Placeholder: Home win
if "HomeShotsOnTarget" not in df.columns:
    df["HomeShotsOnTarget"] = 5 # Placeholder value

# --- END: Placeholder data generation ---

# Page config
st.set_page_config(
    page_title="Premier League Performance Dashboard",
    layout="wide"
)

# Load data
# df = pd.read_csv("IPL.csv") # This line is removed as df is already in kernel

# Sidebar filters
st.sidebar.header("Filters")

season = st.sidebar.selectbox(
    "Select Season",
    sorted(df["Season"].unique())
)

home_team = st.sidebar.selectbox(
    "Select Home Team",
    ["All"] + sorted(df["HomeTeam"].unique())
)

# Apply filters
filtered = df[df["Season"] == season]

if home_team != "All":
    filtered = filtered[filtered["HomeTeam"] == home_team]

# Title & objective
st.title("Premier League Performance Dashboard")
st.markdown("""
**Analytical Objective:**
Analyze home vs away performance and shooting efficiency in the Premier League
to understand how match context influences outcomes across seasons.
""")

# Tabs
tab1, tab2 = st.tabs(["League Overview", "Home vs Away Analysis"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("League Scoring Trends")

    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Home Goals", round(filtered["FullTimeHomeGoals"].mean(), 2))
    col2.metric("Avg Away Goals", round(filtered["FullTimeAwayGoals"].mean(), 2))
    col3.metric("Matches Played", len(filtered))

    # Line chart
    goals_by_date = filtered.groupby("MatchDate")[["FullTimeHomeGoals", "FullTimeAwayGoals"]].mean().reset_index()

    line = px.line(
        goals_by_date,
        x="MatchDate",
        y=["FullTimeHomeGoals", "FullTimeAwayGoals"],
        title="Average Goals Over Time"
    )
    st.plotly_chart(line, use_container_width=True)

    # Bar chart
    bar = px.bar(
        filtered,
        x="FullTimeResult",
        title="Distribution of Match Results"
    )
    st.plotly_chart(bar, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    Home teams consistently score more goals on average than away teams,
    indicating a clear home-field advantage across the selected season.
    """)

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Shooting Efficiency & Match Outcomes")

    # Scatter plot
    scatter = px.scatter(
        filtered,
        x="HomeShotsOnTarget",
        y="FullTimeHomeGoals",
        title="Home Shots on Target vs Goals",
        trendline="ols"
    )
    st.plotly_chart(scatter, use_container_width=True)

    # Heatmap
    heatmap_data = filtered.groupby("HomeTeam")[["FullTimeHomeGoals"]].mean()

    heatmap = px.imshow(
        heatmap_data.T,
        title="Average Home Goals by Team",
        aspect="auto"
    )
    st.plotly_chart(heatmap, use_container_width=True)

    st.markdown("""
    **Interpretation:**
    The scatter plot shows a positive relationship between shots on target
    and goals scored, highlighting the importance of shooting efficiency.
    The heatmap reveals which teams consistently capitalize on home advantage.
    """)
