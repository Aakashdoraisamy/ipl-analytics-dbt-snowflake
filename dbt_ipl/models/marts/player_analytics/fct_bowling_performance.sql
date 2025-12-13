WITH deliveries AS (
    SELECT * FROM {{ ref('stg_deliveries') }}
),

matches AS (
    SELECT * FROM {{ ref('stg_matches') }}
),

bowling_agg AS (
    SELECT
        d.match_id,
        d.bowler,
        d.bowling_team,
        
        -- Bowling metrics
        COUNT(*) as balls_bowled,
        ROUND(COUNT(*) / 6.0, 1) as overs_bowled,
        SUM(d.total_runs) as runs_conceded,
        SUM(d.is_wicket) as wickets_taken,
        
        -- Extras conceded
        SUM(d.wide_runs) as wides,
        SUM(d.noball_runs) as noballs,
        SUM(d.extra_runs) as total_extras,
        
        -- Dot balls bowled
        SUM(CASE WHEN d.total_runs = 0 THEN 1 ELSE 0 END) as dot_balls,
        
        -- Boundaries conceded
        SUM(CASE WHEN d.batsman_runs = 4 THEN 1 ELSE 0 END) as fours_conceded,
        SUM(CASE WHEN d.batsman_runs = 6 THEN 1 ELSE 0 END) as sixes_conceded,
        
        -- Economy rate
        CASE 
            WHEN COUNT(*) >= 6 THEN ROUND((SUM(d.total_runs) * 6.0) / COUNT(*), 2)
            ELSE NULL 
        END as economy_rate,
        
        -- Phase-wise performance
        SUM(CASE WHEN d.phase = 'Powerplay' THEN d.total_runs ELSE 0 END) as powerplay_runs,
        SUM(CASE WHEN d.phase = 'Middle' THEN d.total_runs ELSE 0 END) as middle_runs,
        SUM(CASE WHEN d.phase = 'Death' THEN d.total_runs ELSE 0 END) as death_runs,
        
        COUNT(CASE WHEN d.phase = 'Powerplay' THEN 1 END) as powerplay_balls,
        COUNT(CASE WHEN d.phase = 'Middle' THEN 1 END) as middle_balls,
        COUNT(CASE WHEN d.phase = 'Death' THEN 1 END) as death_balls,
        
        SUM(CASE WHEN d.phase = 'Powerplay' AND d.is_wicket = 1 THEN 1 ELSE 0 END) as powerplay_wickets,
        SUM(CASE WHEN d.phase = 'Death' AND d.is_wicket = 1 THEN 1 ELSE 0 END) as death_wickets
        
    FROM deliveries d
    GROUP BY d.match_id, d.bowler, d.bowling_team
),

final AS (
    SELECT
        b.*,
        m.season,
        m.match_date,
        m.venue,
        m.winner,
        CASE WHEN b.bowling_team = m.winner THEN 1 ELSE 0 END as won_match,
        
        -- Dot ball percentage
        ROUND((b.dot_balls * 100.0) / b.balls_bowled, 2) as dot_ball_percentage,
        
        -- Average (runs per wicket)
        CASE 
            WHEN b.wickets_taken > 0 
            THEN ROUND(b.runs_conceded::FLOAT / b.wickets_taken, 2)
            ELSE NULL 
        END as bowling_average,
        
        -- Strike rate (balls per wicket)
        CASE 
            WHEN b.wickets_taken > 0 
            THEN ROUND(b.balls_bowled::FLOAT / b.wickets_taken, 2)
            ELSE NULL 
        END as bowling_strike_rate,
        
        -- Phase-wise economy
        CASE 
            WHEN b.powerplay_balls >= 6 
            THEN ROUND((b.powerplay_runs * 6.0) / b.powerplay_balls, 2)
            ELSE NULL 
        END as powerplay_economy,
        
        CASE 
            WHEN b.death_balls >= 6 
            THEN ROUND((b.death_runs * 6.0) / b.death_balls, 2)
            ELSE NULL 
        END as death_economy
        
    FROM bowling_agg b
    LEFT JOIN matches m ON b.match_id = m.match_id
    WHERE b.balls_bowled >= 6  -- At least 1 over bowled
)

SELECT * FROM final