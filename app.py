import pandas as pd
import plotly.express as px
import streamlit as st
from nba_api.stats.endpoints import leaguedashplayerstats

# =======================
# PAGE CONFIG
# =======================
st.set_page_config(page_title="NBA Analytics", layout="wide")

# =======================
# GLOBAL ANIMATION STYLES
# =======================
st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .title-anim {
        animation: fadeIn 1.2s ease-in-out;
        font-size: 38px;
        font-weight: 700;
        color: #0d47a1;
        margin-bottom: 10px;
    }

    .objective-box {
        animation: fadeIn 1.8s ease-in-out;
        background: #f5f9ff;
        padding: 16px;
        border-radius: 10px;
        border-left: 6px solid #1976d2;
        color: #0d47a1;
        font-size: 16px;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# DATA RETRIEVAL (FIXED)
# =======================
@st.cache_data
def get_nba_data():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2025-26")
    df = stats.get_data_frames()[0]
    return df

df = get_nba_data()

# =======================
# DASHBOARD TITLE
# =======================
st.markdown(
    "<div class='title-anim'>🏀 NBA Sports Analytics Dashboard</div>",
    unsafe_allow_html=True
)

# =======================
# ANALYTICAL OBJECTIVE 
# =======================
st.markdown(
    """
    <div class="objective-box">
        <strong>🎯 Analytical Objective</strong><br><br>
        This dashboard helps understand NBA player performance by showing who scores
        the most points, how efficient players are at shooting, and which players
        contribute across multiple areas such as assists and rebounds. The interactive
        filters allow easy comparison between teams and players.
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
    ["All Teams"] + sorted(df["TEAM_ABBREVIATION"].unique().tolist())
)

# =======================
# FILTER DATA
# =======================
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

    # BAR CHART
    fig_bar = px.bar(
        filtered_df.nlargest(15, "PTS"),
        x="PLAYER_NAME",
        y="PTS",
        title="Top Scoring Players"
    )
    fig_bar.update_traces(marker_color="#1976d2")
    st.plotly_chart(fig_bar, use_container_width=True)

    # HISTOGRAM
    fig_hist = px.histogram(
        filtered_df,
        x="FG_PCT",
        nbins=20,
        title="Field Goal % Distribution"
    )
    fig_hist.update_traces(marker_color="#64b5f6")
    st.plotly_chart(fig_hist, use_container_width=True)

    st.write(
        "Analysis: The bar chart highlights the highest scorers, while the field goal "
        "percentage distribution shows that most players fall within a moderate "
        "efficiency range, with only a few high-efficiency outliers."
    )

# =======================
# TAB 2
# =======================
with tab2:
    st.header("Efficiency & Comparison")

    # SCATTER PLOT
    fig_scatter = px.scatter(
        filtered_df,
        x="REB",
        y="AST",
        size="PTS",
        hover_name="PLAYER_NAME",
        title="Rebounds vs Assists (Bubble Size = Points)"
    )
    fig_scatter.update_traces(marker=dict(color="#1976d2", opacity=0.7))
    st.plotly_chart(fig_scatter, use_container_width=True)

    # HEATMAP
    corr = filtered_df[["PTS", "REB", "AST", "STL", "BLK"]].corr()
    fig_heatmap = px.imshow(
        corr,
        text_auto=True,
        title="Metric Correlation",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.write(
        "Analysis: Strong correlations between points, assists, and rebounds suggest "
        "that players who contribute across multiple areas tend to have a greater "
        "overall impact on team performance."
        
    )
