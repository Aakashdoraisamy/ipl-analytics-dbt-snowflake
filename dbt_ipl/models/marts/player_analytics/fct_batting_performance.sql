WITH deliveries AS (
    SELECT * FROM {{ ref('stg_deliveries') }}
),

matches AS (
    SELECT * FROM {{ ref('stg_matches') }}
),

batting_agg AS (
    SELECT
        d.match_id,
        d.batsman,
        d.batting_team,
        
        -- Batting metrics
        COUNT(*) as balls_faced,
        SUM(d.batsman_runs) as runs_scored,
        SUM(CASE WHEN d.batsman_runs = 4 THEN 1 ELSE 0 END) as fours,
        SUM(CASE WHEN d.batsman_runs = 6 THEN 1 ELSE 0 END) as sixes,
        SUM(CASE WHEN d.batsman_runs IN (4, 6) THEN 1 ELSE 0 END) as boundaries,
        MAX(CASE WHEN d.player_dismissed = d.batsman THEN 1 ELSE 0 END) as got_out,
        
        -- Dot balls
        SUM(CASE WHEN d.total_runs = 0 THEN 1 ELSE 0 END) as dot_balls,
        
        -- Strike rate calculation
        CASE 
            WHEN COUNT(*) > 0 THEN ROUND((SUM(d.batsman_runs) * 100.0) / COUNT(*), 2)
            ELSE 0 
        END as strike_rate,
        
        -- Phase-wise performance
        SUM(CASE WHEN d.phase = 'Powerplay' THEN d.batsman_runs ELSE 0 END) as powerplay_runs,
        SUM(CASE WHEN d.phase = 'Middle' THEN d.batsman_runs ELSE 0 END) as middle_overs_runs,
        SUM(CASE WHEN d.phase = 'Death' THEN d.batsman_runs ELSE 0 END) as death_overs_runs,
        
        COUNT(CASE WHEN d.phase = 'Powerplay' THEN 1 END) as powerplay_balls,
        COUNT(CASE WHEN d.phase = 'Middle' THEN 1 END) as middle_overs_balls,
        COUNT(CASE WHEN d.phase = 'Death' THEN 1 END) as death_overs_balls
        
    FROM deliveries d
    GROUP BY d.match_id, d.batsman, d.batting_team
),

final AS (
    SELECT
        b.*,
        m.season,
        m.match_date,
        m.venue,
        m.winner,
        CASE WHEN b.batting_team = m.winner THEN 1 ELSE 0 END as won_match,
        
        -- Calculate dot ball percentage
        ROUND((b.dot_balls * 100.0) / b.balls_faced, 2) as dot_ball_percentage,
        
        -- Phase-wise strike rates
        CASE 
            WHEN b.powerplay_balls > 0 
            THEN ROUND((b.powerplay_runs * 100.0) / b.powerplay_balls, 2)
            ELSE NULL 
        END as powerplay_strike_rate,
        
        CASE 
            WHEN b.death_overs_balls > 0 
            THEN ROUND((b.death_overs_runs * 100.0) / b.death_overs_balls, 2)
            ELSE NULL 
        END as death_strike_rate
        
    FROM batting_agg b
    LEFT JOIN matches m ON b.match_id = m.match_id
    WHERE b.balls_faced > 0  -- Exclude players who didn't face a ball
)

SELECT * FROM final