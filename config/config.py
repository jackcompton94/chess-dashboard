from datetime import datetime

# Table name date
month = datetime.today()

# BigQuery table_id - "peak-vortex-376919.chess_dashboard" is the dataset name
table_id = "peak-vortex-376919.chess_dashboard." + month.strftime("%m_%Y") + "_games"

# Configures source_file name based on current date
file_path = "/Users/jackcompton/PycharmProjects/chess-dashboard/csvs/" + month.strftime("%m_%Y") + "_games.csv"

