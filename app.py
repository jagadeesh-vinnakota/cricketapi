import requests
from flask import *
import os
app = Flask(__name__)
from services.player_stats import find_player_biography, find_player_statistics,find_schedule, find_old_match_scores, find_new_match_scores
port = int(os.getenv("PORT"))
# serves the biography of a given player
@app.route('/v1/player/bio')
def findBio():
    playerName = request.args.get('playerName')
    if playerName:
        result_data = requests.get('https://cricapi.com/api/playerFinder?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2&name='+str(playerName))
        return find_player_biography(result_data.json())
    else:
        return jsonify([{"message":"please provide player name"}]),404

#Serves the player statistics for a given player name
@app.route('/v1/player/stats')
def find_stats():
    playerName = request.args.get('playerName')
    if playerName:
        result_data = requests.get('https://cricapi.com/api/playerFinder?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2&name='
                                   + str(playerName))
        return find_player_statistics(result_data.json())
    else:
        return jsonify([{"message":"please provide player name"}]),404

# Serves the future scheduled games
@app.route('/v1/calendar')
def list_calendar():
    requested_calendar = requests.get('https://cricapi.com/api/matchCalendar?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2')
    return find_schedule(requested_calendar.json()),200

# serves the already completed game scores.
@app.route('/v1/oldmatchscores')
def old_game_scores():
    requested_scores = requests.get('https://cricapi.com/api/cricket?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2')
    return find_old_match_scores(requested_scores.json()),200

# serves the scores for ongoing games
@app.route('/v1/newmatchscores')
def new_game_scores():
    requested_scores = requests.get('https://cricapi.com/api/matches?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2')
    return find_new_match_scores(requested_scores.json()),200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = port)
