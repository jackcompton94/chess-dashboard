# Chess-Data-Analysis-Dashboard
![alt text](https://github.com/jackcompton94/Chess-Data-Analysis-Dashboard/blob/main/ChessDashboardDiagram.png)

https://lookerstudio.google.com/reporting/498fd13b-6afe-4ec5-b447-2736f688ceba

## Purpose
To extract, format, store, aggregate, and analyze meaningful statistics in a real-time cloud environment to improve your chess game including:
* Win/Loss/Draw Record
* Win Percentage as White and Black
* Win Percentage vs. Higher and Lower ELOs
* Current Win/Loss Streak
* ELO Rating Overtime
* Win Percentages against different ELOs
* All Time or Monthly Dashboard Views

## How it works
* __main.py__ interacts with the Chess.com API and extracts JSON and formats the relevant data into a local CSV
* __load.py__ interacts with the BigQuery API to create and maintain the local CSV in the cloud
* __view.py__ interacts with the BigQuery API to initialize the views needed that are used in Looker Studio
* __looker.py__ interacts with the Looker API to create and maintain the dashboards needed to visualize the statistics

These scripts are automated with cron on a local machine to maintain up-to-date stats and maintain an autonomous workflow

## Whats Next?
* Replace the cron jobs with a tool that can run independently from the local machine. For example, AWS Lambda, Google Cloud Function, etc.
* Develop a script that transforms the JSON data for moves made during a match to determine the Opening/Defense(s) used and aggregate "Favorites" and the "Win Percentages with 'x' openings" (stockfish)
* Add an option to visualize any month of chess stats for the user, ths will involve getting the "Account Created Date" and to create a monthly dashboard for each month since inception. This also will allow another feature where you can view "All Time" stats by 'UNION ALL' of the monthly tables from creation.
* Create a functioning site that allows user to login to Chess.com and this authentication will provide the username needed for the inital API call and leverage a full-fledged performance dashboard
