WITH deliveries AS (
    SELECT * FROM {{ ref('stg_deliveries') }}
),

matches AS (
    SELECT * FROM {{ ref('stg_matches') }}
),

-- Batting stats by team and match
batting_stats AS (
    SELECT
        match_id,
        batting_team,
        inning,
        SUM(total_runs) as runs_scored,
        COUNT(*) as balls_faced,
        SUM(is_wicket) as wickets_lost,
        SUM(CASE WHEN batsman_runs = 4 THEN 1 ELSE 0 END) as fours,
        SUM(CASE WHEN batsman_runs = 6 THEN 1 ELSE 0 END) as sixes,
        SUM(extra_runs) as extras_received,
        
        -- Phase-wise runs
        SUM(CASE WHEN phase = 'Powerplay' THEN total_runs ELSE 0 END) as powerplay_runs,
        SUM(CASE WHEN phase = 'Middle' THEN total_runs ELSE 0 END) as middle_runs,
        SUM(CASE WHEN phase = 'Death' THEN total_runs ELSE 0 END) as death_runs,
        
        -- Phase-wise wickets
        SUM(CASE WHEN phase = 'Powerplay' AND is_wicket = 1 THEN 1 ELSE 0 END) as powerplay_wickets,
        SUM(CASE WHEN phase = 'Death' AND is_wicket = 1 THEN 1 ELSE 0 END) as death_wickets,
        
        -- Run rate
        ROUND((SUM(total_runs) * 6.0) / COUNT(*), 2) as run_rate
        
    FROM deliveries
    GROUP BY match_id, batting_team, inning
),

-- Bowling stats by team and match
bowling_stats AS (
    SELECT
        match_id,
        bowling_team,
        inning,
        SUM(total_runs) as runs_conceded,
        SUM(is_wicket) as wickets_taken,
        SUM(extra_runs) as extras_conceded,
        COUNT(*) as balls_bowled,
        
        ROUND((SUM(total_runs) * 6.0) / COUNT(*), 2) as economy_rate
        
    FROM deliveries
    GROUP BY match_id, bowling_team, inning
),

-- Combine batting and bowling for each team
team_match_stats AS (
    SELECT
        m.match_id,
        m.season,
        m.match_date,
        m.venue,
        m.city,
        m.toss_winner,
        m.toss_decision,
        m.winner,
        
        -- Team 1 (batting first)
        m.team1 as team_name,
        1 as batted_first,
        
        bat1.runs_scored,
        bat1.wickets_lost,
        bat1.balls_faced,
        bat1.run_rate,
        bat1.fours,
        bat1.sixes,
        bat1.powerplay_runs,
        bat1.middle_runs,
        bat1.death_runs,
        bat1.powerplay_wickets,
        bat1.death_wickets,
        
        bowl2.wickets_taken as wickets_taken_while_bowling,
        bowl2.runs_conceded as runs_conceded_while_bowling,
        bowl2.economy_rate,
        
        CASE WHEN m.winner = m.team1 THEN 1 ELSE 0 END as won_match,
        CASE WHEN m.toss_winner = m.team1 THEN 1 ELSE 0 END as won_toss,
        
        m.win_by_runs as margin_runs,
        m.win_by_wickets as margin_wickets
        
    FROM matches m
    LEFT JOIN batting_stats bat1 
        ON m.match_id = bat1.match_id 
        AND m.team1 = bat1.batting_team 
        AND bat1.inning = 1
    LEFT JOIN bowling_stats bowl2 
        ON m.match_id = bowl2.match_id 
        AND m.team1 = bowl2.bowling_team 
        AND bowl2.inning = 2
    
    UNION ALL
    
    -- Team 2 (chasing)
    SELECT
        m.match_id,
        m.season,
        m.match_date,
        m.venue,
        m.city,
        m.toss_winner,
        m.toss_decision,
        m.winner,
        
        m.team2 as team_name,
        0 as batted_first,
        
        bat2.runs_scored,
        bat2.wickets_lost,
        bat2.balls_faced,
        bat2.run_rate,
        bat2.fours,
        bat2.sixes,
        bat2.powerplay_runs,
        bat2.middle_runs,
        bat2.death_runs,
        bat2.powerplay_wickets,
        bat2.death_wickets,
        
        bowl1.wickets_taken as wickets_taken_while_bowling,
        bowl1.runs_conceded as runs_conceded_while_bowling,
        bowl1.economy_rate,
        
        CASE WHEN m.winner = m.team2 THEN 1 ELSE 0 END as won_match,
        CASE WHEN m.toss_winner = m.team2 THEN 1 ELSE 0 END as won_toss,
        
        m.win_by_runs as margin_runs,
        m.win_by_wickets as margin_wickets
        
    FROM matches m
    LEFT JOIN batting_stats bat2 
        ON m.match_id = bat2.match_id 
        AND m.team2 = bat2.batting_team 
        AND bat2.inning = 2
    LEFT JOIN bowling_stats bowl1 
        ON m.match_id = bowl1.match_id 
        AND m.team2 = bowl1.bowling_team 
        AND bowl1.inning = 1
)

SELECT * FROM team_match_stats