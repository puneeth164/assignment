import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Premier League Performance Dashboard",
    layout="wide"
)

# Load data
df = pd.read_csv("epl_final.csv")

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
