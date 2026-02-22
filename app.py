import pandas as pd
import plotly.express as px
import streamlit as st
from nba_api.stats.endpoints import leaguedashplayerstats

# =======================
# PAGE CONFIG
# =======================
st.set_page_config(page_title="NBA Analytics", layout="wide")

# =======================
# DATA RETRIEVAL
# =======================
@st.cache_data
def get_nba_data():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2023-24")
    return stats.get_data_frames()[0]

df = get_nba_data()

# =======================
# TITLE
# =======================
st.title("🏀 NBA Sports Analytics Dashboard")

# =======================
# 🔥 ANIMATED ANALYTICAL OBJECTIVE
# =======================
st.markdown(
    """
    <style>
    .objective-box {
        background: linear-gradient(270deg, #ff9a9e, #fad0c4, #a18cd1, #fbc2eb);
        background-size: 600% 600%;
        animation: gradientMove 8s ease infinite;
        padding: 20px;
        border-radius: 15px;
        color: #000;
        font-size: 18px;
        font-weight: 500;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 25px;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>

    <div class="objective-box">
        <h3>🎯 Analytical Objective</h3>
        <p>
        This dashboard explores NBA player performance by highlighting top scorers,
        shooting efficiency, and players who contribute across multiple areas such as
        assists and rebounds. Interactive filters allow easy comparison across teams
        and performance metrics.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =======================
# SIDEBAR FILTERS
# =======================
st.sidebar.header("Filter Statistics")

min_pts = st.sidebar.slider("Minimum Points Scored", 0, 2000, 500)

selected_team = st.sidebar.selectbox(
    "Select Team",
    ["All Teams"] + sorted(df["TEAM_ABBREVIATION"].unique())
)

filtered_df = df[df["PTS"] >= min_pts]
if selected_team != "All Teams":
    filtered_df = filtered_df[filtered_df["TEAM_ABBREVIATION"] == selected_team]

# =======================
# TABS
# =======================
tab1, tab2 = st.tabs(["Performance Overview", "Advanced Correlation"])

# =======================
# TAB 1
# =======================
with tab1:
    st.header("Scoring & Distribution")

    # COLORFUL BAR CHART
    fig_bar = px.bar(
        filtered_df.nlargest(15, "PTS"),
        x="PLAYER_NAME",
        y="PTS",
        color="PLAYER_NAME",
        title="Top Scoring Players",
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

    # COLORFUL HISTOGRAM
    fig_hist = px.histogram(
        filtered_df,
        x="FG_PCT",
        nbins=20,
        title="Field Goal % Distribution",
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.write(
        "Analysis: The bar chart highlights scoring leaders within the selected scope, "
        "while the histogram shows how shooting efficiency is distributed among players."
    )

# =======================
# TAB 2
# =======================
with tab2:
    st.header("Efficiency & Comparison")

    # COLORFUL SCATTER PLOT
    fig_scatter = px.scatter(
        filtered_df,
        x="REB",
        y="AST",
        size="PTS",
        color="PTS",
        hover_name="PLAYER_NAME",
        title="Rebounds vs Assists (Colored by Points)",
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # COLORFUL HEATMAP
    corr = filtered_df[["PTS", "REB", "AST", "STL", "BLK"]].corr()
    fig_heatmap = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Between Performance Metrics",
        color_continuous_scale="RdBu"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.write(
        "Analysis: Strong correlations between points, assists, and rebounds indicate "
        "all-around players who contribute beyond scoring alone."
    )
