WITH source AS (
    SELECT * FROM {{ source('raw', 'deliveries') }}
),

cleaned AS (
    SELECT
        match_id,
        inning,
        batting_team,
        bowling_team,
        over,
        ball,
        batsman,
        non_striker,
        bowler,
        is_super_over,
        wide_runs,
        bye_runs,
        legbye_runs,
        noball_runs,
        penalty_runs,
        batsman_runs,
        extra_runs,
        total_runs,
        player_dismissed,
        dismissal_kind,
        fielder,
        
        -- Add calculated fields
        CASE 
            WHEN over < 6 THEN 'Powerplay'
            WHEN over BETWEEN 6 AND 15 THEN 'Middle'
            ELSE 'Death'
        END AS phase,
        
        -- Flag if wicket fell
        CASE WHEN player_dismissed IS NOT NULL THEN 1 ELSE 0 END AS is_wicket
        
    FROM source
)

SELECT * FROM cleaned