import requests
from flask import *
app = Flask(__name__)
from services.player_stats import find_player_biography, find_player_statistics,find_schedule, find_old_match_scores, find_new_match_scores

@app.route('/v1/player/bio')
def findBio():
    playerName = request.args.get('playerName')
    if playerName:
        result_data = requests.get('https://cricapi.com/api/playerFinder?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2&name='+str(playerName))
        return find_player_biography(result_data.json())
    else:
        return jsonify([{"message":"please provide player name"}])

@app.route('/v1/player/stats')
def find_stats():
    playerName = request.args.get('playerName')
    if playerName:
        result_data = requests.get('https://cricapi.com/api/playerFinder?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2&name='
                                   + str(playerName))
        return find_player_statistics(result_data.json())
    else:
        return jsonify([{"message":"please provide player name"}])

@app.route('/v1/calendar')
def list_calendar():
    requested_calendar = requests.get('https://cricapi.com/api/matchCalendar?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2')
    return find_schedule(requested_calendar.json())

@app.route('/v1/oldmatchscores')
def old_game_scores():
    requested_scores = requests.get('https://cricapi.com/api/cricket?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2')
    return find_old_match_scores(requested_scores.json())

@app.route('/v1/newmatchscores')
def new_game_scores():
    requested_scores = requests.get('https://cricapi.com/api/matches?apikey=NcDjzhEkkzLTYQqn1C51qwABQhO2')
    return find_new_match_scores(requested_scores.json())

if __name__ == '__main__':
    app.run(debug=True)
