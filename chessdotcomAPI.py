from datetime import datetime
import requests
import json
import csv


def get_chess_games():
    # Chess data config
    month = datetime.today()
    monthString = str(month.month)

    if int(monthString) < 10:
        monthString = "0" + monthString

    gameUrl = "https://api.chess.com/pub/player/v2j-c/games/2023/" + monthString
    gameResponse = requests.request("GET", gameUrl)
    gameResponseObject = json.loads(gameResponse.text)
    chessGames = json.dumps(gameResponseObject, indent=2)
    chessJSON = gameResponse.json()

    # Opening file locally
    with open("/Users/jackcompton/PycharmProjects/chess-dashboard/csvs/" + month.strftime("%m_%Y") + "_games.csv",
              "w") as file:
        writer = csv.writer(file)
        writer.writerow(["game_id", "white", "white_rating", "white_result", "black", "black_rating", "black_result"])
        i = 0

        for games, game in chessJSON.items():
            for key in game:
                white = key['white']
                black = key['black']
                i += 1

                # Saving file locally
                writer.writerow([i, white['username'], str(white['rating']), white['result'], black['username'],
                                 str(black['rating']), black['result']])
