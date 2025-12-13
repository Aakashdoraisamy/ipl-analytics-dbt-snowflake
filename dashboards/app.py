import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.snowflake_conn import run_query
import pandas as pd

# Page config
st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, professional styling
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #0e1117;
    }
    
    /* Title styling */
    .main-title {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    /* Metric cards */
    .stMetric {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border: 1px solid #475569;
    }
    
    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #312e81 0%, #4c1d95 100%);
        padding: 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #8b5cf6;
        margin: 1rem 0;
        color: #e0e7ff;
    }
    
    /* Filter section */
    .css-1d391kg {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Remove extra padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">🏏 IPL ANALYTICS</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Comprehensive Analysis of Indian Premier League (2008-2020)</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/cricket.png", width=80)
    st.title("🎯 Filters")
    st.markdown("---")
    
    # Season filter
    seasons_query = "SELECT DISTINCT season FROM stg_matches ORDER BY season"
    seasons = run_query(seasons_query)['SEASON'].tolist()
    
    selected_seasons = st.multiselect(
        "📅 Select Seasons",
        options=seasons,
        default=seasons[-3:] if len(seasons) >= 3 else seasons,
        help="Choose seasons to analyze"
    )
    
    # Create season filter
    if selected_seasons:
        season_list = "','".join(selected_seasons)
        season_filter = f"AND season IN ('{season_list}')"
    else:
        season_filter = ""
    
    st.markdown("---")
    
    st.info("""
    **💡 Dashboard Features:**
    - Interactive charts
    - Real-time filtering
    - Comprehensive metrics
    - Hover for details
    """)
    
    st.markdown("---")
    st.markdown("**Tech Stack:**")
    st.markdown("• Snowflake")
    st.markdown("• dbt")
    st.markdown("• Streamlit")
    st.markdown("• Plotly")

# Key Metrics
st.markdown('<p class="section-header">📊 Key Metrics</p>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

# Queries
matches_query = f"SELECT COUNT(DISTINCT match_id) as total FROM stg_matches WHERE 1=1 {season_filter}"
deliveries_query = f"SELECT COUNT(*) as total FROM stg_deliveries WHERE match_id IN (SELECT match_id FROM stg_matches WHERE 1=1 {season_filter})"
players_query = f"SELECT COUNT(DISTINCT batsman) as total FROM stg_deliveries WHERE match_id IN (SELECT match_id FROM stg_matches WHERE 1=1 {season_filter})"
teams_query = f"SELECT COUNT(DISTINCT team_name) as total FROM fct_team_performance WHERE 1=1 {season_filter}"
sixes_query = f"SELECT SUM(sixes) as total FROM fct_batting_performance WHERE match_id IN (SELECT match_id FROM stg_matches WHERE 1=1 {season_filter})"

total_matches = run_query(matches_query)['TOTAL'][0]
total_deliveries = run_query(deliveries_query)['TOTAL'][0]
total_players = run_query(players_query)['TOTAL'][0]
total_teams = run_query(teams_query)['TOTAL'][0]
total_sixes = run_query(sixes_query)['TOTAL'][0]

col1.metric("🏆 Matches", f"{total_matches:,}")
col2.metric("🎯 Deliveries", f"{total_deliveries:,}")
col3.metric("👥 Players", f"{total_players:,}")
col4.metric("🏏 Teams", f"{total_teams}")
col5.metric("🚀 Sixes", f"{total_sixes:,}")

st.markdown("---")

# Top Performers
st.markdown('<p class="section-header">🏆 Top Performers</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top 10 Run Scorers")
    
    batting_query = f"""
    SELECT 
        batsman as Player,
        SUM(runs_scored) as Runs,
        COUNT(DISTINCT match_id) as Matches,
        ROUND(AVG(strike_rate), 2) as Strike_Rate,
        SUM(fours) as Fours,
        SUM(sixes) as Sixes
    FROM fct_batting_performance
    WHERE match_id IN (SELECT match_id FROM stg_matches WHERE 1=1 {season_filter})
    GROUP BY batsman
    HAVING SUM(balls_faced) >= 200
    ORDER BY Runs DESC
    LIMIT 10
    """
    
    top_batsmen = run_query(batting_query)
    
    fig_bat = px.bar(
        top_batsmen,
        x='PLAYER',
        y='RUNS',
        color='STRIKE_RATE',
        color_continuous_scale='Viridis',
        title="",
        labels={'PLAYER': '', 'RUNS': 'Total Runs'},
        hover_data=['MATCHES', 'FOURS', 'SIXES']
    )
    
    fig_bat.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickangle=-45),
        coloraxis_colorbar=dict(title="Strike Rate")
    )
    
    st.plotly_chart(fig_bat, use_container_width=True)
    
    with st.expander("📋 View Detailed Stats"):
        st.dataframe(top_batsmen, use_container_width=True, hide_index=True)

