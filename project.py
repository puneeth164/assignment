import streamlit as st
import pandas as pd
import altair as alt

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_data(loaddata):
    """Loads the IPL dataset and performs initial preprocessing."""
    # Using 'python' engine to handle potential malformed rows and specifying quotechar and escapechar
    df = pd.read_csv("IPL.csv", engine='python', encoding='utf-8', quotechar='"', escapechar='\\')

    # Convert 'date' to datetime objects
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['match_year'] = df['date'].dt.year

    # Filter out rows where 'date' could not be parsed
    df.dropna(subset=['date'], inplace=True)

    return df

@st.cache_data
def preprocess_data(df):
    """Performs further preprocessing to create aggregated dataframes."""
    # Create matches_df from ipl_df
    matches_df = df.drop_duplicates(subset=['match_id']).copy()

    # Handle 'No result' in match_won_by for win outcome analysis
    matches_df['match_won_by'] = matches_df['match_won_by'].fillna('No result')

    # Extract win_outcome type (by runs or by wickets)
    def get_win_outcome_type(outcome_str):
        if 'runs' in str(outcome_str).lower():
            return 'by Runs'
        elif 'wickets' in str(outcome_str).lower():
            return 'by Wickets'
        else:
            return 'Other' # Handle 'No result' or other scenarios

    # Apply the function to the existing 'win_outcome' column
    matches_df['win_outcome_category'] = matches_df['win_outcome'].apply(get_win_outcome_type)
    matches_df = matches_df[matches_df['match_won_by'] != 'No result'] # Filter out 'No result' for win analysis

    # Calculate overall team wins
    team_wins = matches_df['match_won_by'].value_counts().reset_index()
    team_wins.columns = ['Team', 'Wins']

    # Calculate matches per season
    matches_per_season = matches_df['match_year'].value_counts().reset_index()
    matches_per_season.columns = ['Season', 'Matches']
    matches_per_season = matches_per_season.sort_values('Season')

    # Calculate top players of the match (using 'player_of_match')
    pom_counts = df['player_of_match'].value_counts().reset_index()
    pom_counts.columns = ['Player', 'Awards']

    # Calculate toss decision distribution
    toss_decision_counts = matches_df['toss_decision'].value_counts().reset_index()
    toss_decision_counts.columns = ['Decision', 'Count']

    # Calculate win type distribution using the new category
    win_type_counts = matches_df['win_outcome_category'].value_counts().reset_index()
    win_type_counts.columns = ['Win Type', 'Count']

    # Get unique teams and seasons (using 'batting_team' and 'bowling_team')
    unique_teams = sorted(matches_df['batting_team'].unique().tolist() + matches_df['bowling_team'].unique().tolist())
    unique_teams = sorted(list(set(unique_teams))) # Remove duplicates
    all_seasons = sorted(matches_df['match_year'].unique().tolist())
    unique_venues = matches_df['venue'].nunique() # Using 'venue' column

    return matches_df, team_wins, matches_per_season, pom_counts, toss_decision_counts, win_type_counts, unique_teams, all_seasons, unique_venues

# Load and preprocess data
ipl_df = load_data('IPL.csv')
matches_df, team_wins, matches_per_season, pom_counts, toss_decision_counts, win_type_counts, unique_teams, all_seasons, unique_venues = preprocess_data(ipl_df)

# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="IPL Data Dashboard")

st.title("📊 IPL Cricket Data Dashboard")
st.markdown("""
Welcome to the IPL Cricket Data Dashboard! Explore various statistics and insights from Indian Premier League matches.
Use the filters on the sidebar to customize your view.
""")

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# Season filter
selected_seasons = st.sidebar.slider(
    "Select Seasons",
    min_value=min(all_seasons),
    max_value=max(all_seasons),
    value=(min(all_seasons), max(all_seasons)),
    step=1
)
selected_seasons_list = list(range(selected_seasons[0], selected_seasons[1] + 1))

# Team filter
selected_teams = st.sidebar.multiselect(
    "Select Teams",
    options=unique_teams,
    default=unique_teams # Select all by default
)

# Top N Players filter
top_n_players = st.sidebar.slider(
    "Number of Top Players of the Match",
    min_value=5,
    max_value=min(20, len(pom_counts)),
    value=10,
    step=1
)

# --- Filter Data based on selections ---
filtered_matches_df = matches_df[
    (matches_df['match_year'].isin(selected_seasons_list)) &
    (
        matches_df['batting_team'].isin(selected_teams) |
        matches_df['bowling_team'].isin(selected_teams) |
        matches_df['match_won_by'].isin(selected_teams)
    )
].copy()

# Recalculate aggregated dataframes based on filtered matches
filtered_team_wins = filtered_matches_df['match_won_by'].value_counts().reset_index()
filtered_team_wins.columns = ['Team', 'Wins']
filtered_team_wins = filtered_team_wins[filtered_team_wins['Team'].isin(selected_teams)] # Only show selected teams

filtered_matches_per_season = filtered_matches_df['match_year'].value_counts().reset_index()
filtered_matches_per_season.columns = ['Season', 'Matches']
filtered_matches_per_season = filtered_matches_per_season.sort_values('Season')

