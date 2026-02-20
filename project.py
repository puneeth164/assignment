import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------- Page Configuration ----------------
st.set_page_config(
    page_title="IPL Sports Analytics Dashboard",
    layout="wide"
)

# ---------------- Load Data ----------------
df = pd.read_csv("IPL.csv") # This line is commented out as 'df' already exists in the kernel

# Ensure 'season' column is integer type for correct numerical operations
# Handle cases where season might be a string like '2007/08'
df['season'] = df['season'].astype(str).str.extract(r'(\d{4})').astype(int)

# --- START: Placeholder data generation for Streamlit app to run without KeyErrors ---
# This section adds dummy columns to the 'df' DataFrame to match the expectations of the Streamlit app.
# The values in these columns are placeholders and will not provide meaningful insights for an IPL dashboard
# without the correct underlying data. To get a functional dashboard, please load a proper IPL dataset.

if "team" not in df.columns:
    df["team"] = "Default Team" # Placeholder
if "runs" not in df.columns:
    df["runs"] = 0 # Placeholder
if "wickets" not in df.columns:
    df["wickets"] = 0 # Placeholder
if "matches" not in df.columns:
    df["matches"] = 1 # Placeholder
if "player" not in df.columns:
    df["player"] = "Default Player" # Placeholder
if "strike_rate" not in df.columns:
    df["strike_rate"] = 0.0 # Placeholder

# --- END: Placeholder data generation ---

# ---------------- Title & Objective ----------------
st.title("🏏 IPL Sports Analytics Dashboard")

st.markdown("""
**Analytical Objective:**
Analyze team and player performance trends in the Indian Premier League (IPL) across seasons
to identify consistency, efficiency, and key performance drivers using match-level statistics.
""")

# ---------------- Sidebar Filters ----------------
st.sidebar.header("Filters")

season_range = st.sidebar.slider(
    "Select Season Range",
    df["season"].min(),
    df["season"].max(),
    (df["season"].min(), df["season"].max())
)

selected_team = st.sidebar.selectbox(
    "Select Team",
    sorted(df["team"].unique())
)

# Filtered data
filtered_df = df[
    (df["season"].between(season_range[0], season_range[1])) &
    (df["team"] == selected_team)
]

# ---------------- Tabs ----------------
tab1, tab2 = st.tabs(["Season Overview", "Player Analysis"])

# ==================================================
# TAB 1 : SEASON OVERVIEW
# ==================================================
with tab1:
    st.subheader("Season-Level Performance Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Runs", int(filtered_df["runs"].sum()))
    col2.metric("Total Wickets", int(filtered_df["wickets"].sum()))
    col3.metric("Matches Played", int(filtered_df["matches"].sum()))

    # Line Chart – Runs by Season
    runs_by_season = (
        filtered_df.groupby("season")["runs"]
        .sum()
        .reset_index()
    )

    st.line_chart(runs_by_season.set_index("season"))

    # Bar Chart – Wins / Matches by Season
    matches_by_season = (
        filtered_df.groupby("season")["matches"]
        .sum()
        .reset_index()
    )

    fig1, ax1 = plt.subplots()
    sns.barplot(
        data=matches_by_season,
        x="season",
        y="matches",
        ax=ax1
    )
    ax1.set_title("Matches Played per Season")
    st.pyplot(fig1)

    st.markdown("""
    **Interpretation:**
    The line chart highlights how total runs fluctuate across seasons, revealing periods of strong
    batting performance. The bar chart shows match participation trends, which help contextualize
    performance volume across different IPL seasons.
    """)

# ==================================================
# TAB 2 : PLAYER ANALYSIS
# ==================================================
with tab2:
    st.subheader("Player Performance & Efficiency")

    selected_player = st.selectbox(
        "Select Player",
        sorted(filtered_df["player"].unique())
    )

    player_df = filtered_df[filtered_df["player"] == selected_player]

    # Scatter Plot – Runs vs Strike Rate
    fig2, ax2 = plt.subplots()
    sns.scatterplot(
        data=player_df,
        x="strike_rate",
        y="runs",
        ax=ax2
    )
    ax2.set_title("Runs vs Strike Rate")
    st.pyplot(fig2)

    # Heatmap – Correlation
    corr_data = player_df[["runs", "wickets", "matches", "strike_rate"]].corr()

    fig3, ax3 = plt.subplots()
    sns.heatmap(
        corr_data,
        annot=True,
        cmap="coolwarm",
        ax=ax3
    )
    ax3.set_title("Performance Metric Correlation")
    st.pyplot(fig3)

    st.markdown("""
    **Interpretation:**
    The scatter plot reveals the relationship between scoring output and strike efficiency,
    highlighting players who score aggressively. The correlation heatmap identifies strong
    associations between performance variables, offering insights into key success factors.
    """)

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("📊 *Data Source: Publicly available IPL statistics*")
