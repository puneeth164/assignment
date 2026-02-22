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
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season='2023-24')
    return stats.get_data_frames()[0]

df = get_nba_data()

# =======================
# TITLE + OBJECTIVE
# =======================
st.title("🏀 NBA Sports Analytics Dashboard")

st.markdown("""
### 🎯 Analytical Objective
This dashboard helps explore NBA player performance by showing top scorers,
shooting efficiency, and players who contribute across multiple areas such as
assists and rebounds using interactive and colorful visualizations.
""")

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

    # BAR CHART (COLORFUL)
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

    # HISTOGRAM (COLORFUL)
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

    # SCATTER PLOT (COLORFUL)
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

    # HEATMAP (COLORFUL)
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