filtered_pom_counts = ipl_df[
    (ipl_df['match_year'].isin(selected_seasons_list)) &
    (
        ipl_df['batting_team'].isin(selected_teams) |
        ipl_df['bowling_team'].isin(selected_teams)
    )
]['player_of_match'].value_counts().head(top_n_players).reset_index()
filtered_pom_counts.columns = ['Player', 'Awards']

filtered_toss_decision_counts = filtered_matches_df['toss_decision'].value_counts().reset_index()
filtered_toss_decision_counts.columns = ['Decision', 'Count']

filtered_win_type_counts = filtered_matches_df['win_outcome_category'].value_counts().reset_index()
filtered_win_type_counts.columns = ['Win Type', 'Count']

# --- Main Content Area (Tabs) ---
tab1, tab2, tab3 = st.tabs(["Overview", "Match Analysis", "Player Statistics"])

with tab1:
    st.header("Overview")

    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Matches (Filtered)", filtered_matches_df.shape[0])
    with col2:
        st.metric("Total Teams (Selected)", len(selected_teams))
    with col3:
        st.metric("Total Seasons (Selected)", len(selected_seasons_list))
    with col4:
        st.metric("Total Venues (Overall)", unique_venues) # This metric is not filtered by design

    st.markdown("---")

    # Chart 1: Matches Played Per Season
    if not filtered_matches_per_season.empty:
        st.subheader("Matches Played Per Season (Filtered)")
        chart_matches_per_season = alt.Chart(filtered_matches_per_season).mark_bar().encode(
            x=alt.X('Season:O', title='Season'),
            y=alt.Y('Matches:Q', title='Number of Matches'),
            tooltip=['Season', 'Matches']
        ).properties(
            title='Number of Matches Played Per Season'
        ).interactive()
        st.altair_chart(chart_matches_per_season, use_container_width=True)
    else:
        st.warning("No matches found for the selected filters.")

    st.markdown("---")

    # Chart 2: Overall Team Wins
    if not filtered_team_wins.empty:
        st.subheader("Team Wins (Filtered Teams)")
        chart_team_wins = alt.Chart(filtered_team_wins).mark_bar().encode(
            x=alt.X('Team:N', sort='-y', title='Team'),
            y=alt.Y('Wins:Q', title='Number of Wins'),
            tooltip=['Team', 'Wins']
        ).properties(
            title='Overall Wins by Selected Teams'
        ).interactive()
        st.altair_chart(chart_team_wins, use_container_width=True)
    else:
        st.warning("No team wins data available for the selected filters.")

with tab2:
    st.header("Match Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Chart 3: Toss Decision Distribution
        if not filtered_toss_decision_counts.empty:
            st.subheader("Toss Decision Distribution (Filtered)")
            chart_toss_decision = alt.Chart(filtered_toss_decision_counts).mark_arc(outerRadius=120).encode(
                theta=alt.Theta("Count", stack=True),
                color=alt.Color("Decision", title="Toss Decision"),
                tooltip=["Decision", "Count", alt.Tooltip("Count", format=".1%")]
            ).properties(
                title="Toss Decision Distribution"
            )
            st.altair_chart(chart_toss_decision, use_container_width=True)
        else:
            st.warning("No toss decision data available for the selected filters.")

    with col2:
        # Chart 4: Win Type Distribution
        if not filtered_win_type_counts.empty:
            st.subheader("Win Type Distribution (Filtered)")
            chart_win_type = alt.Chart(filtered_win_type_counts).mark_arc(outerRadius=120).encode(
                theta=alt.Theta("Count", stack=True),
                color=alt.Color("Win Type", title="Win Type"),
                tooltip=["Win Type", "Count", alt.Tooltip("Count", format=".1%")]
            ).properties(
                title="Win Type Distribution"
            )
            st.altair_chart(chart_win_type, use_container_width=True)
        else:
            st.warning("No win type data available for the selected filters.")

    st.markdown("---")

    # Display detailed filtered match data
    if not filtered_matches_df.empty:
        st.subheader("Detailed Match Data (Filtered)")
        st.dataframe(filtered_matches_df[['date', 'match_year', 'match_type', 'venue', 'batting_team', 'bowling_team',
                                          'toss_winner', 'toss_decision', 'match_won_by', 'win_outcome_category', 'player_of_match']].reset_index(drop=True))
    else:
        st.warning("No detailed match data to display for the selected filters.")


with tab3:
    st.header("Player Statistics")

    # Chart 5: Top Players of the Match
    if not filtered_pom_counts.empty:
        st.subheader(f"Top {top_n_players} Players of the Match (Filtered)")
        chart_pom = alt.Chart(filtered_pom_counts).mark_bar().encode(
            x=alt.X('Awards:Q', title='Number of Awards'),
            y=alt.Y('Player:N', sort='-x', title='Player'),
            tooltip=['Player', 'Awards']
        ).properties(
            title=f'Top {top_n_players} Players of the Match'
        ).interactive()
        st.altair_chart(chart_pom, use_container_width=True)
    else:
        st.warning("No player of the match data available for the selected filters.")
