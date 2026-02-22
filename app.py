import pandas as pd
import plotly.express as px
import streamlit as st
from nba_api.stats.endpoints import leaguedashplayerstats

# 1. DATA RETRIEVAL
@st.cache_data
def get_nba_data():
    stats = leaguedashplayerstats.LeagueDashPlayerStats(season='2025-26')
    df = stats.get_data_frames()[0]
    return df

df = get_nba_data()

# 2. APP LAYOUT
st.set_page_config(page_title="NBA Analytics", layout="wide")
st.title("🏀 NBA Sports Analytics Dashboard")
st.title("this was reely good)


# Requirements: Sidebar & Filters
st.sidebar.header("Filter Statistics")
min_pts = st.sidebar.slider("Minimum Points Scored", 0, 2000, 500)
selected_team = st.sidebar.selectbox("Select Team", ["All Teams"] + sorted(df['TEAM_ABBREVIATION'].unique().tolist()))

# Filtering Data
filtered_df = df[df['PTS'] >= min_pts]
if selected_team != "All Teams":
    filtered_df = filtered_df[filtered_df['TEAM_ABBREVIATION'] == selected_team]

# 3. TABS
tab1, tab2 = st.tabs(["Performance Overview", "Advanced Correlation"])

with tab1:
    st.header("Scoring & Distribution")
    # Requirement: Chart 1 (Bar)
    fig_bar = px.bar(filtered_df.nlargest(15, 'PTS'), x='PLAYER_NAME', y='PTS', color='PTS')
    st.plotly_chart(fig_bar, use_container_width=True)
    # Requirement: Chart 2 (Histogram)
    fig_hist = px.histogram(filtered_df, x='FG_PCT', nbins=20, title="Field Goal % Distribution")
    st.plotly_chart(fig_hist, use_container_width=True)
    st.write("Analysis: The bar chart shows the league leaders, while the histogram shows how efficient most players are.")

with tab2:
    st.header("Efficiency & Comparison")
    # Requirement: Chart 3 (Scatter)
    fig_scatter = px.scatter(filtered_df, x='REB', y='AST', size='PTS', hover_name='PLAYER_NAME')
    st.plotly_chart(fig_scatter, use_container_width=True)
    # Requirement: Chart 4 (Heatmap)
    corr = filtered_df[['PTS', 'REB', 'AST', 'STL', 'BLK']].corr()
    fig_heatmap = px.imshow(corr, text_auto=True, title="Metric Correlation")
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.write("Analysis: High correlation between stats often indicates 'All-Around' player archetypes.")
