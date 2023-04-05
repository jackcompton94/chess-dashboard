import bigquery
import chessdotcomAPI
from config import config, config_tokens

# # API calls
# profileUrl = "https://api.chess.com/pub/player/v2j-c"
# statsUrl = "https://api.chess.com/pub/player/v2j-c/stats"

# # http responses
# profileResponse = requests.request("GET", profileUrl)
# statsResponse = requests.request("GET", statsUrl)

# # Converting response to object
# profileResponseObject = json.loads(profileResponse.text)
# statsResponseObject = json.loads(statsResponse.text)

# # JSON formatter
# chessProfile = json.dumps(profileResponseObject, indent=2)
# chessStats = json.dumps(statsResponseObject, indent=2)

# print(chessProfile)
# print(chessStats)

chessdotcomAPI.get_chess_games()
bigquery.upload_to_bigquery()
