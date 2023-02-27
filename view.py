from google.cloud import bigquery

def initialize_views(client, month, table_id):

# BLACK WIN PERCENTAGE
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_black_win_percentage"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT 
    ROUND(((SELECT COUNT(*) FROM `{table_id}`
    WHERE black = 'v2j-c' AND black_result = 'win') 
    / 
    (SELECT COUNT(*) FROM `{table_id}`
    WHERE black = 'v2j-c')), 2)
    AS win_percentage_as_black
    """
    client.create_table(view)

# WHITE WIN PERCENTAGE
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_white_win_percentage"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT 
    ROUND(((SELECT COUNT(*) FROM `{table_id}`
    WHERE white = 'v2j-c' AND white_result = 'win') 
    / 
    (SELECT COUNT(*) FROM `{table_id}`
    WHERE white = 'v2j-c')), 2)
    AS win_percentage_as_white
    """
    client.create_table(view)

# LAST 5 GAMES
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_last_5_games"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT game_id, white_result AS result FROM {table_id}
    WHERE white = 'v2j-c'
    UNION ALL
    SELECT game_id, black_result FROM {table_id}
    WHERE black = 'v2j-c'
    ORDER BY game_id DESC
    LIMIT 5
    """
    client.create_table(view)

# ELO RATING
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_elo_rating"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT game_id, white_rating AS rating FROM {table_id}
    WHERE white = 'v2j-c'
    UNION ALL
    SELECT game_id, black_rating FROM {table_id}
    WHERE black = 'v2j-c'
    ORDER BY game_id
    """
    client.create_table(view)

# CURRENT RATING
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_current_rating"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_elo_rating"} 
    ORDER BY game_id DESC
    LIMIT 1
    """
    client.create_table(view)

# WHITE RESULT TOTALS
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_white_result_totals"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT white, white_result, COUNT(*) AS total FROM {table_id} AS wins
    WHERE wins.white_result = 'win' AND wins.white = 'v2j-c'
    GROUP BY white, white_result
    UNION ALL 
    SELECT white, white_result, COUNT(*) FROM {table_id} AS losses
    WHERE losses.white_result != 'win' AND losses.white = 'v2j-c'
    GROUP BY white, white_result
    
    ORDER BY total DESC
    """
    client.create_table(view)

# BLACK RESULT TOTALS
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_black_result_totals"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT black, black_result, COUNT(*) AS total FROM {table_id} AS wins
    WHERE wins.black_result = 'win' AND wins.black = 'v2j-c'
    GROUP BY black, black_result
    UNION ALL 
    SELECT black, black_result, COUNT(*) FROM {table_id} AS losses
    WHERE losses.black_result != 'win' AND losses.black = 'v2j-c'
    GROUP BY black, black_result
    
    ORDER BY total DESC
    """
    client.create_table(view)

# TOTAL WINS
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_total_wins"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT SUM(total) AS total_wins FROM
    (SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_white_result_totals"}
    UNION ALL
    SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_black_result_totals"}) 
    WHERE white_result = 'win'
    """
    client.create_table(view)

# TOTAL LOSSES
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_total_losses"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT SUM(total) AS total_losses FROM
    (SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_white_result_totals"}
    UNION ALL
    SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_black_result_totals"}) 
    WHERE white_result IN ('timeout', 'resigned', 'abandoned', 'checkmated')
    """
    client.create_table(view)

# TOTAL DRAWS
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_total_draws"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT SUM(total) AS total_draws FROM
    (SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_white_result_totals"}
    UNION ALL
    SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_black_result_totals"}) 
    WHERE white_result NOT IN ('timeout', 'resigned', 'abandoned', 'checkmated', 'win')
    """
    client.create_table(view)

# WLD RECORD
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_wld_record"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT * FROM chess_dashboard.{month.strftime("%m_%Y") + "_total_wins"}
    CROSS JOIN chess_dashboard.{month.strftime("%m_%Y") + "_total_losses"}
    CROSS JOIN chess_dashboard.{month.strftime("%m_%Y") + "_total_draws"}
    """
    client.create_table(view)

# OPPONENT ELO RATING
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_opponent_elo_rating"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT game_id, white_rating AS rating FROM {table_id}
    WHERE white != 'v2j-c'
    UNION ALL
    SELECT game_id, black_rating FROM {table_id}
    WHERE black != 'v2j-c'
    ORDER BY game_id
    """
    client.create_table(view)

# GAMES AGAINST HIGHER ELO
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_games_against_higher_elo"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT * FROM {table_id}
    WHERE (white = 'v2j-c' AND white_rating < black_rating) OR (black = 'v2j-c' AND black_rating < white_rating) 
    ORDER BY game_id
    """
    client.create_table(view)

# GAMES AGAINST LOWER ELO
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_games_against_lower_elo"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT * FROM {table_id}
    WHERE (white = 'v2j-c' AND white_rating > black_rating) OR (black = 'v2j-c' AND black_rating > white_rating) 
    ORDER BY game_id
    """
    client.create_table(view)

# WIN PERCENTAGE AGAINST HIGHER ELO
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_win_percentage_against_higher_elo"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT
    ROUND(

    -- Total Wins against Higher Elos
    (SELECT SUM(wins) as wins_against_higher_elo FROM (
      (SELECT COUNT(*) as wins FROM chess_dashboard.{month.strftime("%m_%Y") + "_games_against_higher_elo"} WHERE white = 'v2j-c' AND white_result = 'win') 
      UNION ALL 
      (SELECT COUNT(*) FROM chess_dashboard.{month.strftime("%m_%Y") + "_games_against_higher_elo"} WHERE black = 'v2j-c' AND black_result = 'win')
      )
    )
    
    -- Divide
    /
    
    -- Number of games against Higher Elos
    (SELECT COUNT(*) FROM chess_dashboard.{month.strftime("%m_%Y") + "_games_against_higher_elo"})
    , 2) as win_percentage_against_higher_elo
    """
    client.create_table(view)

# WIN PERCENTAGE AGAINST LOWER ELO
    view_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_win_percentage_against_lower_elo"
    view = bigquery.Table(view_id)
    view.view_query = f"""
    SELECT
    ROUND(
    
    -- Total Wins against Lower Elos
    (SELECT SUM(wins) as wins_against_lower_elo FROM (
      (SELECT COUNT(*) as wins FROM chess_dashboard.{month.strftime("%m_%Y") + "_games_against_lower_elo"} WHERE white = 'v2j-c' AND white_result = 'win') 
      UNION ALL 
      (SELECT COUNT(*) FROM chess_dashboard.{month.strftime("%m_%Y") + "_games_against_lower_elo"} WHERE black = 'v2j-c' AND black_result = 'win')
      )
    )
    
    -- Divide
    /
    
    -- Number of games against Lower Elos
    (SELECT COUNT(*) FROM chess_dashboard.{month.strftime("%m_%Y") + "_games_against_lower_elo"})
    , 2) as win_percentage_against_lower_elo
    """
    client.create_table(view)