with col2:
    st.subheader("⚡ Top 10 Wicket Takers")
    
    bowling_query = f"""
    SELECT 
        bowler as Player,
        SUM(wickets_taken) as Wickets,
        COUNT(DISTINCT match_id) as Matches,
        ROUND(AVG(economy_rate), 2) as Economy,
        SUM(dot_balls) as Dot_Balls
    FROM fct_bowling_performance
    WHERE wickets_taken > 0 
    AND match_id IN (SELECT match_id FROM stg_matches WHERE 1=1 {season_filter})
    GROUP BY bowler
    HAVING SUM(balls_bowled) >= 300
    ORDER BY Wickets DESC
    LIMIT 10
    """
    
    top_bowlers = run_query(bowling_query)
    
    fig_bowl = px.bar(
        top_bowlers,
        x='PLAYER',
        y='WICKETS',
        color='ECONOMY',
        color_continuous_scale='RdYlGn_r',
        title="",
        labels={'PLAYER': '', 'WICKETS': 'Total Wickets'},
        hover_data=['MATCHES', 'DOT_BALLS']
    )
    
    fig_bowl.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickangle=-45),
        coloraxis_colorbar=dict(title="Economy")
    )
    
    st.plotly_chart(fig_bowl, use_container_width=True)
    
    with st.expander("📋 View Detailed Stats"):
        st.dataframe(top_bowlers, use_container_width=True, hide_index=True)

st.markdown("---")

# Advanced Analytics
st.markdown('<p class="section-header">📈 Advanced Analytics</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🎯 Phase-wise Scoring")
    
    phase_query = f"""
    SELECT 
        phase,
        SUM(total_runs) as total_runs,
        SUM(CASE WHEN is_wicket = 1 THEN 1 ELSE 0 END) as wickets
    FROM stg_deliveries
    WHERE match_id IN (SELECT match_id FROM stg_matches WHERE 1=1 {season_filter})
    GROUP BY phase
    ORDER BY CASE 
        WHEN phase = 'Powerplay' THEN 1
        WHEN phase = 'Middle' THEN 2
        ELSE 3
    END
    """
    
    phase_data = run_query(phase_query)
    
    fig_phase = go.Figure()
    
    fig_phase.add_trace(go.Bar(
        x=phase_data['PHASE'],
        y=phase_data['TOTAL_RUNS'],
        name='Runs',
        marker_color=['#8b5cf6', '#3b82f6', '#10b981'],
        text=phase_data['TOTAL_RUNS'],
        textposition='outside'
    ))
    
    fig_phase.update_layout(
        title="Runs by Match Phase",
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=False,
        yaxis_title="Total Runs"
    )
    
    st.plotly_chart(fig_phase, use_container_width=True)

with col2:
    st.subheader("🏏 Batting First vs Chasing")
    
    win_query = f"""
    SELECT 
        CASE WHEN batted_first = 1 THEN 'Batting First' ELSE 'Chasing' END as scenario,
        CASE WHEN won_match = 1 THEN 'Won' ELSE 'Lost' END as result,
        COUNT(*) as matches
    FROM fct_team_performance
    WHERE 1=1 {season_filter}
    GROUP BY scenario, result
    """
    
    win_data = run_query(win_query)
    
    fig_win = px.bar(
        win_data,
        x='SCENARIO',
        y='MATCHES',
        color='RESULT',
        barmode='stack',
        color_discrete_map={'Won': '#10b981', 'Lost': '#ef4444'},
        title="Match Outcomes",
        labels={'MATCHES': 'Number of Matches', 'SCENARIO': ''}
    )
    
    fig_win.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_win, use_container_width=True)

st.markdown("---")

# Team Performance
st.markdown('<p class="section-header">🏏 Team Performance</p>', unsafe_allow_html=True)

team_query = f"""
SELECT 
    team_name,
    COUNT(*) as matches,
    SUM(won_match) as wins,
    ROUND(SUM(won_match) * 100.0 / COUNT(*), 1) as win_pct,
    ROUND(AVG(runs_scored), 0) as avg_runs
FROM fct_team_performance
WHERE 1=1 {season_filter}
GROUP BY team_name
HAVING COUNT(*) >= 5
ORDER BY win_pct DESC
"""

teams = run_query(team_query)

col1, col2 = st.columns([2, 1])

with col1:
    fig_teams = px.bar(
        teams.head(10),
        x='TEAM_NAME',
        y='WIN_PCT',
        color='WIN_PCT',
        color_continuous_scale='RdYlGn',
        title="Top 10 Teams by Win Percentage",
        labels={'TEAM_NAME': '', 'WIN_PCT': 'Win %'},
        hover_data=['MATCHES', 'WINS', 'AVG_RUNS']
    )
    
    fig_teams.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(tickangle=-45),
        showlegend=False
    )
    
    st.plotly_chart(fig_teams, use_container_width=True)

with col2:
    st.markdown("### 🏆 Top 5 Teams")
    for idx, row in teams.head(5).iterrows():
        st.markdown(f"""
        <div class="insight-box">
        <b>{idx+1}. {row['TEAM_NAME']}</b><br>
        Wins: {int(row['WINS'])}/{int(row['MATCHES'])} ({row['WIN_PCT']:.1f}%)<br>
        Avg Runs: {int(row['AVG_RUNS'])}
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-top: 3rem;">
    <h3 style="color: white; margin: 0;">🏏 IPL Analytics Dashboard</h3>
    <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0;">Built with Snowflake • dbt • Streamlit • Plotly</p>
    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 0;">Data: 2008-2020 IPL Seasons</p>
</div>
""", unsafe_allow_html=True)