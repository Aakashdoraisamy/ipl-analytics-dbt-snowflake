import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.snowflake_conn import run_query

# Page config
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# Title
st.title("🏏 IPL Analytics Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.title("About")
st.sidebar.info(
    """
    **IPL Analytics Platform**
    
    Built with:
    - Snowflake (Data Warehouse)
    - dbt (Transformations)
    - Streamlit + Plotly (Dashboard)
    
    Data: IPL matches (2008-2020)
    """
)

# Main metrics
st.header("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

# Query for metrics
matches_query = "SELECT COUNT(DISTINCT match_id) as total_matches FROM stg_matches"
deliveries_query = "SELECT COUNT(*) as total_deliveries FROM stg_deliveries"
players_query = "SELECT COUNT(DISTINCT batsman) as total_players FROM stg_deliveries"
teams_query = "SELECT COUNT(DISTINCT team_name) as total_teams FROM fct_team_performance"

total_matches = run_query(matches_query)['TOTAL_MATCHES'][0]
total_deliveries = run_query(deliveries_query)['TOTAL_DELIVERIES'][0]
total_players = run_query(players_query)['TOTAL_PLAYERS'][0]
total_teams = run_query(teams_query)['TOTAL_TEAMS'][0]

col1.metric("Total Matches", f"{total_matches:,}")
col2.metric("Total Deliveries", f"{total_deliveries:,}")
col3.metric("Unique Players", f"{total_players:,}")
col4.metric("Teams", f"{total_teams}")

st.markdown("---")

# Top Performers Section
st.header("🏆 Top Performers")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Run Scorers (Overall)")
    
    batting_query = """
    SELECT 
        batsman,
        COUNT(DISTINCT match_id) as matches,
        SUM(runs_scored) as total_runs,
        SUM(balls_faced) as balls_faced,
        ROUND(AVG(strike_rate), 2) as avg_strike_rate,
        SUM(fours) as fours,
        SUM(sixes) as sixes
    FROM fct_batting_performance
    GROUP BY batsman
    HAVING SUM(balls_faced) >= 200
    ORDER BY total_runs DESC
    LIMIT 10
    """
    
    top_batsmen = run_query(batting_query)
    
    fig_batting = px.bar(
        top_batsmen,
        x='BATSMAN',
        y='TOTAL_RUNS',
        color='AVG_STRIKE_RATE',
        hover_data=['MATCHES', 'BALLS_FACED', 'FOURS', 'SIXES'],
        title="Top 10 Run Scorers",
        labels={'BATSMAN': 'Player', 'TOTAL_RUNS': 'Total Runs'},
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_batting, use_container_width=True)

with col2:
    st.subheader("Top Wicket Takers (Overall)")
    
    bowling_query = """
    SELECT 
        bowler,
        COUNT(DISTINCT match_id) as matches,
        SUM(wickets_taken) as total_wickets,
        SUM(runs_conceded) as runs_conceded,
        ROUND(AVG(economy_rate), 2) as avg_economy,
        ROUND(AVG(bowling_strike_rate), 2) as avg_strike_rate
    FROM fct_bowling_performance
    WHERE wickets_taken > 0
    GROUP BY bowler
    HAVING SUM(balls_bowled) >= 300
    ORDER BY total_wickets DESC
    LIMIT 10
    """
    
    top_bowlers = run_query(bowling_query)
    
    fig_bowling = px.bar(
        top_bowlers,
        x='BOWLER',
        y='TOTAL_WICKETS',
        color='AVG_ECONOMY',
        hover_data=['MATCHES', 'RUNS_CONCEDED', 'AVG_STRIKE_RATE'],
        title="Top 10 Wicket Takers",
        labels={'BOWLER': 'Player', 'TOTAL_WICKETS': 'Total Wickets'},
        color_continuous_scale='Reds_r'
    )
    st.plotly_chart(fig_bowling, use_container_width=True)

st.markdown("---")

# Season-wise Analysis
st.header("📈 Season-wise Trends")

season_query = """
SELECT 
    season,
    COUNT(DISTINCT match_id) as matches,
    ROUND(AVG(runs_scored), 0) as avg_runs_per_match,
    ROUND(AVG(run_rate), 2) as avg_run_rate
FROM fct_team_performance
GROUP BY season
ORDER BY season
"""

season_data = run_query(season_query)

fig_season = go.Figure()

fig_season.add_trace(go.Scatter(
    x=season_data['SEASON'],
    y=season_data['AVG_RUNS_PER_MATCH'],
    mode='lines+markers',
    name='Avg Runs',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=8)
))

fig_season.update_layout(
    title="Average Runs Per Match by Season",
    xaxis_title="Season",
    yaxis_title="Average Runs",
    hovermode='x unified'
)

st.plotly_chart(fig_season, use_container_width=True)

st.markdown("---")

# Toss Analysis
st.header("🪙 Toss Impact")

toss_query = """
SELECT 
    CASE WHEN won_toss = 1 THEN 'Won Toss' ELSE 'Lost Toss' END as toss_result,
    CASE WHEN won_match = 1 THEN 'Won Match' ELSE 'Lost Match' END as match_result,
    COUNT(*) as count
FROM fct_team_performance
GROUP BY toss_result, match_result
ORDER BY toss_result, match_result
"""

toss_data = run_query(toss_query)

fig_toss = px.bar(
    toss_data,
    x='TOSS_RESULT',
    y='COUNT',
    color='MATCH_RESULT',
    barmode='group',
    title="Match Results by Toss Outcome",
    labels={'COUNT': 'Number of Matches', 'TOSS_RESULT': 'Toss Result'},
    color_discrete_map={'Won Match': '#2ecc71', 'Lost Match': '#e74c3c'}
)

st.plotly_chart(fig_toss, use_container_width=True)

st.markdown("---")
st.info("👈 Check the sidebar for navigation to detailed analysis pages!")