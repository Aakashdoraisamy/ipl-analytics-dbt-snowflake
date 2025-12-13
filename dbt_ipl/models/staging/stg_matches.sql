WITH source AS (
    SELECT * FROM {{ source('raw', 'matches') }}
),

cleaned AS (
    SELECT
        id AS match_id,
        season,
        city,
        TRY_TO_DATE(date, 'YYYY-MM-DD') AS match_date,
        team1,
        team2,
        toss_winner,
        toss_decision,
        result,
        dl_applied,
        winner,
        win_by_runs,
        win_by_wickets,
        player_of_match,
        venue,
        umpire1,
        umpire2,
        umpire3,
        
        -- Add calculated fields
        CASE 
            WHEN toss_winner = winner THEN 1 
            ELSE 0 
        END AS toss_winner_won_match,
        
        CASE
            WHEN win_by_runs > 0 THEN 'Batting First Win'
            WHEN win_by_wickets > 0 THEN 'Chasing Win'
            ELSE 'No Result'
        END AS win_type,
        
        CASE
            WHEN win_by_runs > 0 THEN win_by_runs
            WHEN win_by_wickets > 0 THEN NULL
            ELSE NULL
        END AS margin_runs,
        
        CASE
            WHEN win_by_wickets > 0 THEN win_by_wickets
            WHEN win_by_runs > 0 THEN NULL
            ELSE NULL
        END AS margin_wickets
        
    FROM source
    WHERE result = 'normal' -- Exclude ties, no results
)

SELECT * FROM cleaned