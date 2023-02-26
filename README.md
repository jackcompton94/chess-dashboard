# Chess-Data-Analysis-Dashboard
![alt text](https://github.com/jackcompton94/Chess-Data-Analysis-Dashboard/blob/main/ChessDashboardDiagram.png)

## Purpose
To extract, format, store, aggregate, and analyze meaningful statistics in a real-time cloud environment to improve your chess game including:
* Win/Loss/Draw Record
* Win Percentage as White and Black
* Win Percentage vs. Higher and Lower ELOs
* Current Win/Loss Streak
* ELO Rating Overtime
* Win Percentages against different ELOs
* All Time or Monthly Dashboard Views


## How It Works
First, we interact with the Chess.com API by extracting monthly game data (in JSON) and format tabular rows of win/loss, usernames, and ELO ratings. From there, we load these rows into a table stored in BigQuery (tables are created monthly). Next, we interact with the BigQuery API and run a set of 11 queries to create the different views needed for analysis. Finally, we create a dashboard with the Looker API to reflect the statistics generated with our SQL query views.
* These scripts are ran daily to maintain up-to-date information

https://lookerstudio.google.com/reporting/498fd13b-6afe-4ec5-b447-2736f688ceba
