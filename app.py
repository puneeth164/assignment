import pandas as pd
import plotly.express as px
import streamlit as st
from nba_api.stats.endpoints import leaguedashplayerstats

# =======================
# PAGE CONFIG
# =======================
st.set_page_config(page_title="NBA Sports Analytics", layout="wide")

# =======================
# GLOBAL ANIMATION STYLES
# =======================
st.markdown(
    """
    <style>
    /* Fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Title animation */
    .dashboard-title {
        animation: fadeIn 1.2s ease-in-out;
        font-size: 42px;
        font-weight: 700;
        color: #0d47a1;
        margin-bottom: 10px;
    }

    /* Objective animated box */
    .objective-box {
        animation: fadeIn 1.8s ease-in-out;
        background: linear-gradient(270deg, #e3f2fd, #bbdefb, #e3f2fd);
        background-size: 400% 400%;
        animation: fadeIn 1.8s ease-in-out, gradientMove 12s ease infinite;
        padding: 18px;
        border-radius: 12px;
        color: #0d47a1;
        font-size: 16px;
        font-weight: 500;
        border-left: 6px solid #1976d2;
        margin-bottom: 25px;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =======================
# DATA RETRIEVAL
# =======================
@st.cache_data
def get_nba_data():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season="2023-24")
    return stats.get_data_frames()[0]

df = get_nba_data()

# =======================
# DASHBOARD TITLE (ANIMATED)
# =======================
st.markdown(
    "<div class='dashboard-title'>🏀 NBA Sports Analytics Dashboard</div>",
    unsafe_allow_html=True
)

# =======================
# 🎯 ANALYTICAL OBJECTIVE (ANIMATED)
# =======================
st.markdown(
    """
    <div class="objective-box">
        <h4>🎯 Analytical Objective</h4>
        <p>
        This dashboard analyzes NBA player performance by examining scoring output,
        shooting efficiency, and overall contributions such as assists and rebounds.
        Interactive filters allow users to explore patterns, compare teams, and
        identify all-around player impact in a clear and intuitive way.
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
    st.subheader("Scoring & Distribution")

    fig_bar = px.bar(
        filtered_df.nlargest(15, "PTS"),
        x="PLAYER_NAME",
        y="PTS",
        title="Top Scoring Players"
    )
    fig_bar.update_traces(marker_color="#1976d2")
    fig_bar.update_layout(
        xaxis_title="Player",
        yaxis_title="Total Points"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    fig_hist = px.histogram(
        filtered_df,
        x="FG_PCT",
        nbins=20,
        title="Field Goal Percentage Distribution"
    )
    fig_hist.update_traces(marker_color="#64b5f6")
    fig_hist.update_layout(
        xaxis_title="Field Goal %",
        yaxis_title="Number of Players"
    )
    st.plotly_chart(fig_hist, use_container_width=True)

    st.write(
        "Analysis: The bar chart identifies the highest scorers within the selected "
        "criteria, while the FG% distribution shows that most players fall within "
        "moderate efficiency ranges, with few high-efficiency outliers."
    )

# =======================
# TAB 2
# =======================
with tab2:
    st.subheader("Efficiency & Comparison")

    fig_scatter = px.scatter(
        filtered_df,
        x="REB",
        y="AST",
        size="PTS",
        hover_name="PLAYER_NAME",
        title="Rebounds vs Assists (Bubble Size = Points)"
    )
    fig_scatter.update_traces(marker=dict(color="#1976d2", opacity=0.7))
    fig_scatter.update_layout(
        xaxis_title="Rebounds",
        yaxis_title="Assists"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    corr = filtered_df[["PTS", "REB", "AST", "STL", "BLK"]].corr()
    fig_heatmap = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Between Key Performance Metrics",
        color_continuous_scale="Blues"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.write(
        "Analysis: Strong correlations between scoring, assists, and rebounds indicate "
        "that players who contribute across multiple dimensions tend to provide greater "
        "overall value to their teams."
    )
